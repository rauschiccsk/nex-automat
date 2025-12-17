"""
Move initial row selection to BaseGrid and remove duplicates from windows.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def fix_base_grid():
    file_path = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "self._select_initial_row()" in content:
        print(f"SKIP: {file_path} already fixed")
        return True

    # 1. Add _select_initial_row method after apply_model_and_load_settings
    old_code = '''    def apply_model_and_load_settings(self) -> None:
        """
        Apply settings AFTER model is set.
        MUST be called by subclass AFTER self.table_view.setModel()!
        """
        if self._auto_load:
            self._load_grid_settings()
        self._loading = False  # Now allow saving'''

    new_code = '''    def apply_model_and_load_settings(self) -> None:
        """
        Apply settings AFTER model is set.
        MUST be called by subclass AFTER self.table_view.setModel()!
        """
        if self._auto_load:
            self._load_grid_settings()
        self._loading = False  # Now allow saving
        self._select_initial_row()

    def _select_initial_row(self) -> None:
        """Select first row or restore last position after model load."""
        model = self.table_view.model()
        if not model or model.rowCount() == 0:
            return

        # Try to restore last position first
        if not self.restore_cursor_position():
            # Otherwise select first row
            self.table_view.selectRow(0)'''

    if old_code not in content:
        print("ERROR: Could not find apply_model_and_load_settings")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


def fix_main_window():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Remove duplicate selectRow code
    old_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        # Select first row
        if self._filtered_data:
            self.grid.table_view.selectRow(0)'''

    new_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        file_path.write_text(content, encoding="utf-8")
        print(f"OK: Removed duplicate from {file_path}")
    else:
        print(f"SKIP: {file_path} no duplicate found")

    return True


def fix_items_window():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Remove duplicate selectRow code
    old_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        # Select first row
        if self._filtered_data:
            self.grid.table_view.selectRow(0)'''

    new_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        file_path.write_text(content, encoding="utf-8")
        print(f"OK: Removed duplicate from {file_path}")
    else:
        print(f"SKIP: {file_path} no duplicate found")

    return True


def main():
    fix_base_grid()
    fix_main_window()
    fix_items_window()
    print("Done!")


if __name__ == "__main__":
    main()