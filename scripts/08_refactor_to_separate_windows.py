"""Refactor: Main window shows only invoices, items in separate window"""
from pathlib import Path

APP = Path("C:/Development/nex-automat/apps/supplier-invoice-staging")

# main_window.py - only invoice list
MAIN_WINDOW = '''"""Main Window - Invoice List Only"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStatusBar, QLabel, QMessageBox
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem

from shared_pyside6.ui import BaseWindow, BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository

from config.settings import Settings
from ui.invoice_items_window import InvoiceItemsWindow


class MainWindow(BaseWindow):
    WINDOW_ID = "supplier_invoice_staging_main"
    GRID_NAME = "invoice_list"

    COLUMNS = [
        ("id", "ID", 50, False),
        ("supplier_name", "Dodavatel", 150, True),
        ("invoice_number", "Cislo faktury", 120, True),
        ("invoice_date", "Datum", 90, True),
        ("total_amount", "Suma", 100, True),
        ("currency", "Mena", 50, True),
        ("status", "Stav", 80, True),
        ("item_count", "Poloziek", 60, True),
        ("match_percent", "Match%", 70, True),
    ]

    def __init__(self, settings: Settings):
        self.settings = settings
        self._data = []
        self._filtered_data = []
        self._items_windows = {}  # invoice_id -> window

        super().__init__(
            window_name=self.WINDOW_ID,
            default_size=(900, 600),
            default_pos=(100, 100),
            auto_load=True
        )

        self.setWindowTitle("Supplier Invoice Staging v1.0")
        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        self._connect_signals()

        # Load test data
        self._load_test_data()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Title
        self.title_label = QLabel("Faktury")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title_label)

        # Search
        self.search_edit = QuickSearchEdit()
        self.search_edit.setPlaceholderText("Hladat fakturu...")
        layout.addWidget(self.search_edit)

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
        layout.addWidget(self.grid)

    def _setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&Subor")
        file_menu.addAction("&Obnovit", self._refresh_data, "F5")
        file_menu.addSeparator()
        file_menu.addAction("&Koniec", self.close, "Alt+F4")

        help_menu = menubar.addMenu("&Pomocnik")
        help_menu.addAction("&O programe...", self._show_about)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_label = QLabel("Pripravene")
        self.statusbar.addWidget(self.status_label, 1)

    def _connect_signals(self):
        self.search_edit.search_text_changed.connect(self._on_search_changed)
        self.grid.row_selected.connect(self._on_row_selected)
        self.grid.row_activated.connect(self._on_row_activated)  # double-click or Enter

    @Slot(str)
    def _on_search_changed(self, text: str):
        self._apply_filter(text)

    @Slot(int)
    def _on_row_selected(self, row: int):
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self.status_label.setText(f"Faktura: {inv['invoice_number']} | {inv['supplier_name']}")

    @Slot(int)
    def _on_row_activated(self, row: int):
        """Open items window on double-click or Enter."""
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self._open_items_window(inv)

    def _open_items_window(self, invoice: dict):
        """Open or focus items window for invoice."""
        invoice_id = invoice["id"]

        # Check if window already open
        if invoice_id in self._items_windows:
            window = self._items_windows[invoice_id]
            if window.isVisible():
                window.activateWindow()
                window.raise_()
                return

        # Create new window
        window = InvoiceItemsWindow(
            invoice=invoice,
            settings=self.settings,
            parent=None  # independent window
        )
        window.closed.connect(lambda: self._on_items_window_closed(invoice_id))
        self._items_windows[invoice_id] = window
        window.show()

    def _on_items_window_closed(self, invoice_id: int):
        """Clean up when items window is closed."""
        if invoice_id in self._items_windows:
            del self._items_windows[invoice_id]

    def _apply_filter(self, search_text: str):
        if not search_text:
            self._filtered_data = self._data.copy()
        else:
            from shared_pyside6.utils import normalize_for_search
            s = normalize_for_search(search_text)
            self._filtered_data = [
                r for r in self._data
                if s in normalize_for_search(str(r.get("supplier_name", "")))
                or s in normalize_for_search(str(r.get("invoice_number", "")))
            ]
        self._populate_model()

    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(False)
                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")

    def _load_test_data(self):
        """Load test data for development."""
        self._data = [
            {"id": 1, "supplier_name": "METRO", "invoice_number": "F2024-001", 
             "invoice_date": "2024-12-15", "total_amount": 1250.50, "currency": "EUR",
             "status": "pending", "item_count": 15, "match_percent": 45.0},
            {"id": 2, "supplier_name": "MAKRO", "invoice_number": "F2024-002",
             "invoice_date": "2024-12-14", "total_amount": 890.00, "currency": "EUR",
             "status": "matched", "item_count": 8, "match_percent": 100.0},
            {"id": 3, "supplier_name": "LIDL", "invoice_number": "F2024-003",
             "invoice_date": "2024-12-13", "total_amount": 2100.75, "currency": "EUR",
             "status": "processing", "item_count": 22, "match_percent": 68.0},
        ]
        self._filtered_data = self._data.copy()
        self._populate_model()

    def _refresh_data(self):
        self._load_test_data()

    def _show_about(self):
        QMessageBox.about(self, "O programe", 
            "Supplier Invoice Staging v1.0\\n\\n"
            "Aplikacia pre spravu dodavatelskych faktur\\n"
            "a nastavenie obchodnej marze.\\n\\n"
            "ICC Komarno 2025")

    def closeEvent(self, event):
        """Close all items windows when main window closes."""
        for window in list(self._items_windows.values()):
            window.close()
        super().closeEvent(event)
'''

