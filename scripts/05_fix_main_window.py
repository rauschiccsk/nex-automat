"""Fix main_window.py to use correct BaseWindow API"""
from pathlib import Path

MAIN_WINDOW = Path("C:/Development/nex-automat/apps/supplier-invoice-staging/ui/main_window.py")

CONTENT = '''"""Main Window"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QStatusBar, QLabel, QMessageBox
from PySide6.QtCore import Qt, Slot

from shared_pyside6.ui import BaseWindow
from shared_pyside6.database import SettingsRepository

from config.settings import Settings
from ui.widgets.invoice_list import InvoiceListWidget
from ui.widgets.invoice_items import InvoiceItemsWidget


class MainWindow(BaseWindow):
    WINDOW_ID = "supplier_invoice_staging_main"

    def __init__(self, settings: Settings):
        self.settings = settings

        # Settings repository for grid persistence
        settings_db = settings.get_settings_db_path()
        settings_db.parent.mkdir(parents=True, exist_ok=True)
        self.settings_repo = SettingsRepository(str(settings_db))

        # BaseWindow expects: window_name, default_size, default_pos, user_id, auto_load, parent
        super().__init__(
            window_name=self.WINDOW_ID,
            default_size=(1200, 800),
            default_pos=(100, 100),
            auto_load=True
        )

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

MAIN_WINDOW.write_text(CONTENT, encoding="utf-8")
print(f"Fixed: {MAIN_WINDOW}")
print("\nRun: python app.py")