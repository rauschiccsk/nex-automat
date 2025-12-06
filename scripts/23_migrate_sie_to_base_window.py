"""
Migruje supplier-invoice-editor MainWindow na BaseWindow
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("MIGRÁCIA: supplier-invoice-editor → BaseWindow")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi import sekciu
    import_end = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('from') or line.strip().startswith('import'):
            import_end = i + 1

    print(f"✅ Import sekcia končí na riadku {import_end}")

    # Nájdi class MainWindow(QMainWindow):
    class_line = None
    for i, line in enumerate(lines):
        if 'class MainWindow(QMainWindow):' in line:
            class_line = i
            break

    if class_line is None:
        print("❌ class MainWindow(QMainWindow): nenájdená")
        return

    print(f"✅ class MainWindow nájdená na riadku {class_line + 1}")

    # Zmeny:
    # 1. Pridať import BaseWindow
    new_import = "from nex_shared.ui import BaseWindow\n"

    # Skontroluj či už import existuje
    has_import = any('from nex_shared.ui import BaseWindow' in line for line in lines)

    if not has_import:
        # Nájdi kde pridať import (po ostatných from imports)
        insert_pos = import_end
        lines.insert(insert_pos, new_import)
        print(f"✅ Pridaný import BaseWindow na riadok {insert_pos + 1}")
        class_line += 1  # Adjust class line
    else:
        print(f"⏭️  Import BaseWindow už existuje")

    # 2. Zmeniť QMainWindow na BaseWindow
    old_class = lines[class_line]
    new_class = old_class.replace('QMainWindow', 'BaseWindow')
    lines[class_line] = new_class
    print(f"✅ Zmenené: QMainWindow → BaseWindow")

    # 3. Upraviť __init__ - pridať super().__init__ s BaseWindow parametrami
    # Nájdi __init__
    init_line = None
    for i in range(class_line, min(class_line + 20, len(lines))):
        if 'def __init__(self' in lines[i]:
            init_line = i
            break

    if init_line:
        print(f"✅ __init__ nájdený na riadku {init_line + 1}")

        # Nájdi super().__init__ alebo QMainWindow.__init__
        super_line = None
        for i in range(init_line, min(init_line + 10, len(lines))):
            if 'super().__init__' in lines[i] or 'QMainWindow.__init__' in lines[i]:
                super_line = i
                break

        if super_line:
            print(f"✅ super().__init__ nájdený na riadku {super_line + 1}")

            # Nahraď super().__init__() za BaseWindow init
            indent = "        "
            new_super = f"{indent}super().__init__(\n"
            new_super += f"{indent}    window_name=WINDOW_MAIN,\n"
            new_super += f"{indent}    default_size=(1400, 900),\n"
            new_super += f"{indent}    default_pos=(100, 100)\n"
            new_super += f"{indent})\n"

            lines[super_line] = new_super
            print(f"✅ super().__init__ aktualizovaný s BaseWindow parametrami")

    # 4. Odstrániť _load_geometry() volanie
    for i in range(init_line, min(init_line + 30, len(lines))):
        if 'self._load_geometry()' in lines[i]:
            lines[i] = ''  # Remove line
            print(f"✅ Odstránený riadok {i + 1}: self._load_geometry()")
            break

    # 5. Odstrániť _load_geometry() funkciu
    load_geom_start = None
    for i, line in enumerate(lines):
        if 'def _load_geometry(self):' in line:
            load_geom_start = i
            break

    if load_geom_start:
        # Nájdi koniec funkcie
        load_geom_end = None
        for i in range(load_geom_start + 1, len(lines)):
            if lines[i].strip() and not lines[i].startswith(' '):
                load_geom_end = i
                break
            if 'def ' in lines[i] and not lines[i].startswith('        '):
                load_geom_end = i
                break

        if load_geom_end:
            # Odstráň funkciu
            for i in range(load_geom_start, load_geom_end):
                lines[i] = ''
            print(f"✅ Odstránená _load_geometry() funkcia (riadky {load_geom_start + 1}-{load_geom_end})")

    # 6. Odstrániť closeEvent() - BaseWindow to rieši
    close_event_start = None
    for i, line in enumerate(lines):
        if 'def closeEvent(self, event):' in line:
            close_event_start = i
            break

    if close_event_start:
        # Nájdi koniec funkcie
        close_event_end = None
        for i in range(close_event_start + 1, len(lines)):
            if lines[i].strip() and not lines[i].startswith(' '):
                close_event_end = i
                break
            if 'def ' in lines[i] and not lines[i].startswith('        '):
                close_event_end = i
                break

        if close_event_end:
            # Odstráň funkciu
            for i in range(close_event_start, close_event_end):
                lines[i] = ''
            print(f"✅ Odstránená closeEvent() funkcia (riadky {close_event_start + 1}-{close_event_end})")

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor migrovaný: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("MIGRÁCIA HOTOVÁ")
    print("=" * 80)
    print("\nZmeny:")
    print("  ✅ Import BaseWindow")
    print("  ✅ class MainWindow(BaseWindow)")
    print("  ✅ super().__init__ s BaseWindow parametrami")
    print("  ✅ Odstránené _load_geometry()")
    print("  ✅ Odstránené closeEvent()")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → Maximize")
    print("  → Zavri")
    print("  → Spusti znova")
    print("  → MUSÍ byť maximalizované ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()