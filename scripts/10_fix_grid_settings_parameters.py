"""
NEX Automat v2.1 - Oprava parametrov grid settings funkcií
Opraví volania load/save funkcií - pridá WINDOW_MAIN ako prvý parameter.

Pred:
  load_column_settings(GRID_INVOICE_LIST)

Po:
  load_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST)
"""

from pathlib import Path
import re

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def analyze_grid_calls():
    """Analyzuj volania grid settings funkcií."""
    print(f"\n{'=' * 80}")
    print("1. ANALÝZA VOLANÍ GRID SETTINGS FUNKCIÍ")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi všetky volania grid settings funkcií
    grid_calls = []

    for i, line in enumerate(lines):
        if any(func in line for func in [
            'load_column_settings(',
            'save_column_settings(',
            'load_grid_settings(',
            'save_grid_settings('
        ]):
            grid_calls.append((i + 1, line.rstrip()))

    print(f"\nNájdených {len(grid_calls)} volaní:")
    for line_num, line in grid_calls:
        print(f"  {line_num:4d}: {line}")

    return lines, grid_calls


def fix_load_column_settings(lines):
    """Opraví load_column_settings(GRID_INVOICE_LIST)."""
    print(f"\n{'=' * 80}")
    print("2. OPRAVA load_column_settings()")
    print(f"{'=' * 80}")

    fixed = 0
    for i, line in enumerate(lines):
        if 'load_column_settings(GRID_INVOICE_LIST)' in line:
            original = line
            # Nahraď (GRID_INVOICE_LIST) za (WINDOW_MAIN, GRID_INVOICE_LIST)
            lines[i] = line.replace(
                'load_column_settings(GRID_INVOICE_LIST)',
                'load_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST)'
            )
            print(f"  Riadok {i + 1}:")
            print(f"    Pred: {original.rstrip()}")
            print(f"    Po:   {lines[i].rstrip()}")
            fixed += 1

    print(f"\n✅ Opravených {fixed} volaní")
    return lines, fixed


def fix_save_column_settings(lines):
    """Opraví save_column_settings(GRID_INVOICE_LIST, column_settings)."""
    print(f"\n{'=' * 80}")
    print("3. OPRAVA save_column_settings()")
    print(f"{'=' * 80}")

    fixed = 0
    for i, line in enumerate(lines):
        if 'save_column_settings(GRID_INVOICE_LIST,' in line:
            original = line
            # Nahraď (GRID_INVOICE_LIST, za (WINDOW_MAIN, GRID_INVOICE_LIST,
            lines[i] = line.replace(
                'save_column_settings(GRID_INVOICE_LIST,',
                'save_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST,'
            )
            print(f"  Riadok {i + 1}:")
            print(f"    Pred: {original.rstrip()}")
            print(f"    Po:   {lines[i].rstrip()}")
            fixed += 1

    print(f"\n✅ Opravených {fixed} volaní")
    return lines, fixed


def fix_load_grid_settings(lines):
    """Opraví load_grid_settings(GRID_INVOICE_LIST)."""
    print(f"\n{'=' * 80}")
    print("4. OPRAVA load_grid_settings()")
    print(f"{'=' * 80}")

    fixed = 0
    for i, line in enumerate(lines):
        if 'load_grid_settings(GRID_INVOICE_LIST)' in line:
            original = line
            # Nahraď (GRID_INVOICE_LIST) za (WINDOW_MAIN, GRID_INVOICE_LIST)
            lines[i] = line.replace(
                'load_grid_settings(GRID_INVOICE_LIST)',
                'load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)'
            )
            print(f"  Riadok {i + 1}:")
            print(f"    Pred: {original.rstrip()}")
            print(f"    Po:   {lines[i].rstrip()}")
            fixed += 1

    print(f"\n✅ Opravených {fixed} volaní")
    return lines, fixed


