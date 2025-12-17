"""
Fix: QuickSearch - automatic sort when column changes.
Adds sorting by active column when search column changes.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\quick_search.py"

OLD_CODE = '''    def set_active_column(self, column: int) -> None:
        """Set active column and update UI."""
        self._active_column = column
        self._search_container.set_column(column)

        if self._header:
            self._header.set_active_column(column)

        self.active_column_changed.emit(column)'''

NEW_CODE = '''    def set_active_column(self, column: int) -> None:
        """Set active column and update UI."""
        self._active_column = column
        self._search_container.set_column(column)

        if self._header:
            self._header.set_active_column(column)

        # Auto-sort by new active column (ascending)
        self._sort_by_column(column)

        self.active_column_changed.emit(column)

    def _sort_by_column(self, column: int) -> None:
        """Sort table by column ascending."""
        model = self._table_view.model()
        if model and hasattr(model, 'sort'):
            model.sort(column, Qt.SortOrder.AscendingOrder)'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_CODE not in content:
        print("ERROR: Old code block not found - file may have been modified")
        print("Looking for:")
        print(OLD_CODE[:100] + "...")
        return False

    if "_sort_by_column" in content:
        print("WARNING: _sort_by_column already exists in file")
        return False

    new_content = content.replace(OLD_CODE, NEW_CODE)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("Added: _sort_by_column() method")
    print("Modified: set_active_column() now auto-sorts")
    return True


if __name__ == "__main__":
    main()