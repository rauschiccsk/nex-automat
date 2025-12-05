r"""
Script 20: Integrácia grid settings do invoice_list_widget.py.

Pridá:
1. Importy pre grid settings
2. Volanie _load_grid_settings() v __init__
3. Metódu _load_grid_settings() - načíta a aplikuje nastavenia
4. Metódu _save_grid_settings() - uloží aktuálny stav
5. Handlery pre resize a move signály
6. Pripojenie signálov v _setup_ui()
"""

from pathlib import Path
import re

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"

def main():
    """Integruje grid settings do invoice_list_widget.py."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Záloha s číslom ak už existuje
    backup_num = 1
    while True:
        backup_path = TARGET_FILE.with_suffix(f'.py.backup{backup_num}')
        if not backup_path.exists():
            break
        backup_num += 1

    TARGET_FILE.rename(backup_path)
    print(f"📦 Záloha vytvorená: {backup_path}")

    # 1. PRIDAJ IMPORTY (za quick_search import, cca riadok 10)
    new_lines = []
    imports_added = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        if not imports_added and 'from .quick_search import' in line:
            new_lines.append('from utils.constants import WINDOW_MAIN, GRID_INVOICE_LIST')
            new_lines.append('from utils.grid_settings import load_column_settings, save_column_settings, load_grid_settings, save_grid_settings')
            imports_added = True
            print(f"✅ Pridané importy za riadok {i+1}")

    lines = new_lines

    # 2. PRIDAJ VOLANIE _load_grid_settings() na koniec __init__ (po _connect_signals)
    new_lines = []
    init_updated = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        if not init_updated and 'self._connect_signals()' in line and i > 130:
            new_lines.append('        self._load_grid_settings()')
            init_updated = True
            print(f"✅ Pridané volanie _load_grid_settings() za riadok {i+1}")

    lines = new_lines

    # 3. PRIDAJ PRIPOJENIE SIGNÁLOV v _setup_ui (po nastavení headeru, cca riadok 162)
    new_lines = []
    signals_added = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        if not signals_added and 'header.setSectionResizeMode' in line:
            # Pridaj za tento blok
            new_lines.append('')
            new_lines.append('        # Connect header signals for grid settings')
            new_lines.append('        header.sectionResized.connect(self._on_column_resized)')
            new_lines.append('        header.sectionMoved.connect(self._on_column_moved)')
            signals_added = True
            print(f"✅ Pridané pripojenie signálov za riadok {i+1}")

    lines = new_lines

    # 4. PRIDAJ METÓDY na koniec triedy (pred keyPressEvent alebo pred poslednú metódu)
    # Nájdi koniec triedy InvoiceListWidget
    insert_pos = 0
    for i in range(len(lines)-1, 0, -1):
        line = lines[i]
        # Hľadaj poslednú metódu v InvoiceListWidget (pred inou triedou)
        if line.strip().startswith('def ') and not line.strip().startswith('class'):
            # Nájdi koniec tejto metódy
            for j in range(i+1, len(lines)):
                next_line = lines[j]
                if next_line.strip() and not next_line.startswith('        ') and not next_line.startswith('\t'):
                    insert_pos = j
                    break
                elif j == len(lines) - 1:
                    insert_pos = j + 1
                    break
            if insert_pos > 0:
                break

    if insert_pos == 0:
        insert_pos = len(lines)

    print(f"✅ Vkladám metódy na pozíciu {insert_pos}")

    # Metódy na pridanie
    methods = '''
    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        # Načítaj column settings
        column_settings = load_column_settings(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_LIST
        )
        
        if column_settings:
            self.logger.info(f"Loading grid settings: {len(column_settings)} columns")
            
            header = self.table_view.horizontalHeader()
            
            # Aplikuj nastavenia na stĺpce
            for col_setting in column_settings:
                col_name = col_setting['column_name']
                
                # Nájdi index stĺpca podľa názvu
                col_index = None
                for idx, (display_name, field_name) in enumerate(self.COLUMNS):
                    if field_name == col_name:
                        col_index = idx
                        break
                
                if col_index is not None:
                    # Aplikuj šírku
                    if col_setting.get('width'):
                        header.resizeSection(col_index, col_setting['width'])
                    
                    # Aplikuj viditeľnosť
                    if not col_setting.get('visible', True):
                        self.table_view.hideColumn(col_index)
                    
                    # Aplikuj visual_index (poradie po drag-and-drop)
                    if col_setting.get('visual_index') is not None:
                        header.moveSection(header.visualIndex(col_index), col_setting['visual_index'])
        
        # Načítaj grid-level settings (aktívny stĺpec)
        grid_settings = load_grid_settings(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_LIST
        )
        
        if grid_settings and grid_settings.get('active_column_index') is not None:
            # Nastav aktívny stĺpec v QuickSearchController
            active_col = grid_settings['active_column_index']
            if hasattr(self, 'search_controller') and self.search_controller:
                self.search_controller.set_active_column(active_col)
                self.logger.info(f"Restored active column: {active_col}")

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        header = self.table_view.horizontalHeader()
        
        # Zozbieraj nastavenia všetkých stĺpcov
        columns = []
        for idx, (display_name, field_name) in enumerate(self.COLUMNS):
            columns.append({
                'column_name': field_name,
                'width': header.sectionSize(idx),
                'visual_index': header.visualIndex(idx),
                'visible': not self.table_view.isColumnHidden(idx)
            })
        
        # Ulož column settings
        save_column_settings(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_LIST,
            columns=columns
        )
        
        # Ulož active column z QuickSearchController
        if hasattr(self, 'search_controller') and self.search_controller:
            active_col = self.search_controller.get_active_column()
            save_grid_settings(
                window_name=WINDOW_MAIN,
                grid_name=GRID_INVOICE_LIST,
                active_column_index=active_col
            )

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()
'''

    # Vlož metódy
    lines.insert(insert_pos, methods)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Nové riadky: {len(lines)}")
    print("\nPridané:")
    print("  ✅ Importy: WINDOW_MAIN, GRID_INVOICE_LIST, grid_settings funkcie")
    print("  ✅ Volanie: self._load_grid_settings() v __init__")
    print("  ✅ Signály: sectionResized, sectionMoved")
    print("  ✅ Metóda: _load_grid_settings()")
    print("  ✅ Metóda: _save_grid_settings()")
    print("  ✅ Handlery: _on_column_resized(), _on_column_moved()")
    print("\n⚠️  POZNÁMKA:")
    print("  QuickSearchController musí mať metódy:")
    print("    - set_active_column(index)")
    print("    - get_active_column() -> int")
    print("  Tieto metódy pridáme v ďalšom kroku.")

if __name__ == "__main__":
    main()