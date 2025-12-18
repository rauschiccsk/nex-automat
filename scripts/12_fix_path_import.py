"""
Fix missing Path import in base_grid.py.
"""

from pathlib import Path

BASE_GRID_FILE = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

OLD_IMPORT = '''from typing import Any'''
NEW_IMPORT = '''from typing import Any
from pathlib import Path'''


def main():
    if not BASE_GRID_FILE.exists():
        print(f"ERROR: {BASE_GRID_FILE} not found!")
        return

    content = BASE_GRID_FILE.read_text(encoding="utf-8")

    if "from pathlib import Path" in content:
        print("Path already imported")
        return

    if OLD_IMPORT in content:
        content = content.replace(OLD_IMPORT, NEW_IMPORT)
        BASE_GRID_FILE.write_text(content, encoding="utf-8")
        print(f"Added Path import to {BASE_GRID_FILE}")
    else:
        print("Could not find import location")


if __name__ == "__main__":
    main()