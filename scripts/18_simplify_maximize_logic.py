#!/usr/bin/env python3
"""
Simplify Maximize Logic
========================
Session: 2025-12-06
Location: scripts/18_simplify_maximize_logic.py

Zjednodušuje logiku:
- Maximalizované: uloží len window_state=2, pri load len maximalizuje
- Normálne: uloží súradnice + window_state=0
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def fix_load_geometry():
    """Zjednoduší _load_geometry() v main_window.py"""

    target = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"

    print("=" * 80)
    print("MAIN_WINDOW.PY - Load Geometry")
    print("=" * 80)

    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nahraď celú load logiku
    old_logic = """        if settings:
            self.logger.info(f"DEBUG: load_window_settings returned: {settings}")
        if settings:
            self.setGeometry(
                settings['x'],
                settings['y'],
                settings['width'],
                settings['height']
            )
            # Načítaj a aplikuj window state (maximalizované/normálne)
            if settings.get('window_state', 0) == 2:  # Qt.WindowMaximized = 2
                self.setWindowState(Qt.WindowMaximized)
                self.logger.info(f"Loaded maximized window at ({settings['x']}, {settings['y']})")
            else:
                self.logger.info(f"Loaded window position: ({settings['x']}, {settings['y']}) [{settings['width']}x{settings['height']}]")"""

    new_logic = """        if settings:
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

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        print("   ✅ Load logic zjednodušená")
    else:
        print("   ⚠️  Pattern nenájdený")
        return False

    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")
    return True


def fix_close_event():
    """Zjednoduší closeEvent() v main_window.py"""

    target = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"

    print("\n" + "=" * 80)
    print("MAIN_WINDOW.PY - Close Event")
    print("=" * 80)

    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nahraď close logiku
    old_close = """        # Validuj pozíciu pred uložením
        # Pri maximalizovanom okne použiť normalGeometry() (pozícia pred maximalizáciou)
        if self.isMaximized():
            norm_geom = self.normalGeometry()
            x, y = norm_geom.x(), norm_geom.y()
            width, height = norm_geom.width(), norm_geom.height()
        else:
            x, y = self.x(), self.y()
            width, height = self.width(), self.height()

        # Validačné limity (rovnaké ako v window_settings.py)
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
            # Ulož len validné nastavenia vrátane windowState
            is_max = self.isMaximized()
            window_state = 2 if is_max else 0  # Qt.WindowMaximized = 2
            self.logger.info(f"DEBUG closeEvent: isMaximized()={is_max}, window_state={window_state}")
            save_window_settings(
                window_name=WINDOW_MAIN,
                x=x, y=y,
                width=width, height=height,
                window_state=window_state
            )
            state_str = "maximized" if window_state == 2 else "normal"
            self.logger.info(f"Window settings saved: ({x}, {y}) [{width}x{height}] {state_str}")
        else:
            self.logger.warning(f"Invalid position not saved: ({x}, {y}) [{width}x{height}]")"""

    new_close = """        # Ak je maximalizované, ulož len state
        if self.isMaximized():
            save_window_settings(
                window_name=WINDOW_MAIN,
                x=0, y=0,  # Dummy hodnoty, nepoužijú sa
                width=1400, height=900,
                window_state=2  # Maximalized
            )
            self.logger.info(f"Window settings saved: maximized")
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
                self.logger.warning(f"Invalid position not saved: ({x}, {y}) [{width}x{height}]")"""

    if old_close in content:
        content = content.replace(old_close, new_close)
        print("   ✅ Close logic zjednodušená")
    else:
        print("   ⚠️  Pattern nenájdený")
        return False

    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")
    return True


def main():
    print("=" * 80)
    print("SIMPLIFY MAXIMIZE LOGIC")
    print("=" * 80)

    success1 = fix_load_geometry()
    success2 = fix_close_event()

    print("\n" + "=" * 80)
    if success1 and success2:
        print("✅ HOTOVO - Maximize Logic Simplified")
    else:
        print("⚠️  ČIASTOČNE HOTOVO")
    print("=" * 80)

    print("\nNová logika:")
    print("  • Maximalizované: uloží len window_state=2")
    print("  • Normálne: uloží súradnice + window_state=0")
    print("  • Load: ak state=2 → len maximalizuj, inak aplikuj súradnice")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("1. Spusti aplikáciu, maximalizuj, zatvor")
    print("2. Spusti znovu - malo by sa otvoriť maximalizované")
    print("3. Demaximalizuj, zatvor")
    print("4. Spusti znovu - malo by zapamätať normálnu pozíciu")
    print("=" * 80)

    return success1 and success2


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)