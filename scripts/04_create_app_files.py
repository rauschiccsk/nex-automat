"""
Script: Create supplier-invoice-staging application files
Run from: C:/Development/nex-automat
"""
from pathlib import Path

APP_ROOT = Path("C:/Development/nex-automat/apps/supplier-invoice-staging")

DIRS = [
    "config",
    "database/repositories",
    "database/schemas",
    "models",
    "services",
    "ui/widgets",
    "ui/dialogs",
    "resources/icons",
    "tests",
    "data",
]

INIT_PACKAGES = [
    "",
    "config",
    "database",
    "database/repositories",
    "models",
    "services",
    "ui",
    "ui/widgets",
    "ui/dialogs",
    "tests",
]

FILES = {}

FILES["__main__.py"] = '''"""Entry point: python -m supplier_invoice_staging"""
import sys
from pathlib import Path

app_root = Path(__file__).parent
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

from app import main

if __name__ == "__main__":
    sys.exit(main())
'''

FILES["app.py"] = '''"""Application setup"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow
from config.settings import Settings


def main() -> int:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Supplier Invoice Staging")
    app.setOrganizationName("ICC")
    app.setApplicationVersion("1.0.0")

    settings = Settings()
    window = MainWindow(settings)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
'''

FILES["config/settings.py"] = '''"""Configuration"""
import os
from pathlib import Path
from dataclasses import dataclass, field
import yaml


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "supplier_invoice_staging"
    user: str = "postgres"
    password: str = ""


@dataclass
class Settings:
    app_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    config_file: Path = field(default_factory=lambda: Path(__file__).parent / "config.yaml")
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    default_margin_percent: float = 25.0
    default_vat_rate: float = 20.0

    def __post_init__(self):
        self._load_from_yaml()
        self._load_from_env()

    def _load_from_yaml(self):
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            db = config.get("database", {})
            self.database.host = db.get("host", self.database.host)
            self.database.port = db.get("port", self.database.port)
            self.database.database = db.get("database", self.database.database)
            self.database.user = db.get("user", self.database.user)
            self.database.password = db.get("password", self.database.password)
            ui = config.get("ui", {})
            self.default_margin_percent = ui.get("default_margin_percent", self.default_margin_percent)
            self.default_vat_rate = ui.get("default_vat_rate", self.default_vat_rate)

    def _load_from_env(self):
        if pw := os.environ.get("POSTGRES_PASSWORD"):
            self.database.password = pw

    def get_settings_db_path(self) -> Path:
        return self.app_root / "data" / "settings.db"
'''

FILES["config/config.yaml"] = '''database:
  host: localhost
  port: 5432
  database: supplier_invoice_staging
  user: postgres

ui:
  default_margin_percent: 25.0
  default_vat_rate: 20.0
'''

FILES["requirements.txt"] = '''PySide6>=6.6.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.9
pyyaml>=6.0
'''

FILES["ui/main_window.py"] = '''"""Main Window"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QStatusBar, QLabel, QMessageBox
from PySide6.QtCore import Qt, Slot

from shared_pyside6.ui import BaseWindow
from shared_pyside6.database import SettingsRepository

from config.settings import Settings
from ui.widgets.invoice_list import InvoiceListWidget
from ui.widgets.invoice_items import InvoiceItemsWidget


class MainWindow(BaseWindow):
    WINDOW_ID = "main_window"

    def __init__(self, settings: Settings):
        self.settings = settings

        settings_db = settings.get_settings_db_path()
        settings_db.parent.mkdir(parents=True, exist_ok=True)
        self.settings_repo = SettingsRepository(str(settings_db))

        super().__init__(settings_repository=self.settings_repo, window_id=self.WINDOW_ID)

        self.setWindowTitle("Supplier Invoice Staging v1.0")
        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        self._connect_signals()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.invoice_list = InvoiceListWidget(settings_repo=self.settings_repo, parent=self)
        self.splitter.addWidget(self.invoice_list)

        self.invoice_items = InvoiceItemsWidget(
            settings_repo=self.settings_repo, settings=self.settings, parent=self
        )
        self.splitter.addWidget(self.invoice_items)
        self.splitter.setSizes([300, 450])
        layout.addWidget(self.splitter)

    def _setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&Refresh", self._refresh_data, "F5")
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.close, "Alt+F4")

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About...", self._show_about)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_invoice = QLabel("No invoice selected")
        self.status_items = QLabel("")
        self.status_match = QLabel("")
        self.statusbar.addWidget(self.status_invoice, 1)
        self.statusbar.addWidget(self.status_items)
        self.statusbar.addWidget(self.status_match)

    def _connect_signals(self):
        self.invoice_list.invoice_selected.connect(self._on_invoice_selected)
        self.invoice_items.items_updated.connect(self._update_status)

    @Slot(int, str)
    def _on_invoice_selected(self, invoice_id: int, invoice_number: str):
        self.invoice_items.load_items(invoice_id)
        self.status_invoice.setText(f"Invoice: {invoice_number}")
        self._update_status()

    def _update_status(self):
        stats = self.invoice_items.get_stats()
        if stats:
            self.status_items.setText(f"{stats['total']} items")
            self.status_match.setText(f"{stats['matched_percent']:.0f}% matched")
        else:
            self.status_items.setText("")
            self.status_match.setText("")

    def _refresh_data(self):
        self.invoice_list.load_invoices()

    def _show_about(self):
        QMessageBox.about(self, "About", "Supplier Invoice Staging v1.0\\n\\nICC Komarno 2025")
'''

FILES["ui/widgets/invoice_list.py"] = '''"""Invoice List Widget"""
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

        self.search_edit = QuickSearchEdit(placeholder="Search invoice...")
        layout.addWidget(self.search_edit)

        self.grid = BaseGrid(settings_repository=self.settings_repo, grid_id=self.GRID_ID)
        self.grid.setup_columns(self.COLUMNS)
        layout.addWidget(self.grid)

    def _connect_signals(self):
        self.grid.row_selected.connect(self._on_row_selected)
        self.search_edit.search_changed.connect(self._on_search_changed)

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

FILES["ui/widgets/invoice_items.py"] = '''"""Invoice Items Widget"""
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

        self.search_edit = QuickSearchEdit(placeholder="Search item...")
        layout.addWidget(self.search_edit)

        self.grid = BaseGrid(settings_repository=self.settings_repo, grid_id=self.GRID_ID)
        self.grid.setup_columns(self.COLUMNS)
        self.grid.set_editable(True)
        layout.addWidget(self.grid)

    def _connect_signals(self):
        self.search_edit.search_changed.connect(self._on_search_changed)
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


def main():
    print(f"Creating app in: {APP_ROOT}")

    # Create directories
    for d in DIRS:
        (APP_ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"  [DIR] {d}")

    # Create __init__.py
    for pkg in INIT_PACKAGES:
        init_file = APP_ROOT / pkg / "__init__.py" if pkg else APP_ROOT / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Package."""\n', encoding="utf-8")
            print(f"  [INIT] {pkg or '.'}")

    # Create files
    for filename, content in FILES.items():
        filepath = APP_ROOT / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
        print(f"  [FILE] {filename}")

    print(f"\n OK - App files created!")
    print(f"\nRun:")
    print(f"  cd apps/supplier-invoice-staging")
    print(f"  python app.py")


if __name__ == "__main__":
    main()