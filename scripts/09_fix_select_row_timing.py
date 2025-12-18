"""
Fix: Move select_initial_row call to after data population.
BaseGrid provides the method, windows call it after populating data.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def fix_base_grid():
    """Remove auto-call from apply_model, make method public."""
    file_path = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Remove _select_initial_row call from apply_model_and_load_settings
    old_code = '''    def apply_model_and_load_settings(self) -> None:
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

    new_code = '''    def apply_model_and_load_settings(self) -> None:
        """
        Apply settings AFTER model is set.
        MUST be called by subclass AFTER self.table_view.setModel()!
        """
        if self._auto_load:
            self._load_grid_settings()
        self._loading = False  # Now allow saving

    def select_initial_row(self) -> None:
        """
        Select first row or restore last position.
        Call this AFTER populating model with data.
        """
        model = self.table_view.model()
        if not model or model.rowCount() == 0:
            return

        # Try to restore last position first
        if not self.restore_cursor_position():
            # Otherwise select first row
            self.table_view.selectRow(0)'''

    if old_code not in content:
        print("ERROR: Could not find expected code in base_grid.py")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


def fix_main_window():
    """Add select_initial_row call after _populate_model."""
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    old_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()'''

    new_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()'''

    if old_code not in content:
        print(f"ERROR: Could not find pattern in {file_path}")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


def fix_items_window():
    """Add select_initial_row call after _populate_model."""
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    old_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()'''

    new_code = '''        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()'''

    if old_code not in content:
        print(f"ERROR: Could not find pattern in {file_path}")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


def main():
    fix_base_grid()
    fix_main_window()
    fix_items_window()
    print("Done!")


if __name__ == "__main__":
    main()