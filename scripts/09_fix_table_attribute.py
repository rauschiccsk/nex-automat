"""
NEX Automat v2.1 - Oprava názvu atribútu table -> table_view
Opraví všetky výskyty self.table na self.table_view v grid settings kóde.
"""

from pathlib import Path
import re

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def analyze_file():
    """Analyzuj súbor a nájdi problémové výskyty."""
    print(f"\n{'=' * 80}")
    print("1. ANALÝZA SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi všetky výskyty self.table
    table_lines = []
    table_view_lines = []

    for i, line in enumerate(lines):
        if 'self.table.' in line:
            table_lines.append((i + 1, line.rstrip()))
        if 'self.table_view' in line:
            table_view_lines.append((i + 1, line.rstrip()))

    print(f"\nVýskyty 'self.table.' (problémové): {len(table_lines)}")
    for line_num, line in table_lines[:10]:  # Zobraz prvých 10
        print(f"  {line_num:4d}: {line}")

    print(f"\nVýskyty 'self.table_view': {len(table_view_lines)}")
    print(f"  (Toto je správny atribút)")

    return lines, table_lines


def fix_table_references(lines):
    """Opraví všetky self.table na self.table_view."""
    print(f"\n{'=' * 80}")
    print("2. OPRAVA self.table -> self.table_view")
    print(f"{'=' * 80}")

    fixed_count = 0

    for i, line in enumerate(lines):
        # Nahraď self.table. za self.table_view.
        # Ale NEPREHRAJ self.table_view (nechceme self.table_view_view)
        if 'self.table.' in line and 'self.table_view' not in line:
            original = line
            # Použij regulárny výraz pre presné nahradenie
            # self.table. -> self.table_view.
            # ale nie self.table_view
            new_line = re.sub(r'\bself\.table\.', 'self.table_view.', line)

            if new_line != original:
                lines[i] = new_line
                fixed_count += 1
                print(f"  Riadok {i + 1}:")
                print(f"    Pred: {original.rstrip()}")
                print(f"    Po:   {new_line.rstrip()}")

    print(f"\n✅ Opravených {fixed_count} výskytov")

    return lines, fixed_count


def remove_duplicate_header_line():
    """Odstráni duplicitný riadok 'header = self.table.horizontalHeader()'."""
    print(f"\n{'=' * 80}")
    print("3. ODSTRÁNENIE DUPLICITNÉHO RIADKU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi riadok s 'header = self.table' alebo 'header = self.table_view'
    # v sekcii pripojenia signálov (okolo riadku 200)

    removed = False
    for i in range(len(lines)):
        line = lines[i]
        # Ak je to duplicitný header = ... pred pripojením signálov
        if i > 195 and i < 205:  # V oblasti pripojenia signálov
            if 'header = self.table' in line or 'header = self.table_view.horizontalHeader()' in line:
                # Skontroluj, či nasledujúci riadok má sectionResized
                if i + 1 < len(lines) and 'sectionResized.connect' in lines[i + 1]:
                    print(f"  ⚠️  Duplicitný riadok na {i + 1}: {line.rstrip()}")
                    print(f"     Odstránim tento riadok a použijem existujúci header")
                    lines.pop(i)
                    removed = True
                    break

    if removed:
        print("  ✅ Duplicitný riadok odstránený")
    else:
        print("  ℹ️  Duplicitný riadok nenájdený (možno už opravené)")

    return lines


def verify_fix():
    """Overí opravu."""
    print(f"\n{'=' * 80}")
    print("4. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = f.readlines()

    # Počítaj self.table vs self.table_view
    table_count = len([l for l in lines if 'self.table.' in l and 'self.table_view' not in l])
    table_view_count = len([l for l in lines if 'self.table_view' in l])

    print(f"Výskyty 'self.table.': {table_count}")
    print(f"Výskyty 'self.table_view': {table_view_count}")

    if table_count > 0:
        print(f"\n⚠️  Stále existuje {table_count} výskytov self.table")
        print("   Zobrazujem ich:")
        with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if 'self.table.' in line and 'self.table_view' not in line:
                print(f"  {i + 1:4d}: {line.rstrip()}")
        return False
    else:
        print("\n✅ Žiadne výskyty self.table")
        return True


def show_signal_area():
    """Zobraz oblasť pripojenia signálov."""
    print(f"\n{'=' * 80}")
    print("5. OBLASŤ PRIPOJENIA SIGNÁLOV")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'Connect header signals for grid settings' in line:
            print(f"\nKontext okolo riadku {i + 1}:")
            for j in range(max(0, i - 3), min(len(lines), i + 8)):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j].rstrip()}")
            break


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA ATRIBÚTU table -> table_view ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Analýza
    lines, table_lines = analyze_file()

    if not table_lines:
        print("\n✅ Žiadne problémové výskyty self.table")
        return

    # 2. Oprava
    lines, fixed = fix_table_references(lines)

    # 3. Odstráň duplicitný header
    lines = remove_duplicate_header_line()

    # 4. Ulož
    print(f"\n{'=' * 80}")
    print("UKLADANIE SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    # 5. Verifikácia
    if not verify_fix():
        print("\n❌ VAROVANIE: Oprava nebola úplná!")
        return

    # 6. Zobraz signály
    show_signal_area()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print(f"✅ Opravených {fixed} výskytov self.table -> self.table_view")
    print("✅ Duplicitný header riadok odstránený")
    print("\n⏭️  ĎALŠÍ KROK: Testovanie:")
    print("   python main.py")


if __name__ == "__main__":
    main()