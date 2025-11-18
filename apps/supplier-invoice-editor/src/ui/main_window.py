"""
Main Window - Invoice Editor
Qt5 main application window with menu, toolbar, and invoice list
"""

import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStatusBar,
    QMenuBar, QMenu, QAction, QToolBar, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QKeySequence

from .widgets.invoice_list_widget import InvoiceListWidget
from business.invoice_service import InvoiceService


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, config, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logging.getLogger(__name__)
        self.invoice_service = InvoiceService(config)

        self._setup_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._connect_signals()

        # Load initial data
        QTimer.singleShot(0, self._load_invoices)

    def _setup_ui(self):
        """Setup main window UI"""
        self.setWindowTitle("Invoice Editor - ISDOC Approval")
        self.resize(1400, 900)

        # Central widget with invoice list
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Invoice list widget
        self.invoice_list = InvoiceListWidget(self.invoice_service)
        layout.addWidget(self.invoice_list)

        self.setCentralWidget(central_widget)

        self.logger.info("Main window UI setup complete")

    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&Súbor")

        refresh_action = QAction("&Obnoviť", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.setStatusTip("Obnoviť zoznam faktúr")
        refresh_action.triggered.connect(self._on_refresh)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        exit_action = QAction("&Ukončiť", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Ukončiť aplikáciu")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Upraviť")

        search_action = QAction("&Hľadať", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.setStatusTip("Hľadať faktúru")
        search_action.triggered.connect(self._on_search)
        edit_menu.addAction(search_action)

        # View menu
        view_menu = menubar.addMenu("&Zobrazenie")

        # Help menu
        help_menu = menubar.addMenu("&Pomoc")

        about_action = QAction("&O programe", self)
        about_action.setStatusTip("Informácie o aplikácii")
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

        self.logger.info("Menu bar created")

    def _create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar("Hlavný panel")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Refresh action
        refresh_action = QAction("Obnoviť", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.setStatusTip("Obnoviť zoznam faktúr (F5)")
        refresh_action.triggered.connect(self._on_refresh)
        toolbar.addAction(refresh_action)

        toolbar.addSeparator()

        # Search action
        search_action = QAction("Hľadať", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.setStatusTip("Hľadať faktúru (Ctrl+F)")
        search_action.triggered.connect(self._on_search)
        toolbar.addAction(search_action)

        toolbar.addSeparator()

        # Approve action (placeholder)
        approve_action = QAction("Schváliť", self)
        approve_action.setStatusTip("Schváliť vybranú faktúru")
        approve_action.setEnabled(False)  # Disabled for now
        toolbar.addAction(approve_action)

        # Reject action (placeholder)
        reject_action = QAction("Odmietnuť", self)
        reject_action.setStatusTip("Odmietnuť vybranú faktúru")
        reject_action.setEnabled(False)  # Disabled for now
        toolbar.addAction(reject_action)

        self.logger.info("Toolbar created")

    def _create_status_bar(self):
        """Create status bar"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Initial message
        self.statusbar.showMessage("Pripravené | F5: Obnoviť | Ctrl+F: Hľadať")

        self.logger.info("Status bar created")

    def _connect_signals(self):
        """Connect widget signals"""
        # Invoice selection changed
        self.invoice_list.invoice_selected.connect(self._on_invoice_selected)

        # Invoice double-clicked
        self.invoice_list.invoice_activated.connect(self._on_invoice_activated)

    def _load_invoices(self):
        """Load invoices from database"""
        try:
            self.statusbar.showMessage("Načítavam faktúry...")
            self.logger.info("Loading invoices...")

            invoices = self.invoice_service.get_pending_invoices()
            self.invoice_list.set_invoices(invoices)

            count = len(invoices)
            self.statusbar.showMessage(
                f"Načítaných {count} faktúr | F5: Obnoviť | Ctrl+F: Hľadať"
            )
            self.logger.info(f"Loaded {count} invoices")

        except Exception as e:
            self.logger.exception("Failed to load invoices")
            self.statusbar.showMessage("Chyba pri načítaní faktúr")
            QMessageBox.warning(
                self,
                "Chyba",
                f"Nepodarilo sa načítať faktúry:\n\n{str(e)}"
            )

    def _on_refresh(self):
        """Refresh invoice list"""
        self.logger.info("Refresh triggered")
        self._load_invoices()

    def _on_search(self):
        """Open search dialog"""
        self.logger.info("Search triggered")
        self.statusbar.showMessage("Vyhľadávanie bude dostupné v ďalšej verzii")
        # TODO: Implement search dialog

    def _on_invoice_selected(self, invoice_id):
        """Handle invoice selection"""
        self.logger.info(f"Invoice selected: {invoice_id}")
        self.statusbar.showMessage(f"Vybraná faktúra ID: {invoice_id}")

    def _on_invoice_activated(self, invoice_id):
        """Handle invoice double-click"""
        self.logger.info(f"Invoice activated: {invoice_id}")

        # Open detail window
        from .invoice_detail_window import InvoiceDetailWindow

        detail_window = InvoiceDetailWindow(
            self.invoice_service,
            invoice_id,
            self
        )

        # Connect save signal
        detail_window.invoice_saved.connect(self._on_invoice_saved)

        # Show as modal dialog
        detail_window.exec_()

    def _on_invoice_saved(self, invoice_id):
        """Handle invoice saved signal"""
        self.logger.info(f"Invoice {invoice_id} saved, refreshing list")
        self._load_invoices()


    def _on_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "O programe",
            "<h3>Invoice Editor</h3>"
            "<p>ISDOC Invoice Approval & NEX Genesis Integration</p>"
            "<p>Version: 0.1.0 (Session 3 - UI Foundation)</p>"
            "<p>© 2025 ICC Komárno</p>"
            "<p>Developer: Zoltán</p>"
        )

    def closeEvent(self, event):
        """Handle window close event"""
        self.logger.info("Application closing")
        event.accept()
