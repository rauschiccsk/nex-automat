"""
NEX Automat v2.1 - Oprava indentácie v invoice_items_grid.py
Obnoví zo zálohy a pridá importy na správne miesto.
"""

from pathlib import Path
import shutil

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
ITEMS_GRID = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"
BACKUP = ITEMS_GRID.with_suffix('.py.before_grid')


def restore_from_backup():
    """Obnoví súbor zo zálohy."""
    print(f"\n{'=' * 80}")
    print("1. OBNOVENIE ZO ZÁLOHY")
    print(f"{'=' * 80}")

    if not BACKUP.exists():
        print(f"❌ Záloha neexistuje: {BACKUP}")
        return False

    try:
        shutil.copy2(BACKUP, ITEMS_GRID)
        print(f"✅ Obnovené zo zálohy: {BACKUP.name}")
        return True
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return False


def find_correct_import_location():
    """Nájde správne miesto pre importy - na koniec import sekcie."""
    print(f"\n{'=' * 80}")
    print("2. HĽADANIE SPRÁVNEHO MIESTA PRE IMPORTY")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi poslednú import linku
    last_import = 0
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            last_import = i

    # Pridaj import za posledný import (+ prázdny riadok ak nie je)
    insert_line = last_import + 1

    # Ak nasledujúci riadok nie je prázdny, pridaj prázdny riadok
    if insert_line < len(lines) and lines[insert_line].strip():
        lines.insert(insert_line, '\n')
        insert_line += 1

    print(f"✅ Posledný import na riadku {last_import + 1}")
    print(f"✅ Pridám nové importy na riadok {insert_line + 1}")

    # Zobraz kontext
    print("\nKontext:")
    for i in range(max(0, last_import - 2), min(len(lines), insert_line + 3)):
        marker = ">>>" if i == insert_line else "   "
        print(f"{marker} {i + 1:4d}: {lines[i].rstrip()}")

    return lines, insert_line


def add_imports_correctly(lines, insert_line):
    """Pridá importy na správne miesto."""
    print(f"\n{'=' * 80}")
    print("3. PRIDANIE IMPORTOV")
    print(f"{'=' * 80}")

    imports = [
        'from utils.constants import WINDOW_MAIN, GRID_INVOICE_ITEMS\n',
        'from utils.grid_settings import (\n',
        '    load_column_settings, save_column_settings,\n',
        '    load_grid_settings, save_grid_settings\n',
        ')\n',
        '\n'  # Prázdny riadok po importoch
    ]

    for imp in imports:
        lines.insert(insert_line, imp)
        print(f"  + {imp.rstrip()}")
        insert_line += 1

    return lines


def add_init_call(lines):
    """Pridá volanie do __init__."""
    print(f"\n{'=' * 80}")
    print("4. VOLANIE _load_grid_settings()")
    print(f"{'=' * 80}")

    # Nájdi druhý __init__ (InvoiceItemsGrid)
    init_count = 0
    for i, line in enumerate(lines):
        if 'def __init__(' in line:
            init_count += 1
            if init_count == 2:
                init_line = i
                print(f"✅ __init__ na riadku {i + 1}")
                break

    # Nájdi koniec __init__
    indent = len(lines[init_line]) - len(lines[init_line].lstrip())
    for i in range(init_line + 1, len(lines)):
        line = lines[i]
        if line.strip() and line.strip().startswith('def '):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent:
                lines.insert(i, '\n')
                lines.insert(i + 1, '        # Load grid settings\n')
                lines.insert(i + 2, '        self._load_grid_settings()\n')
                print(f"✅ Pridané na riadok {i + 1}")
                break

    return lines


