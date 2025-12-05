"""
DELETE neplatný window position záznam
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")


def main():
    print("=" * 80)
    print("DELETE WINDOW POSITION")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ukáž aktuálny záznam
    cursor.execute("SELECT * FROM window_settings WHERE window_name = 'sie_main_window'")
    row = cursor.fetchone()

    if row:
        print(f"\n✅ Aktuálny záznam:")
        print(f"   Position: x={row[3]}, y={row[4]}")
        print(f"   Size: {row[5]}x{row[6]}")
        print(f"   State: {row[8]}")
    else:
        print("\n❌ Žiadny záznam nenájdený")
        conn.close()
        return

    # DELETE
    cursor.execute("DELETE FROM window_settings WHERE window_name = 'sie_main_window'")
    conn.commit()

    print(f"\n✅ Záznam DELETED")

    # Verify
    cursor.execute("SELECT * FROM window_settings WHERE window_name = 'sie_main_window'")
    row = cursor.fetchone()

    if row is None:
        print("✅ Verify: Záznam úspešne odstránený")
    else:
        print("❌ Verify: Záznam stále existuje!")

    conn.close()

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("1. Spusti aplikáciu - vytvorí sa nový záznam s default pozíciou")
    print("2. Maximalizuj okno")
    print("3. Zavri aplikáciu")
    print("4. Skontroluj LOG pre DEBUG výpisy o uložení window_state=2")
    print("=" * 80)


if __name__ == '__main__':
    main()