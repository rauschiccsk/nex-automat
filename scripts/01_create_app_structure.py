"""
Script: Create supplier-invoice-staging application structure
Run from: C:\Development\nex-automat
"""
from pathlib import Path

APP_ROOT = Path(r"/apps/supplier-invoice-staging")

# Directory structure
DIRS = [
    "",
    "config",
    "database",
    "database/repositories",
    "database/schemas",
    "models",
    "services",
    "ui",
    "ui/widgets",
    "ui/dialogs",
    "resources",
    "resources/icons",
    "tests",
    "data",
]

# __init__.py files
INIT_FILES = [
    "__init__.py",
    "config/__init__.py",
    "database/__init__.py",
    "database/repositories/__init__.py",
    "models/__init__.py",
    "services/__init__.py",
    "ui/__init__.py",
    "ui/widgets/__init__.py",
    "ui/dialogs/__init__.py",
    "tests/__init__.py",
]

# Files content
FILES = {
    "__main__.py": '''"""
Supplier Invoice Staging - Entry point
Usage: python -m supplier_invoice_staging
"""
import sys
from pathlib import Path

app_root = Path(__file__).parent
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

from app import main

if __name__ == "__main__":
    sys.exit(main())
''',

    "app.py": '''"""
Supplier Invoice Staging - Application setup
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow
from config.settings import Settings


def main() -> int:
    """Main application entry point."""
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
''',

    "config/settings.py": '''"""
Supplier Invoice Staging - Configuration
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
import yaml


@dataclass
class DatabaseConfig:
    """PostgreSQL connection settings."""
    host: str = "localhost"
    port: int = 5432
    database: str = "supplier_invoice_staging"
    user: str = "postgres"
    password: str = ""

    def get_connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class Settings:
    """Application settings."""
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
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}

            db = config.get('database', {})
            self.database.host = db.get('host', self.database.host)
            self.database.port = db.get('port', self.database.port)
            self.database.database = db.get('database', self.database.database)
            self.database.user = db.get('user', self.database.user)
            self.database.password = db.get('password', self.database.password)

            ui = config.get('ui', {})
            self.default_margin_percent = ui.get('default_margin_percent', self.default_margin_percent)
            self.default_vat_rate = ui.get('default_vat_rate', self.default_vat_rate)

    def _load_from_env(self):
        if pw := os.environ.get('POSTGRES_PASSWORD'):
            self.database.password = pw
        if host := os.environ.get('POSTGRES_HOST'):
            self.database.host = host
        if port := os.environ.get('POSTGRES_PORT'):
            self.database.port = int(port)
        if db := os.environ.get('POSTGRES_DATABASE'):
            self.database.database = db
        if user := os.environ.get('POSTGRES_USER'):
            self.database.user = user

    def get_settings_db_path(self) -> Path:
        return self.app_root / "data" / "settings.db"
''',

    "config/config.yaml": '''# Supplier Invoice Staging - Configuration

database:
  host: localhost
  port: 5432
  database: supplier_invoice_staging
  user: postgres
  # password: from POSTGRES_PASSWORD env variable

ui:
  default_margin_percent: 25.0
  default_vat_rate: 20.0
''',

    "requirements.txt": '''# Supplier Invoice Staging - Dependencies
PySide6>=6.6.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.9
pyyaml>=6.0
# shared-pyside6: pip install -e ../../packages/shared-pyside6
''',

    "ui/main_window.py": '''"""
Supplier Invoice Staging - Main Window
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSplitter, QStatusBar, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, Slot

from shared_pyside6.ui import BaseWindow
from shared_pyside6.database import SettingsRepository

from config.settings import Settings
from ui.widgets.invoice_list import InvoiceListWidget
from ui.widgets.invoice_items import InvoiceItemsWidget


class MainWindow(BaseWindow):
    """Main application window."""

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

        file_menu = menubar.addMenu("&Súbor")
        file_menu.addAction("&Obnoviť", self._refresh_data, "F5")
        file_menu.addSeparator()
        file_menu.addAction("&Koniec", self.close, "Alt+F4")

        tools_menu = menubar.addMenu("&Nástroje")
        tools_menu.addAction("&Nastavenia...", self._show_settings)

        help_menu = menubar.addMenu("&Pomocník")
        help_menu.addAction("&O programe...", self._show_about)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.status_invoice = QLabel("Žiadna faktúra")
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
        self.status_invoice.setText(f"Faktúra: {invoice_number}")
        self._update_status()

    def _update_status(self):
        stats = self.invoice_items.get_stats()
        if stats:
            self.status_items.setText(f"{stats['total']} položiek")
            self.status_match.setText(f"{stats['matched_percent']:.0f}% matched")
        else:
            self.status_items.setText("")
            self.status_match.setText("")

    def _refresh_data(self):
        self.invoice_list.load_invoices()

    def _show_settings(self):
        pass  # TODO

    def _show_about(self):
        QMessageBox.about(self, "O programe",
            "Supplier Invoice Staging v1.0\\n\\n"
            "Aplikácia pre správu dodávateľských faktúr\\n"
            "a nastavenie obchodnej marže.\\n\\n"
            "© 2025 ICC Komárno")
''',

    "ui/widgets/invoice_list.py": '''"""
Supplier Invoice Staging - Invoice List Widget
"""
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Slot

from shared_pyside6.ui import BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository


class InvoiceListWidget(QWidget):
    """Widget displaying list of invoices (read-only)."""

    GRID_ID = "invoice_list_grid"
    invoice_selected = Signal(int, str)

    COLUMNS = [
        {"key": "id", "header": "ID", "width": 50, "visible": False},
        {"key": "supplier_name", "header": "Dodávateľ", "width": 150},
        {"key": "invoice_number", "header": "Číslo faktúry", "width": 120},
        {"key": "invoice_date", "header": "Dátum", "width": 90},
        {"key": "total_amount", "header": "Suma", "width": 100, "align": "right"},
        {"key": "currency", "header": "Mena", "width": 50},
        {"key": "status", "header": "Stav", "width": 80},
        {"key": "item_count", "header": "Položiek", "width": 70, "align": "right"},
        {"key": "match_percent", "header": "Match %", "width": 70, "align": "right"},
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

        self.title_label = QLabel("Faktúry")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.title_label)

        self.search_edit = QuickSearchEdit(placeholder="Hľadať faktúru...")
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
            self.invoice_selected.emit(inv['id'], inv['invoice_number'])

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
                if s in normalize_for_search(r.get('supplier_name', ''))
                or s in normalize_for_search(r.get('invoice_number', ''))
            ]
        self.grid.set_data(self._filtered_data)

    def load_invoices(self, invoices: Optional[List[Dict[str, Any]]] = None):
        if invoices is not None:
            self._data = invoices
        self._filtered_data = self._data.copy()
        self.grid.set_data(self._filtered_data)
        self.title_label.setText(f"Faktúry ({len(self._data)})")

    def set_data(self, data: List[Dict[str, Any]]):
        self._data = data
        self.load_invoices()
''',

    "ui/widgets/invoice_items.py": '''"""
Supplier Invoice Staging - Invoice Items Widget
"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Slot

from shared_pyside6.ui import BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository
from config.settings import Settings


class InvoiceItemsWidget(QWidget):
    """Widget displaying invoice items with editable margin/price."""

    GRID_ID = "invoice_items_grid"
    items_updated = Signal()

    COLUMNS = [
        {"key": "id", "header": "ID", "width": 50, "visible": False},
        {"key": "line_number", "header": "#", "width": 40, "align": "right"},
        {"key": "xml_ean", "header": "EAN", "width": 120},
        {"key": "xml_name", "header": "Názov (XML)", "width": 200},
        {"key": "nex_product_name", "header": "Názov (NEX)", "width": 180},
        {"key": "xml_quantity", "header": "Množstvo", "width": 80, "align": "right"},
        {"key": "xml_unit", "header": "MJ", "width": 50},
        {"key": "xml_unit_price", "header": "NC/MJ", "width": 90, "align": "right"},
        {"key": "margin_percent", "header": "Marža %", "width": 80, "align": "right", "editable": True},
        {"key": "selling_price_excl_vat", "header": "PC bez DPH", "width": 100, "align": "right", "editable": True},
        {"key": "selling_price_incl_vat", "header": "PC s DPH", "width": 100, "align": "right"},
        {"key": "in_nex", "header": "V NEX", "width": 60, "align": "center"},
        {"key": "matched_by", "header": "Match", "width": 70},
        {"key": "item_status", "header": "Stav", "width": 80},
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

        self.title_label = QLabel("Položky faktúry")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.title_label)

        self.search_edit = QuickSearchEdit(placeholder="Hľadať položku...")
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
            nc = Decimal(str(item.get('xml_unit_price', 0)))
            vat = Decimal(str(item.get('xml_vat_rate') or self.settings.default_vat_rate))
            item['margin_percent'] = float(margin)
            item['selling_price_excl_vat'] = float(nc * (1 + margin / 100))
            item['selling_price_incl_vat'] = float(Decimal(str(item['selling_price_excl_vat'])) * (1 + vat / 100))
        except (ValueError, TypeError):
            pass

    def _recalc_from_price(self, item: Dict, selling_price: Any):
        try:
            pc = Decimal(str(selling_price or 0))
            nc = Decimal(str(item.get('xml_unit_price', 0)))
            vat = Decimal(str(item.get('xml_vat_rate') or self.settings.default_vat_rate))
            if nc > 0:
                item['margin_percent'] = float(((pc / nc) - 1) * 100)
            item['selling_price_excl_vat'] = float(pc)
            item['selling_price_incl_vat'] = float(pc * (1 + vat / 100))
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
                if s in normalize_for_search(r.get('xml_name', ''))
                or s in normalize_for_search(r.get('xml_ean', ''))
                or s in normalize_for_search(r.get('nex_product_name', ''))
            ]
        self.grid.set_data(self._filtered_data)

    def load_items(self, invoice_id: int, items: Optional[List[Dict[str, Any]]] = None):
        self._invoice_id = invoice_id
        if items is not None:
            self._data = items
        self._filtered_data = self._data.copy()
        self.grid.set_data(self._filtered_data)
        self.title_label.setText(f"Položky faktúry ({len(self._data)})")

    def set_data(self, data: List[Dict[str, Any]]):
        self._data = data
        self._filtered_data = data.copy()
        self.grid.set_data(self._filtered_data)

    def get_stats(self) -> Optional[Dict[str, Any]]:
        if not self._data:
            return None
        total = len(self._data)
        matched = sum(1 for i in self._data if i.get('in_nex'))
        priced = sum(1 for i in self._data if i.get('margin_percent', 0) > 0)
        return {
            'total': total, 'matched': matched, 'priced': priced,
            'matched_percent': (matched / total * 100) if total else 0,
            'priced_percent': (priced / total * 100) if total else 0,
        }

    def get_modified_items(self) -> List[Dict[str, Any]]:
        return [i for i in self._data if i.get('margin_percent', 0) > 0]
''',
}


def main():
    print(f"Creating app structure in: {APP_ROOT}")

    # Create directories
    for d in DIRS:
        path = APP_ROOT / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"  [DIR] {d or '.'}")

    # Create __init__.py files
    for f in INIT_FILES:
        path = APP_ROOT / f
        if not path.exists():
            path.write_text('"""Package."""\n', encoding='utf-8')
            print(f"  [INIT] {f}")

    # Create files
    for filename, content in FILES.items():
        path = APP_ROOT / filename
        path.write_text(content.strip() + '\n', encoding='utf-8')
        print(f"  [FILE] {filename}")

    print(f"\n✅ App structure created!")
    print(f"\nNext steps:")
    print(f"  1. Run: pip install -e packages/shared-pyside6")
    print(f"  2. Create database: supplier_invoice_staging")
    print(f"  3. Run schema: database/schemas/001_staging_schema.sql")
    print(f"  4. Set POSTGRES_PASSWORD environment variable")
    print(f"  5. Run: python -m supplier_invoice_staging")


if __name__ == "__main__":
    main()