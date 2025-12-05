r"""
Script 24: Diagnostika grid_settings.db - čo je uložené v databáze.
"""

from pathlib import Path
import sqlite3

DB_PATH = "C:/NEX/YEARACT/SYSTEM/SQLITE/grid_settings.db"


def main():
    """Diagnostika grid_settings databázy."""
    print("=" * 70)
    print("DIAGNOSTIKA: grid_settings.db")
    print("=" * 70)

    # 1. Skontroluj či databáza existuje
    if not Path(DB_PATH).exists():
        print(f"\n❌ Databáza NEEXISTUJE: {DB_PATH}")
        print("\nPríčina:")
        print("  - Funkcia init_grid_settings_db() sa nevolá")
        print("  - Alebo cesta je nesprávna")
        return

    print(f"\n✅ Databáza existuje: {DB_PATH}")
    print(f"   Veľkosť: {Path(DB_PATH).stat().st_size} bytes")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 2. Skontroluj tabuľky
        print("\n" + "=" * 70)
        print("TABUĽKY:")
        print("=" * 70)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if not tables:
            print("❌ Žiadne tabuľky - databáza je prázdna!")
            return

        for table in tables:
            print(f"  ✅ {table[0]}")

        # 3. Obsah grid_column_settings
        print("\n" + "=" * 70)
        print("OBSAH: grid_column_settings")
        print("=" * 70)

        cursor.execute("SELECT COUNT(*) FROM grid_column_settings")
        count = cursor.fetchone()[0]

        if count == 0:
            print("❌ Tabuľka je PRÁZDNA - žiadne záznamy")
            print("\nPríčina:")
            print("  - Funkcia _save_grid_settings() sa nevolá")
            print("  - Alebo signály sectionResized/sectionMoved nie sú pripojené")
        else:
            print(f"✅ Nájdené záznamy: {count}\n")

            cursor.execute("""
                SELECT user_id, window_name, grid_name, column_name, width, visual_index, visible
                FROM grid_column_settings
                ORDER BY window_name, grid_name, visual_index
            """)
            rows = cursor.fetchall()

            for row in rows:
                print(f"  User: {row[0]}")
                print(f"    Window: {row[1]}, Grid: {row[2]}")
                print(f"    Column: {row[3]}")
                print(f"    Width: {row[4]}, Visual: {row[5]}, Visible: {row[6]}")
                print()

        # 4. Obsah grid_settings
        print("=" * 70)
        print("OBSAH: grid_settings")
        print("=" * 70)

        cursor.execute("SELECT COUNT(*) FROM grid_settings")
        count = cursor.fetchone()[0]

        if count == 0:
            print("❌ Tabuľka je PRÁZDNA - žiadne záznamy")
        else:
            print(f"✅ Nájdené záznamy: {count}\n")

            cursor.execute("""
                SELECT user_id, window_name, grid_name, active_column_index
                FROM grid_settings
            """)
            rows = cursor.fetchall()

            for row in rows:
                print(f"  User: {row[0]}")
                print(f"    Window: {row[1]}, Grid: {row[2]}")
                print(f"    Active column: {row[3]}")
                print()

        conn.close()

        # Záver
        print("=" * 70)
        print("ZÁVER:")
        print("=" * 70)
        print("\nAk sú tabuľky prázdne:")
        print("  1. Signály sectionResized/sectionMoved nie sú pripojené")
        print("  2. Alebo _save_grid_settings() sa nevolá")
        print("\nAk tabuľky obsahujú dáta ale grid sa nenačítava:")
        print("  1. _load_grid_settings() sa nevolá v __init__")
        print("  2. Alebo aplikovanie nastavení nefunguje správne")

    except sqlite3.Error as e:
        print(f"❌ Chyba pri čítaní databázy: {e}")


if __name__ == "__main__":
    main()