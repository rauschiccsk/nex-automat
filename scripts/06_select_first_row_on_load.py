"""
Select first row automatically after data load.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "self.grid.table_view.selectRow(0)" in content:
        print("SKIP: Already fixed")
        return True

    # Add selectRow(0) after populate_model in _load_test_data
    old_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()'''

    new_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        # Select first row
        if self._filtered_data:
            self.grid.table_view.selectRow(0)'''

    if old_code not in content:
        print("ERROR: Could not find _load_test_data pattern")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Added initial row selection to {file_path}")
    return True


if __name__ == "__main__":
    main()