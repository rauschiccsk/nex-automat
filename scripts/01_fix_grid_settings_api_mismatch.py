#!/usr/bin/env python3
"""
Fix Grid Settings API Mismatch
================================
Session: 2025-12-05
Location: scripts/01_fix_grid_settings_api_mismatch.py

Opravuje dva problémy v invoice_list_widget.py:
1. save_grid_settings() volané s dict namiesto int
2. load_grid_settings() používa nesprávny kľúč 'active_column' namiesto 'active_column_index'
"""

import re
from pathlib import Path

# Cesty
PROJECT_ROOT = Path(__file__).parent.parent
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def fix_grid_settings_api():
    """Opraví API mismatch v invoice_list_widget.py"""

    print("=" * 80)
    print("FIX GRID SETTINGS API MISMATCH")
    print("=" * 80)

    # 1. Načítaj súbor
    print(f"\n1. Načítavam: {TARGET_FILE}")
    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    # 2. Fix #1: load_grid_settings() - nesprávny kľúč
    print("\n2. Fix #1: Opravujem kľúč v load_grid_settings()...")

    old_load = """        # Načítaj grid settings (active column pre quick search)
        grid_settings = load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)
        if grid_settings and 'active_column' in grid_settings:
            active_col = grid_settings['active_column']"""

    new_load = """        # Načítaj grid settings (active column pre quick search)
        grid_settings = load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)
        if grid_settings and 'active_column_index' in grid_settings:
            active_col = grid_settings['active_column_index']"""

    if old_load in content:
        content = content.replace(old_load, new_load)
        changes_made.append("Load: 'active_column' → 'active_column_index'")
        print("  ✅ Opravený kľúč: 'active_column' → 'active_column_index'")
    else:
        print("  ⚠️  Pattern pre load nenájdený")

    # 3. Fix #2: save_grid_settings() - dict namiesto int
    print("\n3. Fix #2: Opravujem volanie save_grid_settings()...")

    old_save = """        # Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'search_controller') and self.search_controller:
            active_column = self.search_controller.get_active_column()
            self.logger.info(f"Saving active column: {active_column}")

        grid_settings = {
            'active_column': active_column
        }

        # Ulož grid settings
        save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST, grid_settings)"""

    new_save = """        # Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'search_controller') and self.search_controller:
            active_column = self.search_controller.get_active_column()
            self.logger.info(f"Saving active column: {active_column}")

        # Ulož grid settings (active_column_index ako tretí parameter)
        if active_column is not None:
            save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST, active_column)"""

    if old_save in content:
        content = content.replace(old_save, new_save)
        changes_made.append("Save: dict parameter → int parameter")
        print("  ✅ Opravené volanie: dict → int")
    else:
        print("  ⚠️  Pattern pre save nenájdený")

    # 4. Kontrola zmien
    if content == original_content:
        print("\n❌ Žiadne zmeny neboli aplikované!")
        return False

    # 5. Ulož súbor
    print("\n4. Ukladám opravený súbor...")
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("  ✅ Súbor uložený")

    # 6. Zhrnutie
    print("\n" + "=" * 80)
    print("✅ HOTOVO - Grid Settings API Fixed")
    print("=" * 80)
    print("\nAplikované opravy:")
    for i, change in enumerate(changes_made, 1):
        print(f"  {i}. {change}")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("1. Spusti aplikáciu - error 'dict is not supported' by mal zmiznúť")
    print("2. Zmeň aktívny stĺpec (← → šípky)")
    print("3. Zatvor aplikáciu (ESC)")
    print("4. Spusti znovu - mal by zapamätať aktívny stĺpec")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_grid_settings_api()
    exit(0 if success else 1)