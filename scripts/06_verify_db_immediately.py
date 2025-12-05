"""
Overiť čo je v DB ihneď teraz
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")


def main():
    print("=" * 80)
    print("AKTUÁLNY STAV V DATABÁZE")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Načítaj sie_main_window záznam
    cursor.execute("""
        SELECT user_id, window_name, x, y, width, height, window_state, updated_at
        FROM window_settings
        WHERE window_name = 'sie_main_window'
        ORDER BY updated_at DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if not row:
        print("❌ Žiadny záznam pre sie_main_window")
        conn.close()
        return

    user_id, win_name, x, y, width, height, state, updated = row

    print(f"\n✅ Záznam nájdený:")
    print(f"   User ID: {user_id}")
    print(f"   Window: {win_name}")
    print(f"   Position: x={x}, y={y}")
    print(f"   Size: {width}x{height}")
    print(f"   State: {state} {'🔴 (SHOULD BE 2!)' if state == 0 else '✅ (CORRECT)'}")
    print(f"   Updated: {updated}")

    # Ukáž všetky stĺpce
    cursor.execute("PRAGMA table_info(window_settings)")
    columns = cursor.fetchall()

    print("\n" + "=" * 80)
    print("DATABÁZA SCHEMA:")
    print("=" * 80)
    for col in columns:
        print(f"  {col[1]} ({col[2]})")

    conn.close()

    print("\n" + "=" * 80)
    print("DIAGNÓZA:")
    print("=" * 80)

    if state == 0:
        print("🔴 POTVRDENÉ: window_state=0 v databáze AJ KEĎ log hovorí state=2!")
        print("\nProblém je v INSERT OR REPLACE logike.")
        print("\nMožné príčiny:")
        print("  1. UNIQUE constraint spôsobuje že sa UPDATE nevykoná správne")
        print("  2. Chyba v poradí parametrov VALUES tuple")
        print("  3. INSERT OR REPLACE negeneruje UPDATE pre window_state stĺpec")
        print("\nRIEŠENIE: Zmeniť INSERT OR REPLACE na DELETE + INSERT")
    else:
        print("✅ window_state je správne = 2")
        print("Problém musí byť niekde inde v load chain")

    print("=" * 80)


if __name__ == '__main__':
    main()