#!/usr/bin/env python3
"""
Fix Load Grid Settings Key
===========================
Session: 2025-12-05
Location: scripts/04_fix_load_grid_settings_key.py

Opravuje kľúč v _load_grid_settings() metóde:
'active_column' → 'active_column_index'
"""

from pathlib import Path

# Cesty
PROJECT_ROOT = Path(__file__).parent.parent
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def fix_load_key():
    """Opraví kľúč v load_grid_settings"""

    print("=" * 80)
    print("FIX LOAD GRID SETTINGS KEY")
    print("=" * 80)

    # 1. Načítaj súbor
    print(f"\n1. Načítavam: {TARGET_FILE.name}")
    if not TARGET_FILE.exists():
        print(f"   ❌ Súbor neexistuje")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 2. Oprava: 'active_column' → 'active_column_index'
    print("\n2. Opravujem kľúč...")

    old_str = "if grid_settings and 'active_column' in grid_settings:\n            active_col = grid_settings['active_column']"
    new_str = "if grid_settings and 'active_column_index' in grid_settings:\n            active_col = grid_settings['active_column_index']"

    if old_str in content:
        content = content.replace(old_str, new_str)
        print("   ✅ Opravené: 'active_column' → 'active_column_index'")
    else:
        # Skús bez presnej whitespace
        old_str2 = "'active_column' in grid_settings"
        new_str2 = "'active_column_index' in grid_settings"

        if old_str2 in content:
            content = content.replace(old_str2, new_str2, 1)  # Iba prvý výskyt
            # Teraz oprav aj prístup k hodnote
            old_val = "grid_settings['active_column']"
            new_val = "grid_settings['active_column_index']"
            content = content.replace(old_val, new_val, 1)  # Iba prvý výskyt
            print("   ✅ Opravené: 'active_column' → 'active_column_index'")
        else:
            print("   ⚠️  Pattern nenájdený - možno už je opravené")
            return False

    # 3. Kontrola zmien
    if content == original_content:
        print("\n   ❌ Žiadne zmeny")
        return False

    # 4. Ulož súbor
    print("\n3. Ukladám súbor...")
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")

    # 5. Zhrnutie
    print("\n" + "=" * 80)
    print("✅ HOTOVO - Load Key Fixed")
    print("=" * 80)
    print("\nOprava: grid_settings['active_column'] → ['active_column_index']")
    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("1. Teraz rieš window position problém")
    print("2. Spusti: python scripts\\03_diagnose_window_settings.py")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_load_key()
    exit(0 if success else 1)