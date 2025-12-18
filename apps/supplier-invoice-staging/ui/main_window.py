"""Main Window - Invoice List with QuickSearch"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStatusBar, QLabel, QMessageBox
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem

from shared_pyside6.ui import BaseWindow, BaseGrid
from shared_pyside6.ui.quick_search import QuickSearchContainer, QuickSearchController

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
        self._items_windows = {}

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

        # QuickSearch - positioned under grid
        self.search_container = QuickSearchContainer(self.grid.table_view, self)
        layout.addWidget(self.search_container)

        # QuickSearch Controller
        self.search_controller = QuickSearchController(
            self.grid.table_view,
            self.search_container,
            self.grid.header  # GreenHeaderView
        )

        # Load saved column or default to 1 (skip hidden ID column)
        saved_column = self.grid.get_active_column()
        if saved_column == 0:  # ID column is hidden, use default
            saved_column = 1
        self.search_controller.set_active_column(saved_column)

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
        self.grid.row_selected.connect(self._on_row_selected)
        self.grid.row_activated.connect(self._on_row_activated)
        self.search_controller.active_column_changed.connect(self._on_column_changed)

    @Slot(int)
    def _on_column_changed(self, column: int):
        """Update status when search column changes."""
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            self.status_label.setText(f"Vyhladavanie v: {col_name}")
            # Save active column to grid settings
            self.grid.set_active_column(column)

    @Slot(int)
    def _on_row_selected(self, row: int):
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self.status_label.setText(f"Faktura: {inv['invoice_number']} | {inv['supplier_name']}")

    @Slot(int)
    def _on_row_activated(self, row: int):
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self._open_items_window(inv)

    def _open_items_window(self, invoice: dict):
        invoice_id = invoice["id"]

        if invoice_id in self._items_windows:
            window = self._items_windows[invoice_id]
            if window.isVisible():
                window.activateWindow()
                window.raise_()
                return

        window = InvoiceItemsWindow(
            invoice=invoice,
            settings=self.settings,
            parent=self
        )
        window.closed.connect(lambda: self._on_items_window_closed(invoice_id))
        self._items_windows[invoice_id] = window
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.show()

    def _on_items_window_closed(self, invoice_id: int):
        if invoice_id in self._items_windows:
            del self._items_windows[invoice_id]

    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = self.grid.create_item(value, editable=False)
                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")

    def _load_test_data(self):
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
            {"id": 4, "supplier_name": "TESCO", "invoice_number": "F2024-004",
             "invoice_date": "2024-12-12", "total_amount": 550.25, "currency": "EUR",
             "status": "pending", "item_count": 5, "match_percent": 20.0},
            {"id": 5, "supplier_name": "BILLA", "invoice_number": "F2024-005",
             "invoice_date": "2024-12-11", "total_amount": 1800.00, "currency": "EUR",
             "status": "matched", "item_count": 12, "match_percent": 100.0},
        ]
        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()

    def _refresh_data(self):
        self._load_test_data()

    def _show_about(self):
        QMessageBox.about(self, "O programe", 
            "Supplier Invoice Staging v1.0\n\n"
            "Aplikacia pre spravu dodavatelskych faktur\n"
            "a nastavenie obchodnej marze.\n\n"
            "ICC Komarno 2025")

    def keyPressEvent(self, event):
        """Handle key press - Enter opens invoice items."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            current_row = self.grid.table_view.currentIndex().row()
            if current_row >= 0:
                self._on_row_activated(current_row)
                return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        for window in list(self._items_windows.values()):
            window.close()
        self.grid.save_grid_settings_now()
        super().closeEvent(event)
