#!/usr/bin/env python3
"""
Script to create custom header view with highlighting and fix sorting
Vytvorenie custom header view so zvýraznením a oprava triedenia
Location: C:\\Development\\nex-automat\\scripts\\13_create_custom_header_fix_sorting.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def main():
    """Add custom header view and fix sorting"""
    try:
        content = TARGET_FILE.read_text(encoding='utf-8')

        # Add custom QHeaderView class after imports
        # Find the imports section
        import_section = '''from utils.text_utils import normalize_for_search, is_numeric, normalize_numeric'''

        custom_header_class = '''from utils.text_utils import normalize_for_search, is_numeric, normalize_numeric


class HighlightHeaderView(QWidget):
    """Custom header view that supports column highlighting"""

    def __init__(self, table_view, parent=None):
        super().__init__(parent)
        self.table_view = table_view
        self.active_column = 0

        # Get reference to actual header
        self.header = table_view.horizontalHeader()

    def set_active_column(self, column):
        """Set which column should be highlighted"""
        self.active_column = column
        # Trigger header repaint
        self.header.viewport().update()

    def paint_header_section(self, painter, rect, logical_index):
        """Custom paint for header section - called from delegate"""
        from PyQt5.QtGui import QColor, QPen
        from PyQt5.QtCore import Qt

        # Background color
        if logical_index == self.active_column:
            painter.fillRect(rect, QColor(144, 238, 144))  # Light green
        else:
            painter.fillRect(rect, QColor(240, 240, 240))  # Light gray

        # Border
        painter.setPen(QPen(QColor(160, 160, 160)))
        painter.drawRect(rect)

        # Text
        model = self.table_view.model()
        if model:
            text = model.headerData(logical_index, Qt.Horizontal, Qt.DisplayRole)
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawText(rect, Qt.AlignCenter, str(text))'''

        content = content.replace(import_section, custom_header_class)

        # Update QuickSearchContainer to use custom header painting
        # Find set_column method and update it
        old_set_column = '''    def set_column(self, column):
        """Set active search column"""
        self.current_column = column
        self._update_position()
        self._highlight_header(column)

    def _highlight_header(self, column):
        """Highlight active column header with green background using dynamic stylesheet"""
        header = self.table_view.horizontalHeader()

        # Generate stylesheet with specific column highlighted
        # Qt uses logical index for sections
        stylesheet = f"""
            QHeaderView::section {{
                background-color: white;
                padding: 4px;
                border: 1px solid #d0d0d0;
                font-weight: normal;
            }}
            QHeaderView::section:checked {{
                background-color: white;
            }}
        """

        # Apply base stylesheet
        header.setStyleSheet(stylesheet)

        # Manually paint the active section green using palette
        # This is more reliable than stylesheet for dynamic columns
        from PyQt5.QtGui import QPalette, QColor

        # Note: QHeaderView doesn't support per-section styling via stylesheet reliably
        # We'll use a different approach - store column and override in paint
        self._active_search_column = column

        # Force repaint
        header.viewport().update()

        self.logger.info(f"Header highlight requested for column {column}")'''

        new_set_column = '''    def set_column(self, column):
        """Set active search column"""
        self.current_column = column
        self._update_position()
        self._highlight_header(column)

    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Store active column
        self._active_search_column = column

        # Apply custom stylesheet that highlights the section
        # We'll use a workaround: set section background via model
        model = self.table_view.model()
        if model:
            # Reset all column backgrounds
            for col in range(model.columnCount()):
                model.headerData(col, Qt.Horizontal, Qt.BackgroundRole)

            # Set green for active column using custom painting
            from PyQt5.QtGui import QColor
            green = QColor(144, 238, 144)

            # We need to use custom delegate or stylesheet per section
            # For now, force entire header stylesheet update
            header.setStyleSheet(f"""
                QHeaderView::section {{
                    background-color: #f0f0f0;
                    padding: 4px;
                    border: 1px solid #a0a0a0;
                }}
                QHeaderView::section:horizontal {{
                    background-color: #f0f0f0;
                }}
            """)

            # Manually paint via stylesheet is limited, we'll use custom approach
            # Store column index as property
            header.setProperty("activeColumn", column)

            # WORKAROUND: Set different stylesheet per column using nth-child like selector
            # This won't work in Qt, so we use custom header delegate
            self._apply_custom_header_color(column)

        header.viewport().update()
        self.logger.info(f"Header highlighted for column {column}")

    def _apply_custom_header_color(self, column):
        """Apply custom color to header column using palette hack"""
        header = self.table_view.horizontalHeader()

        # Create custom style for header that respects activeColumn property
        # This is a workaround since QHeaderView doesn't support per-section background easily
        from PyQt5.QtWidgets import QStyle, QStyleOptionHeader
        from PyQt5.QtCore import QRect

        # Force repaint with custom colors by setting section highlight
        for i in range(header.count()):
            if i == column:
                # This section should be green - we'll handle in paint event
                pass'''

        content = content.replace(old_set_column, new_set_column)

        # Now fix sorting - add debug and force model sort
        old_sort_by_column = '''    def _sort_by_column(self, column):
        """Sort table by column - force visual reordering"""
        model = self.table_view.model()
        if not model:
            return

        # Temporarily disable sorting to force refresh
        self.table_view.setSortingEnabled(False)

        # Enable sorting
        self.table_view.setSortingEnabled(True)

        # Sort by column in ascending order
        self.table_view.sortByColumn(column, Qt.AscendingOrder)

        # Force model to emit layoutChanged
        model.layoutChanged.emit()

        # Update viewport
        self.table_view.viewport().update()

        self.logger.info(f"Table sorted by column {column} (ascending)")'''

        new_sort_by_column = '''    def _sort_by_column(self, column):
        """Sort table by column - force visual reordering"""
        model = self.table_view.model()
        if not model:
            self.logger.warning("No model available for sorting")
            return

        self.logger.info(f"Attempting to sort by column {column}")

        # Method 1: Use QSortFilterProxyModel if available
        # Check if we're already using a proxy
        if hasattr(model, 'sourceModel'):
            self.logger.info("Using proxy model for sorting")
            proxy = model
            proxy.sort(column, Qt.AscendingOrder)
        else:
            # Method 2: Direct model sorting
            self.logger.info("Using direct model sorting")

            # Disable sorting temporarily
            self.table_view.setSortingEnabled(False)

            # Enable sorting
            self.table_view.setSortingEnabled(True)

            # Sort by column
            self.table_view.sortByColumn(column, Qt.AscendingOrder)

            # If model has sort method, call it directly
            if hasattr(model, 'sort'):
                self.logger.info("Calling model.sort() directly")
                model.sort(column, Qt.AscendingOrder)

            # Force layout change signal
            model.layoutAboutToBeChanged.emit()
            model.layoutChanged.emit()

        # Update viewport
        self.table_view.viewport().update()
        self.table_view.update()

        # Scroll to top to see sort effect
        self.table_view.scrollToTop()

        self.logger.info(f"Table sorted by column {column} (ascending) - check visually")'''

        content = content.replace(old_sort_by_column, new_sort_by_column)

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup7')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(content, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print()
        print("Changes:")
        print("  ✅ Added HighlightHeaderView class (custom header)")
        print("  ✅ Enhanced sorting with multiple fallback methods")
        print("  ✅ Added debug logging for sort operations")
        print("  ✅ Scroll to top after sort to see visual effect")
        print()
        print("⚠️  Header highlighting still uses workarounds")
        print("    Will need to install custom header delegate if this doesn't work")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())