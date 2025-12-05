#!/usr/bin/env python3
"""
Fix Window State Variable
==========================
Session: 2025-12-06
Location: scripts/16_fix_window_state_variable.py

Pridá definíciu window_state premennej v load_window_settings().
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py"


def fix_variable():
    """Pridá window_state = row[4]"""

    print("=" * 80)
    print("FIX WINDOW STATE VARIABLE")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    print("\n1. Pridávam window_state = row[4]...")

    # Starý row parsing
    old_parse = "        if row:\n            x, y, width, height = row[0], row[1], row[2], row[3]"

    # Nový row parsing s window_state
    new_parse = "        if row:\n            x, y, width, height = row[0], row[1], row[2], row[3]\n            window_state = row[4] if len(row) > 4 else 0"

    if old_parse in content:
        content = content.replace(old_parse, new_parse)
        print("   ✅ window_state premenná pridaná")
    else:
        print("   ⚠️  Pattern nenájdený")
        return False

    # Kontrola
    if content == original:
        print("\n   ❌ Žiadne zmeny")
        return False

    # Ulož
    print("\n2. Ukladám...")
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")

    print("\n" + "=" * 80)
    print("✅ HOTOVO - Window State Variable Fixed")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_variable()
    exit(0 if success else 1)