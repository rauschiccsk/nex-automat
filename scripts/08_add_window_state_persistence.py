#!/usr/bin/env python3
"""
Add Window State Persistence
=============================
Session: 2025-12-05
Location: scripts/08_add_window_state_persistence.py

Pridáva stĺpec window_state do databázy pre ukladanie maximalizovaného stavu.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")


def add_window_state_column():
    """Pridá stĺpec window_state do window_settings tabuľky"""

    print("=" * 80)
    print("ADD WINDOW STATE PERSISTENCE")
    print("=" * 80)

    # 1. Kontrola DB
    print(f"\n1. Kontrolujem databázu: {DB_PATH}")
    if not DB_PATH.exists():
        print("   ❌ Databáza neexistuje")
        return False

    print("   ✅ Databáza existuje")

    # 2. Pripojenie
    print("\n2. Pripájam sa...")
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        print("   ✅ Pripojené")
    except sqlite3.Error as e:
        print(f"   ❌ Chyba: {e}")
        return False

    # 3. Kontrola či stĺpec už existuje
    print("\n3. Kontrolujem či stĺpec window_state existuje...")
    cursor.execute("PRAGMA table_info(window_settings)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'window_state' in columns:
        print("   ⚠️  Stĺpec window_state už existuje")
        conn.close()
        return True

    print("   ℹ️  Stĺpec neexistuje, pridávam...")

    # 4. Pridaj stĺpec
    try:
        cursor.execute("""
            ALTER TABLE window_settings
            ADD COLUMN window_state INTEGER DEFAULT 0
        """)
        conn.commit()
        print("   ✅ Stĺpec window_state pridaný")
    except sqlite3.Error as e:
        print(f"   ❌ Chyba: {e}")
        conn.close()
        return False

    # 5. Overenie
    print("\n4. Overujem štruktúru tabuľky...")
    cursor.execute("PRAGMA table_info(window_settings)")
    columns = cursor.fetchall()

    print("   Stĺpce v tabuľke:")
    for col in columns:
        print(f"     • {col[1]} ({col[2]})")

    conn.close()

    # 6. Zhrnutie
    print("\n" + "=" * 80)
    print("✅ HOTOVO - Window State Column Added")
    print("=" * 80)
    print("\nPridaný stĺpec:")
    print("  • window_state INTEGER DEFAULT 0")
    print("  • 0 = normálne, 2 = maximalizované")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("Teraz treba upraviť window_settings.py a main_window.py")
    print("aby ukladali a načítavali windowState")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = add_window_state_column()
    exit(0 if success else 1)