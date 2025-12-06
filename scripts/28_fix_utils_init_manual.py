"""
Manuálny fix utils/__init__.py - čistá implementácia
"""
from pathlib import Path

UTILS_INIT_PATH = Path("apps/supplier-invoice-editor/src/utils/__init__.py")

CORRECT_CONTENT = '''"""Utils package - pomocné moduly."""

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
    # grid_settings
    'load_column_settings',
    'save_column_settings',
    'load_grid_settings',
    'save_grid_settings',
    'init_grid_settings_db',
]
'''


def main():
    print("=" * 80)
    print("MANUAL FIX: utils/__init__.py")
    print("=" * 80)

    # Zapíš správny obsah
    with open(UTILS_INIT_PATH, 'w', encoding='utf-8') as f:
        f.write(CORRECT_CONTENT)

    print(f"✅ Súbor prepísaný: {UTILS_INIT_PATH}")

    print("\nOdstránené imports:")
    print("  ❌ load_window_settings")
    print("  ❌ save_window_settings")
    print("  ❌ get_current_user_id")
    print("  ❌ init_settings_db")

    print("\nPonechané imports:")
    print("  ✅ text_utils (všetky)")
    print("  ✅ constants (všetky)")
    print("  ✅ grid_settings (všetky)")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → Ak ModuleNotFoundError 'nex_shared', pridám path fix")
    print("=" * 80)


if __name__ == '__main__':
    main()