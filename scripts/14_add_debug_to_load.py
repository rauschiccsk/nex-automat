#!/usr/bin/env python3
"""
Add Debug to Load
==================
Session: 2025-12-05
Location: scripts/14_add_debug_to_load.py

Pridá debug output do _load_geometry() aby sme videli čo vracia load_window_settings().
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def add_debug():
    """Pridá debug output"""

    print("=" * 80)
    print("ADD DEBUG TO LOAD")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    print("\n1. Pridávam debug do _load_geometry()...")

    # Nájdi load metódu a pridaj debug
    old_load_start = "    def _load_geometry(self):\n        \"\"\"Načíta a aplikuje uloženú pozíciu a veľkosť okna.\"\"\"\n        settings = load_window_settings(window_name=WINDOW_MAIN)"

    new_load_start = "    def _load_geometry(self):\n        \"\"\"Načíta a aplikuje uloženú pozíciu a veľkosť okna.\"\"\"\n        settings = load_window_settings(window_name=WINDOW_MAIN)\n        if settings:\n            self.logger.info(f\"DEBUG: load_window_settings returned: {settings}\")"

    if old_load_start in content:
        content = content.replace(old_load_start, new_load_start)
        print("   ✅ Debug pridaný")
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
    print("✅ HOTOVO - Debug Added")
    print("=" * 80)
    print("\nTEST:")
    print("  Spusti aplikáciu a pozri log:")
    print("  DEBUG: load_window_settings returned: {'x': ..., 'window_state': ...}")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = add_debug()
    exit(0 if success else 1)