"""
NEX Automat v2.1 - Oprava pripojenia signálov pre grid settings
Pripojí sectionResized a sectionMoved signály.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def find_best_place_for_signals():
    """Nájde najlepšie miesto pre pripojenie signálov."""
    print(f"\n{'=' * 80}")
    print("1. ANALÝZA _setup_ui()")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi _setup_ui v InvoiceListWidget (po riadku 130)
    setup_line = None
    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line and i > 130:
            setup_line = i
            print(f"✅ _setup_ui nájdená na riadku {i + 1}")
            break

    if setup_line is None:
        print("❌ _setup_ui nenájdená!")
        return None, None

    # Nájdi koniec _setup_ui
    indent = len(lines[setup_line]) - len(lines[setup_line].lstrip())
    end_line = None

    for i in range(setup_line + 1, min(setup_line + 150, len(lines))):
        line = lines[i]
        if line.strip() and not line.strip().startswith('#'):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent and line.strip().startswith('def '):
                end_line = i
                break

    if end_line is None:
        end_line = min(setup_line + 150, len(lines))

    print(f"✅ _setup_ui končí na riadku {end_line}")

    # Zobraz kľúčové riadky v _setup_ui
    print("\nKľúčové riadky v _setup_ui:")
    for i in range(setup_line, min(end_line, setup_line + 50)):
        line = lines[i].rstrip()
        if any(keyword in line for keyword in ['table', 'header', 'Header', 'quick_search', 'layout']):
            print(f"  {i + 1:4d}: {line}")

    # Stratégia: Pripojíme signály na koniec _setup_ui
    insert_line = end_line - 1

    # Ak je tam prázdny riadok, použime ten
    while insert_line > setup_line and not lines[insert_line].strip():
        insert_line -= 1

    insert_line += 1  # Za posledný neprázdny riadok

    print(f"\n✅ Signály pripojím na riadok {insert_line}")

    return lines, insert_line


def add_signal_connections(lines, insert_line):
    """Pridá pripojenie signálov."""
    print(f"\n{'=' * 80}")
    print("2. PRIDANIE PRIPOJENIA SIGNÁLOV")
    print(f"{'=' * 80}")

    # Skontroluj, či už signály sú pripojené
    content = ''.join(lines)
    if 'header.sectionResized.connect' in content:
        print("✅ Signály už sú pripojené")
        return lines

    # Signály na pripojenie
    signal_code = [
        '\n',
        '        # Connect header signals for grid settings\n',
        '        header = self.table.horizontalHeader()\n',
        '        header.sectionResized.connect(self._on_column_resized)\n',
        '        header.sectionMoved.connect(self._on_column_moved)\n'
    ]

    print("Pridávam:")
    for line in signal_code:
        print(f"  {line.rstrip()}")

    # Vlož signály
    for idx, line in enumerate(signal_code):
        lines.insert(insert_line + idx, line)

    print(f"\n✅ Signály pridané na riadok {insert_line}")

    return lines


def verify_signals():
    """Overí, že signály sú správne pripojené."""
    print(f"\n{'=' * 80}")
    print("3. VERIFIKÁCIA SIGNÁLOV")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'sectionResized.connect': 'header.sectionResized.connect(self._on_column_resized)' in content,
        'sectionMoved.connect': 'header.sectionMoved.connect(self._on_column_moved)' in content,
        'Metóda _on_column_resized': 'def _on_column_resized(self' in content,
        'Metóda _on_column_moved': 'def _on_column_moved(self' in content,
    }

    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_ok = False

    return all_ok


def show_signal_context():
    """Zobrazí kontext okolo pripojených signálov."""
    print(f"\n{'=' * 80}")
    print("4. KONTEXT SIGNÁLOV")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'sectionResized.connect' in line:
            print(f"\nNájdené na riadku {i + 1}:")
            for j in range(max(0, i - 3), min(len(lines), i + 5)):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j].rstrip()}")
            break


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA PRIPOJENIA SIGNÁLOV ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Nájdi miesto
    lines, insert_line = find_best_place_for_signals()

    if lines is None:
        print("\n❌ STOP: Nepodarilo sa nájsť _setup_ui()")
        return

    # 2. Pridaj signály
    lines = add_signal_connections(lines, insert_line)

    # 3. Ulož súbor
    print(f"\n{'=' * 80}")
    print("UKLADANIE SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor uložený")
    print(f"✅ Počet riadkov: {len(lines)}")

    # 4. Verifikácia
    if not verify_signals():
        print("\n❌ VAROVANIE: Niektoré signály chýbajú!")
        return

    # 5. Kontext
    show_signal_context()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Signály sectionResized a sectionMoved pripojené")
    print("✅ Grid settings integrácia DOKONČENÁ")
    print("\n⏭️  ĎALŠÍ KROK: Testovanie:")
    print("   1. python main.py")
    print("   2. Zmeniť šírku stĺpca (potiahnuť okraj hlavičky)")
    print("   3. Zatvoriť aplikáciu")
    print("   4. Overiť databázu:")
    print("      C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\grid_settings.db")
    print("   5. Znovu spustiť - šírka by mala zostať")


if __name__ == "__main__":
    main()