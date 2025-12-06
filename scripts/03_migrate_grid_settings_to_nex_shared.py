"""
Migrate: Presun grid_settings.py do nex-shared package
- Vytvorí packages/nex-shared/utils/
- Skopíruje grid_settings.py
- Vytvorí __init__.py
Location: C:\Development\nex-automat\scripts\03_migrate_grid_settings_to_nex_shared.py
"""
from pathlib import Path
import shutil

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent

SOURCE_FILE = DEV_ROOT / "apps" / "supplier-invoice-editor" / "src" / "utils" / "grid_settings.py"
TARGET_DIR = DEV_ROOT / "packages" / "nex-shared" / "utils"
TARGET_FILE = TARGET_DIR / "grid_settings.py"
INIT_FILE = TARGET_DIR / "__init__.py"


def migrate():
    """Presunie grid_settings.py do nex-shared"""

    print("=" * 80)
    print("MIGRÁCIA: grid_settings.py -> nex-shared/utils/")
    print("=" * 80)

    # Check source exists
    if not SOURCE_FILE.exists():
        print(f"\n❌ Source file not found: {SOURCE_FILE}")
        return

    print(f"\n✓ Source: {SOURCE_FILE.relative_to(DEV_ROOT)}")

    # Create target directory
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Target dir: {TARGET_DIR.relative_to(DEV_ROOT)}")

    # Copy grid_settings.py
    shutil.copy2(SOURCE_FILE, TARGET_FILE)
    print(f"✓ Copied: grid_settings.py")

    # Create __init__.py
    init_content = '''"""
Utils modul pre nex-shared package.
Zdieľané utility funkcie pre všetky NEX Automat aplikácie.
"""
from .grid_settings import (
    get_grid_settings_db_path,
    init_grid_settings_db,
    get_current_user_id,
    load_column_settings,
    save_column_settings,
    load_grid_settings,
    save_grid_settings
)

__all__ = [
    'get_grid_settings_db_path',
    'init_grid_settings_db',
    'get_current_user_id',
    'load_column_settings',
    'save_column_settings',
    'load_grid_settings',
    'save_grid_settings'
]
'''

    with open(INIT_FILE, 'w', encoding='utf-8') as f:
        f.write(init_content)

    print(f"✓ Created: __init__.py")

    print("\n" + "=" * 80)
    print("ÚSPECH - Migrácia dokončená")
    print("=" * 80)

    print("\nVytvorené:")
    print(f"  {TARGET_FILE.relative_to(DEV_ROOT)}")
    print(f"  {INIT_FILE.relative_to(DEV_ROOT)}")

    print("\nPôvodný súbor ponechaný:")
    print(f"  {SOURCE_FILE.relative_to(DEV_ROOT)}")
    print("  (Môže byť odstránený po testovaní)")

    print("\nImport v base_grid.py:")
    print("  from ..utils.grid_settings import load_column_settings, ...")

    print("\n✓ Hotovo - Testuj aplikáciu")


if __name__ == "__main__":
    migrate()