"""
Fix: Apply custom headers when loading grid settings.
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
    if "# Apply custom headers to model" in content:
        print("SKIP: Already fixed")
        return True

    # Find where custom headers are loaded and add application to model
    old_code = '''        # Load custom headers
        self._custom_headers = settings.get("custom_headers", {})

        # Load active column'''

    new_code = '''        # Load custom headers
        self._custom_headers = settings.get("custom_headers", {})

        # Apply custom headers to model
        for col_str, header_text in self._custom_headers.items():
            col = int(col_str)
            if 0 <= col < model.columnCount():
                model.setHeaderData(col, Qt.Orientation.Horizontal, header_text)

        # Load active column'''

    if old_code not in content:
        print("ERROR: Could not find custom headers load pattern")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


if __name__ == "__main__":
    main()