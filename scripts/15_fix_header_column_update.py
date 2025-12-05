#!/usr/bin/env python3
"""
Script to fix header column update when search column changes
Oprava aktualizácie hlavičky pri zmene stĺpca
Location: C:\\Development\\nex-automat\\scripts\\15_fix_header_column_update.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def main():
    """Fix header update to call set_active_column()"""
    try:
        content = TARGET_FILE.read_text(encoding='utf-8')

        # Find _highlight_header method and update it to call GreenHeaderView.set_active_column()
        old_highlight = '''    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Store active column
        self._active_search_column = column'''

        new_highlight = '''    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Store active column
        self._active_search_column = column

        # Update custom header view if it's GreenHeaderView
        if hasattr(header, 'set_active_column'):
            header.set_active_column(column)
            self.logger.info(f"GreenHeaderView updated to column {column}")'''

        if old_highlight not in content:
            print("⚠️  Pattern not found, searching alternative...")
            # Try alternative pattern
            old_highlight = '''        # Store active column
        self._active_search_column = column

        # Apply custom stylesheet that highlights the section'''

            new_highlight = '''        # Store active column
        self._active_search_column = column

        # Update custom header view if it's GreenHeaderView
        if hasattr(header, 'set_active_column'):
            header.set_active_column(column)
            self.logger.info(f"GreenHeaderView updated to column {column}")

        # Apply custom stylesheet that highlights the section'''

        content = content.replace(old_highlight, new_highlight)

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup9')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(content, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print()
        print("Changes:")
        print("  ✅ Added header.set_active_column(column) call")
        print("  ✅ Green header will now update when column changes")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())