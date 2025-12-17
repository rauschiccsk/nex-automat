"""Invoice Items Window with QuickSearch"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, Slot, Qt

from shared_pyside6.ui import BaseWindow, BaseGrid
from shared_pyside6.ui.quick_search import QuickSearchContainer, QuickSearchController

from config.settings import Settings


class InvoiceItemsWindow(BaseWindow):
    WINDOW_ID = "invoice_items_window"
    GRID_NAME = "invoice_items"

    closed = Signal()

    COLUMNS = [
        ("id", "ID", 50, False, False),
        ("line_number", "#", 40, True, False),
        ("xml_ean", "EAN", 120, True, False),
        ("xml_name", "Nazov (XML)", 200, True, False),
        ("nex_product_name", "Nazov (NEX)", 180, True, False),
        ("xml_quantity", "Mnozstvo", 70, True, False),
        ("xml_unit", "MJ", 50, True, False),
        ("xml_unit_price", "NC", 90, True, False),
        ("margin_percent", "Marza %", 80, True, True),
        ("selling_price_excl_vat", "PC bez DPH", 90, True, True),
        ("selling_price_incl_vat", "PC s DPH", 90, True, False),
        ("in_nex", "NEX", 50, True, False),
        ("matched_by", "Match", 60, True, False),
        ("item_status", "Stav", 70, True, False),
    ]

    def __init__(self, invoice: dict, settings: Settings, parent=None):
        self.invoice = invoice
        self.settings = settings
        self._data: List[Dict[str, Any]] = []
        self._filtered_data: List[Dict[str, Any]] = []

        super().__init__(
            window_name=self.WINDOW_ID,
            default_size=(1200, 600),
            default_pos=(150, 150),
            auto_load=True,
            parent=parent
        )

        self.setWindowTitle(f"Polozky faktury: {invoice['invoice_number']} - {invoice['supplier_name']}")
        self._setup_ui()
        self._connect_signals()
        self._load_test_items()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Header info
        header_layout = QHBoxLayout()

        info_text = (f"Dodavatel: {self.invoice['supplier_name']} | "
                     f"Faktura: {self.invoice['invoice_number']} | "
                     f"Datum: {self.invoice['invoice_date']} | "
                     f"Suma: {self.invoice['total_amount']} {self.invoice['currency']}")
        self.info_label = QLabel(info_text)
        self.info_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(self.info_label)

        header_layout.addStretch()

        self.save_btn = QPushButton("Ulozit")
        self.save_btn.clicked.connect(self._save_items)
        header_layout.addWidget(self.save_btn)

        layout.addLayout(header_layout)

        # Grid
        self.grid = BaseGrid(
            window_name=self.WINDOW_ID,
            grid_name=self.GRID_NAME,
            parent=self
        )

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([col[1] for col in self.COLUMNS])
        self.grid.table_view.setModel(self.model)

        # Hide ID column
        self.grid.table_view.setColumnHidden(0, True)

        # Set column widths
        for i, col in enumerate(self.COLUMNS):
            self.grid.table_view.setColumnWidth(i, col[2])

        self.grid.apply_model_and_load_settings()

        # Connect model for edits
        self.model.itemChanged.connect(self._on_item_changed)

        layout.addWidget(self.grid)

        # QuickSearch
        self.search_container = QuickSearchContainer(self.grid.table_view, self)
        layout.addWidget(self.search_container)

        self.search_controller = QuickSearchController(
            self.grid.table_view,
            self.search_container,
            self.grid.header
        )
        self.search_controller.set_active_column(2)  # EAN column

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def _connect_signals(self):
        self.search_controller.active_column_changed.connect(self._on_column_changed)

    @Slot(int)
    def _on_column_changed(self, column: int):
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            # Keep stats but add column info
            self._update_status(f" | Stlpec: {col_name}")

    @Slot(QStandardItem)
    def _on_item_changed(self, item: QStandardItem):
        row = item.row()
        col = item.column()

        if row < 0 or row >= len(self._filtered_data):
            return

        col_key = self.COLUMNS[col][0]
        new_value = item.text()
        data_item = self._filtered_data[row]

        if col_key == "margin_percent":
            self._recalc_from_margin(data_item, new_value)
            self._update_row(row)
        elif col_key == "selling_price_excl_vat":
            self._recalc_from_price(data_item, new_value)
            self._update_row(row)

        self._update_status()

    def _recalc_from_margin(self, item: Dict, margin_percent: Any):
        try:
            margin = Decimal(str(margin_percent or 0))
            nc = Decimal(str(item.get("xml_unit_price", 0)))
            vat = Decimal(str(item.get("xml_vat_rate") or self.settings.default_vat_rate))
            item["margin_percent"] = float(margin)
            item["selling_price_excl_vat"] = float(nc * (1 + margin / 100))
            item["selling_price_incl_vat"] = float(Decimal(str(item["selling_price_excl_vat"])) * (1 + vat / 100))
        except (ValueError, TypeError):
            pass

    def _recalc_from_price(self, item: Dict, selling_price: Any):
        try:
            pc = Decimal(str(selling_price or 0))
            nc = Decimal(str(item.get("xml_unit_price", 0)))
            vat = Decimal(str(item.get("xml_vat_rate") or self.settings.default_vat_rate))
            if nc > 0:
                item["margin_percent"] = float(((pc / nc) - 1) * 100)
            item["selling_price_excl_vat"] = float(pc)
            item["selling_price_incl_vat"] = float(pc * (1 + vat / 100))
        except (ValueError, TypeError, ZeroDivisionError):
            pass

    def _update_row(self, row: int):
        if row < 0 or row >= len(self._filtered_data):
            return

        data_item = self._filtered_data[row]
        self.model.blockSignals(True)

        for col, (col_key, _, _, _, _) in enumerate(self.COLUMNS):
            value = data_item.get(col_key, "")
            if isinstance(value, float):
                value = f"{value:.2f}"
            item = self.model.item(row, col)
            if item:
                item.setText(str(value) if value is not None else "")

        self.model.blockSignals(False)

    def _populate_model(self):
        self.model.layoutAboutToBeChanged.emit()
        self.model.removeRows(0, self.model.rowCount())

        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _, editable in self.COLUMNS:
                value = row_data.get(col_key, "")
                if isinstance(value, float):
                    value = f"{value:.2f}"
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(editable)
                row_items.append(item)
            self.model.appendRow(row_items)

        self.model.layoutChanged.emit()
        self._update_status()

    def _update_status(self, extra: str = ""):
        total = len(self._data)
        matched = sum(1 for i in self._data if i.get("in_nex"))
        priced = sum(1 for i in self._data if (i.get("margin_percent") or 0) > 0)
        self.status_label.setText(
            f"Poloziek: {total} | Matched: {matched} ({matched/total*100:.0f}%) | "
            f"S marzou: {priced} ({priced/total*100:.0f}%){extra}" if total else ""
        )

    def _load_test_items(self):
        self._data = [
            {"id": 1, "line_number": 1, "xml_ean": "8590123456789", "xml_name": "Mlieko 1L",
             "nex_product_name": "Mlieko polotucne 1L", "xml_quantity": 10, "xml_unit": "ks",
             "xml_unit_price": 1.20, "xml_vat_rate": 20.0, "margin_percent": 0,
             "selling_price_excl_vat": 0, "selling_price_incl_vat": 0,
             "in_nex": True, "matched_by": "ean", "item_status": "matched"},
            {"id": 2, "line_number": 2, "xml_ean": "8590123456790", "xml_name": "Chlieb",
             "nex_product_name": "", "xml_quantity": 5, "xml_unit": "ks",
             "xml_unit_price": 2.50, "xml_vat_rate": 20.0, "margin_percent": 0,
             "selling_price_excl_vat": 0, "selling_price_incl_vat": 0,
             "in_nex": False, "matched_by": "", "item_status": "pending"},
            {"id": 3, "line_number": 3, "xml_ean": "8590123456791", "xml_name": "Maslo 250g",
             "nex_product_name": "Maslo 82% 250g", "xml_quantity": 20, "xml_unit": "ks",
             "xml_unit_price": 3.80, "xml_vat_rate": 20.0, "margin_percent": 25.0,
             "selling_price_excl_vat": 4.75, "selling_price_incl_vat": 5.70,
             "in_nex": True, "matched_by": "ean", "item_status": "priced"},
            {"id": 4, "line_number": 4, "xml_ean": "8590123456792", "xml_name": "Jogurt biely",
             "nex_product_name": "Jogurt biely 150g", "xml_quantity": 30, "xml_unit": "ks",
             "xml_unit_price": 0.65, "xml_vat_rate": 20.0, "margin_percent": 0,
             "selling_price_excl_vat": 0, "selling_price_incl_vat": 0,
             "in_nex": True, "matched_by": "name", "item_status": "matched"},
            {"id": 5, "line_number": 5, "xml_ean": "8590123456793", "xml_name": "Syry Edamsky",
             "nex_product_name": "", "xml_quantity": 8, "xml_unit": "ks",
             "xml_unit_price": 4.20, "xml_vat_rate": 20.0, "margin_percent": 0,
             "selling_price_excl_vat": 0, "selling_price_incl_vat": 0,
             "in_nex": False, "matched_by": "", "item_status": "pending"},
        ]
        self._filtered_data = self._data.copy()
        self._populate_model()
        # Select first row
        if self._filtered_data:
            self.grid.table_view.selectRow(0)

    def _save_items(self):
        modified = [i for i in self._data if (i.get("margin_percent") or 0) > 0]
        print(f"Saving {len(modified)} modified items...")
        self.status_label.setText(f"Ulozene {len(modified)} poloziek")

    def keyPressEvent(self, event):
        """Handle key press - ESC closes window."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        self.grid.save_grid_settings_now()
        self.closed.emit()
        super().closeEvent(event)
