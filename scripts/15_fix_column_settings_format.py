"""
NEX Automat v2.1 - Oprava formátu column settings
Zmení formát dát z dictionary na list of dictionaries.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def fix_save_grid_settings():
    """Opraví _save_grid_settings() - zmení dict na list."""
    print(f"\n{'=' * 80}")
    print("1. OPRAVA _save_grid_settings()")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi _save_grid_settings
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            save_start = i
            print(f"✅ Metóda nájdená na riadku {i + 1}")
            break

    # Nájdi a opravi riadky
    # 1. Zmeniť column_settings = {} na column_settings = []
    for i in range(save_start, save_start + 30):
        if 'column_settings = {}' in lines[i]:
            old = lines[i]
            lines[i] = lines[i].replace('column_settings = {}', 'column_settings = []')
            print(f"\nRiadok {i + 1}:")
            print(f"  Pred: {old.rstrip()}")
            print(f"  Po:   {lines[i].rstrip()}")
            dict_line = i
            break

    # 2. Zmeniť pridávanie do dictionary na append do listu
    # Nájdi riadok s column_settings[col_name] =
    for i in range(dict_line, dict_line + 15):
        if 'column_settings[col_name] = {' in lines[i]:
            # Získaj indentáciu
            indent = len(lines[i]) - len(lines[i].lstrip())
            spaces = ' ' * indent

            print(f"\nRiadok {i + 1}:")
            print(f"  Pred: {lines[i].rstrip()}")

            # Nahraď riadok
            lines[i] = f"{spaces}column_settings.append({{\n"

            # Pridaj column_name ako prvý kľúč
            lines.insert(i + 1, f"{spaces}    'column_name': col_name,\n")

            print(f"  Po:   {lines[i].rstrip()}")
            print(f"        {lines[i + 1].rstrip()}")

            # Nájdi uzatváraciu zátvorku } a pridaj })
            for j in range(i + 1, i + 10):
                if lines[j].strip() == '}':
                    lines[j] = lines[j].replace('}', '})')
                    print(f"  Uzatvorenie: {lines[j].rstrip()}")
                    break

            break

    return lines


def fix_load_grid_settings(lines):
    """Opraví _load_grid_settings() - zmení iteráciu pre list formát."""
    print(f"\n{'=' * 80}")
    print("2. OPRAVA _load_grid_settings()")
    print(f"{'=' * 80}")

    # Nájdi _load_grid_settings
    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            load_start = i
            print(f"✅ Metóda nájdená na riadku {i + 1}")
            break

    # Nájdi problémový blok kódu
    # Hľadáme: for col_idx in range... if col_name in column_settings:

    for i in range(load_start, load_start + 40):
        if 'for col_idx in range(self.model.columnCount()):' in lines[i]:
            loop_start = i
            print(f"\n✅ Našiel som loop na riadku {i + 1}")

            # Získaj indentáciu
            indent = len(lines[i]) - len(lines[i].lstrip())
            spaces = ' ' * indent

            # Zobraz starý kód (5 riadkov)
            print("\nPôvodný kód:")
            for j in range(loop_start, min(loop_start + 15, len(lines))):
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")

            # Nájdi koniec iterácie (hľadáme if col_name in column_settings:)
            for j in range(loop_start, loop_start + 15):
                if 'if col_name in column_settings:' in lines[j]:
                    # Nahradíme tento if blok
                    # Musíme nájsť príslušné nastavenie v liste

                    old_if_line = lines[j]

                    # Nový kód: nájdi setting v liste
                    new_code = f"{spaces}    # Nájdi nastavenia pre tento stĺpec\n"
                    new_code += f"{spaces}    col_settings = next((s for s in column_settings if s.get('column_name') == col_name), None)\n"
                    new_code += f"{spaces}    if col_settings:\n"

                    # Nahraď if col_name in column_settings:
                    lines[j] = new_code

                    # Upravi nasledujúce riadky ktoré používajú column_settings[col_name]
                    # Nahraď column_settings[col_name] za col_settings
                    # a settings za col_settings (odstránime settings = column_settings[col_name])

                    # Nájdi: settings = column_settings[col_name]
                    for k in range(j + 1, j + 5):
                        if 'settings = column_settings[col_name]' in lines[k]:
                            # Odstráň tento riadok
                            lines.pop(k)
                            break

                    # Nahraď všetky settings za col_settings v nasledujúcich riadkoch
                    for k in range(j + 1, j + 15):
                        if lines[k].strip().startswith('if ') and "'width' in settings" in lines[k]:
                            lines[k] = lines[k].replace("'width' in settings", "'width' in col_settings")
                        if lines[k].strip().startswith('header.resizeSection') and 'settings[' in lines[k]:
                            lines[k] = lines[k].replace("settings['width']", "col_settings['width']")
                        if "'visual_index' in settings" in lines[k]:
                            lines[k] = lines[k].replace("'visual_index' in settings", "'visual_index' in col_settings")
                        if "settings['visual_index']" in lines[k]:
                            lines[k] = lines[k].replace("settings['visual_index']", "col_settings['visual_index']")
                        if "'visible' in settings" in lines[k]:
                            lines[k] = lines[k].replace("'visible' in settings", "'visible' in col_settings")
                        if "settings['visible']" in lines[k]:
                            lines[k] = lines[k].replace("settings['visible']", "col_settings['visible']")

                    print("\nNový kód:")
                    for k in range(loop_start, min(loop_start + 20, len(lines))):
                        print(f"  {k + 1:4d}: {lines[k].rstrip()}")

                    break

            break

    return lines


def verify_changes():
    """Overí zmeny."""
    print(f"\n{'=' * 80}")
    print("3. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'column_settings = []': 'column_settings = []' in content,
        'column_settings.append': 'column_settings.append' in content,
        "'column_name': col_name": "'column_name': col_name" in content,
        'col_settings = next(': 'col_settings = next(' in content,
        'Staré: column_settings = {} (malo by chýbať)': 'column_settings = {}' not in content,
        'Staré: column_settings[col_name] (malo by chýbať)': 'column_settings[col_name]' not in content,
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
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA FORMÁTU COLUMN SETTINGS ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Oprav _save_grid_settings
    lines = fix_save_grid_settings()

    # 2. Oprav _load_grid_settings
    lines = fix_load_grid_settings(lines)

    # 3. Ulož
    print(f"\n{'=' * 80}")
    print("UKLADANIE SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    # 4. Verifikácia
    if not verify_changes():
        print("\n❌ VAROVANIE: Niektoré zmeny chýbajú!")
        return

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Formát column settings opravený:")
    print("   - _save_grid_settings: dict → list of dicts")
    print("   - _load_grid_settings: prístup cez next() a get()")
    print("\n⏭️  FINÁLNY TEST:")
    print("   python main.py")
    print("\n   Grid settings by mali KONEČNE fungovať!")


if __name__ == "__main__":
    main()