"""
Invoice Items Grid - Editable grid for invoice line items
Refactored to use BaseGrid from nex-shared
"""

import logging
from pathlib import Path
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex, pyqtSignal
from decimal import Decimal, InvalidOperation

# Import BaseGrid from nex-shared
nex_shared_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "nex-shared"
import sys
sys.path.insert(0, str(nex_shared_path))
from nex_shared.ui import BaseGrid

# Import QuickSearch components from local widgets
from .quick_search import QuickSearchContainer, QuickSearchController

from ...utils.constants import WINDOW_MAIN, GRID_INVOICE_ITEMS


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
        ('Suma', 'total_price', False),       # Calculated
        # NEX Genesis enrichment columns
        ('NEX Kód', 'nex_gs_code', False),    # From enrichment
        ('NEX Názov', 'nex_name', False),     # From enrichment
        ('NEX Kat.', 'nex_category', False),  # From enrichment
        ('Match', 'in_nex', False)            # Match status
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
            from PyQt5.QtGui import QColor
            column_key = self.COLUMNS[index.column()][1]

            # Highlight calculated columns
            if column_key in ('price_after_rabat', 'total_price'):
                return QColor(240, 240, 240)

            # Color rows based on NEX match status
            in_nex = item.get('in_nex')
            if in_nex is True:
                # Matched - light green
                return QColor(200, 255, 200)
            elif in_nex is False:
                # No match - light red
                return QColor(255, 200, 200)
            elif in_nex is None:
                # Pending - light yellow
                return QColor(255, 255, 200)

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


class InvoiceItemsGrid(BaseGrid):
    """Widget for editable invoice items grid - uses BaseGrid"""

    # Signal when items changed
    items_changed = pyqtSignal()

    def __init__(self, invoice_service, parent=None):
        # Initialize BaseGrid
        super().__init__(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_ITEMS,
            parent=parent
        )

        self.invoice_service = invoice_service

        # Create and set model
        self.model = InvoiceItemsModel(self)
        self.table_view.setModel(self.model)

        # Setup custom UI (column widths, etc.)
        # REMOVED: self._setup_custom_ui() - BaseGrid loads settings from DB

        # Setup quick search
        self.setup_quick_search(QuickSearchContainer, QuickSearchController)

        # Connect signals
        self._connect_signals()

        # Apply model and load settings (AFTER model is set)
        self.apply_model_and_load_settings()

        self.logger.info("Invoice items grid initialized with BaseGrid")

    # REMOVED: _setup_custom_ui() - BaseGrid loads settings from DB
    # If you need default widths, set them in first run only
    def _connect_signals(self):
        """Connect signals"""
        self.model.items_changed.connect(self.items_changed.emit)

    def set_items(self, items):
        """Set item data"""
        self.model.set_items(items)
        self.logger.info(f"Items grid updated with {len(items)} items")

        # Sort by current search column after data loaded
        if self.search_controller:
            current_col = self.search_controller.current_column
            self.search_controller._sort_by_column(current_col)
            self.logger.info(f"Re-sorted by column {current_col} after data load")

    def get_items(self):
        """Get current items"""
        return self.model.get_items()
