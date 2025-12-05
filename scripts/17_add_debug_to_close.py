#!/usr/bin/env python3
"""
Add Debug to Close Event
=========================
Session: 2025-12-06
Location: scripts/17_add_debug_to_close.py

Pridá debug output do closeEvent() aby sme videli hodnoty premenných.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def add_debug():
    """Pridá debug output"""

    print("=" * 80)
    print("ADD DEBUG TO CLOSE EVENT")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    print("\n1. Pridávam debug...")

    # Nájdi riadok kde sa nastavuje window_state
    old_line = "            window_state = 2 if self.isMaximized() else 0  # Qt.WindowMaximized = 2"
    new_line = """            is_max = self.isMaximized()
            window_state = 2 if is_max else 0  # Qt.WindowMaximized = 2
            self.logger.info(f"DEBUG closeEvent: isMaximized()={is_max}, window_state={window_state}")"""

    if old_line in content:
        content = content.replace(old_line, new_line)
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
    print("  1. Maximalizuj okno")
    print("  2. Zatvor - pozri log:")
    print("     DEBUG closeEvent: isMaximized()=True, window_state=2")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = add_debug()
    exit(0 if success else 1)