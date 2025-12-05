"""
NEX Automat v2.1 - Restore invoice_list_widget.py na funkčnú verziu
Obnoví súbor z commitu ca84ef6 (pred grid settings).
"""

import os
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
GOOD_COMMIT = "ca84ef6"  # Commit s funkčným quick search (pred grid settings)


def run_command(cmd, cwd=None):
    """Spustí command a vráti výstup."""
    result = subprocess.run(
        cmd,
        cwd=cwd or BASE_DIR,
        capture_output=True,
        text=True,
        shell=True
    )
    return result.stdout, result.stderr, result.returncode


def backup_current():
    """Zazálohuje aktuálny súbor."""
    print(f"\n{'=' * 80}")
    print("1. ZÁLOHA AKTUÁLNEHO SÚBORU")
    print(f"{'=' * 80}")

    backup_file = WIDGET_FILE.with_suffix('.py.broken')

    try:
        # Skopíruj aktuálny súbor
        import shutil
        shutil.copy2(WIDGET_FILE, backup_file)
        print(f"✅ Zálohované do: {backup_file.name}")
        return True
    except Exception as e:
        print(f"❌ Chyba pri zálohovaní: {e}")
        return False


def restore_from_commit():
    """Obnoví súbor z konkrétneho commitu."""
    print(f"\n{'=' * 80}")
    print("2. RESTORE Z COMMITU")
    print(f"{'=' * 80}")

    rel_path = WIDGET_FILE.relative_to(BASE_DIR)

    # Git checkout z konkrétneho commitu
    cmd = f'git checkout {GOOD_COMMIT} -- "{rel_path}"'
    print(f"Príkaz: {cmd}")

    stdout, stderr, code = run_command(cmd)

    if code == 0:
        print(f"✅ Súbor obnovený z commitu {GOOD_COMMIT}")
        return True
    else:
        print(f"❌ Chyba pri restore: {stderr}")
        return False


def verify_methods():
    """Overí prítomnosť potrebných metód."""
    print(f"\n{'=' * 80}")
    print("3. VERIFIKÁCIA METÓD")
    print(f"{'=' * 80}")

    required_methods = [
        '_on_selection_changed',
        '_on_double_clicked',
        '__init__',
        '_setup_ui',
        'load_data',
        'refresh_data'
    ]

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\nKľúčové metódy:")
    print(f"{'Metóda':<30} {'Status'}")
    print("-" * 50)

    all_present = True
    for method in required_methods:
        if f'def {method}(' in content:
            print(f"{method:<30} ✅")
        else:
            print(f"{method:<30} ❌ CHÝBA")
            all_present = False

    return all_present


def check_no_grid_settings():
    """Overí, že grid settings NIE sú v súbore."""
    print(f"\n{'=' * 80}")
    print("4. KONTROLA GRID SETTINGS (mali by CHÝBAŤ)")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    grid_methods = [
        '_load_grid_settings',
        '_save_grid_settings',
        '_on_column_resized',
        '_on_column_moved'
    ]

    no_grid = True
    for method in grid_methods:
        if f'def {method}(' in content:
            print(f"⚠️  {method} - JE prítomná (nečakané)")
            no_grid = False
        else:
            print(f"✅ {method} - chýba (očakávané)")

    return no_grid


def show_file_info():
    """Zobrazí info o obnovenom súbore."""
    print(f"\n{'=' * 80}")
    print("5. INFO O OBNOVENOM SÚBORE")
    print(f"{'=' * 80}")

    size = WIDGET_FILE.stat().st_size

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Veľkosť: {size:,} bytes")
    print(f"Riadkov: {len(lines)}")

    # Posledných 5 riadkov
    print("\nPosledných 5 riadkov:")
    for line in lines[-5:]:
        print(f"  {line.rstrip()}")


def main():
    """Hlavná funkcia restore."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - RESTORE invoice_list_widget.py ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Záloha
    if not backup_current():
        print("\n❌ STOP: Záloha zlyhala")
        return

    # 2. Restore
    if not restore_from_commit():
        print("\n❌ STOP: Restore zlyhal")
        return

    # 3. Verifikácia metód
    if not verify_methods():
        print("\n❌ VAROVANIE: Niektoré metódy chýbajú!")
    else:
        print("\n✅ Všetky kľúčové metódy prítomné")

    # 4. Kontrola grid settings
    if check_no_grid_settings():
        print("\n✅ Grid settings správne chýbajú")
    else:
        print("\n⚠️  VAROVANIE: Grid settings sú stále prítomné")

    # 5. Info
    show_file_info()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print(f"✅ Súbor obnovený z commitu {GOOD_COMMIT}")
    print(f"✅ Záloha: invoice_list_widget.py.broken")
    print("\n⏭️  ĎALŠÍ KROK: Spustiť aplikáciu a otestovať:")
    print("   python main.py")
    print("\nPo teste môžeme pridať grid settings správnym scriptom.")


if __name__ == "__main__":
    main()