"""
Invoice List Widget - QTableView for displaying pending invoices
Refactored to use BaseGrid from nex-shared
"""

import logging
from decimal import Decimal
from pathlib import Path

from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, pyqtSignal

# Import BaseGrid from nex-shared
nex_shared_path = (
    Path(__file__).parent.parent.parent.parent.parent / "packages" / "nex-shared"
)
import sys

sys.path.insert(0, str(nex_shared_path))
from nex_shared.ui import BaseGrid

from ...utils.constants import GRID_INVOICE_LIST, WINDOW_MAIN

# Import QuickSearch components from local widgets
from .quick_search import QuickSearchContainer, QuickSearchController


class InvoiceListModel(QAbstractTableModel):
    """Table model for invoice list"""

    COLUMNS = [
        ("ID", "id"),
        ("Číslo faktúry", "invoice_number"),
        ("Dátum", "invoice_date"),
        ("Dodávateľ", "supplier_name"),
        ("IČO", "supplier_ico"),
        ("Suma", "total_amount"),
        ("Mena", "currency"),
        ("Stav", "status"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._invoices = []
        self.logger = logging.getLogger(__name__)

    def set_invoices(self, invoices):
        """Set invoice data"""
        self.beginResetModel()
        self._invoices = invoices
        self.endResetModel()
        self.logger.info(f"Model updated with {len(invoices)} invoices")

    def update_invoices(self, invoices):
        """Alias for set_invoices() - for compatibility with main_window.py"""
        self.set_invoices(invoices)

    def rowCount(self, parent=None):
        """Return number of rows"""
        return len(self._invoices)

    def columnCount(self, parent=None):
        """Return number of columns"""
        return len(self.COLUMNS)

    def data(self, index, role=Qt.DisplayRole):
        """Return cell data"""
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            invoice = self._invoices[index.row()]
            column_key = self.COLUMNS[index.column()][1]
            value = invoice.get(column_key, "")

            # Format values
            if column_key == "total_amount":
                if isinstance(value, (int, float, Decimal)):
                    return f"{float(value):.2f}"
            elif column_key == "status":
                status_map = {
                    "pending": "Čaká",
                    "approved": "Schválené",
                    "rejected": "Odmietnuté",
                }
                return status_map.get(value, value)

            return str(value)

        elif role == Qt.TextAlignmentRole:
            column_key = self.COLUMNS[index.column()][1]
            if column_key in ("id", "total_amount"):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Return header data"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.COLUMNS[section][0]
            else:
                return str(section + 1)
        return QVariant()

    def get_invoice(self, row):
        """Get invoice at row"""
        if 0 <= row < len(self._invoices):
            return self._invoices[row]
        return None

    def get_invoice_id(self, row):
        """Get invoice ID at row"""
        invoice = self.get_invoice(row)
        return invoice["id"] if invoice else None

    def sort(self, column, order=Qt.AscendingOrder):
        """Sort data by column"""
        if not self._invoices:
            return

        self.layoutAboutToBeChanged.emit()

        # Get column key
        column_key = self.COLUMNS[column][1]

        # Sort invoices
        reverse = order == Qt.DescendingOrder

        try:
            self._invoices.sort(key=lambda x: x.get(column_key, ""), reverse=reverse)
        except Exception as e:
            self.logger.error(f"Sort error: {e}")

        self.layoutChanged.emit()
        self.logger.info(f"Sorted by {column_key}, reverse={reverse}")


class InvoiceListWidget(BaseGrid):
    """Widget for displaying invoice list - uses BaseGrid"""

    # Signals
    invoice_selected = pyqtSignal(int)  # invoice_id
    invoice_activated = pyqtSignal(int)  # invoice_id (double-click)

    def __init__(self, invoice_service, parent=None):
        # Initialize BaseGrid
        super().__init__(
            window_name=WINDOW_MAIN, grid_name=GRID_INVOICE_LIST, parent=parent
        )

        self.invoice_service = invoice_service

        # Create and set model
        self.model = InvoiceListModel(self)
        self.table_view.setModel(self.model)

        # Setup custom UI (column widths, etc.)
        # REMOVED: self._setup_custom_ui() - BaseGrid loads settings from DB

        # Setup quick search
        self.setup_quick_search(QuickSearchContainer, QuickSearchController)

        # Connect signals
        self._connect_signals()

        # Apply model and load settings (AFTER model is set)
        self.apply_model_and_load_settings()

        self.logger.info("Invoice list widget initialized with BaseGrid")

    # REMOVED: _setup_custom_ui() - BaseGrid loads settings from DB
    # If you need default widths, set them in first run only
    def _connect_signals(self):
        """Connect signals"""
        # Selection changed
        selection_model = self.table_view.selectionModel()
        selection_model.currentRowChanged.connect(self._on_selection_changed)

        # Double-click
        self.table_view.doubleClicked.connect(self._on_double_clicked)

    def set_invoices(self, invoices):
        """Set invoice data"""
        self.model.set_invoices(invoices)
        self.logger.info(f"Invoice list updated with {len(invoices)} invoices")

        # Sort by current search column after data loaded
        if self.search_controller:
            current_col = self.search_controller.current_column
            self.search_controller._sort_by_column(current_col)
            self.logger.info(f"Re-sorted by column {current_col} after data load")

    def update_invoices(self, invoices):
        """Alias for set_invoices() - for compatibility with main_window.py"""
        self.set_invoices(invoices)

    def _on_selection_changed(self, current, previous):
        """Handle selection change"""
        if current.isValid():
            row = current.row()
            invoice_id = self.model.get_invoice_id(row)
            if invoice_id:
                self.invoice_selected.emit(invoice_id)

    def _on_double_clicked(self, index):
        """Handle double-click"""
        if index.isValid():
            row = index.row()
            invoice_id = self.model.get_invoice_id(row)
            if invoice_id:
                self.invoice_activated.emit(invoice_id)

    def get_selected_invoice(self):
        """Get currently selected invoice"""
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return self.model.get_invoice(row)
        return None

    def get_selected_invoice_id(self):
        """Get currently selected invoice ID"""
        invoice = self.get_selected_invoice()
        return invoice["id"] if invoice else None
