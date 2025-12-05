#!/usr/bin/env python3
"""
Script to fix initial sorting on startup
Oprava počiatočného triedenia pri spustení
Location: C:\\Development\\nex-automat\\scripts\\16_fix_initial_sorting.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target files
QUICK_SEARCH_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"
INVOICE_LIST_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
INVOICE_ITEMS_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"


def fix_quick_search_init():
    """Fix QuickSearchController to disable initial sort and enable fresh sort"""
    content = QUICK_SEARCH_FILE.read_text(encoding='utf-8')

    # Find __init__ and update to disable sorting before setting up
    old_init = '''        # Install event filter on table to intercept arrow keys
        self.table_view.installEventFilter(self)

        # Connect signals
        self._connect_signals()

        # Initial sort
        self._sort_by_column(self.current_column)'''

    new_init = '''        # Disable any existing sorting first
        self.table_view.setSortingEnabled(False)

        # Install event filter on table to intercept arrow keys
        self.table_view.installEventFilter(self)

        # Connect signals
        self._connect_signals()

        # Initial sort - explicitly sort by first column
        self._sort_by_column(self.current_column)

        # Update header highlight for initial column
        if hasattr(self.search_container, '_highlight_header'):
            self.search_container._highlight_header(self.current_column)'''

    content = content.replace(old_init, new_init)

    # Backup and save
    backup = QUICK_SEARCH_FILE.with_suffix('.py.backup10')
    import shutil
    shutil.copy2(QUICK_SEARCH_FILE, backup)
    QUICK_SEARCH_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Fixed QuickSearchController initial sort")


def fix_invoice_list_widget():
    """Disable initial sorting in InvoiceListWidget"""
    content = INVOICE_LIST_FILE.read_text(encoding='utf-8')

    # Find where setSortingEnabled is called
    old_sorting = '''        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSortingEnabled(True)'''

    new_sorting = '''        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        # Sorting will be enabled by QuickSearchController
        self.table_view.setSortingEnabled(False)'''

    if old_sorting in content:
        content = content.replace(old_sorting, new_sorting)

        # Backup and save
        backup = INVOICE_LIST_FILE.with_suffix('.py.backup_init')
        import shutil
        shutil.copy2(INVOICE_LIST_FILE, backup)
        INVOICE_LIST_FILE.write_text(content, encoding='utf-8')
        print(f"✅ Fixed InvoiceListWidget initial sorting")
    else:
        print(f"⚠️  Pattern not found in InvoiceListWidget")


def fix_invoice_items_grid():
    """Disable initial sorting in InvoiceItemsGrid"""
    content = INVOICE_ITEMS_FILE.read_text(encoding='utf-8')

    # Find where table_view is created (no setSortingEnabled, so add it)
    old_creation = '''        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)

        # Create and set model'''

    new_creation = '''        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        # Sorting will be enabled by QuickSearchController
        self.table_view.setSortingEnabled(False)

        # Create and set model'''

    if old_creation in content:
        content = content.replace(old_creation, new_creation)

        # Backup and save
        backup = INVOICE_ITEMS_FILE.with_suffix('.py.backup_init')
        import shutil
        shutil.copy2(INVOICE_ITEMS_FILE, backup)
        INVOICE_ITEMS_FILE.write_text(content, encoding='utf-8')
        print(f"✅ Fixed InvoiceItemsGrid initial sorting")
    else:
        print(f"⚠️  Pattern not found in InvoiceItemsGrid")


def main():
    """Main execution"""
    try:
        print("=" * 60)
        print("Fixing initial sorting on startup...")
        print("=" * 60)
        print()

        # Step 1: Disable sorting in widgets (controller will enable it)
        fix_invoice_list_widget()
        fix_invoice_items_grid()
        print()

        # Step 2: Fix controller to explicitly sort on init
        fix_quick_search_init()
        print()

        print("=" * 60)
        print("✅ INITIAL SORTING FIXED")
        print("=" * 60)
        print()
        print("Changes:")
        print("  1. ✅ Disabled setSortingEnabled in both widgets")
        print("  2. ✅ QuickSearchController disables sorting before init")
        print("  3. ✅ QuickSearchController explicitly sorts by column 0 on init")
        print()
        print("Now test: Data should be sorted by PLU on startup!")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())