r"""
Script 06: Oprava utils/__init__.py - správne názvy funkcií z text_utils.

Opraví import error - použije správne názvy funkcií ktoré skutočne existujú.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/__init__.py"

# Správny obsah súboru
CORRECT_CONTENT = r'''"""Utils package - pomocné moduly."""

from .text_utils import normalize_for_search, remove_diacritics, is_numeric, normalize_numeric
from .constants import (
    APP_PREFIX,
    WINDOW_MAIN,
    WINDOW_INVOICE_DETAIL,
    DIALOG_SETTINGS,
    DIALOG_ABOUT
)
from .window_settings import (
    load_window_settings,
    save_window_settings,
    get_current_user_id,
    init_settings_db
)

__all__ = [
    # text_utils
    'normalize_for_search',
    'remove_diacritics', 
    'is_numeric',
    'normalize_numeric',
    # constants
    'APP_PREFIX',
    'WINDOW_MAIN',
    'WINDOW_INVOICE_DETAIL',
    'DIALOG_SETTINGS',
    'DIALOG_ABOUT',
    # window_settings
    'load_window_settings',
    'save_window_settings',
    'get_current_user_id',
    'init_settings_db',
]
'''


def main():
    """Opraví utils/__init__.py s korrektnými názvami funkcií."""
    print(f"Opravujem: {TARGET_FILE}")

    # Zapíš správny obsah
    TARGET_FILE.write_text(CORRECT_CONTENT.strip(), encoding='utf-8')

    print(f"✅ Súbor opravený: {TARGET_FILE}")
    print(f"   Veľkosť: {TARGET_FILE.stat().st_size} bytes")
    print(f"   Riadkov: {len(CORRECT_CONTENT.strip().splitlines())}")
    print("\nOpravené importy z text_utils:")
    print("  ✅ normalize_for_search (bolo: normalize_text)")
    print("  ✅ is_numeric (bolo: is_numeric_match)")
    print("  ✅ normalize_numeric (pridané)")
    print("  ✅ remove_diacritics (OK)")
    print("\nSkús spustiť aplikáciu znova")


if __name__ == "__main__":
    main()