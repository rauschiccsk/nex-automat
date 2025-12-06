#!/usr/bin/env python3
"""
Script 05: Check window_settings.db content
Overí čo je skutočne uložené v databáze
"""

import sqlite3
from pathlib import Path
from datetime import datetime


def check_database():
    """Zobrazí obsah window_settings tabuľky"""

    db_path = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    print("=" * 80)
    print(f"DATABASE: {db_path}")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Zisti štruktúru tabuľky
    cursor.execute("PRAGMA table_info(window_settings)")
    columns = cursor.fetchall()

    print("\n📋 Table structure:")
    for col in columns:
        print(f"  {col[1]:20s} {col[2]:10s}")

    # Načítaj všetky záznamy
    cursor.execute("SELECT * FROM window_settings ORDER BY updated_at DESC")
    rows = cursor.fetchall()

    print(f"\n📊 Total records: {len(rows)}")
    print("=" * 80)

    if rows:
        # Hlavička
        col_names = [col[1] for col in columns]
        header = " | ".join(f"{name:15s}" for name in col_names)
        print(header)
        print("-" * len(header))

        # Dáta
        for row in rows:
            row_str = " | ".join(f"{str(val):15s}" for val in row)
            print(row_str)
    else:
        print("⚠️  No records found!")

    # Špecificky pre sie_main_window
    print("\n" + "=" * 80)
    print("RECORD FOR: sie_main_window")
    print("=" * 80)

    cursor.execute("""
        SELECT user_id, window_name, x, y, width, height, window_state, updated_at
        FROM window_settings 
        WHERE window_name = 'sie_main_window'
        ORDER BY updated_at DESC
        LIMIT 1
    """)

    record = cursor.fetchone()
    if record:
        print(f"User ID:       {record[0]}")
        print(f"Window Name:   {record[1]}")
        print(f"Position:      x={record[2]}, y={record[3]}")
        print(f"Size:          width={record[4]}, height={record[5]}")
        print(f"State:         {record[6]} (0=Normal, 2=Maximized)")
        print(f"Updated:       {record[7]}")

        # Overenie
        if record[4] == 1400 and record[5] == 900:
            print("\n❌ PROBLEM: Database contains DEFAULT size (1400x900)!")
            print("   Expected: Your resized dimensions (e.g. 1179x344)")
        else:
            print(f"\n✅ Database contains CUSTOM size: {record[4]}x{record[5]}")
    else:
        print("❌ No record found for sie_main_window!")

    conn.close()


if __name__ == "__main__":
    check_database()