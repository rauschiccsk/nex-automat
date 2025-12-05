#!/usr/bin/env python3
"""
Update Diagnose Script
=======================
Session: 2025-12-05
Location: scripts/13_update_diagnose_script.py

Aktualizuje diagnose script:
1. MIN_X = -3840 (multi-monitor)
2. Zobrazuje window_state stĺpec
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "scripts/03_diagnose_window_settings.py"


def update_diagnose():
    """Aktualizuje diagnose script"""

    print("=" * 80)
    print("UPDATE DIAGNOSE SCRIPT")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. Zmeň MIN_X
    print("\n1. Aktualizujem MIN_X...")
    if "MIN_X = -50" in content:
        content = content.replace("MIN_X = -50", "MIN_X = -3840  # Dual 4K monitor support")
        changes.append("MIN_X: -50 → -3840")
        print("   ✅ MIN_X aktualizovaný")
    else:
        print("   ℹ️  MIN_X už aktualizovaný alebo nenájdený")

    # 2. Pridaj window_state do SELECT
    print("\n2. Pridávam window_state do SELECT...")
    old_select = "SELECT id, user_id, window_name, x, y, width, height, updated_at"
    new_select = "SELECT id, user_id, window_name, x, y, width, height, window_state, updated_at"

    if old_select in content:
        content = content.replace(old_select, new_select)
        changes.append("SELECT rozšírený o window_state")
        print("   ✅ SELECT rozšírený")
    else:
        print("   ℹ️  SELECT už má window_state alebo nenájdený")

    # 3. Pridaj window_state do unpacking
    print("\n3. Pridávam window_state do row unpacking...")
    old_unpack = "id, user_id, window_name, x, y, width, height, updated_at = row"
    new_unpack = "id, user_id, window_name, x, y, width, height, window_state, updated_at = row"

    if old_unpack in content:
        content = content.replace(old_unpack, new_unpack)
        changes.append("Row unpacking rozšírený")
        print("   ✅ Unpacking rozšírený")
    else:
        print("   ℹ️  Unpacking už má window_state alebo nenájdený")

    # 4. Pridaj window_state do outputu
    print("\n4. Pridávam window_state do outputu...")

    # Nájdi output sekciu a pridaj window_state
    old_output = """        print(f"   Updated: {updated_at}")

        if not is_valid:
            print(f"   Issues: {', '.join(issues)}")"""

    new_output = """        print(f"   Window State: {'Maximized' if window_state == 2 else 'Normal'} ({window_state})")
        print(f"   Updated: {updated_at}")

        if not is_valid:
            print(f"   Issues: {', '.join(issues)}")"""

    if old_output in content:
        content = content.replace(old_output, new_output)
        changes.append("Output rozšírený o window_state")
        print("   ✅ Output rozšírený")
    else:
        print("   ℹ️  Output už má window_state alebo nenájdený")

    # Kontrola
    if content == original:
        print("\n   ⚠️  Žiadne zmeny")
        return False

    # Ulož
    print("\n5. Ukladám...")
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")

    print("\n" + "=" * 80)
    print("✅ HOTOVO - Diagnose Script Updated")
    print("=" * 80)
    print("\nZmeny:")
    for i, change in enumerate(changes, 1):
        print(f"  {i}. {change}")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("Spusti: python scripts\\03_diagnose_window_settings.py")
    print("Teraz by mal vidieť window_state a validné pozície")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = update_diagnose()
    exit(0 if success else 1)