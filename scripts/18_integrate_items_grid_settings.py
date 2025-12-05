"""
NEX Automat v2.1 - Integrácia Grid Settings do invoice_items_grid.py
Aplikuje rovnakú logiku ako pri invoice_list_widget.py.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
ITEMS_GRID = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"

# Grid settings metódy (upravené pre GRID_INVOICE_ITEMS)
GRID_METHODS = '''
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
                col_name = self.model.COLUMNS[col_idx][0]  # Prvý element tuplu
                # Nájdi nastavenia pre tento stĺpec
                col_settings = next((s for s in column_settings if s.get('column_name') == col_name), None)
                if col_settings:

                    # Šírka stĺpca
                    if 'width' in col_settings:
                        header.resizeSection(col_idx, col_settings['width'])

                    # Vizuálny index (poradie)
                    if 'visual_index' in col_settings:
                        header.moveSection(header.visualIndex(col_idx), col_settings['visual_index'])

                    # Viditeľnosť
                    if 'visible' in col_settings:
                        self.table_view.setColumnHidden(col_idx, not col_settings['visible'])

        # Načítaj grid settings (active column pre quick search)
        grid_settings = load_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS)

        if grid_settings and 'active_column' in grid_settings:
            active_col = grid_settings['active_column']
            # Nastav aktívny stĺpec v quick search
            if hasattr(self, 'quick_search_container') and self.quick_search_container:
                # Quick search controller je dostupný cez container
                if hasattr(self.quick_search_container, 'search_controller'):
                    # TODO: Implementovať set_active_column v quick search
                    pass

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        from utils.constants import GRID_INVOICE_ITEMS, WINDOW_MAIN
        from utils.grid_settings import save_column_settings, save_grid_settings

        header = self.table_view.horizontalHeader()

        # Zozbieraj column settings
        column_settings = []
        for col_idx in range(self.model.columnCount()):
            col_name = self.model.COLUMNS[col_idx][0]  # Prvý element tuplu
            column_settings.append({
                'column_name': col_name,
                'width': header.sectionSize(col_idx),
                'visual_index': header.visualIndex(col_idx),
                'visible': not self.table_view.isColumnHidden(col_idx)
            })

        # Ulož column settings
        save_column_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, column_settings)

        # Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'quick_search_container') and self.quick_search_container:
            if hasattr(self.quick_search_container, 'search_controller'):
                # TODO: Získať active column z quick search
                pass

        grid_settings = {
            'active_column': active_column
        }

        # Ulož grid settings
        save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, grid_settings)

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()
'''


def backup_file():
    """Zazálohuje súbor."""
    print(f"\n{'=' * 80}")
    print("1. ZÁLOHA SÚBORU")
    print(f"{'=' * 80}")

    backup_file = ITEMS_GRID.with_suffix('.py.before_grid')

    try:
        import shutil
        shutil.copy2(ITEMS_GRID, backup_file)
        print(f"✅ Zálohované do: {backup_file.name}")
        return True
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return False


def add_imports():
    """Pridá importy."""
    print(f"\n{'=' * 80}")
    print("2. PRIDANIE IMPORTOV")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi riadok s PyQt5 importami
    insert_line = 0
    for i, line in enumerate(lines):
        if 'from PyQt5' in line:
            insert_line = i + 1

    # Pridaj importy za PyQt5
    imports = [
        'from utils.constants import WINDOW_MAIN, GRID_INVOICE_ITEMS\n',
        'from utils.grid_settings import (\n',
        '    load_column_settings, save_column_settings,\n',
        '    load_grid_settings, save_grid_settings\n',
        ')\n'
    ]

    print(f"Pridávam importy na riadok {insert_line}:")
    for imp in imports:
        print(f"  {imp.rstrip()}")
        lines.insert(insert_line, imp)
        insert_line += 1

    return lines


def add_load_call_to_init(lines):
    """Pridá volanie _load_grid_settings() do __init__."""
    print(f"\n{'=' * 80}")
    print("3. VOLANIE _load_grid_settings() V __init__")
    print(f"{'=' * 80}")

    # Nájdi druhý __init__ (v InvoiceItemsGrid)
    init_count = 0
    for i, line in enumerate(lines):
        if 'def __init__(' in line:
            init_count += 1
            if init_count == 2:  # Druhý je v InvoiceItemsGrid
                init_line = i
                print(f"✅ __init__ InvoiceItemsGrid na riadku {i + 1}")
                break

    # Nájdi koniec __init__ (ďalšia metóda)
    indent = len(lines[init_line]) - len(lines[init_line].lstrip())
    for i in range(init_line + 1, len(lines)):
        line = lines[i]
        if line.strip() and line.strip().startswith('def '):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent:
                # Pridaj volanie pred túto metódu
                lines.insert(i, '\n')
                lines.insert(i + 1, '        # Load grid settings\n')
                lines.insert(i + 2, '        self._load_grid_settings()\n')
                print(f"✅ Pridané volanie na riadok {i + 1}")
                break

    return lines


def add_signal_connections(lines):
    """Pripojí signály v _setup_ui()."""
    print(f"\n{'=' * 80}")
    print("4. PRIPOJENIE SIGNÁLOV V _setup_ui()")
    print(f"{'=' * 80}")

    # Nájdi _setup_ui v InvoiceItemsGrid (po riadku 220)
    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line and i > 220:
            setup_line = i
            print(f"✅ _setup_ui nájdená na riadku {i + 1}")
            break

    # Nájdi kde je header = self.table_view.horizontalHeader()
    for i in range(setup_line, setup_line + 50):
        if 'header = self.table_view.horizontalHeader()' in lines[i]:
            header_line = i
            print(f"✅ header na riadku {i + 1}")
            break

    # Nájdi koniec _setup_ui
    indent = len(lines[setup_line]) - len(lines[setup_line].lstrip())
    for i in range(setup_line + 1, len(lines)):
        line = lines[i]
        if line.strip() and line.strip().startswith('def '):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent:
                # Pridaj signály pred túto metódu
                lines.insert(i, '\n')
                lines.insert(i + 1, '        # Connect header signals for grid settings\n')
                lines.insert(i + 2, '        header.sectionResized.connect(self._on_column_resized)\n')
                lines.insert(i + 3, '        header.sectionMoved.connect(self._on_column_moved)\n')
                print(f"✅ Signály pripojené na riadok {i + 1}")
                break

    return lines


def add_grid_methods(lines):
    """Pridá 4 grid metódy na koniec."""
    print(f"\n{'=' * 80}")
    print("5. PRIDANIE GRID METÓD")
    print(f"{'=' * 80}")

    # Pridaj metódy na koniec súboru
    method_lines = GRID_METHODS.split('\n')
    for method_line in method_lines:
        lines.append(method_line + '\n')

    print("✅ Pridané 4 metódy:")
    print("   - _load_grid_settings()")
    print("   - _save_grid_settings()")
    print("   - _on_column_resized()")
    print("   - _on_column_moved()")

    return lines


def save_file(lines):
    """Uloží súbor."""
    print(f"\n{'=' * 80}")
    print("6. UKLADANIE SÚBORU")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    return True


def verify_integration():
    """Overí integráciu."""
    print(f"\n{'=' * 80}")
    print("7. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'Import GRID_INVOICE_ITEMS': 'GRID_INVOICE_ITEMS' in content,
        'Import grid_settings': 'from utils.grid_settings import' in content,
        'Volanie _load_grid_settings': 'self._load_grid_settings()' in content,
        'Signal sectionResized': 'header.sectionResized.connect' in content,
        'Signal sectionMoved': 'header.sectionMoved.connect' in content,
        'Metóda _load_grid_settings': 'def _load_grid_settings(self):' in content,
        'Metóda _save_grid_settings': 'def _save_grid_settings(self):' in content,
        'Metóda _on_column_resized': 'def _on_column_resized(self' in content,
        'Metóda _on_column_moved': 'def _on_column_moved(self' in content,
    }

    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_ok = False

    return all_ok


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - GRID SETTINGS PRE ITEMS GRID ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Záloha
    if not backup_file():
        print("\n❌ STOP: Záloha zlyhala")
        return

    # 2. Importy
    lines = add_imports()

    # 3. Volanie v __init__
    lines = add_load_call_to_init(lines)

    # 4. Signály
    lines = add_signal_connections(lines)

    # 5. Metódy
    lines = add_grid_methods(lines)

    # 6. Uloženie
    if not save_file(lines):
        print("\n❌ STOP: Uloženie zlyhalo")
        return

    # 7. Verifikácia
    if not verify_integration():
        print("\n❌ VAROVANIE: Niektoré komponenty chýbajú!")

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Grid settings integrované do invoice_items_grid.py")
    print("✅ Použitá konštanta: GRID_INVOICE_ITEMS")
    print("✅ Záloha: invoice_items_grid.py.before_grid")
    print("\n⏭️  TEST:")
    print("   1. python main.py")
    print("   2. Otvor faktúru (double-click)")
    print("   3. Zmeň šírku stĺpca položiek")
    print("   4. Zatvoriť a znovu otvoriť")
    print("   5. Šírka by mala zostať!")


if __name__ == "__main__":
    main()