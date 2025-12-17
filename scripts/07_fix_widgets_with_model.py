"""Fix widgets to use correct BaseGrid API with QStandardItemModel"""
from pathlib import Path

APP = Path("C:/Development/nex-automat/apps/supplier-invoice-staging")

# invoice_list.py
INVOICE_LIST = '''"""Invoice List Widget"""
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, Slot, Qt

from shared_pyside6.ui import BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository


class InvoiceListWidget(QWidget):
    """Widget displaying list of invoices (read-only)."""

    WINDOW_NAME = "supplier_invoice_staging"
    GRID_NAME = "invoice_list"

    invoice_selected = Signal(int, str)  # invoice_id, invoice_number

    COLUMNS = [
        ("id", "ID", 50, False),
        ("supplier_name", "Supplier", 150, True),
        ("invoice_number", "Invoice #", 120, True),
        ("invoice_date", "Date", 90, True),
        ("total_amount", "Amount", 100, True),
        ("currency", "Cur", 50, True),
        ("status", "Status", 80, True),
        ("item_count", "Items", 60, True),
        ("match_percent", "Match%", 70, True),
    ]

    def __init__(self, settings_repo: SettingsRepository, parent=None):
        super().__init__(parent)
        self.settings_repo = settings_repo
        self._data: List[Dict[str, Any]] = []
        self._filtered_data: List[Dict[str, Any]] = []
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.title_label = QLabel("Invoices")
        self.title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title_label)

        self.search_edit = QuickSearchEdit()
        self.search_edit.setPlaceholderText("Search invoice...")
        layout.addWidget(self.search_edit)

        # Create grid with model
        self.grid = BaseGrid(
            window_name=self.WINDOW_NAME,
            grid_name=self.GRID_NAME,
            parent=self
        )

        # Setup model
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

    def _connect_signals(self):
        self.grid.row_selected.connect(self._on_row_selected)
        self.search_edit.search_text_changed.connect(self._on_search_changed)

    @Slot(int)
    def _on_row_selected(self, row: int):
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self.invoice_selected.emit(inv["id"], inv["invoice_number"])

    @Slot(str)
    def _on_search_changed(self, text: str):
        self._apply_filter(text)

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
        """Populate model with filtered data."""
        self.model.removeRows(0, self.model.rowCount())

        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(False)
                row_items.append(item)
            self.model.appendRow(row_items)

    def load_invoices(self, invoices: Optional[List[Dict[str, Any]]] = None):
        if invoices is not None:
            self._data = invoices
        self._filtered_data = self._data.copy()
        self._populate_model()
        self.title_label.setText(f"Invoices ({len(self._data)})")

    def set_data(self, data: List[Dict[str, Any]]):
        self._data = data
        self.load_invoices()
'''

# invoice_items.py
INVOICE_ITEMS = '''"""Invoice Items Widget"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, Slot, Qt

from shared_pyside6.ui import BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository
from config.settings import Settings


class InvoiceItemsWidget(QWidget):
    """Widget displaying invoice items with editable margin/price."""

    WINDOW_NAME = "supplier_invoice_staging"
    GRID_NAME = "invoice_items"

    items_updated = Signal()

    COLUMNS = [
        ("id", "ID", 50, False, False),
        ("line_number", "#", 40, True, False),
        ("xml_ean", "EAN", 120, True, False),
        ("xml_name", "Name (XML)", 200, True, False),
        ("nex_product_name", "Name (NEX)", 180, True, False),
        ("xml_quantity", "Qty", 70, True, False),
        ("xml_unit", "Unit", 50, True, False),
        ("xml_unit_price", "Purchase", 90, True, False),
        ("margin_percent", "Margin%", 80, True, True),  # editable
        ("selling_price_excl_vat", "Sell excl", 90, True, True),  # editable
        ("selling_price_incl_vat", "Sell incl", 90, True, False),
        ("in_nex", "NEX", 50, True, False),
        ("matched_by", "Match", 60, True, False),
        ("item_status", "Status", 70, True, False),
    ]

    def __init__(self, settings_repo: SettingsRepository, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings_repo = settings_repo
        self.settings = settings
        self._invoice_id: Optional[int] = None
        self._data: List[Dict[str, Any]] = []
        self._filtered_data: List[Dict[str, Any]] = []
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.title_label = QLabel("Invoice Items")
        self.title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title_label)

        self.search_edit = QuickSearchEdit()
        self.search_edit.setPlaceholderText("Search item...")
        layout.addWidget(self.search_edit)

        # Create grid with model
        self.grid = BaseGrid(
            window_name=self.WINDOW_NAME,
            grid_name=self.GRID_NAME,
            parent=self
        )

        # Setup model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([col[1] for col in self.COLUMNS])
        self.grid.table_view.setModel(self.model)

        # Hide ID column
        self.grid.table_view.setColumnHidden(0, True)

        # Set column widths
        for i, col in enumerate(self.COLUMNS):
            self.grid.table_view.setColumnWidth(i, col[2])

        self.grid.apply_model_and_load_settings()

        # Connect model change for editable cells
        self.model.itemChanged.connect(self._on_item_changed)

        layout.addWidget(self.grid)

    def _connect_signals(self):
        self.search_edit.search_text_changed.connect(self._on_search_changed)

    @Slot(str)
    def _on_search_changed(self, text: str):
        self._apply_filter(text)

    @Slot(QStandardItem)
    def _on_item_changed(self, item: QStandardItem):
        """Handle cell edit."""
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

        self.items_updated.emit()

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
        """Update row display after recalculation."""
        if row < 0 or row >= len(self._filtered_data):
            return

        data_item = self._filtered_data[row]

        # Block signals to avoid recursion
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
        """Populate model with filtered data."""
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

    def load_items(self, invoice_id: int, items: Optional[List[Dict[str, Any]]] = None):
        self._invoice_id = invoice_id
        if items is not None:
            self._data = items
        self._filtered_data = self._data.copy()
        self._populate_model()
        self.title_label.setText(f"Invoice Items ({len(self._data)})")

    def set_data(self, data: List[Dict[str, Any]]):
        self._data = data
        self._filtered_data = data.copy()
        self._populate_model()

    def get_stats(self) -> Optional[Dict[str, Any]]:
        if not self._data:
            return None
        total = len(self._data)
        matched = sum(1 for i in self._data if i.get("in_nex"))
        priced = sum(1 for i in self._data if i.get("margin_percent", 0) > 0)
        return {
            "total": total,
            "matched": matched,
            "priced": priced,
            "matched_percent": (matched / total * 100) if total else 0,
        }

    def get_modified_items(self) -> List[Dict[str, Any]]:
        return [i for i in self._data if i.get("margin_percent", 0) > 0]
'''

(APP / "ui/widgets/invoice_list.py").write_text(INVOICE_LIST, encoding="utf-8")
(APP / "ui/widgets/invoice_items.py").write_text(INVOICE_ITEMS, encoding="utf-8")
print("Fixed invoice_list.py and invoice_items.py with proper model usage")
print("\nRun: python app.py")