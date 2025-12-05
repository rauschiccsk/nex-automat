r"""
Script 11: Diagnostika __init__ metódy a _load_geometry.
"""

from pathlib import Path
import sqlite3

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"
DB_PATH = "C:/NEX/YEARACT/SYSTEM/SQLITE/window_settings.db"


def main():
    """Skontroluje __init__ a databázu."""
    print(f"Analyzujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # 1. Skontroluj či existuje metóda _load_geometry
    print("\n" + "=" * 60)
    print("1. METÓDA _load_geometry:")
    print("=" * 60)

    has_load_geometry = False
    for i, line in enumerate(lines, 1):
        if 'def _load_geometry(self):' in line:
            print(f"✅ Metóda existuje na riadku {i}")
            has_load_geometry = True
            # Zobraz metódu
            for j in range(i - 1, min(i + 10, len(lines))):
                print(f"  {j + 1:3d}: {lines[j]}")
            break

    if not has_load_geometry:
        print("❌ Metóda _load_geometry() NEEXISTUJE!")

    # 2. Skontroluj či sa volá v __init__
    print("\n" + "=" * 60)
    print("2. VOLANIE v __init__:")
    print("=" * 60)

    in_init = False
    has_call = False
    init_start = 0

    for i, line in enumerate(lines, 1):
        if 'def __init__(self' in line:
            in_init = True
            init_start = i
            print(f"__init__ začína na riadku {i}")

        if in_init and 'self._load_geometry()' in line:
            print(f"✅ Volanie na riadku {i}: {line.strip()}")
            has_call = True

        # Koniec __init__ - ďalšia metóda
        if in_init and i > init_start and line.strip().startswith('def '):
            print(f"__init__ končí pred riadkom {i}")
            break

    if not has_call:
        print("❌ VOLANIE self._load_geometry() CHÝBA v __init__!")

    # 3. Skontroluj databázu
    print("\n" + "=" * 60)
    print("3. OBSAH DATABÁZY:")
    print("=" * 60)

    if Path(DB_PATH).exists():
        print(f"✅ Databáza existuje: {DB_PATH}")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM window_settings")
            rows = cursor.fetchall()

            if rows:
                print(f"\nNájdené záznamy: {len(rows)}")
                for row in rows:
                    print(f"  ID={row[0]}, user={row[1]}, window={row[2]}")
                    print(f"    x={row[3]}, y={row[4]}, width={row[5]}, height={row[6]}")
            else:
                print("⚠️  Databáza je prázdna - žiadne záznamy")

            conn.close()
        except Exception as e:
            print(f"❌ Chyba pri čítaní databázy: {e}")
    else:
        print(f"❌ Databáza neexistuje: {DB_PATH}")

    # Výsledok
    print("\n" + "=" * 60)
    print("DIAGNÓZA:")
    print("=" * 60)

    if has_load_geometry and has_call:
        print("✅ Metóda existuje a volá sa - mala by fungovať")
    elif not has_load_geometry:
        print("❌ CHÝBA metóda _load_geometry() - treba ju vytvoriť")
    elif not has_call:
        print("❌ CHÝBA volanie self._load_geometry() v __init__ - treba pridať")


if __name__ == "__main__":
    main()