def fix_save_grid_settings(lines):
    """Opraví save_grid_settings(GRID_INVOICE_LIST, grid_settings)."""
    print(f"\n{'=' * 80}")
    print("5. OPRAVA save_grid_settings()")
    print(f"{'=' * 80}")

    fixed = 0
    for i, line in enumerate(lines):
        if 'save_grid_settings(GRID_INVOICE_LIST,' in line:
            original = line
            # Nahraď (GRID_INVOICE_LIST, za (WINDOW_MAIN, GRID_INVOICE_LIST,
            lines[i] = line.replace(
                'save_grid_settings(GRID_INVOICE_LIST,',
                'save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST,'
            )
            print(f"  Riadok {i + 1}:")
            print(f"    Pred: {original.rstrip()}")
            print(f"    Po:   {lines[i].rstrip()}")
            fixed += 1

    print(f"\n✅ Opravených {fixed} volaní")
    return lines, fixed


def verify_fixes():
    """Overí správnosť opráv."""
    print(f"\n{'=' * 80}")
    print("6. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Kontrola správnych volaní
    checks = {
        'load_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST)':
            'load_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST)' in content,

        'save_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST,':
            'save_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST,' in content,

        'load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)':
            'load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)' in content,

        'save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST,':
            'save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST,' in content,
    }

    # Kontrola nesprávnych volaní (mali by chýbať)
    bad_checks = {
        'load_column_settings(GRID_INVOICE_LIST)':
            'load_column_settings(GRID_INVOICE_LIST)' in content,

        'load_grid_settings(GRID_INVOICE_LIST)':
            'load_grid_settings(GRID_INVOICE_LIST)' in content,
    }

    print("\nSprávne volania:")
    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_ok = False

    print("\nNesprávne volania (mali by CHÝBAŤ):")
    for check_name, result in bad_checks.items():
        status = "❌" if result else "✅"
        print(f"{status} {check_name}")
        if result:
            all_ok = False

    return all_ok


def show_fixed_methods():
    """Zobraz opravené metódy."""
    print(f"\n{'=' * 80}")
    print("7. UKÁŽKA OPRAVENÝCH METÓD")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi _load_grid_settings
    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            print("\n_load_grid_settings() (prvých 15 riadkov):")
            for j in range(i, min(i + 15, len(lines))):
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            break

    # Nájdi _save_grid_settings
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            print("\n_save_grid_settings() (prvých 15 riadkov):")
            for j in range(i, min(i + 15, len(lines))):
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            break


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA PARAMETROV GRID SETTINGS ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Analýza
    lines, grid_calls = analyze_grid_calls()

    if not grid_calls:
        print("\n✅ Žiadne grid settings volania")
        return

    # 2-5. Opravy
    lines, f1 = fix_load_column_settings(lines)
    lines, f2 = fix_save_column_settings(lines)
    lines, f3 = fix_load_grid_settings(lines)
    lines, f4 = fix_save_grid_settings(lines)

    total_fixed = f1 + f2 + f3 + f4

    if total_fixed == 0:
        print("\n✅ Všetky volania už sú správne")
        return

    # 6. Ulož
    print(f"\n{'=' * 80}")
    print("UKLADANIE SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    # 7. Verifikácia
    if not verify_fixes():
        print("\n❌ VAROVANIE: Niektoré volania nie sú správne!")
        return

    # 8. Ukážka
    show_fixed_methods()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print(f"✅ Opravených {total_fixed} volaní grid settings funkcií")
    print("✅ Všetky funkcie teraz majú správne parametre:")
    print("   - load_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST)")
    print("   - save_column_settings(WINDOW_MAIN, GRID_INVOICE_LIST, ...)")
    print("   - load_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST)")
    print("   - save_grid_settings(WINDOW_MAIN, GRID_INVOICE_LIST, ...)")
    print("\n⏭️  ĎALŠÍ KROK: Testovanie:")
    print("   python main.py")


if __name__ == "__main__":
    main()