# invoice_items_window.py - separate window for items
ITEMS_WINDOW = '''"""Invoice Items Window - Separate window for editing items"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, Slot, Qt

from shared_pyside6.ui import BaseWindow, BaseGrid, QuickSearchEdit

from config.settings import Settings


class InvoiceItemsWindow(BaseWindow):
    """Separate window for invoice items editing."""

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
        ("margin_percent", "Marza %", 80, True, True),  # editable
        ("selling_price_excl_vat", "PC bez DPH", 90, True, True),  # editable
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
            window_name=f"{self.WINDOW_ID}_{invoice['id']}",
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

        # Search
        self.search_edit = QuickSearchEdit()
        self.search_edit.setPlaceholderText("Hladat polozku...")
        layout.addWidget(self.search_edit)

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

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def _connect_signals(self):
        self.search_edit.search_text_changed.connect(self._on_search_changed)

    @Slot(str)
    def _on_search_changed(self, text: str):
        self._apply_filter(text)

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

    def _apply_filter(self, search_text: str):
        if not search_text:
            self._filtered_data = self._data.copy()
        else:
            from shared_pyside6.utils import normalize_for_search
            s = normalize_for_search(search_text)
            self._filtered_data = [
                r for r in self._data
                if s in normalize_for_search(str(r.get("xml_name", "")))
                or s in normalize_for_search(str(r.get("xml_ean", "")))
            ]
        self._populate_model()

    def _populate_model(self):
        self.model.blockSignals(True)
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

        self.model.blockSignals(False)
        self._update_status()

    def _update_status(self):
        total = len(self._data)
        matched = sum(1 for i in self._data if i.get("in_nex"))
        priced = sum(1 for i in self._data if (i.get("margin_percent") or 0) > 0)
        self.status_label.setText(
            f"Poloziek: {total} | Matched: {matched} ({matched/total*100:.0f}%) | "
            f"S marzou: {priced} ({priced/total*100:.0f}%)" if total else ""
        )

    def _load_test_items(self):
        """Load test items for development."""
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
        ]
        self._filtered_data = self._data.copy()
        self._populate_model()

    def _save_items(self):
        """Save items to database."""
        # TODO: Implement save to database
        modified = [i for i in self._data if (i.get("margin_percent") or 0) > 0]
        print(f"Saving {len(modified)} modified items...")
        self.status_label.setText(f"Ulozene {len(modified)} poloziek")

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
'''

# Update ui/__init__.py
UI_INIT = '''"""UI package."""
from ui.main_window import MainWindow
from ui.invoice_items_window import InvoiceItemsWindow

__all__ = ["MainWindow", "InvoiceItemsWindow"]
'''

# Write files
(APP / "ui/main_window.py").write_text(MAIN_WINDOW, encoding="utf-8")
(APP / "ui/invoice_items_window.py").write_text(ITEMS_WINDOW, encoding="utf-8")
(APP / "ui/__init__.py").write_text(UI_INIT, encoding="utf-8")

# Remove old widgets folder (no longer needed)
import shutil

widgets_dir = APP / "ui/widgets"
if widgets_dir.exists():
    shutil.rmtree(widgets_dir)
    print("Removed ui/widgets/ (no longer needed)")

print("Created:")
print("  - ui/main_window.py (invoice list only)")
print("  - ui/invoice_items_window.py (separate items window)")
print("\nRun: python app.py")