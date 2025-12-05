r"""
Script 27: Skontroluje a pridá handlery _on_column_resized a _on_column_moved.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Skontroluje a pridá handlery."""
    print(f"Analyzujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či handlery existujú
    has_on_resized = 'def _on_column_resized' in content
    has_on_moved = 'def _on_column_moved' in content
    has_save = 'def _save_grid_settings' in content
    has_load = 'def _load_grid_settings' in content

    print("\nStav metód:")
    print(f"  _load_grid_settings: {'✅' if has_load else '❌'}")
    print(f"  _save_grid_settings: {'✅' if has_save else '❌'}")
    print(f"  _on_column_resized: {'✅' if has_on_resized else '❌'}")
    print(f"  _on_column_moved: {'✅' if has_on_moved else '❌'}")

    if has_on_resized and has_on_moved:
        print("\n✅ Všetky handlery už existujú!")
        return

    # Nájdi koniec InvoiceListWidget triedy
    widget_start = 0
    widget_end = 0

    for i, line in enumerate(lines):
        if 'class InvoiceListWidget' in line:
            widget_start = i
        elif widget_start > 0 and line.strip() and not line.startswith('    ') and not line.startswith('\t'):
            # Koniec triedy = riadok bez odsadenia
            widget_end = i
            break

    if widget_end == 0:
        widget_end = len(lines)

    # Pridaj metódy pred koniec triedy
    insert_pos = widget_end

    print(f"\n✅ Vkladám handlery na riadok {insert_pos + 1}")

    # Metódy na pridanie
    methods = [
        '',
        '    def _on_column_resized(self, logical_index, old_size, new_size):',
        '        """Handler pre zmenu šírky stĺpca."""',
        '        self._save_grid_settings()',
        '',
        '    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):',
        '        """Handler pre presunutie stĺpca."""',
        '        self._save_grid_settings()',
        ''
    ]

    # Vlož metódy
    for line in reversed(methods):
        lines.insert(insert_pos, line)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Nové riadky: {len(lines)}")
    print("\nPridané handlery:")
    print("  ✅ _on_column_resized(logical_index, old_size, new_size)")
    print("  ✅ _on_column_moved(logical_index, old_visual_index, new_visual_index)")
    print("\nTeraz spusti aplikáciu znova!")


if __name__ == "__main__":
    main()