"""Fix widgets to use correct QuickSearchEdit API"""
from pathlib import Path

APP = Path("C:/Development/nex-automat/apps/supplier-invoice-staging")

# invoice_list.py
INVOICE_LIST = '''"""Invoice List Widget"""
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Slot

from shared_pyside6.ui import BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository


class InvoiceListWidget(QWidget):
    GRID_ID = "invoice_list_grid"
    invoice_selected = Signal(int, str)

    COLUMNS = [
        {"key": "id", "header": "ID", "width": 50, "visible": False},
        {"key": "supplier_name", "header": "Supplier", "width": 150},
        {"key": "invoice_number", "header": "Invoice #", "width": 120},
        {"key": "invoice_date", "header": "Date", "width": 90},
        {"key": "total_amount", "header": "Amount", "width": 100, "align": "right"},
        {"key": "currency", "header": "Cur", "width": 50},
        {"key": "status", "header": "Status", "width": 80},
        {"key": "item_count", "header": "Items", "width": 60, "align": "right"},
        {"key": "match_percent", "header": "Match%", "width": 70, "align": "right"},
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

        self.grid = BaseGrid(settings_repository=self.settings_repo, grid_id=self.GRID_ID)
        self.grid.setup_columns(self.COLUMNS)
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
                if s in normalize_for_search(r.get("supplier_name", ""))
                or s in normalize_for_search(r.get("invoice_number", ""))
            ]
        self.grid.set_data(self._filtered_data)

    def load_invoices(self, invoices: Optional[List[Dict[str, Any]]] = None):
        if invoices is not None:
            self._data = invoices
        self._filtered_data = self._data.copy()
        self.grid.set_data(self._filtered_data)
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
from PySide6.QtCore import Signal, Slot

from shared_pyside6.ui import BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository
from config.settings import Settings


class InvoiceItemsWidget(QWidget):
    GRID_ID = "invoice_items_grid"
    items_updated = Signal()

    COLUMNS = [
        {"key": "id", "header": "ID", "width": 50, "visible": False},
        {"key": "line_number", "header": "#", "width": 40, "align": "right"},
        {"key": "xml_ean", "header": "EAN", "width": 120},
        {"key": "xml_name", "header": "Name (XML)", "width": 200},
        {"key": "nex_product_name", "header": "Name (NEX)", "width": 180},
        {"key": "xml_quantity", "header": "Qty", "width": 70, "align": "right"},
        {"key": "xml_unit", "header": "Unit", "width": 50},
        {"key": "xml_unit_price", "header": "Purchase", "width": 90, "align": "right"},
        {"key": "margin_percent", "header": "Margin%", "width": 80, "align": "right", "editable": True},
        {"key": "selling_price_excl_vat", "header": "Sell excl", "width": 90, "align": "right", "editable": True},
        {"key": "selling_price_incl_vat", "header": "Sell incl", "width": 90, "align": "right"},
        {"key": "in_nex", "header": "NEX", "width": 50, "align": "center"},
        {"key": "matched_by", "header": "Match", "width": 60},
        {"key": "item_status", "header": "Status", "width": 70},
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

        self.grid = BaseGrid(settings_repository=self.settings_repo, grid_id=self.GRID_ID)
        self.grid.setup_columns(self.COLUMNS)
        self.grid.set_editable(True)
        layout.addWidget(self.grid)

    def _connect_signals(self):
        self.search_edit.search_text_changed.connect(self._on_search_changed)
        self.grid.cell_edited.connect(self._on_cell_edited)

    @Slot(str)
    def _on_search_changed(self, text: str):
        self._apply_filter(text)

    @Slot(int, str, object)
    def _on_cell_edited(self, row: int, column_key: str, new_value: Any):
        if row < 0 or row >= len(self._filtered_data):
            return
        item = self._filtered_data[row]
        if column_key == "margin_percent":
            self._recalc_from_margin(item, new_value)
        elif column_key == "selling_price_excl_vat":
            self._recalc_from_price(item, new_value)
        self.grid.refresh_row(row)
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

    def _apply_filter(self, search_text: str):
        if not search_text:
            self._filtered_data = self._data.copy()
        else:
            from shared_pyside6.utils import normalize_for_search
            s = normalize_for_search(search_text)
            self._filtered_data = [
                r for r in self._data
                if s in normalize_for_search(r.get("xml_name", ""))
                or s in normalize_for_search(r.get("xml_ean", ""))
            ]
        self.grid.set_data(self._filtered_data)

    def load_items(self, invoice_id: int, items: Optional[List[Dict[str, Any]]] = None):
        self._invoice_id = invoice_id
        if items is not None:
            self._data = items
        self._filtered_data = self._data.copy()
        self.grid.set_data(self._filtered_data)
        self.title_label.setText(f"Invoice Items ({len(self._data)})")

    def set_data(self, data: List[Dict[str, Any]]):
        self._data = data
        self._filtered_data = data.copy()
        self.grid.set_data(self._filtered_data)

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
print("Fixed invoice_list.py and invoice_items.py")
print("\nRun: python app.py")