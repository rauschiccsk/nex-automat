"""
Invoice List Widget - QTableView for displaying pending invoices
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, pyqtSignal
from ...utils.constants import WINDOW_MAIN, GRID_INVOICE_LIST
from ...utils.grid_settings import (
    load_column_settings, save_column_settings,
    load_grid_settings, save_grid_settings
)
from decimal import Decimal

from .quick_search import QuickSearchContainer, QuickSearchController, GreenHeaderView


class InvoiceListModel(QAbstractTableModel):
    """Table model for invoice list"""

    COLUMNS = [
        ('ID', 'id'),
        ('Číslo faktúry', 'invoice_number'),
        ('Dátum', 'invoice_date'),
        ('Dodávateľ', 'supplier_name'),
        ('IČO', 'supplier_ico'),
        ('Suma', 'total_amount'),
        ('Mena', 'currency'),
        ('Stav', 'status')
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
            value = invoice.get(column_key, '')

            # Format values
            if column_key == 'total_amount':
                if isinstance(value, (int, float, Decimal)):
                    return f"{float(value):.2f}"
            elif column_key == 'status':
                status_map = {
                    'pending': 'Čaká',
                    'approved': 'Schválené',
                    'rejected': 'Odmietnuté'
                }
                return status_map.get(value, value)

            return str(value)

        elif role == Qt.TextAlignmentRole:
            column_key = self.COLUMNS[index.column()][1]
            if column_key in ('id', 'total_amount'):
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
        return invoice['id'] if invoice else None

    def sort(self, column, order=Qt.AscendingOrder):
        """Sort data by column"""
        if not self._invoices:
            return

        self.layoutAboutToBeChanged.emit()

        # Get column key
        column_key = self.COLUMNS[column][1]

        # Sort invoices
        reverse = (order == Qt.DescendingOrder)

        try:
            self._invoices.sort(
                key=lambda x: x.get(column_key, ''),
                reverse=reverse
            )
        except Exception as e:
            self.logger.error(f"Sort error: {e}")

        self.layoutChanged.emit()
        self.logger.info(f"Sorted by {column_key}, reverse={reverse}")


class InvoiceListWidget(QWidget):
    """Widget for displaying invoice list"""

    # Signals
    invoice_selected = pyqtSignal(int)  # invoice_id
    invoice_activated = pyqtSignal(int)  # invoice_id (double-click)

    def __init__(self, invoice_service, parent=None):
        super().__init__(parent)

        self.invoice_service = invoice_service
        self.logger = logging.getLogger(__name__)

        self._setup_ui()
        self._connect_signals()


        # Load grid settings
        self._load_grid_settings()
    def _setup_ui(self):
        """Setup widget UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create table view
        self.table_view = QTableView()

        # Replace header with custom green header
        custom_header = GreenHeaderView(Qt.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(custom_header)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        # Sorting will be enabled by QuickSearchController
        self.table_view.setSortingEnabled(False)

        # Create and set model
        self.model = InvoiceListModel(self)
        self.table_view.setModel(self.model)

        # Configure headers
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)

        # Set column widths
        header.resizeSection(0, 60)   # ID
        header.resizeSection(1, 150)  # Invoice Number
        header.resizeSection(2, 100)  # Date
        header.resizeSection(3, 300)  # Supplier Name
        header.resizeSection(4, 100)  # ICO
        header.resizeSection(5, 100)  # Amount
        header.resizeSection(6, 60)   # Currency
        header.resizeSection(7, 100)  # Status

        layout.addWidget(self.table_view)

        # Add quick search container (positions editor under active column)
        self.quick_search_container = QuickSearchContainer(self.table_view, self)
        layout.addWidget(self.quick_search_container)

        # Create quick search controller
        self.search_controller = QuickSearchController(self.table_view, self.quick_search_container)

        self.logger.info("Invoice list widget UI setup complete (with quick search)")

        # Connect header signals for grid settings
        header.sectionResized.connect(self._on_column_resized)
        header.sectionMoved.connect(self._on_column_moved)

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
        if hasattr(self, 'search_controller'):
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
        return invoice['id'] if invoice else None


    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        from ...utils.constants import GRID_INVOICE_LIST
        from ...utils.grid_settings import load_column_settings, load_grid_settings

        # Načítaj column settings
        column_settings = load_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST)

        if column_settings:
            header = self.table_view.horizontalHeader()

            # Aplikuj nastavenia pre každý stĺpec
            for col_idx in range(self.model.columnCount()):
                col_name = self.model.COLUMNS[col_idx][0]
                # Nájdi nastavenia pre tento stĺpec
                col_settings = next((s for s in column_settings if s.get('column_name') == col_name), None)
                if col_settings:

                    # Šírka stĺpca
                    if 'width' in col_settings:
                        header.resizeSection(col_idx, col_settings['width'])

                    # Vizuálny index (poradie)
                    if 'visual_index' in col_settings:
                        header.moveSection(header.visualIndex(col_idx), col_settings['visual_index'])

                    # Viditeľnosť
                    if 'visible' in col_settings:
                        self.table_view.setColumnHidden(col_idx, not col_settings['visible'])

        # Načítaj grid settings (active column pre quick search)
        grid_settings = load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)

        if grid_settings and 'active_column_index' in grid_settings:
            active_col = grid_settings['active_column_index']
            # Nastav aktívny stĺpec v quick search
            if hasattr(self, 'search_controller') and self.search_controller:
                self.search_controller.set_active_column(active_col)
                self.logger.info(f"Loaded active column: {active_col}")

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        from ...utils.constants import GRID_INVOICE_LIST
        from ...utils.grid_settings import save_column_settings, save_grid_settings

        header = self.table_view.horizontalHeader()

        # Zozbieraj column settings
        column_settings = []
        for col_idx in range(self.model.columnCount()):
            col_name = self.model.COLUMNS[col_idx][0]
            column_settings.append({
                'column_name': col_name,
                'width': header.sectionSize(col_idx),
                'visual_index': header.visualIndex(col_idx),
                'visible': not self.table_view.isColumnHidden(col_idx)
            })

        # Ulož column settings
        save_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST, column_settings)

        # Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'search_controller') and self.search_controller:
            active_column = self.search_controller.get_active_column()
            self.logger.info(f"Saving active column: {active_column}")

        # Ulož grid settings (active_column_index ako tretí parameter)
        if active_column is not None:
            save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST, active_column)

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()
