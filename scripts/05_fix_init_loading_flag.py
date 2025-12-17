"""
Fix: Set _loading=True in __init__, clear only after apply_model_and_load_settings().
This prevents saving during initial setup in main_window.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\base_grid.py"

# 1. Change initial value to True
OLD_INIT_FLAG = '''        # Flag to prevent saving during load
        self._loading = False'''

NEW_INIT_FLAG = '''        # Flag to prevent saving during load (True until apply_model_and_load_settings)
        self._loading = True'''

# 2. Remove setting True at start of _load_grid_settings (it's already True)
OLD_LOAD_START = '''    def _load_grid_settings(self) -> None:
        """Load and apply saved grid settings."""
        self._loading = True  # Prevent save during load
        settings = self._repository.load_grid_settings('''

NEW_LOAD_START = '''    def _load_grid_settings(self) -> None:
        """Load and apply saved grid settings."""
        settings = self._repository.load_grid_settings('''

# 3. Move _loading = False to apply_model_and_load_settings (AFTER load)
OLD_APPLY = '''    def apply_model_and_load_settings(self) -> None:
        """
        Apply settings AFTER model is set.
        MUST be called by subclass AFTER self.table_view.setModel()!
        """
        if self._auto_load:
            self._load_grid_settings()'''

NEW_APPLY = '''    def apply_model_and_load_settings(self) -> None:
        """
        Apply settings AFTER model is set.
        MUST be called by subclass AFTER self.table_view.setModel()!
        """
        if self._auto_load:
            self._load_grid_settings()
        self._loading = False  # Now allow saving'''

# 4. Remove _loading = False from end of _load_grid_settings
OLD_LOAD_END = '''        if self._sort_column is not None:
            self.table_view.sortByColumn(self._sort_column, self._sort_order)

        self._loading = False  # Allow saving again'''

NEW_LOAD_END = '''        if self._sort_column is not None:
            self.table_view.sortByColumn(self._sort_column, self._sort_order)'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check all patterns
    checks = [
        (OLD_INIT_FLAG, "OLD_INIT_FLAG"),
        (OLD_LOAD_START, "OLD_LOAD_START"),
        (OLD_APPLY, "OLD_APPLY"),
        (OLD_LOAD_END, "OLD_LOAD_END"),
    ]

    for pattern, name in checks:
        if pattern not in content:
            print(f"ERROR: {name} not found")
            return False

    # Apply replacements
    content = content.replace(OLD_INIT_FLAG, NEW_INIT_FLAG)
    content = content.replace(OLD_LOAD_START, NEW_LOAD_START)
    content = content.replace(OLD_APPLY, NEW_APPLY)
    content = content.replace(OLD_LOAD_END, NEW_LOAD_END)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("_loading=True from init until apply_model_and_load_settings() completes")
    return True


if __name__ == "__main__":
    main()