"""Invoice Items Window with QuickSearch"""

from decimal import Decimal
from typing import Any

from config.settings import Settings
from nex_staging import InvoiceRepository
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from shared_pyside6.ui import BaseGrid, BaseWindow
from shared_pyside6.ui.quick_search import QuickSearchContainer, QuickSearchController


class InvoiceItemsWindow(BaseWindow):
    WINDOW_ID = "invoice_items_window"
    GRID_NAME = "invoice_items"

    closed = Signal()

    COLUMNS = [
        ("id", "ID", 50, True, False),
        ("xml_line_number", "#", 40, True, False),
        ("xml_seller_code", "Kod dod.", 80, True, False),
        ("xml_ean", "EAN", 120, True, False),
        ("xml_product_name", "Nazov (XML)", 200, True, False),
        ("nex_product_name", "Nazov (NEX)", 180, True, False),
        ("nex_ean", "EAN (NEX)", 120, True, False),
        ("xml_quantity", "Mnozstvo", 70, True, False),
        ("xml_unit", "MJ", 50, True, False),
        ("xml_unit_price", "JC bez DPH", 90, True, False),
        ("xml_unit_price_vat", "JC s DPH", 90, True, False),
        ("xml_total_price", "Spolu", 90, True, False),
        ("xml_vat_rate", "DPH %", 60, True, False),
        ("nex_product_id", "NEX Prod ID", 80, True, False),
        ("nex_stock_code", "Sklad kod", 80, True, False),
        ("matched", "Matched", 60, True, False),
        ("matched_by", "Match by", 70, True, False),
        ("match_confidence", "Confidence", 70, True, False),
        ("validation_status", "Stav", 70, True, False),
    ]

    def __init__(self, invoice: dict, settings: Settings, repository: InvoiceRepository, parent=None):
        self.invoice = invoice
        self.settings = settings
        self.repository = repository
        self._data: list[dict[str, Any]] = []
        self._filtered_data: list[dict[str, Any]] = []

        super().__init__(
            window_name=self.WINDOW_ID, default_size=(1200, 600), default_pos=(150, 150), auto_load=True, parent=parent
        )

        self.setWindowTitle(f"Polozky faktury: {invoice['xml_invoice_number']} - {invoice['xml_supplier_name']}")
        self._setup_ui()
        self._connect_signals()
        self._load_items()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Header info
        header_layout = QHBoxLayout()

        info_text = (
            f"Dodavatel: {self.invoice['xml_supplier_name']} | "
            f"Faktura: {self.invoice['xml_invoice_number']} | "
            f"Datum: {self.invoice['xml_issue_date']} | "
            f"Suma: {self.invoice['xml_total_with_vat']} {self.invoice['xml_currency']}"
        )
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
            settings_db_path=self.settings.get_settings_db_path(),
            parent=self,
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

        self.search_controller = QuickSearchController(self.grid.table_view, self.search_container, self.grid.header)
        # Load saved column or default to 2 (EAN)
        saved_column = self.grid.get_active_column()
        if saved_column == 0:  # ID column is hidden
            saved_column = 2
        self.search_controller.set_active_column(saved_column)

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def _connect_signals(self):
        self.search_controller.active_column_changed.connect(self._on_column_changed)

    @Slot(int)
    def _on_column_changed(self, column: int):
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            self._update_status(f" | Stlpec: {col_name}")
            self.grid.set_active_column(column)

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

    def _recalc_from_margin(self, item: dict, margin_percent: Any):
        try:
            margin = Decimal(str(margin_percent or 0))
            nc = Decimal(str(item.get("xml_unit_price", 0)))
            vat = Decimal(str(item.get("xml_vat_rate") or self.settings.default_vat_rate))
            item["margin_percent"] = float(margin)
            item["selling_price_excl_vat"] = float(nc * (1 + margin / 100))
            item["selling_price_incl_vat"] = float(Decimal(str(item["selling_price_excl_vat"])) * (1 + vat / 100))
        except (ValueError, TypeError):
            pass

    def _recalc_from_price(self, item: dict, selling_price: Any):
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
                item = self.grid.create_item(value, editable=editable)
                row_items.append(item)
            self.model.appendRow(row_items)

        self.model.layoutChanged.emit()
        self._update_status()

    def _update_status(self, extra: str = ""):
        total = len(self._data)
        matched = sum(1 for i in self._data if i.get("in_nex"))
        priced = sum(1 for i in self._data if (i.get("margin_percent") or 0) > 0)
        self.status_label.setText(
            f"Poloziek: {total} | Matched: {matched} ({matched / total * 100:.0f}%) | "
            f"S marzou: {priced} ({priced / total * 100:.0f}%){extra}"
            if total
            else ""
        )

    def _load_items(self):
        """Load invoice items from database."""
        try:
            # Use dict method for grid compatibility
            self._data = self.repository.get_invoice_items_dict(self.invoice["id"])
            self._filtered_data = self._data.copy()
            self._populate_model()
            self.grid.select_initial_row()
            self.grid.table_view.setFocus()
        except Exception as e:
            self._data = []
            self._filtered_data = []
            self._populate_model()
            self.status_label.setText(f"Chyba: {e}")

    def _save_items(self):
        """Save modified items to database."""
        modified = [i for i in self._data if (i.get("margin_percent") or 0) > 0]
        if not modified:
            self.status_label.setText("Žiadne položky na uloženie")
            return

        try:
            count = self.repository.save_items_batch(modified)
            self.status_label.setText(f"Uložených {count} položiek")
        except Exception as e:
            self.status_label.setText(f"Chyba pri ukladaní: {e}")

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
