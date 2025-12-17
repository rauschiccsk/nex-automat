"""
Fix: Prevent saving during initialization.
Column resize during init was overwriting saved settings.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\base_grid.py"

# 1. Add _loading flag to __init__
OLD_INIT = '''        # Debounce timer for saving
        self._save_pending = False

        self._setup_base_ui()'''

NEW_INIT = '''        # Debounce timer for saving
        self._save_pending = False

        # Flag to prevent saving during load
        self._loading = False

        self._setup_base_ui()'''

# 2. Set flag during load
OLD_LOAD = '''    def _load_grid_settings(self) -> None:
        """Load and apply saved grid settings."""
        settings = self._repository.load_grid_settings('''

NEW_LOAD = '''    def _load_grid_settings(self) -> None:
        """Load and apply saved grid settings."""
        self._loading = True  # Prevent save during load
        settings = self._repository.load_grid_settings('''

# 3. Clear flag after load - find the end of _load_grid_settings
OLD_LOAD_END = '''        if self._sort_column is not None:
            self.table_view.sortByColumn(self._sort_column, self._sort_order)'''

NEW_LOAD_END = '''        if self._sort_column is not None:
            self.table_view.sortByColumn(self._sort_column, self._sort_order)

        self._loading = False  # Allow saving again'''

# 4. Check flag before saving
OLD_SAVE_CHECK = '''    def _save_grid_settings(self) -> None:
        """Save current grid settings."""
        model = self.table_view.model()
        if not model:
            return'''

NEW_SAVE_CHECK = '''    def _save_grid_settings(self) -> None:
        """Save current grid settings."""
        if self._loading:
            return  # Don't save during initialization

        model = self.table_view.model()
        if not model:
            return'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check all patterns exist
    checks = [
        (OLD_INIT, "OLD_INIT"),
        (OLD_LOAD, "OLD_LOAD"),
        (OLD_LOAD_END, "OLD_LOAD_END"),
        (OLD_SAVE_CHECK, "OLD_SAVE_CHECK"),
    ]

    for pattern, name in checks:
        if pattern not in content:
            print(f"ERROR: {name} not found in file")
            return False

    # Apply all replacements
    content = content.replace(OLD_INIT, NEW_INIT)
    content = content.replace(OLD_LOAD, NEW_LOAD)
    content = content.replace(OLD_LOAD_END, NEW_LOAD_END)
    content = content.replace(OLD_SAVE_CHECK, NEW_SAVE_CHECK)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("Added: _loading flag to prevent save during init")
    return True


if __name__ == "__main__":
    main()