#!/usr/bin/env python3
"""
Fix Load Window Settings Return
================================
Session: 2025-12-05
Location: scripts/15_fix_load_window_settings_return.py

Opravuje load_window_settings() aby vrátila window_state v dictionary.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py"


def fix_load_return():
    """Opraví return statement v load_window_settings"""

    print("=" * 80)
    print("FIX LOAD WINDOW SETTINGS RETURN")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    print("\n1. Hľadám return statement...")

    # Starý return (bez window_state)
    old_return = """            return {
                'x': x,
                'y': y,
                'width': width,
                'height': height
            }"""

    # Nový return (s window_state)
    new_return = """            return {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'window_state': window_state
            }"""

    if old_return in content:
        content = content.replace(old_return, new_return)
        print("   ✅ Return statement opravený")
    else:
        print("   ℹ️  Return už má window_state alebo má iný formát")
        # Možno je tam už window_state ale nebola správne pridaná
        # Skúsme alternatívu
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
    print("✅ HOTOVO - Load Return Fixed")
    print("=" * 80)
    print("\nTEST:")
    print("  Spusti aplikáciu")
    print("  Debug by mal ukazovať: 'window_state': 0 alebo 2")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_load_return()
    exit(0 if success else 1)