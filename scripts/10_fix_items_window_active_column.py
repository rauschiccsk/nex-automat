"""
Fix InvoiceItemsWindow to save/load active search column.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # 1. Fix _on_column_changed to save active column
    old_code = '''    @Slot(int)
    def _on_column_changed(self, column: int):
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            # Keep stats but add column info
            self._update_status(f" | Stlpec: {col_name}")'''

    new_code = '''    @Slot(int)
    def _on_column_changed(self, column: int):
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            self._update_status(f" | Stlpec: {col_name}")
            # Save active column to grid settings
            self.grid.set_active_column(column)'''

    if old_code not in content:
        print("ERROR: Could not find _on_column_changed")
        return False

    content = content.replace(old_code, new_code)

    # 2. Fix initial column - load from saved settings instead of hardcoded 2
    old_code2 = '''        self.search_controller = QuickSearchController(
            self.grid.table_view,
            self.search_container,
            self.grid.header
        )
        self.search_controller.set_active_column(2)  # EAN column'''

    new_code2 = '''        self.search_controller = QuickSearchController(
            self.grid.table_view,
            self.search_container,
            self.grid.header
        )
        # Load saved column or default to 2 (EAN)
        saved_column = self.grid.get_active_column()
        if saved_column == 0:  # ID column is hidden
            saved_column = 2
        self.search_controller.set_active_column(saved_column)'''

    if old_code2 not in content:
        print("ERROR: Could not find search_controller setup")
        return False

    content = content.replace(old_code2, new_code2)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


if __name__ == "__main__":
    main()