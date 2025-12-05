#!/usr/bin/env python3
"""
Script to fix editor positioning, sorting and add header highlighting
Oprava pozície editora, triedenia a zvýraznenie hlavičky
Location: C:\\Development\\nex-automat\\scripts\\10_fix_positioning_sorting_highlight.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def main():
    """Fix positioning, sorting and add header highlighting"""
    try:
        content = TARGET_FILE.read_text(encoding='utf-8')

        # Fix 1: Update _update_position to account for vertical header
        old_update_position = '''    def _update_position(self):
        """Update editor position to match current column"""
        header = self.table_view.horizontalHeader()

        # Get column position and width
        col_x = header.sectionViewportPosition(self.current_column)
        col_width = header.sectionSize(self.current_column)

        # Position editor under column
        self.search_edit.setGeometry(col_x, 0, col_width, 25)

        self.logger.debug(f"Search editor positioned: x={col_x}, width={col_width}, column={self.current_column}")'''

        new_update_position = '''    def _update_position(self):
        """Update editor position to match current column"""
        header = self.table_view.horizontalHeader()

        # Account for vertical header (row numbers)
        vertical_header_width = self.table_view.verticalHeader().width()

        # Get column position and width
        col_x = header.sectionViewportPosition(self.current_column) + vertical_header_width
        col_width = header.sectionSize(self.current_column)

        # Position editor under column
        self.search_edit.setGeometry(col_x, 0, col_width, 25)

        self.logger.debug(f"Search editor positioned: x={col_x}, width={col_width}, column={self.current_column}")'''

        content = content.replace(old_update_position, new_update_position)

        # Fix 2: Add method to highlight header
        # Find the set_column method and add highlight logic
        old_set_column = '''    def set_column(self, column):
        """Set active search column"""
        self.current_column = column
        self._update_position()'''

        new_set_column = '''    def set_column(self, column):
        """Set active search column"""
        self.current_column = column
        self._update_position()
        self._highlight_header(column)

    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Reset all headers to default
        for col in range(header.count()):
            header.model().setHeaderData(col, Qt.Horizontal, None, Qt.BackgroundRole)

        # Set green background for active column
        from PyQt5.QtGui import QColor
        green = QColor(144, 238, 144)  # Light green - same as editor
        header.model().setHeaderData(column, Qt.Horizontal, green, Qt.BackgroundRole)'''

        content = content.replace(old_set_column, new_set_column)

        # Fix 3: Ensure sorting happens on column change
        # The _sort_by_column already exists, but let's make sure it's actually sorting
        old_sort_by_column = '''    def _sort_by_column(self, column):
        """Sort table by column"""
        self.table_view.sortByColumn(column, Qt.AscendingOrder)
        self.logger.debug(f"Sorted by column {column}")'''

        new_sort_by_column = '''    def _sort_by_column(self, column):
        """Sort table by column"""
        # Ensure sorting is enabled
        if not self.table_view.isSortingEnabled():
            self.table_view.setSortingEnabled(True)

        # Sort by column
        self.table_view.sortByColumn(column, Qt.AscendingOrder)

        self.logger.info(f"Sorted by column {column}")'''

        content = content.replace(old_sort_by_column, new_sort_by_column)

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup4')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(content, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print()
        print("Changes:")
        print("  ✅ Fix 1: Editor position accounts for vertical header (row numbers)")
        print("  ✅ Fix 2: Active column header highlighted with green background")
        print("  ✅ Fix 3: Sorting explicitly enabled and logged")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())