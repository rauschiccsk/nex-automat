"""
Remove debug print statements from base_grid.py.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\base_grid.py"

OLD_CODE = '''        # Load column widths
        self._column_widths = settings.get("column_widths", {})
        print(f"DEBUG: Loading column widths: {self._column_widths}")
        for col_str, width in self._column_widths.items():
            col = int(col_str)
            if 0 <= col < model.columnCount():
                print(f"DEBUG: Setting column {col} width to {width}")
                self.table_view.setColumnWidth(col, width)
                actual = self.table_view.columnWidth(col)
                print(f"DEBUG: Column {col} actual width after set: {actual}")'''

NEW_CODE = '''        # Load column widths
        self._column_widths = settings.get("column_widths", {})
        for col_str, width in self._column_widths.items():
            col = int(col_str)
            if 0 <= col < model.columnCount():
                self.table_view.setColumnWidth(col, width)'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_CODE not in content:
        print("ERROR: Debug code not found (already removed?)")
        return False

    new_content = content.replace(OLD_CODE, NEW_CODE)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"SUCCESS: Removed debug output from {TARGET_FILE}")
    return True


if __name__ == "__main__":
    main()