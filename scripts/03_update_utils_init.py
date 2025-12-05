r"""
Script 03: Aktualizácia utils/__init__.py pre export nových modulov.

Pridá importy pre constants a window_settings moduly.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/__init__.py"

# Nový obsah súboru
NEW_CONTENT = r'''"""Utils package - pomocné moduly."""

from .text_utils import normalize_text, remove_diacritics, is_numeric_match
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
    'normalize_text',
    'remove_diacritics', 
    'is_numeric_match',
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
    """Aktualizuje utils/__init__.py súbor."""
    print(f"Aktualizujem: {TARGET_FILE}")

    # Zálohuj pôvodný súbor ak existuje
    if TARGET_FILE.exists():
        backup_path = TARGET_FILE.with_suffix('.py.backup')
        TARGET_FILE.rename(backup_path)
        print(f"📦 Záloha vytvorená: {backup_path}")

    # Zapíš nový obsah
    TARGET_FILE.write_text(NEW_CONTENT.strip(), encoding='utf-8')

    print(f"✅ Súbor aktualizovaný: {TARGET_FILE}")
    print(f"   Veľkosť: {TARGET_FILE.stat().st_size} bytes")
    print(f"   Riadkov: {len(NEW_CONTENT.strip().splitlines())}")
    print("\nPridané exporty:")
    print("  📝 text_utils: normalize_text, remove_diacritics, is_numeric_match")
    print("  🏷️  constants: APP_PREFIX, WINDOW_MAIN, WINDOW_INVOICE_DETAIL, ...")
    print("  💾 window_settings: load_window_settings, save_window_settings, ...")


if __name__ == "__main__":
    main()