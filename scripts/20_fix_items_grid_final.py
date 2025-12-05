"""
NEX Automat v2.1 - Finálna oprava invoice_items_grid.py
Nájde SPRÁVNE top-level importy a pridá grid settings.
"""

from pathlib import Path
import shutil

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
ITEMS_GRID = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"
BACKUP = ITEMS_GRID.with_suffix('.py.before_grid')


def restore_and_analyze():
    """Obnoví a analyzuje súbor."""
    print(f"\n{'=' * 80}")
    print("1. OBNOVENIE A ANALÝZA")
    print(f"{'=' * 80}")

    if not BACKUP.exists():
        print(f"❌ Záloha neexistuje")
        return None

    shutil.copy2(BACKUP, ITEMS_GRID)
    print("✅ Obnovené zo zálohy")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi koniec TOP-LEVEL importov (pred prvou triedou/funkciou)
    last_import = 0

    for i, line in enumerate(lines):
        # Top-level import - nezačína medzerou/tabom
        if line.startswith(('import ', 'from ')) and not line[0].isspace():
            last_import = i

        # Ak sme narazili na class/def na top-level, skončíme
        if (line.startswith('class ') or line.startswith('def ')) and not line[0].isspace():
            break

    print(f"✅ Posledný top-level import: riadok {last_import + 1}")

    # Zobraz kontext
    print("\nTop-level importy:")
    for i in range(max(0, last_import - 5), min(len(lines), last_import + 5)):
        marker = ">>>" if i == last_import else "   "
        print(f"{marker} {i + 1:4d}: {lines[i].rstrip()}")

    # Insert line je za posledným importom
    insert_line = last_import + 1

    # Pridaj prázdny riadok ak neexistuje
    if insert_line < len(lines) and lines[insert_line].strip():
        lines.insert(insert_line, '\n')
        insert_line += 1

    return lines, insert_line


def add_all_changes(lines, insert_line):
    """Pridá všetky zmeny naraz."""
    print(f"\n{'=' * 80}")
    print("2. PRIDANIE VŠETKÝCH ZMIEN")
    print(f"{'=' * 80}")

    # 1. Importy
    print("\n📝 Pridávam importy na riadok", insert_line + 1)
    imports = [
        'from utils.constants import WINDOW_MAIN, GRID_INVOICE_ITEMS\n',
        'from utils.grid_settings import (\n',
        '    load_column_settings, save_column_settings,\n',
        '    load_grid_settings, save_grid_settings\n',
        ')\n',
        '\n'
    ]

    for imp in imports:
        lines.insert(insert_line, imp)
        insert_line += 1

    # 2. Volanie v __init__
    print("📝 Pridávam volanie _load_grid_settings()")
    init_count = 0
    for i, line in enumerate(lines):
        if 'def __init__(' in line:
            init_count += 1
            if init_count == 2:  # InvoiceItemsGrid
                # Nájdi koniec __init__
                indent = len(lines[i]) - len(lines[i].lstrip())
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and lines[j].strip().startswith('def '):
                        current_indent = len(lines[j]) - len(lines[j].lstrip())
                        if current_indent <= indent:
                            lines.insert(j, '\n')
                            lines.insert(j + 1, '        # Load grid settings\n')
                            lines.insert(j + 2, '        self._load_grid_settings()\n')
                            print(f"   ✅ Pridané na riadok {j + 1}")
                            break
                break

    # 3. Signály
    print("📝 Pridávam pripojenie signálov")
    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line and i > 200:
            indent = len(lines[i]) - len(lines[i].lstrip())
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and lines[j].strip().startswith('def '):
                    current_indent = len(lines[j]) - len(lines[j].lstrip())
                    if current_indent <= indent:
                        lines.insert(j, '\n')
                        lines.insert(j + 1, '        # Connect header signals for grid settings\n')
                        lines.insert(j + 2, '        header = self.table_view.horizontalHeader()\n')
                        lines.insert(j + 3, '        header.sectionResized.connect(self._on_column_resized)\n')
                        lines.insert(j + 4, '        header.sectionMoved.connect(self._on_column_moved)\n')
                        print(f"   ✅ Pridané na riadok {j + 1}")
                        break
            break

    # 4. Metódy
    print("📝 Pridávam grid metódy")
    methods = '''
    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        column_settings = load_column_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS)

        if column_settings:
            header = self.table_view.horizontalHeader()
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
        save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, {'active_column': None})

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()
'''

    for line in methods.split('\n'):
        lines.append(line + '\n')

    print("   ✅ Pridané 4 metódy")

    return lines


def save_and_verify(lines):
    """Uloží a overí súbor."""
    print(f"\n{'=' * 80}")
    print("3. UKLADANIE A VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Uložené: {len(lines)} riadkov")

    # Syntaktická kontrola
    try:
        with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
            compile(f.read(), ITEMS_GRID, 'exec')
        print("✅ Syntaktická kontrola: OK")
        return True
    except SyntaxError as e:
        print(f"❌ Syntaktická chyba: {e}")
        print(f"   Riadok {e.lineno}: {e.text}")
        return False


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - FINÁLNA OPRAVA ITEMS GRID ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Obnov a analyzuj
    result = restore_and_analyze()
    if result is None:
        return

    lines, insert_line = result

    # 2. Pridaj všetky zmeny
    lines = add_all_changes(lines, insert_line)

    # 3. Ulož a verifikuj
    if not save_and_verify(lines):
        print("\n❌ CHYBA: Oprava zlyhala")
        return

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Grid settings integrované")
    print("✅ Syntaktická kontrola OK")
    print("✅ Importy na správnom mieste (top-level)")
    print("\n⏭️  FINÁLNY TEST:")
    print("   python main.py")


if __name__ == "__main__":
    main()