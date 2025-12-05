r"""
Script 14: Pridanie ENTER key handlera do invoice_list_widget.py.

Pridá keyPressEvent metódu ktorá na ENTER otvorí detail faktúry.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Pridá keyPressEvent handler."""
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

    # Nájdi metódu _on_double_clicked (riadok ~214)
    insert_pos = 0
    for i, line in enumerate(lines):
        if 'def _on_double_clicked(self, index):' in line:
            # Nájdi koniec tejto metódy
            for j in range(i + 1, len(lines)):
                # Koniec metódy = ďalšia metóda alebo koniec triedy
                if lines[j].strip().startswith('def ') or (
                        lines[j].strip() == '' and j + 1 < len(lines) and not lines[j + 1].startswith('    ')):
                    insert_pos = j
                    break
            break

    if insert_pos == 0:
        print("❌ Nepodarilo sa nájsť _on_double_clicked metódu")
        return

    print(f"✅ Vkladám keyPressEvent po riadku {insert_pos + 1}")

    # Vytvor keyPressEvent metódu
    key_press_method = [
        '',
        '    def keyPressEvent(self, event):',
        '        """Handle key press events - ENTER opens invoice detail."""',
        '        from PyQt5.QtCore import Qt',
        '        ',
        '        if event.key() in (Qt.Key_Return, Qt.Key_Enter):',
        '            # Get currently selected row',
        '            current_index = self.table_view.currentIndex()',
        '            if current_index.isValid():',
        '                # Call the same method as double-click',
        '                self._on_double_clicked(current_index)',
        '                event.accept()',
        '                return',
        '        ',
        '        # Pass other keys to parent',
        '        super().keyPressEvent(event)',
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
    print("  ✅ keyPressEvent() metóda")
    print("  ✅ Reaguje na ENTER (Qt.Key_Return aj Qt.Key_Enter)")
    print("  ✅ Volá _on_double_clicked() pre aktuálny riadok")
    print("\nTest:")
    print("  1. Spusti aplikáciu")
    print("  2. Klikni na faktúru (vyber riadok)")
    print("  3. Stlač ENTER")
    print("  4. Malo by sa otvoriť detail okno faktúry")


if __name__ == "__main__":
    main()