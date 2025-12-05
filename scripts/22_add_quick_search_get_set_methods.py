r"""
Script 22: Pridanie metód set_active_column() a get_active_column() do QuickSearchController.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/quick_search.py"


def main():
    """Pridá get/set metódy do QuickSearchController."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či už metódy existujú
    if 'def set_active_column(self' in content and 'def get_active_column(self' in content:
        # Ale musia byť v QuickSearchController, nie v iných triedach
        in_controller = False
        has_set = False
        has_get = False

        for i, line in enumerate(lines):
            if 'class QuickSearchController' in line:
                in_controller = True
            elif in_controller and line.strip().startswith('class '):
                in_controller = False

            if in_controller:
                if 'def set_active_column(self' in line:
                    has_set = True
                if 'def get_active_column(self' in line:
                    has_get = True

        if has_set and has_get:
            print("✅ Metódy už existujú v QuickSearchController")
            return

    # Nájdi koniec QuickSearchController triedy
    controller_start = 0
    controller_end = 0

    for i, line in enumerate(lines):
        if 'class QuickSearchController' in line:
            controller_start = i
        elif controller_start > 0 and line.strip().startswith('class '):
            # Ďalšia trieda = koniec QuickSearchController
            controller_end = i - 1
            break

    if controller_end == 0:
        controller_end = len(lines) - 1

    # Nájdi poslednú metódu v QuickSearchController
    last_method_end = controller_start
    for i in range(controller_end, controller_start, -1):
        line = lines[i]
        # Hľadaj riadok ktorý nie je prázdny a nie je odsadený (koniec metódy)
        if line.strip() and not line.startswith('        ') and not line.startswith('\t\t'):
            last_method_end = i
            break

    print(f"✅ Vkladám metódy na riadok {last_method_end + 1}")

    # Metódy na pridanie
    methods = [
        '',
        '    def get_active_column(self):',
        '        """',
        '        Vráti index aktuálne aktívneho stĺpca.',
        '        ',
        '        Returns:',
        '            int: Index aktívneho stĺpca',
        '        """',
        '        return self.current_column',
        '',
        '    def set_active_column(self, column):',
        '        """',
        '        Nastaví aktívny stĺpec a aktualizuje UI.',
        '        ',
        '        Args:',
        '            column: Index stĺpca',
        '        """',
        '        if 0 <= column < self.table_view.model().columnCount():',
        '            self.current_column = column',
        '            self._sort_by_column(column)',
        '            self.search_container.set_column(column)',
        '            self.logger.info(f"Active column set to {column}")',
    ]

    # Vlož metódy
    for line in reversed(methods):
        lines.insert(last_method_end, line)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Nové riadky: {len(lines)}")
    print("\nPridané metódy:")
    print("  ✅ get_active_column() → int")
    print("  ✅ set_active_column(column) - nastaví a aktualizuje UI")
    print("\nTeraz môžeš spustiť aplikáciu a otestovať grid settings!")


if __name__ == "__main__":
    main()