"""
Invoice Items Grid - Editable grid for invoice line items
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex, pyqtSignal
from decimal import Decimal, InvalidOperation

from .quick_search import QuickSearchContainer, QuickSearchController, GreenHeaderView
from ...utils.constants import WINDOW_MAIN, GRID_INVOICE_ITEMS
from ...utils.grid_settings import (
    load_column_settings, save_column_settings,
    load_grid_settings, save_grid_settings
)



class InvoiceItemsModel(QAbstractTableModel):
    """Editable table model for invoice items"""

    COLUMNS = [
        ('PLU', 'plu_code', False),           # Not editable
        ('Názov', 'item_name', True),         # Editable
        ('Kategória', 'category_code', True), # Editable
        ('MJ', 'unit', True),                 # Editable
        ('Množstvo', 'quantity', True),       # Editable
        ('Cena', 'unit_price', True),         # Editable
        ('Rabat %', 'rabat_percent', True),   # Editable
        ('Po rabate', 'price_after_rabat', False),  # Calculated
        ('Suma', 'total_price', False)        # Calculated
    ]

    # Signal when items changed
    items_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []
        self.logger = logging.getLogger(__name__)

    def set_items(self, items):
        """Set item data"""
        self.beginResetModel()
        self._items = [dict(item) for item in items]  # Deep copy
        self.endResetModel()
        self.logger.info(f"Model updated with {len(items)} items")

    def get_items(self):
        """Get current items"""
        return self._items

    def rowCount(self, parent=None):
        """Return number of rows"""
        return len(self._items)

    def columnCount(self, parent=None):
        """Return number of columns"""
        return len(self.COLUMNS)

    def data(self, index, role=Qt.DisplayRole):
        """Return cell data"""
        if not index.isValid():
            return QVariant()

        item = self._items[index.row()]
        column_key = self.COLUMNS[index.column()][1]

        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = item.get(column_key, '')

            # Format numeric values for display
            if role == Qt.DisplayRole:
                if column_key in ('unit_price', 'price_after_rabat', 'total_price'):
                    if isinstance(value, (int, float, Decimal)):
                        return f"{float(value):.2f}"
                elif column_key == 'rabat_percent':
                    if isinstance(value, (int, float, Decimal)):
                        return f"{float(value):.1f}"
                elif column_key == 'quantity':
                    if isinstance(value, (int, float, Decimal)):
                        return f"{float(value):.3f}"

            return str(value)

        elif role == Qt.TextAlignmentRole:
            column_key = self.COLUMNS[index.column()][1]
            if column_key in ('quantity', 'unit_price', 'rabat_percent', 'price_after_rabat', 'total_price'):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.BackgroundRole:
            # Highlight calculated columns
            column_key = self.COLUMNS[index.column()][1]
            if column_key in ('price_after_rabat', 'total_price'):
                from PyQt5.QtGui import QColor
                return QColor(240, 240, 240)

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        """Set cell data"""
        if not index.isValid() or role != Qt.EditRole:
            return False

        column_key = self.COLUMNS[index.column()][1]
        column_editable = self.COLUMNS[index.column()][2]

        if not column_editable:
            return False

        item = self._items[index.row()]

        try:
            # Validate and convert value
            if column_key in ('quantity', 'unit_price', 'rabat_percent'):
                # Numeric fields
                value = value.strip() if isinstance(value, str) else str(value)
                if not value:
                    value = '0'

                # Convert to Decimal
                decimal_value = Decimal(value)

                # Range validation
                if column_key == 'rabat_percent':
                    if decimal_value < 0 or decimal_value > 100:
                        self.logger.warning(f"Invalid rabat: {decimal_value}")
                        return False
                elif column_key in ('quantity', 'unit_price'):
                    if decimal_value < 0:
                        self.logger.warning(f"Negative value not allowed: {decimal_value}")
                        return False

                item[column_key] = decimal_value

            else:
                # Text fields
                item[column_key] = str(value).strip()

            # Recalculate prices
            self._calculate_item_prices(item)

            # Emit signals
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])

            # Also update calculated columns in same row
            row = index.row()
            first_calc = self.index(row, 7)  # price_after_rabat
            last_calc = self.index(row, 8)   # total_price
            self.dataChanged.emit(first_calc, last_calc, [Qt.DisplayRole])

            self.items_changed.emit()

            return True

        except (ValueError, InvalidOperation) as e:
            self.logger.warning(f"Invalid input for {column_key}: {value} - {e}")
            return False

    def _calculate_item_prices(self, item):
        """Calculate price_after_rabat and total_price"""
        try:
            unit_price = Decimal(str(item.get('unit_price', 0)))
            rabat_percent = Decimal(str(item.get('rabat_percent', 0)))
            quantity = Decimal(str(item.get('quantity', 0)))

            # Price after rabat = unit_price * (1 - rabat_percent/100)
            price_after_rabat = unit_price * (Decimal('1') - rabat_percent / Decimal('100'))
            price_after_rabat = price_after_rabat.quantize(Decimal('0.01'))

            # Total price = price_after_rabat * quantity
            total_price = price_after_rabat * quantity
            total_price = total_price.quantize(Decimal('0.01'))

            item['price_after_rabat'] = price_after_rabat
            item['total_price'] = total_price

        except (ValueError, InvalidOperation) as e:
            self.logger.error(f"Price calculation error: {e}")
            item['price_after_rabat'] = Decimal('0.00')
            item['total_price'] = Decimal('0.00')

    def flags(self, index):
        """Return item flags"""
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        # Check if column is editable
        column_editable = self.COLUMNS[index.column()][2]
        if column_editable:
            flags |= Qt.ItemIsEditable

        return flags

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Return header data"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.COLUMNS[section][0]
            else:
                return str(section + 1)
        return QVariant()

    def sort(self, column, order=Qt.AscendingOrder):
        """Sort data by column"""
        if not self._items:
            return

        self.layoutAboutToBeChanged.emit()

        # Get column key
        column_key = self.COLUMNS[column][1]

        # Sort items
        reverse = (order == Qt.DescendingOrder)

        try:
            self._items.sort(
                key=lambda x: x.get(column_key, ''),
                reverse=reverse
            )
        except Exception as e:
            self.logger.error(f"Sort error: {e}")

        self.layoutChanged.emit()
        self.logger.info(f"Sorted by {column_key}, reverse={reverse}")


class InvoiceItemsGrid(QWidget):
    """Widget for editable invoice items grid"""

    # Signal when items changed
    items_changed = pyqtSignal()

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
        layout.setContentsMargins(0, 0, 0, 0)

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
        self.model = InvoiceItemsModel(self)
        self.table_view.setModel(self.model)

        # Configure headers
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)

        # Set column widths
        header.resizeSection(0, 80)   # PLU
        header.resizeSection(1, 300)  # Názov
        header.resizeSection(2, 80)   # Kategória
        header.resizeSection(3, 60)   # MJ
        header.resizeSection(4, 80)   # Množstvo
        header.resizeSection(5, 80)   # Cena
        header.resizeSection(6, 80)   # Rabat
        header.resizeSection(7, 90)   # Po rabate
        header.resizeSection(8, 90)   # Suma

        layout.addWidget(self.table_view)

        # Add quick search container (positions editor under active column)
        self.quick_search_container = QuickSearchContainer(self.table_view, self)
        layout.addWidget(self.quick_search_container)

        # Create quick search controller
        self.search_controller = QuickSearchController(self.table_view, self.quick_search_container)

        self.logger.info("Invoice items grid UI setup complete (with quick search)")


        # Connect header signals for grid settings
        header = self.table_view.horizontalHeader()
        header.sectionResized.connect(self._on_column_resized)
        header.sectionMoved.connect(self._on_column_moved)
    def _connect_signals(self):
        """Connect signals"""
        self.model.items_changed.connect(self.items_changed.emit)

    def set_items(self, items):
        """Set item data"""
        self.model.set_items(items)
        self.logger.info(f"Items grid updated with {len(items)} items")

        # Sort by current search column after data loaded
        if hasattr(self, 'search_controller'):
            current_col = self.search_controller.current_column
            self.search_controller._sort_by_column(current_col)
            self.logger.info(f"Re-sorted by column {current_col} after data load")

    def get_items(self):
        """Get current items"""
        return self.model.get_items()

    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        column_settings = load_column_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS)

        if column_settings:
            header = self.table_view.horizontalHeader()
            for col_idx in range(self.model.columnCount()):
                col_name = self.model.COLUMNS[col_idx][0]
                col_settings = next((s for s in column_settings if s.get('column_name') == col_name), None)
                if col_settings:
                    if 'width' in col_settings:
                        header.resizeSection(col_idx, col_settings['width'])
                    if 'visual_index' in col_settings:
                        header.moveSection(header.visualIndex(col_idx), col_settings['visual_index'])
                    if 'visible' in col_settings:
                        self.table_view.setColumnHidden(col_idx, not col_settings['visible'])

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        header = self.table_view.horizontalHeader()
        column_settings = []
        for col_idx in range(self.model.columnCount()):
            col_name = self.model.COLUMNS[col_idx][0]
            column_settings.append({
                'column_name': col_name,
                'width': header.sectionSize(col_idx),
                'visual_index': header.visualIndex(col_idx),
                'visible': not self.table_view.isColumnHidden(col_idx)
            })
        save_column_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, column_settings)
        save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, -1)  # -1 = no active column

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()

