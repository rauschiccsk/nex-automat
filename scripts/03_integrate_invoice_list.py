#!/usr/bin/env python3
"""
Script to integrate quick search into invoice_list_widget.py
Integruje rýchlo-vyhľadávač do invoice_list_widget.py
Location: C:\\Development\\nex-automat\\scripts\\03_integrate_invoice_list.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"

# New content
NEW_CONTENT = '''"""
Invoice List Widget - QTableView for displaying pending invoices
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, pyqtSignal
from decimal import Decimal

from .quick_search import QuickSearchEdit, QuickSearchController


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

        # Add quick search widget
        self.quick_search = QuickSearchEdit(self)
        layout.addWidget(self.quick_search)

        # Create quick search controller
        self.search_controller = QuickSearchController(self.table_view, self.quick_search)

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


def main():
    """Update invoice_list_widget.py file"""
    try:
        # Check if file exists
        if not TARGET_FILE.exists():
            print(f"❌ File not found: {TARGET_FILE}")
            return 1

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup')
        TARGET_FILE.rename(backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(NEW_CONTENT, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print(f"📝 Lines: {len(NEW_CONTENT.splitlines())}")
        print()
        print("Changes:")
        print("  + Added import: QuickSearchEdit, QuickSearchController")
        print("  + Added quick_search widget to layout")
        print("  + Created search_controller instance")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

        # Restore backup if exists
        if backup_file.exists() and not TARGET_FILE.exists():
            backup_file.rename(TARGET_FILE)
            print(f"↩️  Backup restored")

        return 1


if __name__ == "__main__":
    sys.exit(main())