#!/usr/bin/env python3
"""
Script to update widgets __init__.py to export quick search components
Aktualizuje __init__.py pre export quick search komponentov
Location: C:\\Development\\nex-automat\\scripts\\05_update_widgets_init.py
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
from .quick_search import QuickSearchEdit, QuickSearchController

__all__ = [
    'InvoiceListWidget',
    'InvoiceListModel',
    'InvoiceItemsGrid',
    'InvoiceItemsModel',
    'QuickSearchEdit',
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
        backup_file = TARGET_FILE.with_suffix('.py.backup')
        if TARGET_FILE.exists():
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
        print("  + Updated __all__ exports")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

        # Restore backup if exists
        backup_file = TARGET_FILE.with_suffix('.py.backup')
        if backup_file.exists() and not TARGET_FILE.exists():
            backup_file.rename(TARGET_FILE)
            print(f"↩️  Backup restored")

        return 1


if __name__ == "__main__":
    sys.exit(main())