#!/usr/bin/env python3
"""
Script 12: Fix get_safe_position() to preserve size when position is invalid
Opraví bug, kde invalid pozícia prepíše aj rozmery na default
"""

from pathlib import Path


def fix_get_safe_position():
    """Opraví get_safe_position() aby zachovala rozmery aj pri invalid pozícii"""

    persistence_path = Path("packages/nex-shared/ui/window_persistence.py")

    if not persistence_path.exists():
        print(f"❌ File not found: {persistence_path}")
        return False

    content = persistence_path.read_text(encoding='utf-8')

    # Nájdi a nahrať problematický blok kódu
    old_code = """        # Ak je pozícia invalid, použiť default
        if not cls.validate_position(x, y, width, height):
            logger.info(f"Using default position due to invalid settings")
            return {
                'x': default_pos[0],
                'y': default_pos[1],
                'width': default_size[0],
                'height': default_size[1],
                'window_state': 0  # Reset to normal
            }"""

    # Nový kód - opraví len pozíciu, zachová rozmery
    new_code = """        # Ak je pozícia invalid, opraviť pozíciu ale ZACHOVAŤ rozmery z DB
        if not cls.validate_position(x, y, width, height):
            logger.info(f"Invalid position ({x}, {y}) - correcting but keeping size {width}x{height}")

            # Opraviť len pozíciu - posunúť okno na viditeľnú oblasť
            screen = QApplication.primaryScreen().geometry()

            # Ensure window fits on screen
            x = max(0, min(x, screen.width() - width))
            y = max(0, min(y, screen.height() - height))

            # If still doesn't fit, use default position but KEEP size from DB
            if x < 0 or y < 0:
                x = default_pos[0]
                y = default_pos[1]

            logger.info(f"Corrected position to ({x}, {y}) with original size {width}x{height}")

            return {
                'x': x,
                'y': y,
                'width': width,  # ✅ ZACHOVANÉ z DB!
                'height': height,  # ✅ ZACHOVANÉ z DB!
                'window_state': window_state  # ✅ ZACHOVANÉ z DB!
            }"""

    # Nahraď kód
    if old_code in content:
        content = content.replace(old_code, new_code)

        # Pridaj import QApplication ak chýba
        if 'from PyQt5.QtWidgets import QApplication' not in content:
            # Nájdi existujúce importy z PyQt5.QtWidgets
            import_line = None
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'from PyQt5.QtWidgets import' in line:
                    import_line = i
                    break

            if import_line is not None:
                # Pridaj QApplication do existujúceho importu
                lines[import_line] = lines[import_line].rstrip()
                if lines[import_line].endswith(')'):
                    # Multi-line import
                    lines[import_line] = lines[import_line][:-1] + ', QApplication)'
                else:
                    lines[import_line] += ', QApplication'
                content = '\n'.join(lines)

        # Ulož súbor
        persistence_path.write_text(content, encoding='utf-8')

        print("✅ get_safe_position() FIXED!")
        print("\nChanges:")
        print("  - Invalid position now corrects ONLY position")
        print("  - Width and height PRESERVED from database")
        print("  - Window state PRESERVED from database")
        print("\n⚠️  Otestuj aplikáciu:")
        print("  1. Zmeň veľkosť okna")
        print("  2. Zavri aplikáciu")
        print("  3. Otvor znova → mal by sa otvoriť so ZMENENÝMI rozmermi!")

        return True
    else:
        print("❌ Could not find the code block to replace!")
        print("   The file might have been modified already.")
        return False


if __name__ == "__main__":
    success = fix_get_safe_position()
    if success:
        print("\n" + "=" * 80)
        print("NEXT STEP: Test the fix")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")