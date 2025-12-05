#!/usr/bin/env python3
"""
Script to fix header highlighting and sorting behavior
Oprava zvýraznenia hlavičky a správneho triedenia
Location: C:\\Development\\nex-automat\\scripts\\11_fix_header_highlight_and_sorting.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def main():
    """Fix header highlighting using stylesheet and force sorting"""
    try:
        content = TARGET_FILE.read_text(encoding='utf-8')

        # Fix 1: Replace _highlight_header method with stylesheet approach
        old_highlight = '''    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Reset all headers to default
        for col in range(header.count()):
            header.model().setHeaderData(col, Qt.Horizontal, None, Qt.BackgroundRole)

        # Set green background for active column
        from PyQt5.QtGui import QColor
        green = QColor(144, 238, 144)  # Light green - same as editor
        header.model().setHeaderData(column, Qt.Horizontal, green, Qt.BackgroundRole)'''

        new_highlight = '''    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Store current column for stylesheet
        self._active_column = column

        # Force header repaint with stylesheet
        # We'll set a property and use stylesheet selector
        header.setProperty("activeColumn", column)
        header.style().unpolish(header)
        header.style().polish(header)
        header.update()

        self.logger.debug(f"Header highlighted for column {column}")'''

        content = content.replace(old_highlight, new_highlight)

        # Fix 2: Improve _sort_by_column to force visual reordering
        old_sort = '''    def _sort_by_column(self, column):
        """Sort table by column"""
        # Ensure sorting is enabled
        if not self.table_view.isSortingEnabled():
            self.table_view.setSortingEnabled(True)

        # Sort by column
        self.table_view.sortByColumn(column, Qt.AscendingOrder)

        self.logger.info(f"Sorted by column {column}")'''

        new_sort = '''    def _sort_by_column(self, column):
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

        content = content.replace(old_sort, new_sort)

        # Fix 3: Update QuickSearchContainer to apply stylesheet to header
        # Find the __init__ method of QuickSearchContainer
        old_container_init = '''    def __init__(self, table_view, parent=None):
        super().__init__(parent)

        self.table_view = table_view
        self.logger = logging.getLogger(__name__)

        # Create search edit
        self.search_edit = QuickSearchEdit(self)

        # Set container height
        self.setFixedHeight(25)

        # Current column
        self.current_column = 0

        # Update position when table layout changes
        self.table_view.horizontalHeader().sectionResized.connect(self._update_position)

        # Initial position
        QTimer.singleShot(0, self._update_position)'''

        new_container_init = '''    def __init__(self, table_view, parent=None):
        super().__init__(parent)

        self.table_view = table_view
        self.logger = logging.getLogger(__name__)

        # Create search edit
        self.search_edit = QuickSearchEdit(self)

        # Set container height
        self.setFixedHeight(25)

        # Current column
        self.current_column = 0

        # Apply stylesheet to header for highlighting
        header = self.table_view.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: white;
                padding: 4px;
                border: 1px solid #d0d0d0;
            }
            QHeaderView::section[activeColumn="0"] {
                background-color: rgb(144, 238, 144);
            }
        """)

        # Update position when table layout changes
        self.table_view.horizontalHeader().sectionResized.connect(self._update_position)

        # Initial position
        QTimer.singleShot(0, self._update_position)'''

        content = content.replace(old_container_init, new_container_init)

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup5')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(content, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print()
        print("Changes:")
        print("  ✅ Header highlight: Using stylesheet + property for green background")
        print("  ✅ Sorting: Force layoutChanged emit + viewport update")
        print("  ✅ Added stylesheet to header in container init")
        print()
        print("Note: Header stylesheet may need per-column logic - will verify after test")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())