#!/usr/bin/env python3
"""
Script to update __init__.py to export QuickSearchContainer
Aktualizuje __init__.py pre export QuickSearchContainer
Location: C:\\Development\\nex-automat\\scripts\\08_update_init_for_container.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "__init__.py"

# New content
NEW_CONTENT = '''"""
UI Widgets Package
"""

from .invoice_list_widget import InvoiceListWidget, InvoiceListModel
from .invoice_items_grid import InvoiceItemsGrid, InvoiceItemsModel
from .quick_search import QuickSearchEdit, QuickSearchContainer, QuickSearchController

__all__ = [
    'InvoiceListWidget',
    'InvoiceListModel',
    'InvoiceItemsGrid',
    'InvoiceItemsModel',
    'QuickSearchEdit',
    'QuickSearchContainer',
    'QuickSearchController',
]
'''


def main():
    """Update __init__.py file"""
    try:
        # Check if file exists
        if not TARGET_FILE.exists():
            print(f"❌ File not found: {TARGET_FILE}")
            return 1

        # Backup original
        backup_file = TARGET_FILE.with_suffix('.py.backup2')
        import shutil
        shutil.copy2(TARGET_FILE, backup_file)
        print(f"📦 Backup created: {backup_file}")

        # Write new content
        TARGET_FILE.write_text(NEW_CONTENT, encoding='utf-8')

        print(f"✅ Updated: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print(f"📝 Lines: {len(NEW_CONTENT.splitlines())}")
        print()
        print("Changes:")
        print("  + Added export: QuickSearchContainer")
        print("  + All quick search components now exported")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())