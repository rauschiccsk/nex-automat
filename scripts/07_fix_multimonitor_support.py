#!/usr/bin/env python3
"""
Fix Multi-Monitor Support
==========================
Session: 2025-12-05
Location: scripts/07_fix_multimonitor_support.py

Rozširuje MIN_X validáciu na -3840 pre dual 4K monitor setup.
Ľavý monitor má negatívne X súradnice.
"""

from pathlib import Path

# Cesty
PROJECT_ROOT = Path(__file__).parent.parent
TARGET_FILES = [
    PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py",
    PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"
]


def fix_multimonitor():
    """Rozšíri MIN_X validáciu pre dual monitor"""

    print("=" * 80)
    print("FIX MULTI-MONITOR SUPPORT")
    print("=" * 80)

    success_count = 0

    for target_file in TARGET_FILES:
        print(f"\n{'=' * 80}")
        print(f"Súbor: {target_file.name}")
        print("=" * 80)

        # 1. Načítaj súbor
        print(f"\n1. Načítavam...")
        if not target_file.exists():
            print(f"   ❌ Súbor neexistuje")
            continue

        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 2. Zmena MIN_X = -50 na MIN_X = -3840
        print("\n2. Mením MIN_X validáciu...")

        old_min_x = "MIN_X = -50"
        new_min_x = "MIN_X = -3840  # Dual 4K monitor support"

        if old_min_x in content:
            content = content.replace(old_min_x, new_min_x)
            print(f"   ✅ Zmenené: MIN_X = -50 → MIN_X = -3840")
        else:
            # Skús aj s komentárom
            old_min_x_alt = "MIN_X, MIN_Y = -50, 0"
            new_min_x_alt = "MIN_X, MIN_Y = -3840, 0  # Dual 4K monitor support"

            if old_min_x_alt in content:
                content = content.replace(old_min_x_alt, new_min_x_alt)
                print(f"   ✅ Zmenené: MIN_X = -50 → MIN_X = -3840")
            else:
                print(f"   ⚠️  Pattern nenájdený")
                continue

        # 3. Kontrola zmien
        if content == original_content:
            print("\n   ❌ Žiadne zmeny")
            continue

        # 4. Ulož súbor
        print("\n3. Ukladám...")
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("   ✅ Uložené")
        success_count += 1

    # 5. Zhrnutie
    print("\n" + "=" * 80)
    if success_count == len(TARGET_FILES):
        print("✅ HOTOVO - Multi-Monitor Support Added")
    else:
        print(f"⚠️  ČIASTOČNE HOTOVO - {success_count}/{len(TARGET_FILES)} súborov")
    print("=" * 80)

    print("\nZmeny:")
    print("  • MIN_X: -50 → -3840")
    print("  • Podporuje dual 4K monitor (3840x2 px)")
    print("  • Ľavý monitor môže mať negatívne X súradnice")

    print("\n" + "=" * 80)
    print("FINÁLNY TEST:")
    print("=" * 80)
    print("1. Vyčisti DB: python scripts\\clean_invalid_window_positions.py")
    print("2. Spusti aplikáciu na pravom monitore")
    print("3. Presuň okno na ľavý monitor")
    print("4. Zatvor (ESC) - malo by sa uložiť")
    print("5. Spusti znovu - malo by sa otvoriť na ľavom monitore")
    print("=" * 80)

    return success_count == len(TARGET_FILES)


if __name__ == "__main__":
    success = fix_multimonitor()
    exit(0 if success else 1)