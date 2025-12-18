"""
Fix: Display 0 as 0.00 for float values.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Fix: Check for int before float (0 is int in Python)
    # Change logic to treat 0 as float if it comes from float context
    old_code = '''        # Determine text and alignment based on type
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
            align_right = False'''

    new_code = '''        # Determine text and alignment based on type
        if value is None:
            text = ""
            align_right = False
        elif isinstance(value, bool):
            text = str(value)
            align_right = False
        elif isinstance(value, float):
            # Float always with 2 decimal places (including 0.0)
            text = f"{value:.2f}"
            align_right = True
        elif isinstance(value, int):
            text = str(value)
            align_right = True
        else:
            # Try to detect numeric strings
            text = str(value)
            align_right = False'''

    if old_code not in content:
        print("ERROR: Could not find create_item type checking code")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


if __name__ == "__main__":
    main()