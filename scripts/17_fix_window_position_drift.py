#!/usr/bin/env python3
"""
Script 17: Fix window position drift
Opraví posúvanie okna použitím pos() + resize() namiesto setGeometry()
"""

from pathlib import Path


def fix_position_drift():
    """Opraví posúvanie okna zmenou na pos() + resize()"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return False

    content = base_window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("FIXING WINDOW POSITION DRIFT")
    print("=" * 80)

    # 1. Oprav _save_settings() - použiť pos() a size()
    old_save = """            else:
                # Normal window - get actual size
                x, y = self.x(), self.y()
                width, height = self.width(), self.height()"""

    new_save = """            else:
                # Normal window - get actual position and size
                # Use pos() and size() to avoid frame geometry issues
                pos = self.pos()
                size = self.size()
                x, y = pos.x(), pos.y()
                width, height = size.width(), size.height()"""

    if old_save in content:
        content = content.replace(old_save, new_save)
        print("✅ Fixed _save_settings() to use pos() and size()")
    else:
        print("⚠️  _save_settings() pattern not found - might be already fixed")

    # 2. Oprav _load_and_apply_settings() - použiť move() + resize()
    old_load = """            # Apply geometry
            self.setGeometry(
                safe_settings['x'],
                safe_settings['y'],
                safe_settings['width'],
                safe_settings['height']
            )
            print(f"🔍 DEBUG: setGeometry({safe_settings['x']}, {safe_settings['y']}, {safe_settings['width']}, {safe_settings['height']})")"""

    new_load = """            # Apply position and size separately to avoid frame geometry drift
            # Use move() for position and resize() for size
            self.move(safe_settings['x'], safe_settings['y'])
            self.resize(safe_settings['width'], safe_settings['height'])
            print(f"🔍 DEBUG: move({safe_settings['x']}, {safe_settings['y']}) + resize({safe_settings['width']}, {safe_settings['height']})")"""

    if old_load in content:
        content = content.replace(old_load, new_load)
        print("✅ Fixed _load_and_apply_settings() to use move() + resize()")
    else:
        print("⚠️  _load_and_apply_settings() pattern not found")

    # 3. Oprav aj fallback v _load_and_apply_settings
    old_fallback = """            # Fallback to defaults
            self.setGeometry(
                self._default_pos[0],
                self._default_pos[1],
                self._default_size[0],
                self._default_size[1]
            )"""

    new_fallback = """            # Fallback to defaults
            self.move(self._default_pos[0], self._default_pos[1])
            self.resize(self._default_size[0], self._default_size[1])"""

    if old_fallback in content:
        content = content.replace(old_fallback, new_fallback)
        print("✅ Fixed fallback to use move() + resize()")

    # Ulož súbor
    base_window_path.write_text(content, encoding='utf-8')

    print("\n📝 CHANGES SUMMARY:")
    print("  - _save_settings(): Using pos() and size() instead of x(), y(), width(), height()")
    print("  - _load_and_apply_settings(): Using move() + resize() instead of setGeometry()")
    print("  - This prevents Qt frame geometry drift issues")

    return True


if __name__ == "__main__":
    success = fix_position_drift()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test position stability")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Otvor a zavri aplikáciu 5x")
        print("2. Pozícia by mala ostať STABILNÁ! ✅")