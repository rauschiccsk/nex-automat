"""
NEX Automat v2.1 - Oprava self.model.HEADERS na self.model.COLUMNS
Zmení prístup k názvom stĺpcov na správny formát.

Pred:
  for col_idx, col_name in enumerate(self.model.HEADERS):

Po:
  for col_idx in range(self.model.columnCount()):
      col_name = self.model.COLUMNS[col_idx][0]
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def show_current_code():
    """Zobrazí aktuálny kód s problémom."""
    print(f"\n{'=' * 80}")
    print("1. AKTUÁLNY PROBLÉMOVÝ KÓD")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi oba výskyty
    for i, line in enumerate(lines):
        if 'for col_idx, col_name in enumerate(self.model.HEADERS):' in line:
            print(f"\nRiadok {i + 1}:")
            for j in range(max(0, i - 2), min(len(lines), i + 8)):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j].rstrip()}")


def fix_load_grid_settings():
    """Opraví _load_grid_settings metódu."""
    print(f"\n{'=' * 80}")
    print("2. OPRAVA _load_grid_settings()")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi _load_grid_settings
    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            load_start = i
            break

    # Nájdi problémový riadok
    for i in range(load_start, load_start + 30):
        if 'for col_idx, col_name in enumerate(self.model.HEADERS):' in lines[i]:
            print(f"Našiel som problém na riadku {i + 1}")

            # Získaj indentáciu
            indent = len(lines[i]) - len(lines[i].lstrip())
            spaces = ' ' * indent

            # Nahraď riadok
            old_line = lines[i]
            lines[i] = f"{spaces}for col_idx in range(self.model.columnCount()):\n"

            # Pridaj riadok na získanie názvu
            lines.insert(i + 1, f"{spaces}    col_name = self.model.COLUMNS[col_idx][0]\n")

            print(f"Pred:\n  {old_line.rstrip()}")
            print(f"Po:\n  {lines[i].rstrip()}")
            print(f"  {lines[i + 1].rstrip()}")
            break

    return lines


def fix_save_grid_settings(lines):
    """Opraví _save_grid_settings metódu."""
    print(f"\n{'=' * 80}")
    print("3. OPRAVA _save_grid_settings()")
    print(f"{'=' * 80}")

    # Nájdi _save_grid_settings
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            save_start = i
            break

    # Nájdi problémový riadok
    for i in range(save_start, save_start + 30):
        if 'for col_idx, col_name in enumerate(self.model.HEADERS):' in lines[i]:
            print(f"Našiel som problém na riadku {i + 1}")

            # Získaj indentáciu
            indent = len(lines[i]) - len(lines[i].lstrip())
            spaces = ' ' * indent

            # Nahraď riadok
            old_line = lines[i]
            lines[i] = f"{spaces}for col_idx in range(self.model.columnCount()):\n"

            # Pridaj riadok na získanie názvu
            lines.insert(i + 1, f"{spaces}    col_name = self.model.COLUMNS[col_idx][0]\n")

            print(f"Pred:\n  {old_line.rstrip()}")
            print(f"Po:\n  {lines[i].rstrip()}")
            print(f"  {lines[i + 1].rstrip()}")
            break

    return lines


def verify_fix():
    """Overí opravu."""
    print(f"\n{'=' * 80}")
    print("4. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'range(self.model.columnCount())': 'range(self.model.columnCount())' in content,
        'self.model.COLUMNS[col_idx][0]': 'self.model.COLUMNS[col_idx][0]' in content,
        'Nesprávne self.model.HEADERS (malo by chýbať)': 'self.model.HEADERS' not in content,
    }

    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_ok = False

    return all_ok


def show_fixed_code():
    """Zobraz opravený kód."""
    print(f"\n{'=' * 80}")
    print("5. OPRAVENÝ KÓD")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # _load_grid_settings
    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            print("\n_load_grid_settings() - relevantné riadky:")
            for j in range(i, min(i + 25, len(lines))):
                if 'for col_idx' in lines[j] or 'col_name' in lines[j] or 'COLUMNS' in lines[j]:
                    print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            break

    # _save_grid_settings
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            print("\n_save_grid_settings() - relevantné riadky:")
            for j in range(i, min(i + 20, len(lines))):
                if 'for col_idx' in lines[j] or 'col_name' in lines[j] or 'COLUMNS' in lines[j]:
                    print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            break


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA HEADERS -> COLUMNS ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Zobraz aktuálny problém
    show_current_code()

    # 2-3. Opravy
    lines = fix_load_grid_settings()
    lines = fix_save_grid_settings(lines)

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

    # 6. Zobraz opravený kód
    show_fixed_code()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Opravené: self.model.HEADERS -> self.model.COLUMNS[col_idx][0]")
    print("✅ Použitý správny formát pre iteráciu stĺpcov")
    print("\n⏭️  FINÁLNY TEST:")
    print("   python main.py")
    print("\n   Aplikácia by mala:")
    print("   1. Spustiť sa BEZ CHYBY")
    print("   2. Načítať invoice list")
    print("   3. Uložiť grid settings pri zmene šírky")


if __name__ == "__main__":
    main()