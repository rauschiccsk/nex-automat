#!/usr/bin/env python3
"""
Script to implement sort() in models and create custom header view
Implementácia sort() v modeloch a vytvorenie custom header view
Location: C:\\Development\\nex-automat\\scripts\\14_implement_sort_and_custom_header.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target files
QUICK_SEARCH_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"
INVOICE_LIST_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
INVOICE_ITEMS_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"

# New custom header view code for quick_search.py
CUSTOM_HEADER_VIEW = '''from utils.text_utils import normalize_for_search, is_numeric, normalize_numeric


class SearchableHeaderView(QWidget):
    """Custom header view with green highlighting for active search column"""

    def __init__(self, orientation, parent=None):
        from PyQt5.QtWidgets import QHeaderView
        # We need to return actual QHeaderView subclass
        # This won't work as widget, needs to be proper header
        pass


class HighlightableHeaderView(QWidget):
    """Header view that supports column highlighting - uses custom paint delegate"""

    from PyQt5.QtWidgets import QHeaderView
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter, QColor

    def __init__(self, table_view):
        from PyQt5.QtWidgets import QHeaderView, QStyledItemDelegate
        from PyQt5.QtCore import Qt, QRect
        from PyQt5.QtGui import QPainter, QColor, QPen

        # Create custom QHeaderView subclass
        class GreenHeaderView(QHeaderView):
            def __init__(self, orientation, parent=None):
                super().__init__(orientation, parent)
                self.active_column = 0

            def paintSection(self, painter, rect, logicalIndex):
                """Custom paint for each section"""
                painter.save()

                # Background
                if logicalIndex == self.active_column:
                    painter.fillRect(rect, QColor(144, 238, 144))  # Green
                else:
                    painter.fillRect(rect, QColor(240, 240, 240))  # Light gray

                # Border
                painter.setPen(QPen(QColor(160, 160, 160)))
                painter.drawLine(rect.topRight(), rect.bottomRight())
                painter.drawLine(rect.bottomLeft(), rect.bottomRight())

                # Text
                text = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
                painter.setPen(QPen(QColor(0, 0, 0)))
                painter.drawText(rect, Qt.AlignCenter, str(text) if text else "")

                painter.restore()

            def set_active_column(self, column):
                """Set active column and repaint"""
                self.active_column = column
                self.viewport().update()

        self.HeaderClass = GreenHeaderView'''

# Code to add to quick_search.py after imports
QUICK_SEARCH_HEADER_ADDITION = '''from utils.text_utils import normalize_for_search, is_numeric, normalize_numeric
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen


class GreenHeaderView(QHeaderView):
    """Custom QHeaderView with green highlighting for active column"""

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.active_column = 0

    def paintSection(self, painter, rect, logicalIndex):
        """Custom paint for each header section"""
        painter.save()

        # Background color
        if logicalIndex == self.active_column:
            painter.fillRect(rect, QColor(144, 238, 144))  # Light green
        else:
            painter.fillRect(rect, QColor(240, 240, 240))  # Light gray

        # Border
        painter.setPen(QPen(QColor(160, 160, 160)))
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        # Text
        text = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(rect, Qt.AlignCenter, str(text) if text else "")

        painter.restore()

    def set_active_column(self, column):
        """Set which column is active for search"""
        self.active_column = column
        self.viewport().update()'''


def add_sort_to_invoice_list_model():
    """Add sort() method to InvoiceListModel"""
    content = INVOICE_LIST_FILE.read_text(encoding='utf-8')

    # Find the get_invoice_id method and add sort after it
    insertion_point = '''    def get_invoice_id(self, row):
        """Get invoice ID at row"""
        invoice = self.get_invoice(row)
        return invoice['id'] if invoice else None'''

    sort_method = '''    def get_invoice_id(self, row):
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
        self.logger.info(f"Sorted by {column_key}, reverse={reverse}")'''

    content = content.replace(insertion_point, sort_method)

    # Backup and save
    backup = INVOICE_LIST_FILE.with_suffix('.py.backup_sort')
    import shutil
    shutil.copy2(INVOICE_LIST_FILE, backup)
    INVOICE_LIST_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Added sort() to InvoiceListModel")


def add_sort_to_invoice_items_model():
    """Add sort() method to InvoiceItemsModel"""
    content = INVOICE_ITEMS_FILE.read_text(encoding='utf-8')

    # Find the headerData method and add sort after it
    insertion_point = '''    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Return header data"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.COLUMNS[section][0]
            else:
                return str(section + 1)
        return QVariant()'''

    sort_method = '''    def headerData(self, section, orientation, role=Qt.DisplayRole):
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
        self.logger.info(f"Sorted by {column_key}, reverse={reverse}")'''

    content = content.replace(insertion_point, sort_method)

    # Backup and save
    backup = INVOICE_ITEMS_FILE.with_suffix('.py.backup_sort')
    import shutil
    shutil.copy2(INVOICE_ITEMS_FILE, backup)
    INVOICE_ITEMS_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Added sort() to InvoiceItemsModel")


def add_custom_header_to_quick_search():
    """Add GreenHeaderView class to quick_search.py"""
    content = QUICK_SEARCH_FILE.read_text(encoding='utf-8')

    # Replace import line
    old_import = '''from utils.text_utils import normalize_for_search, is_numeric, normalize_numeric'''
    content = content.replace(old_import, QUICK_SEARCH_HEADER_ADDITION)

    # Backup and save
    backup = QUICK_SEARCH_FILE.with_suffix('.py.backup8')
    import shutil
    shutil.copy2(QUICK_SEARCH_FILE, backup)
    QUICK_SEARCH_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Added GreenHeaderView to quick_search.py")


def update_widgets_to_use_green_header():
    """Update both widgets to use GreenHeaderView"""
    for file_path, widget_name in [(INVOICE_LIST_FILE, "InvoiceListWidget"),
                                   (INVOICE_ITEMS_FILE, "InvoiceItemsGrid")]:
        content = file_path.read_text(encoding='utf-8')

        # Add import
        old_import = '''from .quick_search import QuickSearchContainer, QuickSearchController'''
        new_import = '''from .quick_search import QuickSearchContainer, QuickSearchController, GreenHeaderView'''
        content = content.replace(old_import, new_import)

        # Find where table_view is created and replace header
        # Look for "self.table_view = QTableView()"
        old_table_creation = '''        # Create table view
        self.table_view = QTableView()'''

        new_table_creation = '''        # Create table view
        self.table_view = QTableView()

        # Replace header with custom green header
        custom_header = GreenHeaderView(Qt.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(custom_header)'''

        content = content.replace(old_table_creation, new_table_creation)

        # Save
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Updated {widget_name} to use GreenHeaderView")


def main():
    """Main execution"""
    try:
        print("=" * 60)
        print("Implementing sort() and custom header view...")
        print("=" * 60)
        print()

        # Step 1: Add sort() to models
        add_sort_to_invoice_list_model()
        add_sort_to_invoice_items_model()
        print()

        # Step 2: Add GreenHeaderView to quick_search
        add_custom_header_to_quick_search()
        print()

        # Step 3: Update widgets to use GreenHeaderView
        update_widgets_to_use_green_header()
        print()

        print("=" * 60)
        print("✅ ALL UPDATES COMPLETE")
        print("=" * 60)
        print()
        print("Changes:")
        print("  1. ✅ Added sort() method to InvoiceListModel")
        print("  2. ✅ Added sort() method to InvoiceItemsModel")
        print("  3. ✅ Created GreenHeaderView class (custom QHeaderView)")
        print("  4. ✅ Updated InvoiceListWidget to use GreenHeaderView")
        print("  5. ✅ Updated InvoiceItemsGrid to use GreenHeaderView")
        print()
        print("Now test: sorting should work AND headers should be green!")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())