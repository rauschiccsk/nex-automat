"""
Add colored icons for boolean values in BaseGrid.create_item.
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
    if "QBrush" in content and "setForeground" in content:
        print("SKIP: Already fixed")
        return True

    # Add QBrush to imports
    old_import = "from PySide6.QtGui import QPainter, QColor, QPalette, QAction"
    new_import = "from PySide6.QtGui import QPainter, QColor, QPalette, QAction, QBrush"

    if old_import not in content:
        print("ERROR: Could not find imports")
        return False

    content = content.replace(old_import, new_import)

    # Update boolean handling in create_item
    old_code = '''        elif isinstance(value, bool):
            text = str(value)
            align_right = False'''

    new_code = '''        elif isinstance(value, bool):
            # Use icons for boolean: green checkmark / red X
            text = "✓" if value else "✗"
            is_boolean = True
            align_right = False'''

    if old_code not in content:
        print("ERROR: Could not find boolean handling")
        return False

    content = content.replace(old_code, new_code)

    # Add is_boolean initialization and color handling
    old_code2 = '''        # Determine text and alignment based on type
        if value is None:
            text = ""
            align_right = False'''

    new_code2 = '''        # Determine text and alignment based on type
        is_boolean = False
        if value is None:
            text = ""
            align_right = False'''

    if old_code2 not in content:
        print("ERROR: Could not find type checking start")
        return False

    content = content.replace(old_code2, new_code2)

    # Add color setting after item creation
    old_code3 = '''        item = QStandardItem(text)
        item.setEditable(editable)

        if align_right:
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

        return item'''

    new_code3 = '''        item = QStandardItem(text)
        item.setEditable(editable)

        if align_right:
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
        else:
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            ) if is_boolean else None

        # Set color for boolean icons
        if is_boolean:
            if value:
                item.setForeground(QBrush(QColor(0, 200, 0)))  # Green
            else:
                item.setForeground(QBrush(QColor(220, 50, 50)))  # Red

        return item'''

    if old_code3 not in content:
        print("ERROR: Could not find item creation code")
        return False

    content = content.replace(old_code3, new_code3)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Added boolean icons to {file_path}")
    return True


if __name__ == "__main__":
    main()