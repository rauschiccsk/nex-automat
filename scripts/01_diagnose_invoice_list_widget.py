"""
NEX Automat v2.1 - Diagnostika invoice_list_widget.py
Zistí aktuálny stav súboru a chýbajúce metódy.
"""

import os
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


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


def check_file_exists():
    """Skontroluje existenciu súboru."""
    print(f"\n{'=' * 80}")
    print("1. EXISTENCIA SÚBORU")
    print(f"{'=' * 80}")

    if WIDGET_FILE.exists():
        size = WIDGET_FILE.stat().st_size
        print(f"✅ Súbor existuje: {WIDGET_FILE}")
        print(f"   Veľkosť: {size:,} bytes")
        return True
    else:
        print(f"❌ Súbor neexistuje: {WIDGET_FILE}")
        return False


def check_git_status():
    """Zistí git status súboru."""
    print(f"\n{'=' * 80}")
    print("2. GIT STATUS")
    print(f"{'=' * 80}")

    rel_path = WIDGET_FILE.relative_to(BASE_DIR)
    stdout, stderr, code = run_command(f'git status "{rel_path}"')

    if code == 0:
        print(stdout)
    else:
        print(f"❌ Git error: {stderr}")


def check_missing_methods():
    """Skontroluje prítomnosť kritických metód."""
    print(f"\n{'=' * 80}")
    print("3. CHÝBAJÚCE METÓDY")
    print(f"{'=' * 80}")

    required_methods = [
        '_on_selection_changed',
        '_on_double_clicked',
        '_load_grid_settings',
        '_save_grid_settings',
        '_on_column_resized',
        '_on_column_moved'
    ]

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\nStav metód:")
    print(f"{'Metóda':<30} {'Status'}")
    print("-" * 50)

    missing = []
    for method in required_methods:
        if f'def {method}(' in content:
            print(f"{method:<30} ✅ Prítomná")
        else:
            print(f"{method:<30} ❌ CHÝBA")
            missing.append(method)

    return missing


def check_imports():
    """Skontroluje importy pre grid settings."""
    print(f"\n{'=' * 80}")
    print("4. IMPORTY PRE GRID SETTINGS")
    print(f"{'=' * 80}")

    required_imports = [
        'from utils.constants import',
        'from utils.grid_settings import'
    ]

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\nStav importov:")
    for imp in required_imports:
        if imp in content:
            print(f"✅ {imp}")
        else:
            print(f"❌ {imp} - CHÝBA")


def show_git_diff():
    """Zobrazí rozdiel oproti poslednej verzii."""
    print(f"\n{'=' * 80}")
    print("5. GIT DIFF (posledných 30 riadkov)")
    print(f"{'=' * 80}")

    rel_path = WIDGET_FILE.relative_to(BASE_DIR)
    stdout, stderr, code = run_command(f'git diff HEAD "{rel_path}"')

    if stdout:
        lines = stdout.split('\n')
        # Zobraz posledných 30 riadkov
        for line in lines[-30:]:
            print(line)
    else:
        print("✅ Žiadne zmeny oproti HEAD")


def get_last_commit_hash():
    """Získa hash posledného commitu kde súbor fungoval."""
    print(f"\n{'=' * 80}")
    print("6. POSLEDNÉ COMMITY SÚBORU")
    print(f"{'=' * 80}")

    rel_path = WIDGET_FILE.relative_to(BASE_DIR)
    stdout, stderr, code = run_command(
        f'git log --oneline -5 "{rel_path}"'
    )

    if stdout:
        print("Posledných 5 commitov:")
        print(stdout)
    else:
        print("❌ Žiadne commity")


def main():
    """Hlavná diagnostická funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - DIAGNOSTIKA invoice_list_widget.py ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Existencia
    if not check_file_exists():
        print("\n❌ KRITICKÁ CHYBA: Súbor neexistuje!")
        return

    # 2. Git status
    check_git_status()

    # 3. Chýbajúce metódy
    missing = check_missing_methods()

    # 4. Importy
    check_imports()

    # 5. Git diff
    show_git_diff()

    # 6. Commity
    get_last_commit_hash()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")

    if missing:
        print(f"\n❌ PROBLÉM: Chýba {len(missing)} metód:")
        for m in missing:
            print(f"   - {m}")
        print("\n✅ RIEŠENIE: Git restore + komplexný integračný script")
    else:
        print("\n✅ Všetky metódy prítomné - problém môže byť inde")


if __name__ == "__main__":
    main()