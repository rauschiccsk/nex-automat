#!/usr/bin/env python3
"""
Script 41: Diagnose window settings in database
Check what's actually stored for sie_main_window
"""

import sqlite3
from pathlib import Path
import os


def main():
    """Check window settings in database"""
    print("=" * 60)
    print("Diagnosing window settings in database")
    print("=" * 60)

    # Find window_settings.db - CORRECTED PATH
    db_path = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")

    if not db_path.exists():
        print(f"\n❌ Database not found: {db_path}")
        return False

    print(f"\n📁 Database: {db_path}")

    # Connect and query
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get sie_main_window settings
    cursor.execute("""
        SELECT window_name, x, y, width, height, window_state, updated_at
        FROM window_settings
        WHERE window_name = 'sie_main_window'
    """)

    row = cursor.fetchone()

    if row:
        print("\n📋 Current settings for 'sie_main_window':")
        print(f"   Window name:  {row[0]}")
        print(f"   Position:     x={row[1]}, y={row[2]}")
        print(f"   Size:         w={row[3]}, h={row[4]}")
        print(f"   Window state: {row[5]}")
        print(f"   Updated:      {row[6]}")

        # Decode window_state
        state_map = {0: "Normal", 1: "Minimized", 2: "Maximized"}
        state_name = state_map.get(row[5], f"Unknown ({row[5]})")
        print(f"\n   State decoded: {state_name}")

        if row[5] == 2:
            print("   ✅ Window is marked as MAXIMIZED")
        else:
            print("   ⚠️  Window is NOT maximized")
    else:
        print("\n⚠️  No settings found for 'sie_main_window'")

    # Show all window settings
    cursor.execute("SELECT window_name, window_state FROM window_settings")
    all_rows = cursor.fetchall()

    if all_rows:
        print(f"\n📊 All window settings ({len(all_rows)} windows):")
        for window_name, state in all_rows:
            state_map = {0: "Normal", 1: "Minimized", 2: "Maximized"}
            state_name = state_map.get(state, f"Unknown ({state})")
            print(f"   {window_name:30s} → {state_name}")

    conn.close()

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()