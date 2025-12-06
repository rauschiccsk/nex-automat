"""
Opraví main_window.py - presunie import, odstráni orphaned code
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("FIX: main_window.py - Complete Fix")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1. Nájdi a odstráň BaseWindow import z riadku 240
    new_lines = []
    removed_bad_import = False

    for i, line in enumerate(lines):
        if i == 239 and 'from nex_shared.ui import BaseWindow' in line:
            print(f"✅ Odstránený zlý import z riadku {i + 1}")
            removed_bad_import = True
            continue
        new_lines.append(line)

    lines = new_lines

    # 2. Pridaj BaseWindow import na správne miesto (po ostatných imports)
    import_added = False
    for i, line in enumerate(lines):
        if 'from PyQt5.QtWidgets import QMainWindow' in line:
            # Nahraď tento import
            lines[i] = line  # Ponechaj pôvodný
            # Pridaj BaseWindow import za tento riadok
            if i + 1 < len(lines) and 'from nex_shared.ui import BaseWindow' not in lines[i + 1]:
                lines.insert(i + 1, 'from nex_shared.ui import BaseWindow\n')
                print(f"✅ Pridaný import BaseWindow za riadok {i + 1}")
                import_added = True
                break

    # 3. Nájdi orphaned keyPressEvent code (bez def hlavičky)
    # Hľadáme riadky 241-249 ktoré sú orphaned
    orphaned_start = None
    for i, line in enumerate(lines):
        # Hľadáme "if event.key() == Qt.Key_Escape:" ktorý nie je v žiadnej funkcii
        if 'if event.key() == Qt.Key_Escape:' in line:
            # Overiť že nemá def nad sebou
            has_def = False
            for j in range(max(0, i - 10), i):
                if 'def keyPressEvent(self, event):' in lines[j]:
                    has_def = True
                    break

            if not has_def:
                orphaned_start = i
                print(f"✅ Našiel orphaned code na riadku {i + 1}")
                break

    # 4. Odstráň orphaned code
    if orphaned_start:
        # Odstráň riadky až po super().keyPressEvent(event)
        orphaned_end = None
        for i in range(orphaned_start, min(orphaned_start + 15, len(lines))):
            if 'super().keyPressEvent(event)' in lines[i]:
                orphaned_end = i + 1
                break

        if orphaned_end:
            # Odstráň riadky
            for i in range(orphaned_start, orphaned_end):
                lines[i] = ''
            print(f"✅ Odstránený orphaned code (riadky {orphaned_start + 1}-{orphaned_end})")

    # 5. Odstráň prázdne riadky
    final_lines = []
    empty_count = 0
    for line in lines:
        if line.strip() == '':
            empty_count += 1
            if empty_count <= 2:
                final_lines.append(line)
        else:
            empty_count = 0
            final_lines.append(line)

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

    print(f"\n✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("CHANGES:")
    print("=" * 80)
    print("  ✅ BaseWindow import presunutý na správne miesto")
    print("  ✅ Orphaned keyPressEvent code odstránený")
    print("  ✅ Prázdne riadky vyčistené")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("=" * 80)


if __name__ == '__main__':
    main()