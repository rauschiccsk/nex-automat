"""
Opraví utils/__init__.py - odstráni staré window_settings imports
"""
from pathlib import Path

UTILS_INIT_PATH = Path("apps/supplier-invoice-editor/src/utils/__init__.py")


def main():
    print("=" * 80)
    print("FIX: utils/__init__.py")
    print("=" * 80)

    # Načítaj súbor
    with open(UTILS_INIT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Zobraz aktuálny obsah
    print("\nAktuálny obsah:")
    for i, line in enumerate(lines):
        print(f"{i + 1:3d}: {line}", end='')

    # Nájdi a odstráň import window_settings funkcií
    new_lines = []
    skip_until = -1

    for i, line in enumerate(lines):
        # Skip ak sme v multiline import
        if i <= skip_until:
            continue

        # Nájdi import z window_settings
        if 'from .window_settings import' in line:
            # Skontroluj či je multiline
            if '(' in line and ')' not in line:
                # Multiline import - nájdi koniec
                end_line = i
                for j in range(i + 1, len(lines)):
                    if ')' in lines[j]:
                        end_line = j
                        break

                # Prečítaj celý import
                import_text = ''.join(lines[i:end_line + 1])

                print(f"\n✅ Našiel multiline import (riadky {i + 1}-{end_line + 1})")

                # Odstráň load_window_settings a save_window_settings
                import_text = import_text.replace('load_window_settings,', '')
                import_text = import_text.replace('save_window_settings,', '')
                import_text = import_text.replace('load_window_settings', '')
                import_text = import_text.replace('save_window_settings', '')

                # Vyčisti
                import_text = import_text.replace(',,', ',')
                import_text = import_text.replace('(\n,', '(')
                import_text = import_text.replace(',\n)', '\n)')

                # Ak je import prázdny, preskočiť celý block
                if '()' in import_text or import_text.strip() == 'from .window_settings import':
                    print(f"   → Odstránený celý import (prázdny)")
                    skip_until = end_line
                    continue

                # Inak pridaj upravený import
                new_lines.append(import_text)
                skip_until = end_line
                print(f"   → Upravený import")
            else:
                # Single line import
                if 'load_window_settings' in line or 'save_window_settings' in line:
                    print(f"\n✅ Našiel single-line import na riadku {i + 1}")
                    print(f"   → Odstránený")
                    continue
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Ak je výsledok prázdny alebo len whitespace, vytvor minimal __init__
    if all(line.strip() == '' for line in new_lines):
        new_lines = [
            '"""Utils package"""\n',
            'from .constants import WINDOW_MAIN, GRID_INVOICE_LIST\n',
            'from .window_settings import save_grid_settings, load_grid_settings\n',
            '\n',
            '__all__ = [\n',
            '    "WINDOW_MAIN",\n',
            '    "GRID_INVOICE_LIST",\n',
            '    "save_grid_settings",\n',
            '    "load_grid_settings",\n',
            ']\n'
        ]
        print("\n✅ Vytvorený nový minimal __init__.py")

    # Ulož súbor
    with open(UTILS_INIT_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Súbor opravený: {UTILS_INIT_PATH}")

    print("\n" + "=" * 80)
    print("NOVÝ OBSAH:")
    print("=" * 80)
    for i, line in enumerate(new_lines):
        print(f"{i + 1:3d}: {line}", end='')

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("python main.py")
    print("=" * 80)


if __name__ == '__main__':
    main()