"""
Fix: Restore column width when making column visible.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "Restore minimum width" in content:
        print("SKIP: Already fixed")
        return True

    # Fix set_column_visible to restore width
    old_code = '''    def set_column_visible(self, column: int, visible: bool) -> None:
        """Set column visibility."""
        self.table_view.setColumnHidden(column, not visible)
        self._column_visibility[str(column)] = visible
        self._save_grid_settings()'''

    new_code = '''    def set_column_visible(self, column: int, visible: bool) -> None:
        """Set column visibility."""
        self.table_view.setColumnHidden(column, not visible)
        self._column_visibility[str(column)] = visible

        # Restore minimum width when making visible
        if visible:
            current_width = self.table_view.columnWidth(column)
            if current_width < 20:
                # Restore from saved width or use default
                saved_width = self._column_widths.get(str(column), 80)
                self.table_view.setColumnWidth(column, max(saved_width, 50))

        self._save_grid_settings()'''

    if old_code not in content:
        print("ERROR: Could not find set_column_visible method")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


if __name__ == "__main__":
    main()