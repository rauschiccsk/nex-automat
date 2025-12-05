#!/usr/bin/env python3
"""
Fix Window Position Validation - Window Settings
=================================================

Location: scripts/02_fix_window_position_validation.py

Pridá validáciu pozície okna aby sa predišlo posunu mimo obrazovky.

Problém:
- load_window_settings() môže vrátiť záporné hodnoty pre x, y
- Okno sa posunie mimo obrazovky (hlavička nie je viditeľná)

Riešenie:
- Pridať validáciu do load_window_settings()
- Ak je pozícia nevalidná, vrátiť None (použije sa default)
"""

from pathlib import Path
import sys

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Cesta k súboru
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "utils" / "window_settings.py"


def fix_window_position_validation():
    """Pridá validáciu pozície okna."""

    print("=" * 80)
    print("FIX WINDOW POSITION VALIDATION")
    print("=" * 80)

    # 1. Načítaj súbor
    print(f"\n1. Načítavam: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"✅ Súbor načítaný ({len(content)} znakov)")

    # 2. Vytvor backup
    backup_file = TARGET_FILE.with_suffix('.py.backup_validation')
    print(f"\n2. Vytváram backup: {backup_file.name}")

    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Backup vytvorený")

    # 3. Pridaj validáciu
    print(f"\n3. Pridávam validáciu pozície...")

    # Nájdi koniec load_window_settings funkcie (pred return)
    old_code = """        if row:
            return {
                'x': row[0],
                'y': row[1],
                'width': row[2],
                'height': row[3]
            }
        return None"""

    new_code = """        if row:
            x, y, width, height = row[0], row[1], row[2], row[3]

            # Validácia pozície okna - musí byť viditeľné na obrazovke
            MIN_X = -50  # Povoliť čiastočne mimo obrazovky (pre multi-monitor)
            MIN_Y = 0    # Y musí byť >= 0 (hlavička musí byť viditeľná)
            MIN_WIDTH = 400
            MIN_HEIGHT = 300
            MAX_WIDTH = 3840  # 4K rozlíšenie
            MAX_HEIGHT = 2160

            # Kontrola hraníc
            if x < MIN_X or y < MIN_Y:
                print(f"⚠️  Invalid position: x={x}, y={y} (outside screen bounds)")
                return None

            if width < MIN_WIDTH or width > MAX_WIDTH:
                print(f"⚠️  Invalid width: {width} (must be {MIN_WIDTH}-{MAX_WIDTH})")
                return None

            if height < MIN_HEIGHT or height > MAX_HEIGHT:
                print(f"⚠️  Invalid height: {height} (must be {MIN_HEIGHT}-{MAX_HEIGHT})")
                return None

            return {
                'x': x,
                'y': y,
                'width': width,
                'height': height
            }
        return None"""

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("  ✅ Validácia pridaná")
    else:
        print("  ❌ Pattern nenájdený - možno už je opravené?")
        return False

    # 4. Ulož opravený súbor
    print(f"\n4. Ukladám opravený súbor...")

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Súbor uložený: {TARGET_FILE}")

    # 5. Zhrnutie
    print("\n" + "=" * 80)
    print("✅ HOTOVO - Window Position Validation ADDED")
    print("=" * 80)
    print(f"\nValidačné pravidlá:")
    print(f"  • X >= -50 (povoliť čiastočne mimo pre multi-monitor)")
    print(f"  • Y >= 0 (hlavička musí byť viditeľná)")
    print(f"  • Width: 400-3840 px")
    print(f"  • Height: 300-2160 px")
    print(f"  • Ak validácia zlyhá → použije sa default pozícia")

    print(f"\nBackup: {backup_file}")
    print(f"Fixed:  {TARGET_FILE}")

    print("\n" + "=" * 80)
    print("RIEŠENIE AKTUÁLNEHO PROBLÉMU:")
    print("=" * 80)
    print("Option 1 - Reset pozície okna v databáze:")
    print('  sqlite3 "C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\window_settings.db"')
    print('  DELETE FROM window_settings WHERE window_name = "sie_main_window";')
    print('  .quit')
    print("")
    print("Option 2 - Vymazať celú databázu (reset všetkých okien):")
    print('  del "C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\window_settings.db"')
    print("")
    print("Po resete: Spustiť aplikáciu znovu - použije default pozíciu.")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_window_position_validation()
    exit(0 if success else 1)