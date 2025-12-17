"""
Fix: Column navigation should use visual index, not logical index.
Arrow keys should move in visual order after column reordering.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\quick_search.py"

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

        # Clear search text when changing column
        self._search_container.search_edit.clear()

        self.set_active_column(new_column)'''

NEW_CHANGE_COLUMN = '''    def _change_column(self, direction: int) -> None:
        """Change search column using visual order."""
        model = self._table_view.model()
        if not model:
            return

        header = self._table_view.horizontalHeader()
        col_count = model.columnCount()

        # Get current visual index from logical index
        current_visual = header.visualIndex(self._active_column)

        # Move in visual order
        new_visual = current_visual + direction

        # Wrap around
        if new_visual < 0:
            new_visual = col_count - 1
        elif new_visual >= col_count:
            new_visual = 0

        # Convert visual to logical index
        new_logical = header.logicalIndex(new_visual)

        # Skip hidden columns (in visual order)
        attempts = 0
        while self._table_view.isColumnHidden(new_logical) and attempts < col_count:
            new_visual += direction
            if new_visual < 0:
                new_visual = col_count - 1
            elif new_visual >= col_count:
                new_visual = 0
            new_logical = header.logicalIndex(new_visual)
            attempts += 1

        # Clear search text when changing column
        self._search_container.search_edit.clear()

        self.set_active_column(new_logical)'''


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
    print("- Column navigation now uses visual order")
    return True


if __name__ == "__main__":
    main()