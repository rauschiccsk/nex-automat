r"""
Script 26: Pripojenie signálov sectionResized a sectionMoved v _setup_ui.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Pripojí header signály v _setup_ui."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či už signály sú pripojené
    if 'header.sectionResized.connect' in content:
        print("✅ Signály už sú pripojené")
        return

    # Nájdi _setup_ui metódu a v nej miesto kde je "header ="
    new_lines = []
    added = False
    in_setup_ui = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        if 'def _setup_ui(self):' in line:
            in_setup_ui = True

        # Koniec _setup_ui
        if in_setup_ui and i > 143 and line.strip().startswith('def '):
            in_setup_ui = False

        # Hľadaj kde sa nastavuje header (header = self.table_view.horizontalHeader())
        # Alebo kde je header.setSectionResizeMode alebo header.setStretchLastSection
        if not added and in_setup_ui and ('header = self.table_view.horizontalHeader()' in line
                                          or 'header.setSectionResizeMode' in line
                                          or 'header.setStretchLastSection' in line):
            # Po tomto riadku skontroluj ešte ďalšie 5 riadkov, možno tam sú header.set... volania
            # Pridaj signály až za všetky header.set... volania

            # Pozri sa 10 riadkov dopredu
            j = i + 1
            last_header_line = i
            while j < len(lines) and j < i + 10:
                if 'header.' in lines[j] and '.connect(' not in lines[j]:
                    last_header_line = j
                j += 1

            # Teraz vieme že last_header_line je posledný riadok s header. nastavením
            # Signály pridáme hneď po ňom
            if i == last_header_line:
                # Sme na poslednom header riadku, môžeme pridať teraz
                new_lines.append('')
                new_lines.append('        # Connect header signals for grid settings')
                new_lines.append('        header.sectionResized.connect(self._on_column_resized)')
                new_lines.append('        header.sectionMoved.connect(self._on_column_moved)')
                added = True
                print(f"✅ Pridané signály za riadok {i + 1}")

    if not added:
        print("❌ Nepodarilo sa nájsť vhodné miesto pre pripojenie signálov")
        print("⚠️  Skúsim ešte iný prístup...")

        # Pokus 2: Pridaj signály za riadok kde je "# Configure headers" komentár
        new_lines = []
        added = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            if not added and '# Configure headers' in line:
                # Pozri sa 15 riadkov dopredu a nájdi posledný riadok s header.
                j = i + 1
                last_header_line = i
                while j < len(lines) and j < i + 15:
                    if 'header.' in lines[j] and '.connect(' not in lines[j]:
                        last_header_line = j
                    j += 1

                # Preskočíme do last_header_line
                while i < last_header_line:
                    i += 1
                    if i < len(lines):
                        new_lines.append(lines[i])

                # Teraz pridáme signály
                new_lines.append('')
                new_lines.append('        # Connect header signals for grid settings')
                new_lines.append('        header.sectionResized.connect(self._on_column_resized)')
                new_lines.append('        header.sectionMoved.connect(self._on_column_moved)')
                added = True
                print(f"✅ Pridané signály za riadok {last_header_line + 1}")
                break

    if not added:
        print("❌ Stále sa nepodarilo - použijem jednoduchší prístup")
        # Pokus 3: Pridaj na koniec _setup_ui metódy (pred quick search container)
        new_lines = []
        added = False

        for i, line in enumerate(lines):
            # Hľadaj riadok kde je QuickSearchContainer
            if not added and 'QuickSearchContainer' in line and 'self.quick_search_container' in line:
                # Pridaj signály PRED tento riadok
                new_lines.append('')
                new_lines.append('        # Connect header signals for grid settings')
                new_lines.append('        header = self.table_view.horizontalHeader()')
                new_lines.append('        header.sectionResized.connect(self._on_column_resized)')
                new_lines.append('        header.sectionMoved.connect(self._on_column_moved)')
                new_lines.append('')
                added = True
                print(f"✅ Pridané signály pred riadok {i + 1}")

            new_lines.append(line)

    if added:
        # Zapíš späť
        content = '\n'.join(new_lines)
        TARGET_FILE.write_text(content, encoding='utf-8')

        print(f"\n✅ Súbor upravený: {TARGET_FILE}")
        print(f"   Nové riadky: {len(new_lines)}")
        print("\nPridané:")
        print("  ✅ header.sectionResized.connect(self._on_column_resized)")
        print("  ✅ header.sectionMoved.connect(self._on_column_moved)")
        print("\nTeraz spusti aplikáciu, zmeň šírku stĺpca a skontroluj databázu!")
    else:
        print("\n❌ Nepodarilo sa pridať signály automaticky")
        print("Pozri sa do súboru manuálne a pridaj do _setup_ui:")
        print("  header = self.table_view.horizontalHeader()")
        print("  header.sectionResized.connect(self._on_column_resized)")
        print("  header.sectionMoved.connect(self._on_column_moved)")


if __name__ == "__main__":
    main()