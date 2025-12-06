#!/usr/bin/env python3
"""
Script 46: Fix _save_settings to always save size
Even if position is invalid, save corrected position + actual size
"""

from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BASE_WINDOW = PROJECT_ROOT / "packages" / "nex-shared" / "ui" / "base_window.py"


def main():
    """Fix _save_settings to always save"""
    print("=" * 60)
    print("Fixing _save_settings to always save window size")
    print("=" * 60)

    if not BASE_WINDOW.exists():
        print(f"❌ File not found: {BASE_WINDOW}")
        return False

    content = BASE_WINDOW.read_text(encoding='utf-8')

    # New _save_settings that ALWAYS saves (corrects invalid position)
    new_save_settings = '''    def _save_settings(self):
        """Uloží window settings do DB."""
        try:
            if self.isMaximized():
                # Save normalGeometry (position before maximize)
                norm_geom = self.normalGeometry()
                self._db.save(
                    window_name=self._window_name,
                    x=norm_geom.x(),
                    y=norm_geom.y(),
                    width=norm_geom.width(),
                    height=norm_geom.height(),
                    window_state=2,  # Maximized
                    user_id=self._user_id
                )
                logger.info(f"Window '{self._window_name}' saved as maximized")
            else:
                # Normal window - get actual size
                x, y = self.x(), self.y()
                width, height = self.width(), self.height()

                # Validate and correct position if needed
                if not self._persistence.validate_position(x, y, width, height):
                    logger.warning(
                        f"Invalid position for '{self._window_name}': "
                        f"({x}, {y}) [{width}x{height}] - correcting"
                    )
                    # Correct position but keep actual size
                    x = max(0, min(x, 1920 - width))  # Keep on primary monitor
                    y = max(0, min(y, 1080 - height))

                # ALWAYS save (with corrected position if needed)
                self._db.save(
                    window_name=self._window_name,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    window_state=0,  # Normal
                    user_id=self._user_id
                )
                logger.info(
                    f"Window '{self._window_name}' saved at "
                    f"({x}, {y}) [{width}x{height}]"
                )

        except Exception as e:
            logger.error(f"Error saving window settings for '{self._window_name}': {e}")
'''

    # Find and replace _save_settings
    pattern = r'    def _save_settings\(self\):.*?(?=\n    def |\Z)'
    content = re.sub(pattern, new_save_settings.rstrip(), content, flags=re.DOTALL)

    # Write updated file
    BASE_WINDOW.write_text(content, encoding='utf-8')
    print(f"\n✅ Updated: {BASE_WINDOW}")

    # Verify syntax
    try:
        compile(content, str(BASE_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n📋 Changes:")
    print("   - ALWAYS saves window size (even if position invalid)")
    print("   - Corrects invalid position to keep on screen")
    print("   - Logs warning when position corrected")

    print("\n" + "=" * 60)
    print("ÚSPECH: _save_settings fixed")
    print("=" * 60)
    print("\nNext step: Test window resize")
    print("1. Spusti aplikáciu")
    print("2. Zmeň rozmery okna (nie maximalizované)")
    print("3. Zavri aplikáciu")
    print("4. Spusti znova → malo by sa otvoriť s NOVÝMI rozmermi")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)