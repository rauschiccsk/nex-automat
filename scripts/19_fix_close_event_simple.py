#!/usr/bin/env python3
"""
Fix Close Event Simple
=======================
Session: 2025-12-06
Location: scripts/19_fix_close_event_simple.py

Nahradí celú closeEvent() metódu zjednodušenou verziou.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def fix_close():
    """Nahradí closeEvent()"""

    print("=" * 80)
    print("FIX CLOSE EVENT - SIMPLE VERSION")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi začiatok closeEvent
    start_idx = None
    for i, line in enumerate(lines):
        if 'def closeEvent(self, event):' in line:
            start_idx = i
            break

    if start_idx is None:
        print("   ❌ closeEvent metóda nenájdená")
        return False

    print(f"\n1. Našiel som closeEvent na riadku {start_idx + 1}")

    # Nájdi koniec metódy (ďalšia def alebo koniec súboru)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].strip() and not lines[i].startswith(' ') and not lines[i].startswith('\t'):
            end_idx = i
            break
        if lines[i].strip().startswith('def ') and i > start_idx + 1:
            end_idx = i
            break

    print(f"   Koniec metódy na riadku {end_idx}")

    # Nová closeEvent metóda
    new_close = '''    def closeEvent(self, event):
        """Handle window close event"""
        self.logger.info("Application closing")

        # Ak je maximalizované, ulož normalGeometry (pozícia pred maximalizáciou)
        if self.isMaximized():
            norm_geom = self.normalGeometry()
            save_window_settings(
                window_name=WINDOW_MAIN,
                x=norm_geom.x(), y=norm_geom.y(),
                width=norm_geom.width(), height=norm_geom.height(),
                window_state=2  # Maximalized
            )
            self.logger.info(f"Window settings saved: maximized on monitor at ({norm_geom.x()}, {norm_geom.y()})")
        else:
            # Normálne okno - validuj a ulož súradnice
            x, y = self.x(), self.y()
            width, height = self.width(), self.height()

            # Validačné limity
            MIN_X, MIN_Y = -3840, 0  # Dual 4K monitor support
            MIN_WIDTH, MIN_HEIGHT = 400, 300
            MAX_WIDTH, MAX_HEIGHT = 3840, 2160

            # Kontrola validity
            is_valid = (
                x >= MIN_X and y >= MIN_Y and
                MIN_WIDTH <= width <= MAX_WIDTH and
                MIN_HEIGHT <= height <= MAX_HEIGHT
            )

            if is_valid:
                save_window_settings(
                    window_name=WINDOW_MAIN,
                    x=x, y=y,
                    width=width, height=height,
                    window_state=0  # Normal
                )
                self.logger.info(f"Window settings saved: ({x}, {y}) [{width}x{height}] normal")
            else:
                self.logger.warning(f"Invalid position not saved: ({x}, {y}) [{width}x{height}]")

        event.accept()

'''

    # Nahraď metódu
    print("\n2. Nahrádzam closeEvent()...")
    new_lines = lines[:start_idx] + [new_close] + lines[end_idx:]

    # Ulož
    print("\n3. Ukladám...")
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("   ✅ Uložené")

    print("\n" + "=" * 80)
    print("✅ HOTOVO - Close Event Simplified")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_close()
    exit(0 if success else 1)