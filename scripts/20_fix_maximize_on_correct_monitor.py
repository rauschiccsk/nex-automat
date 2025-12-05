#!/usr/bin/env python3
"""
Fix Maximize On Correct Monitor
================================
Session: 2025-12-06
Location: scripts/20_fix_maximize_on_correct_monitor.py

Pred maximalizáciou nastaví geometriu aby Qt vedel na ktorom monitore maximalizovať.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def fix_load():
    """Opraví _load_geometry()"""

    print("=" * 80)
    print("FIX MAXIMIZE ON CORRECT MONITOR")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    print("\n1. Opravujem _load_geometry()...")

    # Starý kód
    old_logic = """        if settings:
            self.logger.info(f"DEBUG: load_window_settings returned: {settings}")
            # Ak je maximalizované, len maximalizuj bez súradníc
            if settings.get('window_state', 0) == 2:  # Qt.WindowMaximized = 2
                self.setWindowState(Qt.WindowMaximized)
                self.logger.info(f"Window maximized")
            else:
                # Normálne okno - aplikuj súradnice
                self.setGeometry(
                    settings['x'],
                    settings['y'],
                    settings['width'],
                    settings['height']
                )
                self.logger.info(f"Loaded window position: ({settings['x']}, {settings['y']}) [{settings['width']}x{settings['height']}]")"""

    # Nový kód - vždy nastav geometriu, potom maximalizuj ak treba
    new_logic = """        if settings:
            self.logger.info(f"DEBUG: load_window_settings returned: {settings}")

            # Vždy aplikuj geometriu (ak je validná) - určuje monitor
            if settings.get('x') is not None and settings.get('width'):
                self.setGeometry(
                    settings['x'],
                    settings['y'],
                    settings['width'],
                    settings['height']
                )

            # Potom maximalizuj ak je to potrebné
            if settings.get('window_state', 0) == 2:  # Qt.WindowMaximized = 2
                self.setWindowState(Qt.WindowMaximized)
                self.logger.info(f"Window maximized on monitor with position ({settings.get('x', 0)}, {settings.get('y', 0)})")
            else:
                self.logger.info(f"Loaded window position: ({settings['x']}, {settings['y']}) [{settings['width']}x{settings['height']}]")"""

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        print("   ✅ _load_geometry() opravená")
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
    print("✅ HOTOVO - Maximize Monitor Fixed")
    print("=" * 80)
    print("\nLogika:")
    print("  1. Vždy aplikuj geometriu (určuje monitor)")
    print("  2. Ak state=2, potom maximalizuj na tom monitore")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("1. Vyčisti DB: python scripts\\clean_invalid_window_positions.py")
    print("2. Spusti app na ľavom monitore, maximalizuj, zatvor")
    print("3. Spusti znovu - malo by maximalizovať na ľavom monitore")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_load()
    exit(0 if success else 1)