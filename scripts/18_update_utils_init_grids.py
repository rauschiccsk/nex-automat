r"""
Script 18: Aktualizácia utils/__init__.py pre export grid_settings modulov.

Pridá importy pre grid_settings funkcie a grid konštanty.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/__init__.py"

# Nový obsah súboru
NEW_CONTENT = r'''"""Utils package - pomocné moduly."""

from .text_utils import normalize_for_search, remove_diacritics, is_numeric, normalize_numeric
from .constants import (
    APP_PREFIX,
    WINDOW_MAIN,
    WINDOW_INVOICE_DETAIL,
    DIALOG_SETTINGS,
    DIALOG_ABOUT,
    GRID_INVOICE_LIST,
    GRID_INVOICE_ITEMS
)
from .window_settings import (
    load_window_settings,
    save_window_settings,
    get_current_user_id,
    init_settings_db
)
from .grid_settings import (
    load_column_settings,
    save_column_settings,
    load_grid_settings,
    save_grid_settings,
    init_grid_settings_db
)

__all__ = [
    # text_utils
    'normalize_for_search',
    'remove_diacritics', 
    'is_numeric',
    'normalize_numeric',
    # constants - windows
    'APP_PREFIX',
    'WINDOW_MAIN',
    'WINDOW_INVOICE_DETAIL',
    'DIALOG_SETTINGS',
    'DIALOG_ABOUT',
    # constants - grids
    'GRID_INVOICE_LIST',
    'GRID_INVOICE_ITEMS',
    # window_settings
    'load_window_settings',
    'save_window_settings',
    'get_current_user_id',
    'init_settings_db',
    # grid_settings
    'load_column_settings',
    'save_column_settings',
    'load_grid_settings',
    'save_grid_settings',
    'init_grid_settings_db',
]
'''


def main():
    """Aktualizuje utils/__init__.py súbor."""
    print(f"Aktualizujem: {TARGET_FILE}")

    # Zálohuj pôvodný súbor
    if TARGET_FILE.exists():
        backup_path = TARGET_FILE.with_suffix('.py.backup2')
        TARGET_FILE.rename(backup_path)
        print(f"📦 Záloha vytvorená: {backup_path}")

    # Zapíš nový obsah
    TARGET_FILE.write_text(NEW_CONTENT.strip(), encoding='utf-8')

    print(f"✅ Súbor aktualizovaný: {TARGET_FILE}")
    print(f"   Veľkosť: {TARGET_FILE.stat().st_size} bytes")
    print(f"   Riadkov: {len(NEW_CONTENT.strip().splitlines())}")
    print("\nPridané exporty:")
    print("  🏷️  constants: GRID_INVOICE_LIST, GRID_INVOICE_ITEMS")
    print("  📊 grid_settings: load_column_settings, save_column_settings")
    print("  📊 grid_settings: load_grid_settings, save_grid_settings")
    print("  📊 grid_settings: init_grid_settings_db")


if __name__ == "__main__":
    main()