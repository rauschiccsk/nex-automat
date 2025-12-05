#!/usr/bin/env python3
"""
Script to fix sorting by calling it AFTER data is loaded
Oprava triedenia - zavolá sa PO načítaní dát
Location: C:\\Development\\nex-automat\\scripts\\17_fix_sort_after_data_load.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target files
INVOICE_LIST_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
INVOICE_ITEMS_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"


def fix_invoice_list_widget():
    """Add sort call after set_invoices()"""
    content = INVOICE_LIST_FILE.read_text(encoding='utf-8')

    # Find set_invoices method and add sort call
    old_set_invoices = '''    def set_invoices(self, invoices):
        """Set invoice data"""
        self.model.set_invoices(invoices)
        self.logger.info(f"Invoice list updated with {len(invoices)} invoices")'''

    new_set_invoices = '''    def set_invoices(self, invoices):
        """Set invoice data"""
        self.model.set_invoices(invoices)
        self.logger.info(f"Invoice list updated with {len(invoices)} invoices")

        # Sort by current search column after data loaded
        if hasattr(self, 'search_controller'):
            current_col = self.search_controller.current_column
            self.search_controller._sort_by_column(current_col)
            self.logger.info(f"Re-sorted by column {current_col} after data load")'''

    content = content.replace(old_set_invoices, new_set_invoices)

    # Backup and save
    backup = INVOICE_LIST_FILE.with_suffix('.py.backup_sort2')
    import shutil
    shutil.copy2(INVOICE_LIST_FILE, backup)
    INVOICE_LIST_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Fixed InvoiceListWidget to sort after data load")


def fix_invoice_items_grid():
    """Add sort call after set_items()"""
    content = INVOICE_ITEMS_FILE.read_text(encoding='utf-8')

    # Find set_items method and add sort call
    old_set_items = '''    def set_items(self, items):
        """Set item data"""
        self.model.set_items(items)
        self.logger.info(f"Items grid updated with {len(items)} items")'''

    new_set_items = '''    def set_items(self, items):
        """Set item data"""
        self.model.set_items(items)
        self.logger.info(f"Items grid updated with {len(items)} items")

        # Sort by current search column after data loaded
        if hasattr(self, 'search_controller'):
            current_col = self.search_controller.current_column
            self.search_controller._sort_by_column(current_col)
            self.logger.info(f"Re-sorted by column {current_col} after data load")'''

    content = content.replace(old_set_items, new_set_items)

    # Backup and save
    backup = INVOICE_ITEMS_FILE.with_suffix('.py.backup_sort2')
    import shutil
    shutil.copy2(INVOICE_ITEMS_FILE, backup)
    INVOICE_ITEMS_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Fixed InvoiceItemsGrid to sort after data load")


def main():
    """Main execution"""
    try:
        print("=" * 60)
        print("Fixing sort to happen AFTER data load...")
        print("=" * 60)
        print()

        fix_invoice_list_widget()
        fix_invoice_items_grid()
        print()

        print("=" * 60)
        print("✅ SORT AFTER DATA LOAD FIXED")
        print("=" * 60)
        print()
        print("Changes:")
        print("  ✅ set_invoices() now sorts after data is loaded")
        print("  ✅ set_items() now sorts after data is loaded")
        print()
        print("Logic: Controller sorts empty model → ignored")
        print("       Data loads → set_invoices() → sorts with actual data!")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())