def add_signals(lines):
    """Pridá signály."""
    print(f"\n{'=' * 80}")
    print("5. PRIPOJENIE SIGNÁLOV")
    print(f"{'=' * 80}")

    # Nájdi _setup_ui v InvoiceItemsGrid (po riadku 200)
    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line and i > 200:
            setup_line = i
            print(f"✅ _setup_ui na riadku {i + 1}")
            break

    # Nájdi koniec _setup_ui
    indent = len(lines[setup_line]) - len(lines[setup_line].lstrip())
    for i in range(setup_line + 1, len(lines)):
        line = lines[i]
        if line.strip() and line.strip().startswith('def '):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent:
                lines.insert(i, '\n')
                lines.insert(i + 1, '        # Connect header signals for grid settings\n')
                lines.insert(i + 2, '        header = self.table_view.horizontalHeader()\n')
                lines.insert(i + 3, '        header.sectionResized.connect(self._on_column_resized)\n')
                lines.insert(i + 4, '        header.sectionMoved.connect(self._on_column_moved)\n')
                print(f"✅ Signály na riadok {i + 1}")
                break

    return lines


def add_methods(lines):
    """Pridá grid metódy."""
    print(f"\n{'=' * 80}")
    print("6. PRIDANIE METÓD")
    print(f"{'=' * 80}")

    # Grid settings metódy
    methods = '''
    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        from utils.constants import GRID_INVOICE_ITEMS, WINDOW_MAIN
        from utils.grid_settings import load_column_settings, load_grid_settings

        # Načítaj column settings
        column_settings = load_column_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS)

        if column_settings:
            header = self.table_view.horizontalHeader()

            # Aplikuj nastavenia pre každý stĺpec
            for col_idx in range(self.model.columnCount()):
                col_name = self.model.COLUMNS[col_idx][0]
                col_settings = next((s for s in column_settings if s.get('column_name') == col_name), None)
                if col_settings:
                    if 'width' in col_settings:
                        header.resizeSection(col_idx, col_settings['width'])
                    if 'visual_index' in col_settings:
                        header.moveSection(header.visualIndex(col_idx), col_settings['visual_index'])
                    if 'visible' in col_settings:
                        self.table_view.setColumnHidden(col_idx, not col_settings['visible'])

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        from utils.constants import GRID_INVOICE_ITEMS, WINDOW_MAIN
        from utils.grid_settings import save_column_settings, save_grid_settings

        header = self.table_view.horizontalHeader()

        column_settings = []
        for col_idx in range(self.model.columnCount()):
            col_name = self.model.COLUMNS[col_idx][0]
            column_settings.append({
                'column_name': col_name,
                'width': header.sectionSize(col_idx),
                'visual_index': header.visualIndex(col_idx),
                'visible': not self.table_view.isColumnHidden(col_idx)
            })

        save_column_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, column_settings)

        grid_settings = {'active_column': None}
        save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, grid_settings)

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()
'''

    for line in methods.split('\n'):
        lines.append(line + '\n')

    print("✅ Pridané 4 metódy")

    return lines


def verify():
    """Overí súbor."""
    print(f"\n{'=' * 80}")
    print("7. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    # Skúsime načítať súbor a skontrolovať syntax
    try:
        with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
            compile(f.read(), ITEMS_GRID, 'exec')
        print("✅ Syntaktická kontrola: OK")
        return True
    except SyntaxError as e:
        print(f"❌ Syntaktická chyba: {e}")
        return False


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA INDENTÁCIE ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Obnov zo zálohy
    if not restore_from_backup():
        print("\n❌ STOP: Obnovenie zlyhalo")
        return

    # 2. Nájdi správne miesto
    lines, insert_line = find_correct_import_location()

    # 3. Pridaj importy
    lines = add_imports_correctly(lines, insert_line)

    # 4. Pridaj volanie
    lines = add_init_call(lines)

    # 5. Pridaj signály
    lines = add_signals(lines)

    # 6. Pridaj metódy
    lines = add_methods(lines)

    # 7. Ulož
    with open(ITEMS_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor uložený: {len(lines)} riadkov")

    # 8. Verifikácia
    if not verify():
        print("\n❌ Syntaktická chyba! Skontroluj súbor.")
        return

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Importy pridané na správne miesto")
    print("✅ Grid settings kompletne integrované")
    print("✅ Syntaktická kontrola OK")
    print("\n⏭️  TEST:")
    print("   python main.py")


if __name__ == "__main__":
    main()