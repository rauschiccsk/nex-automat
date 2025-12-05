#!/usr/bin/env python3
"""
Script to update widgets to use QuickSearchContainer
Aktualizuje widgety pre použitie QuickSearchContainer
Location: C:\\Development\\nex-automat\\scripts\\07_update_widgets_for_container.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target files
TARGET_FILE_1 = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
TARGET_FILE_2 = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"

# Content for invoice_list_widget.py
CONTENT_1 = '''"""
Invoice List Widget - QTableView for displaying pending invoices
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, pyqtSignal
from decimal import Decimal

from .quick_search import QuickSearchContainer, QuickSearchController


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

    def _setup_ui(self):
        """Setup widget UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create table view
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSortingEnabled(True)

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
'''

# Content for invoice_items_grid.py
CONTENT_2 = '''"""
Invoice Items Grid - Editable grid for invoice line items
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex, pyqtSignal
from decimal import Decimal, InvalidOperation

from .quick_search import QuickSearchContainer, QuickSearchController


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

    def _setup_ui(self):
        """Setup widget UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create table view
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)

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

    def _connect_signals(self):
        """Connect signals"""
        self.model.items_changed.connect(self.items_changed.emit)

    def set_items(self, items):
        """Set item data"""
        self.model.set_items(items)
        self.logger.info(f"Items grid updated with {len(items)} items")

    def get_items(self):
        """Get current items"""
        return self.model.get_items()
'''


def main():
    """Update both widget files"""
    try:
        success_count = 0

        # Update invoice_list_widget.py
        if TARGET_FILE_1.exists():
            backup_file_1 = TARGET_FILE_1.with_suffix('.py.backup2')
            import shutil
            shutil.copy2(TARGET_FILE_1, backup_file_1)
            print(f"📦 Backup created: {backup_file_1}")

            TARGET_FILE_1.write_text(CONTENT_1, encoding='utf-8')
            print(f"✅ Updated: {TARGET_FILE_1}")
            success_count += 1
        else:
            print(f"⚠️  File not found: {TARGET_FILE_1}")

        print()

        # Update invoice_items_grid.py
        if TARGET_FILE_2.exists():
            backup_file_2 = TARGET_FILE_2.with_suffix('.py.backup2')
            shutil.copy2(TARGET_FILE_2, backup_file_2)
            print(f"📦 Backup created: {backup_file_2}")

            TARGET_FILE_2.write_text(CONTENT_2, encoding='utf-8')
            print(f"✅ Updated: {TARGET_FILE_2}")
            success_count += 1
        else:
            print(f"⚠️  File not found: {TARGET_FILE_2}")

        print()
        print(f"✅ Successfully updated {success_count}/2 files")
        print()
        print("Changes:")
        print("  + Import changed: QuickSearchEdit → QuickSearchContainer")
        print("  + Widget changed: quick_search → quick_search_container")
        print("  + Container automatically positions editor under active column")

        return 0 if success_count == 2 else 1

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())