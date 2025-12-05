"""
NEX Automat v2.1 - Oprava zvyšných self.table v grid metódach
Opraví self.table na self.table_view v _load_grid_settings a _save_grid_settings.
"""

from pathlib import Path
import re

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def find_all_table_references():
    """Nájdi všetky výskyty self.table."""
    print(f"\n{'=' * 80}")
    print("1. HĽADANIE VŠETKÝCH self.table")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    table_refs = []

    for i, line in enumerate(lines):
        # Hľadaj self.table. ale nie self.table_view
        if 'self.table.' in line or 'self.table)' in line:
            if 'self.table_view' not in line:
                table_refs.append((i + 1, line.rstrip()))

    if table_refs:
        print(f"\nNájdených {len(table_refs)} problémových výskytov:")
        for line_num, line in table_refs:
            print(f"  {line_num:4d}: {line}")
    else:
        print("\n✅ Žiadne problémové výskyty")

    return lines, table_refs


def fix_all_table_references(lines):
    """Opraví všetky self.table na self.table_view."""
    print(f"\n{'=' * 80}")
    print("2. OPRAVA VŠETKÝCH VÝSKYTOV")
    print(f"{'=' * 80}")

    fixed = 0

    for i, line in enumerate(lines):
        # Nahraď self.table za self.table_view, ale nie self.table_view_view
        if ('self.table.' in line or 'self.table)' in line) and 'self.table_view' not in line:
            original = line

            # Použij regex pre presné nahradenie
            new_line = re.sub(r'\bself\.table\b', 'self.table_view', line)

            if new_line != original:
                lines[i] = new_line
                fixed += 1
                print(f"  Riadok {i + 1}:")
                print(f"    Pred: {original.rstrip()}")
                print(f"    Po:   {new_line.rstrip()}")

    print(f"\n✅ Opravených {fixed} výskytov")

    return lines, fixed


def verify_no_table_left():
    """Overí, že neostali žiadne self.table."""
    print(f"\n{'=' * 80}")
    print("3. FINÁLNA VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    remaining = []

    for i, line in enumerate(lines):
        if ('self.table.' in line or 'self.table)' in line) and 'self.table_view' not in line:
            remaining.append((i + 1, line.rstrip()))

    if remaining:
        print(f"\n❌ Ešte {len(remaining)} problémových výskytov:")
        for line_num, line in remaining:
            print(f"  {line_num:4d}: {line}")
        return False
    else:
        print("\n✅ Žiadne self.table výskyty")
        print("✅ Všetky referencie sú self.table_view")
        return True


def show_grid_methods():
    """Zobraz grid metódy s opravami."""
    print(f"\n{'=' * 80}")
    print("4. UKÁŽKA OPRAVENÝCH METÓD")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # _load_grid_settings - zobraz kritické riadky
    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            print("\n_load_grid_settings() - kritické riadky:")
            for j in range(i, min(i + 25, len(lines))):
                if 'header' in lines[j].lower() or 'table' in lines[j].lower():
                    print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            break

    # _save_grid_settings - zobraz kritické riadky
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            print("\n_save_grid_settings() - kritické riadky:")
            for j in range(i, min(i + 20, len(lines))):
                if 'header' in lines[j].lower() or 'table' in lines[j].lower():
                    print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            break


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA ZVYŠNÝCH self.table ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Nájdi všetky výskyty
    lines, table_refs = find_all_table_references()

    if not table_refs:
        print("\n✅ Nič na opravu")
        return

    # 2. Oprav všetky
    lines, fixed = fix_all_table_references(lines)

    if fixed == 0:
        print("\n⚠️  Žiadne zmeny")
        return

    # 3. Ulož
    print(f"\n{'=' * 80}")
    print("UKLADANIE SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    # 4. Verifikácia
    if not verify_no_table_left():
        print("\n❌ VAROVANIE: Ešte ostali problémové výskyty!")
        return

    # 5. Ukážka
    show_grid_methods()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print(f"✅ Opravených {fixed} výskytov self.table -> self.table_view")
    print("✅ Grid settings metódy teraz používajú správny atribút")
    print("\n⏭️  KONEČNÝ TEST:")
    print("   python main.py")
    print("\n   Aplikácia by mala:")
    print("   1. Spustiť sa bez chyby")
    print("   2. Načítať invoice list")
    print("   3. Uložiť šírku stĺpca po zmene")


if __name__ == "__main__":
    main()