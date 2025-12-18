"""
Add create_item helper method to BaseGrid for automatic alignment and formatting.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def fix_base_grid():
    file_path = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already implemented
    if "def create_item(" in content:
        print(f"SKIP: {file_path} already has create_item")
        return True

    # Add QStandardItem import if not present
    if "QStandardItem" not in content:
        old_import = "from PySide6.QtCore import Qt, Signal, QModelIndex"
        new_import = """from PySide6.QtCore import Qt, Signal, QModelIndex
from PySide6.QtGui import QStandardItem"""
        content = content.replace(old_import, new_import)

    # Add create_item method after set_active_column method
    old_code = '''    def set_active_column(self, column: int) -> None:
        """Set active column."""
        self._active_column = column
        self.header.set_active_column(column)
        self._save_grid_settings()

    # === Export ==='''

    new_code = '''    def set_active_column(self, column: int) -> None:
        """Set active column."""
        self._active_column = column
        self.header.set_active_column(column)
        self._save_grid_settings()

    # === Item Creation ===

    def create_item(self, value, editable: bool = False) -> "QStandardItem":
        """
        Create QStandardItem with automatic formatting and alignment.

        - Integers: right-aligned, no decimal places
        - Floats: right-aligned, 2 decimal places
        - Strings/other: left-aligned

        Args:
            value: The value to display
            editable: Whether the item is editable

        Returns:
            Configured QStandardItem
        """
        from PySide6.QtGui import QStandardItem

        # Determine text and alignment based on type
        if value is None:
            text = ""
            align_right = False
        elif isinstance(value, bool):
            text = str(value)
            align_right = False
        elif isinstance(value, int):
            text = str(value)
            align_right = True
        elif isinstance(value, float):
            text = f"{value:.2f}"
            align_right = True
        else:
            # Try to detect numeric strings
            text = str(value)
            align_right = False

        item = QStandardItem(text)
        item.setEditable(editable)

        if align_right:
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

        return item

    # === Export ==='''

    if old_code not in content:
        print("ERROR: Could not find insertion point for create_item")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Added create_item to {file_path}")
    return True


def fix_main_window():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "self.grid.create_item" in content:
        print(f"SKIP: {file_path} already uses create_item")
        return True

    # Remove NUMERIC_COLUMNS and simplify _populate_model
    old_code = '''    # Columns that should be right-aligned and formatted as decimals
    NUMERIC_COLUMNS = {"total_amount", "match_percent"}

    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")

                # Format numeric columns
                if col_key in self.NUMERIC_COLUMNS and value is not None:
                    try:
                        text = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        text = str(value) if value is not None else ""
                else:
                    text = str(value) if value is not None else ""

                item = QStandardItem(text)
                item.setEditable(False)

                # Right-align numeric columns
                if col_key in self.NUMERIC_COLUMNS:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")'''

    new_code = '''    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = self.grid.create_item(value, editable=False)
                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")'''

    if old_code not in content:
        print("ERROR: Could not find _populate_model in main_window")
        return False

    content = content.replace(old_code, new_code)

    # Remove unused import QStandardItem if only used in old code
    # Keep it for now as it may be used elsewhere

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Updated {file_path}")
    return True


def fix_items_window():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "self.grid.create_item" in content:
        print(f"SKIP: {file_path} already uses create_item")
        return True

    # Fix _populate_model
    old_code = '''    def _populate_model(self):
        self.model.layoutAboutToBeChanged.emit()
        self.model.removeRows(0, self.model.rowCount())

        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _, editable in self.COLUMNS:
                value = row_data.get(col_key, "")
                if isinstance(value, float):
                    value = f"{value:.2f}"
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(editable)
                row_items.append(item)
            self.model.appendRow(row_items)

        self.model.layoutChanged.emit()
        self._update_status()'''

    new_code = '''    def _populate_model(self):
        self.model.layoutAboutToBeChanged.emit()
        self.model.removeRows(0, self.model.rowCount())

        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _, editable in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = self.grid.create_item(value, editable=editable)
                row_items.append(item)
            self.model.appendRow(row_items)

        self.model.layoutChanged.emit()
        self._update_status()'''

    if old_code not in content:
        print("ERROR: Could not find _populate_model in invoice_items_window")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Updated {file_path}")
    return True


def main():
    fix_base_grid()
    fix_main_window()
    fix_items_window()
    print("Done!")


if __name__ == "__main__":
    main()