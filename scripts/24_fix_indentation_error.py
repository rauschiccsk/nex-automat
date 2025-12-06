"""
Opraví indentation error v main_window.py
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("FIX: Indentation Error")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi problémový riadok
    for i, line in enumerate(lines):
        if 'if event.key() == Qt.Key_Escape:' in line:
            print(f"✅ Problémový riadok nájdený: {i + 1}")
            print(f"   Aktuálny indent: {len(line) - len(line.lstrip())} spaces")

            # Overiť či je to v správnej funkcii
            # Nájdi predchádzajúcu def
            for j in range(i - 1, max(0, i - 50), -1):
                if 'def ' in lines[j]:
                    print(f"   Funkcia: {lines[j].strip()}")
                    break

    # Odstráň všetky prázdne riadky (zostali po odstránení closeEvent)
    new_lines = []
    empty_count = 0

    for line in lines:
        if line.strip() == '':
            empty_count += 1
            # Max 2 prázdne riadky po sebe
            if empty_count <= 2:
                new_lines.append(line)
        else:
            empty_count = 0
            new_lines.append(line)

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Odstránených {len(lines) - len(new_lines)} prázdnych riadkov")
    print(f"✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("python main.py")
    print("  → Ak je stále error, pošli mi riadok okolo 242")
    print("=" * 80)


if __name__ == '__main__':
    main()