"""
Fix: Save active search column to grid settings when changed.
"""
import os

TARGET_FILE = r"apps\supplier-invoice-staging\ui\main_window.py"

# 1. Update _on_column_changed to save to grid
OLD_ON_COLUMN = '''    @Slot(int)
    def _on_column_changed(self, column: int):
        """Update status when search column changes."""
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            self.status_label.setText(f"Vyhladavanie v: {col_name}")'''

NEW_ON_COLUMN = '''    @Slot(int)
    def _on_column_changed(self, column: int):
        """Update status when search column changes."""
        if 0 <= column < len(self.COLUMNS):
            col_name = self.COLUMNS[column][1]
            self.status_label.setText(f"Vyhladavanie v: {col_name}")
            # Save active column to grid settings
            self.grid.set_active_column(column)'''

# 2. Load saved column on startup (after search_controller init)
OLD_SEARCH_INIT = '''        # Set initial column (skip hidden ID column)
        self.search_controller.set_active_column(1)'''

NEW_SEARCH_INIT = '''        # Load saved column or default to 1 (skip hidden ID column)
        saved_column = self.grid.get_active_column()
        if saved_column == 0:  # ID column is hidden, use default
            saved_column = 1
        self.search_controller.set_active_column(saved_column)'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_ON_COLUMN not in content:
        print("ERROR: OLD_ON_COLUMN not found")
        return False

    if OLD_SEARCH_INIT not in content:
        print("ERROR: OLD_SEARCH_INIT not found")
        return False

    content = content.replace(OLD_ON_COLUMN, NEW_ON_COLUMN)
    content = content.replace(OLD_SEARCH_INIT, NEW_SEARCH_INIT)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("- _on_column_changed now saves to grid")
    print("- Startup loads saved column from grid")
    return True


if __name__ == "__main__":
    main()