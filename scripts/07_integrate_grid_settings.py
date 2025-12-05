"""
NEX Automat v2.1 - Komplexná integrácia Grid Settings
Pridá grid settings do InvoiceListWidget SPRÁVNE (bez straty kódu).

Kroky:
1. Pridá importy
2. Pridá volanie _load_grid_settings() do __init__
3. Pripojí signály v _setup_ui()
4. Pridá 4 metódy na koniec triedy
"""

from pathlib import Path
import re

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"

# Grid settings metódy
GRID_METHODS = '''
    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        from utils.constants import GRID_INVOICE_LIST
        from utils.grid_settings import load_column_settings, load_grid_settings

        # Načítaj column settings
        column_settings = load_column_settings(GRID_INVOICE_LIST)

        if column_settings:
            header = self.table.horizontalHeader()

            # Aplikuj nastavenia pre každý stĺpec
            for col_idx, col_name in enumerate(self.model.HEADERS):
                if col_name in column_settings:
                    settings = column_settings[col_name]

                    # Šírka stĺpca
                    if 'width' in settings:
                        header.resizeSection(col_idx, settings['width'])

                    # Vizuálny index (poradie)
                    if 'visual_index' in settings:
                        header.moveSection(header.visualIndex(col_idx), settings['visual_index'])

                    # Viditeľnosť
                    if 'visible' in settings:
                        self.table.setColumnHidden(col_idx, not settings['visible'])

        # Načítaj grid settings (active column pre quick search)
        grid_settings = load_grid_settings(GRID_INVOICE_LIST)

        if grid_settings and 'active_column' in grid_settings:
            active_col = grid_settings['active_column']
            # Nastav aktívny stĺpec v quick search
            if hasattr(self, 'quick_search') and self.quick_search:
                self.quick_search.set_active_column(active_col)

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        from utils.constants import GRID_INVOICE_LIST
        from utils.grid_settings import save_column_settings, save_grid_settings

        header = self.table.horizontalHeader()

        # Zozbieraj column settings
        column_settings = {}
        for col_idx, col_name in enumerate(self.model.HEADERS):
            column_settings[col_name] = {
                'width': header.sectionSize(col_idx),
                'visual_index': header.visualIndex(col_idx),
                'visible': not self.table.isColumnHidden(col_idx)
            }

        # Ulož column settings
        save_column_settings(GRID_INVOICE_LIST, column_settings)

        # Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'quick_search') and self.quick_search:
            active_column = self.quick_search.get_active_column()

        grid_settings = {
            'active_column': active_column
        }

        # Ulož grid settings
        save_grid_settings(GRID_INVOICE_LIST, grid_settings)

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

    backup_file = WIDGET_FILE.with_suffix('.py.before_grid')

    try:
        import shutil
        shutil.copy2(WIDGET_FILE, backup_file)
        print(f"✅ Zálohované do: {backup_file.name}")
        return True
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return False


def check_imports():
    """Skontroluje a pridá importy."""
    print(f"\n{'=' * 80}")
    print("2. KONTROLA A PRIDANIE IMPORTOV")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Kontrola
    has_constants = 'from utils.constants import' in content
    has_grid_settings = 'from utils.grid_settings import' in content

    print(f"from utils.constants: {'✅ Existuje' if has_constants else '❌ Chýba'}")
    print(f"from utils.grid_settings: {'✅ Existuje' if has_grid_settings else '❌ Chýba'}")

    if has_constants and has_grid_settings:
        print("\n✅ Všetky importy sú prítomné")
        return lines

    # Pridaj importy
    print("\n📝 Pridávam importy...")

    # Nájdi riadok kde sú importy (za from PyQt5...)
    insert_line = 0
    for i, line in enumerate(lines):
        if line.startswith('from PyQt5'):
            insert_line = i + 1

    # Ak nie sú constants
    if not has_constants:
        lines.insert(insert_line, 'from utils.constants import WINDOW_MAIN, GRID_INVOICE_LIST')
        insert_line += 1
        print("✅ Pridaný import: from utils.constants import...")

    # Ak nie sú grid_settings
    if not has_grid_settings:
        lines.insert(insert_line, 'from utils.grid_settings import (')
        lines.insert(insert_line + 1, '    load_column_settings, save_column_settings,')
        lines.insert(insert_line + 2, '    load_grid_settings, save_grid_settings')
        lines.insert(insert_line + 3, ')')
        print("✅ Pridaný import: from utils.grid_settings import...")

    return lines


def add_load_call_to_init(lines):
    """Pridá volanie _load_grid_settings() do __init__."""
    print(f"\n{'=' * 80}")
    print("3. PRIDANIE VOLANIA _load_grid_settings() DO __init__")
    print(f"{'=' * 80}")

    # Nájdi __init__ v InvoiceListWidget (druhý __init__)
    init_count = 0
    init_line = None

    for i, line in enumerate(lines):
        if 'def __init__(' in line:
            init_count += 1
            if init_count == 2:  # Druhý __init__ je v InvoiceListWidget
                init_line = i
                print(f"✅ Nájdený __init__ InvoiceListWidget na riadku {i + 1}")
                break

    if init_line is None:
        print("❌ __init__ nenájdený!")
        return lines

    # Nájdi koniec __init__ (ďalšia metóda)
    indent = len(lines[init_line]) - len(lines[init_line].lstrip())
    end_line = None

    for i in range(init_line + 1, len(lines)):
        line = lines[i]
        if line.strip() and not line.strip().startswith('#'):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent and line.strip().startswith('def '):
                end_line = i
                break

    if end_line is None:
        end_line = len(lines)

    print(f"✅ Koniec __init__ na riadku {end_line}")

    # Skontroluj, či už volanie existuje
    init_block = '\n'.join(lines[init_line:end_line])
    if '_load_grid_settings()' in init_block:
        print("✅ Volanie _load_grid_settings() už existuje")
        return lines

    # Pridaj volanie pred koniec __init__
    lines.insert(end_line, '')
    lines.insert(end_line + 1, '        # Load grid settings')
    lines.insert(end_line + 2, '        self._load_grid_settings()')

    print("✅ Pridané volanie: self._load_grid_settings()")

    return lines


def add_signal_connections(lines):
    """Pripojí signály v _setup_ui()."""
    print(f"\n{'=' * 80}")
    print("4. PRIPOJENIE SIGNÁLOV V _setup_ui()")
    print(f"{'=' * 80}")

    # Nájdi _setup_ui v InvoiceListWidget
    setup_line = None
    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line and i > 130:  # Po riadku 130 je InvoiceListWidget
            setup_line = i
            print(f"✅ Nájdená _setup_ui na riadku {i + 1}")
            break

    if setup_line is None:
        print("❌ _setup_ui nenájdená!")
        return lines

    # Nájdi kde je header = self.table.horizontalHeader()
    header_line = None
    for i in range(setup_line, min(setup_line + 100, len(lines))):
        if 'header = self.table.horizontalHeader()' in lines[i]:
            header_line = i
            print(f"✅ Nájdený header na riadku {i + 1}")
            break

    if header_line is None:
        print("❌ header = self.table.horizontalHeader() nenájdený!")
        return lines

    # Nájdi kde ukončiť (po header.resizeSection)
    insert_line = None
    for i in range(header_line, min(header_line + 20, len(lines))):
        if 'header.resizeSection' in lines[i]:
            insert_line = i + 1
            break

    if insert_line is None:
        insert_line = header_line + 1

    # Skontroluj, či signály už sú pripojené
    setup_block = '\n'.join(lines[setup_line:setup_line + 100])
    if 'header.sectionResized.connect' in setup_block:
        print("✅ Signály už sú pripojené")
        return lines

    # Pridaj pripojenie signálov
    lines.insert(insert_line, '')
    lines.insert(insert_line + 1, '        # Connect header signals for grid settings')
    lines.insert(insert_line + 2, '        header.sectionResized.connect(self._on_column_resized)')
    lines.insert(insert_line + 3, '        header.sectionMoved.connect(self._on_column_moved)')

    print("✅ Pripojené signály: sectionResized, sectionMoved")

    return lines


def add_grid_methods(lines):
    """Pridá 4 grid metódy na koniec InvoiceListWidget."""
    print(f"\n{'=' * 80}")
    print("5. PRIDANIE GRID METÓD")
    print(f"{'=' * 80}")

    content = '\n'.join(lines)

    # Skontroluj, či metódy už existujú
    if '_load_grid_settings' in content and '_save_grid_settings' in content:
        print("✅ Grid metódy už existujú")
        return lines

    # Nájdi koniec InvoiceListWidget (druhá trieda)
    class_count = 0
    widget_start = None

    for i, line in enumerate(lines):
        if line.strip().startswith('class '):
            class_count += 1
            if class_count == 2:  # InvoiceListWidget
                widget_start = i
                print(f"✅ InvoiceListWidget začína na riadku {i + 1}")
                break

    # Koniec triedy = koniec súboru alebo začiatok ďalšej triedy
    widget_end = len(lines)
    print(f"✅ Pridám metódy na koniec súboru (riadok {widget_end})")

    # Pridaj metódy
    method_lines = GRID_METHODS.split('\n')
    for method_line in method_lines:
        lines.append(method_line)

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

    content = '\n'.join(lines)

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    return True


def verify_integration():
    """Overí úspešnú integráciu."""
    print(f"\n{'=' * 80}")
    print("7. VERIFIKÁCIA INTEGRÁCIE")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'Import constants': 'from utils.constants import' in content,
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
    """Hlavná funkcia integrácie."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - KOMPLEXNÁ INTEGRÁCIA GRID SETTINGS ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Záloha
    if not backup_file():
        print("\n❌ STOP: Záloha zlyhala")
        return

    # 2. Importy
    lines = check_imports()

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
    print("✅ Grid settings integrované do InvoiceListWidget")
    print("✅ Záloha: invoice_list_widget.py.before_grid")
    print("\n⏭️  ĎALŠÍ KROK: Otestovať aplikáciu:")
    print("   1. python main.py")
    print("   2. Zmeniť šírku stĺpca")
    print("   3. Zatvoriť a znovu otvoriť")
    print("   4. Overiť, že šírka zostala")


if __name__ == "__main__":
    main()