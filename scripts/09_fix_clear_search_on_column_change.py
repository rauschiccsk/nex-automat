"""
Fix: Clear search text when changing column with arrow keys.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\quick_search.py"

# In QuickSearchController._change_column, clear search edit after changing column
OLD_CHANGE_COLUMN = '''    def _change_column(self, direction: int) -> None:
        """Change search column."""
        model = self._table_view.model()
        if not model:
            return

        new_column = self._active_column + direction

        # Wrap around
        if new_column < 0:
            new_column = model.columnCount() - 1
        elif new_column >= model.columnCount():
            new_column = 0

        # Skip hidden columns
        while self._table_view.isColumnHidden(new_column):
            new_column += direction
            if new_column < 0:
                new_column = model.columnCount() - 1
            elif new_column >= model.columnCount():
                new_column = 0

        self.set_active_column(new_column)'''

NEW_CHANGE_COLUMN = '''    def _change_column(self, direction: int) -> None:
        """Change search column."""
        model = self._table_view.model()
        if not model:
            return

        new_column = self._active_column + direction

        # Wrap around
        if new_column < 0:
            new_column = model.columnCount() - 1
        elif new_column >= model.columnCount():
            new_column = 0

        # Skip hidden columns
        while self._table_view.isColumnHidden(new_column):
            new_column += direction
            if new_column < 0:
                new_column = model.columnCount() - 1
            elif new_column >= model.columnCount():
                new_column = 0

        # Clear search text when changing column
        self._search_container.search_edit.clear()

        self.set_active_column(new_column)'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_CHANGE_COLUMN not in content:
        print("ERROR: OLD_CHANGE_COLUMN not found")
        return False

    content = content.replace(OLD_CHANGE_COLUMN, NEW_CHANGE_COLUMN)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("- Search text cleared when changing column with arrows")
    return True


if __name__ == "__main__":
    main()