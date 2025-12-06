"""
Fix: Oprava relative imports v base_grid.py
Zmena: ... -> .. (3 úrovne -> 2 úrovne)
"""
import os
from pathlib import Path

# Paths
DEV_ROOT = Path(r"C:\Development\nex-automat")
BASE_GRID_FILE = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"


def fix_imports():
    """Oprav relative imports v base_grid.py"""

    print(f"Fixing: {BASE_GRID_FILE}")

    # Read file
    with open(BASE_GRID_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace
    old_import1 = "from ...utils.grid_settings import load_column_settings, load_grid_settings"
    new_import1 = "from ..utils.grid_settings import load_column_settings, load_grid_settings"

    old_import2 = "from ...utils.grid_settings import save_column_settings, save_grid_settings"
    new_import2 = "from ..utils.grid_settings import save_column_settings, save_grid_settings"

    # Replace
    if old_import1 in content:
        content = content.replace(old_import1, new_import1)
        print(f"✓ Fixed load imports: ... -> ..")
    else:
        print(f"✗ Load import not found!")

    if old_import2 in content:
        content = content.replace(old_import2, new_import2)
        print(f"✓ Fixed save imports: ... -> ..")
    else:
        print(f"✗ Save import not found!")

    # Write back
    with open(BASE_GRID_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ File updated: {BASE_GRID_FILE}")
    print("\nNext: Test application")


if __name__ == "__main__":
    fix_imports()