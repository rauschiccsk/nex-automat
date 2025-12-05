r"""
Script 15: Pridanie ESC key handlera do main_window.py.

Pridá keyPressEvent metódu ktorá na ESC zatvorí aplikáciu.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def main():
    """Pridá keyPressEvent handler do MainWindow."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či už keyPressEvent existuje
    if 'def keyPressEvent' in content:
        print("✅ keyPressEvent už existuje")
        return

    # Nájdi closeEvent metódu (okolo riadku 243)
    insert_pos = 0
    for i, line in enumerate(lines):
        if 'def closeEvent(self, event):' in line:
            # Vložíme pred closeEvent
            insert_pos = i
            break

    if insert_pos == 0:
        print("❌ Nepodarilo sa nájsť closeEvent metódu")
        return

    print(f"✅ Vkladám keyPressEvent pred closeEvent (riadok {insert_pos + 1})")

    # Vytvor keyPressEvent metódu
    key_press_method = [
        '    def keyPressEvent(self, event):',
        '        """Handle key press events - ESC closes application."""',
        '        from PyQt5.QtCore import Qt',
        '        ',
        '        if event.key() == Qt.Key_Escape:',
        '            self.logger.info("ESC pressed - closing application")',
        '            self.close()',
        '            event.accept()',
        '            return',
        '        ',
        '        # Pass other keys to parent',
        '        super().keyPressEvent(event)',
        '',
    ]

    # Vlož metódu
    for line in reversed(key_press_method):
        lines.insert(insert_pos, line)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Pôvodné riadky: {len(lines) - len(key_press_method)}")
    print(f"   Nové riadky: {len(lines)}")
    print(f"   Pridané: {len(key_press_method)} riadkov")
    print("\nPridané:")
    print("  ✅ keyPressEvent() metóda v MainWindow")
    print("  ✅ Reaguje na ESC (Qt.Key_Escape)")
    print("  ✅ Volá self.close() - normálne zatvorenie s uložením pozície")
    print("\nTest:")
    print("  1. Spusti aplikáciu")
    print("  2. Stlač ESC")
    print("  3. Aplikácia by sa mala zatvoriť (ako X alebo Alt+F4)")


if __name__ == "__main__":
    main()