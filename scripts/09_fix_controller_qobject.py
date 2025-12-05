#!/usr/bin/env python3
"""
Script to fix QuickSearchController - must inherit from QObject
Oprava QuickSearchController - musí dediť z QObject
Location: C:\\Development\\nex-automat\\scripts\\09_fix_controller_qobject.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def main():
    """Fix QuickSearchController inheritance"""
    try:
        # Read current content
        content = TARGET_FILE.read_text(encoding='utf-8')

        # Find and replace the class definition
        old_line = "class QuickSearchController:"
        new_line = "class QuickSearchController(QObject):"

        if old_line not in content:
            print(f"⚠️  Pattern not found: {old_line}")
            return 1

        # Replace
        new_content = content.replace(old_line, new_line)

        # Also need to add QObject import if not present
        import_line = "from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QEvent"
        new_import_line = "from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QEvent, QObject"

        if import_line in new_content:
            new_content = new_content.replace(import_line, new_import_line)

        # Also need to call super().__init__() in __init__
        # Find the __init__ method of QuickSearchController
        init_pattern = '''    def __init__(self, table_view, search_container):
        """
        Initialize quick search controller

        Args:
            table_view: QTableView instance
            search_container: QuickSearchContainer instance
        """
        self.table_view = table_view'''

        new_init_pattern = '''    def __init__(self, table_view, search_container):
        """
        Initialize quick search controller

        Args:
            table_view: QTableView instance
            search_container: QuickSearchContainer instance
        """
        super().__init__()

        self.table_view = table_view'''

        if init_pattern in new_content:
            new_content = new_content.replace(init_pattern, new_init_pattern)

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup3')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(new_content, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print()
        print("Changes:")
        print(f"  - Old: class QuickSearchController:")
        print(f"  + New: class QuickSearchController(QObject):")
        print(f"  + Added: QObject to imports")
        print(f"  + Added: super().__init__() call")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())