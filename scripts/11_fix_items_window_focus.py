"""
Fix: Set focus to table_view in InvoiceItemsWindow after data load.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    if "self.grid.table_view.setFocus()" in content:
        print("SKIP: Already fixed")
        return True

    old_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()'''

    new_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()
        self.grid.table_view.setFocus()'''

    if old_code not in content:
        print("ERROR: Could not find pattern")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


if __name__ == "__main__":
    main()