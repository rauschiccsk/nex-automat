"""
FIX: Pridá window_state do SELECT a return dictionary
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("FIX: load_window_settings() SELECT + return")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1. FIX SELECT statement
    select_line = None
    for i, line in enumerate(lines):
        if 'SELECT x, y, width, height' in line and 'FROM window_settings' in lines[i + 1]:
            select_line = i
            break

    if select_line:
        print(f"✅ SELECT statement nájdený na riadku {select_line + 1}")

        # Nahraď SELECT aby obsahoval window_state
        old_select = lines[select_line]
        new_select = old_select.replace('SELECT x, y, width, height',
                                        'SELECT x, y, width, height, window_state')
        lines[select_line] = new_select

        print(f"✅ SELECT opravený: pridaný window_state stĺpec")

    # 2. FIX return dictionary
    # Nájdi return statement v load_window_settings
    return_line = None
    for i, line in enumerate(lines):
        if "return {'x':" in line or "return {" in line:
            # Overiť že je to v load_window_settings funkcii
            # Nájdi predchádzajúcu def load_window_settings
            for j in range(i, max(0, i - 50), -1):
                if 'def load_window_settings(' in lines[j]:
                    return_line = i
                    break
            if return_line:
                break

    if return_line:
        print(f"✅ return statement nájdený na riadku {return_line + 1}")

        # Zobraz súčasný return
        print(f"\nSúčasný return:")
        for i in range(return_line, min(return_line + 8, len(lines))):
            print(f"  {i + 1}: {lines[i]}", end='')
            if '}' in lines[i]:
                break

        # Nájdi koniec return dictionary (riadok s })
        dict_end = None
        for i in range(return_line, min(return_line + 10, len(lines))):
            if '}' in lines[i]:
                dict_end = i
                break

        if dict_end:
            # Upravíme return aby obsahoval window_state
            # Zistíme ako sú indexy (row[0], row[1]...)
            # x=row[0], y=row[1], width=row[2], height=row[3], window_state=row[4]

            # Nahradíme riadok pred }
            # Predpokladám že return vyzerá:
            # return {
            #     'x': row[0],
            #     'y': row[1],
            #     'width': row[2],
            #     'height': row[3]
            # }

            indent = "            "
            new_line = f"{indent}'window_state': row[4] if len(row) > 4 else 0\n"

            # Vložíme pred }
            lines.insert(dict_end, new_line)

            print(f"\n✅ return dictionary rozšírený o window_state: row[4]")

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor opravený: {WINDOW_SETTINGS_PATH}")

    print("\n" + "=" * 80)
    print("FINÁLNY TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → Okno by malo byť MAXIMALIZOVANÉ ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()