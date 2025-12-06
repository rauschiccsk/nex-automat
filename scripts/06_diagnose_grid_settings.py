"""
Diagnose: Kontrola grid_settings databázy
Location: C:\Development\nex-automat\scripts\06_diagnose_grid_settings.py
"""
from pathlib import Path
import sqlite3

DB_PATH = Path("C:/NEX/YEARACT/SYSTEM/SQLITE/grid_settings.db")


def diagnose():
    """Diagnostika grid settings databázy"""

    print("=" * 80)
    print("DIAGNOSTIKA: grid_settings.db")
    print("=" * 80)

    # Check DB exists
    print(f"\nDatabáza: {DB_PATH}")

    if not DB_PATH.exists():
        print("❌ Databáza neexistuje!")
        print("\nPríčina: init_grid_settings_db() nebola zavolaná alebo zlyhala")
        return

    print("✓ Databáza existuje")
    print(f"  Veľkosť: {DB_PATH.stat().st_size:,} bytes")

    # Connect and check tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # List tables
    print("\n" + "=" * 80)
    print("TABUĽKY")
    print("=" * 80)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        print(f"\n✓ {table[0]}")

        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  Počet záznamov: {count}")

        # Show schema
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print("  Stĺpce:")
        for col in columns:
            print(f"    - {col[1]} ({col[2]})")

    # Check grid_column_settings data
    print("\n" + "=" * 80)
    print("GRID_COLUMN_SETTINGS - Posledných 10 záznamov")
    print("=" * 80)

    cursor.execute("""
        SELECT user_id, window_name, grid_name, column_name, width, visual_index, visible, updated_at
        FROM grid_column_settings
        ORDER BY updated_at DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    if not rows:
        print("\n❌ ŽIADNE ZÁZNAMY!")
        print("\nPríčina: save_column_settings() nebola zavolaná alebo zlyhala")
    else:
        for row in rows:
            print(f"\n  User: {row[0]}")
            print(f"  Window: {row[1]}")
            print(f"  Grid: {row[2]}")
            print(f"  Column: {row[3]} | Width: {row[4]} | Index: {row[5]} | Visible: {row[6]}")
            print(f"  Updated: {row[7]}")

    # Check grid_settings data
    print("\n" + "=" * 80)
    print("GRID_SETTINGS - Všetky záznamy")
    print("=" * 80)

    cursor.execute("""
        SELECT user_id, window_name, grid_name, active_column_index, updated_at
        FROM grid_settings
        ORDER BY updated_at DESC
    """)

    rows = cursor.fetchall()

    if not rows:
        print("\n❌ ŽIADNE ZÁZNAMY!")
        print("\nPríčina: save_grid_settings() nebola zavolaná alebo zlyhala")
    else:
        for row in rows:
            print(f"\n  User: {row[0]}")
            print(f"  Window: {row[1]}")
            print(f"  Grid: {row[2]}")
            print(f"  Active Column: {row[3]}")
            print(f"  Updated: {row[4]}")

    conn.close()

    print("\n" + "=" * 80)
    print("HOTOVO")
    print("=" * 80)


if __name__ == "__main__":
    diagnose()