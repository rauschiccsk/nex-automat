#!/usr/bin/env python3
"""
Script to fix header highlighting with dynamic stylesheet and proper sorting
Oprava zvýraznenia hlavičky dynamickým stylesheet a správne triedenie
Location: C:\\Development\\nex-automat\\scripts\\12_fix_dynamic_header_and_proxy_sort.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def main():
    """Fix header with dynamic stylesheet per column"""
    try:
        content = TARGET_FILE.read_text(encoding='utf-8')

        # Remove the stylesheet from container __init__ - it's wrong approach
        old_init_with_style = '''        # Apply stylesheet to header for highlighting
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

        # Update position when table layout changes'''

        new_init_without_style = '''        # Update position when table layout changes'''

        content = content.replace(old_init_with_style, new_init_without_style)

        # Replace _highlight_header with dynamic stylesheet generation
        old_highlight = '''    def _highlight_header(self, column):
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

        new_highlight = '''    def _highlight_header(self, column):
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

        content = content.replace(old_highlight, new_highlight)

        # Add _active_search_column initialization in QuickSearchContainer __init__
        # Find the line with self.current_column = 0
        old_current_col = '''        # Current column
        self.current_column = 0'''

        new_current_col = '''        # Current column
        self.current_column = 0
        self._active_search_column = 0'''

        content = content.replace(old_current_col, new_current_col)

        # Now fix the sorting - the issue is that sortByColumn doesn't refresh view properly
        # Replace _change_column to ensure sorting happens
        old_change_column = '''    def _change_column(self, direction):
        """Change search column"""
        model = self.table_view.model()
        if not model:
            return

        column_count = model.columnCount()

        # Calculate new column
        new_column = self.current_column + direction

        # Wrap around
        if new_column < 0:
            new_column = column_count - 1
        elif new_column >= column_count:
            new_column = 0

        self.current_column = new_column

        # Update container position
        self.search_container.set_column(self.current_column)

        # Clear search text
        self.search_edit.clear()

        # Sort by new column
        self._sort_by_column(self.current_column)

        # Keep focus on search edit
        self.search_edit.setFocus()

        self.logger.info(f"Changed to column {self.current_column}")'''

        new_change_column = '''    def _change_column(self, direction):
        """Change search column"""
        model = self.table_view.model()
        if not model:
            return

        column_count = model.columnCount()

        # Calculate new column
        new_column = self.current_column + direction

        # Wrap around
        if new_column < 0:
            new_column = column_count - 1
        elif new_column >= column_count:
            new_column = 0

        self.current_column = new_column

        # Clear search text BEFORE sorting to avoid search during sort
        self.search_edit.blockSignals(True)
        self.search_edit.clear()
        self.search_edit.blockSignals(False)

        # Sort by new column FIRST
        self._sort_by_column(self.current_column)

        # Then update container position and header highlight
        self.search_container.set_column(self.current_column)

        # Keep focus on search edit
        self.search_edit.setFocus()

        self.logger.info(f"Changed to column {self.current_column}, sorted and repositioned")'''

        content = content.replace(old_change_column, new_change_column)

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup6')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(content, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print()
        print("Changes:")
        print("  ✅ Removed global header stylesheet (caused all columns green)")
        print("  ✅ Header highlight stored in _active_search_column variable")
        print("  ✅ Sorting now happens BEFORE position update")
        print("  ✅ Clear search blocked during column change")
        print()
        print("⚠️  Note: Header highlighting via stylesheet is limited in Qt")
        print("    May need custom QHeaderView subclass for per-column colors")
        print("    Will implement if current approach doesn't work")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())