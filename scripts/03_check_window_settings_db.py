#!/usr/bin/env python3
"""
Check Window Settings Database
===============================

Location: scripts/03_check_window_settings_db.py

Zobrazí obsah window_settings databázy.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")


def check_database():
    """Skontroluje a zobrazí obsah databázy."""

    print("=" * 80)
    print("CHECK WINDOW SETTINGS DATABASE")
    print("=" * 80)

    # 1. Existuje databáza?
    print(f"\n1. Databáza: {DB_PATH}")

    if not DB_PATH.exists():
        print("❌ Databáza NEEXISTUJE")
        print("\nDôvody:")
        print("  • Aplikácia ešte nebola spustená")
        print("  • Databáza bola vymazaná")
        print("  • Chyba pri vytváraní databázy")
        return False

    print(f"✅ Databáza existuje")
    size = DB_PATH.stat().st_size
    print(f"   Veľkosť: {size:,} bytes")

    # 2. Pripoj sa na databázu
    print(f"\n2. Čítam obsah...")

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Zisti štruktúru tabuľky
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='window_settings'")
        schema = cursor.fetchone()

        if not schema:
            print("❌ Tabuľka 'window_settings' NEEXISTUJE")
            conn.close()
            return False

        print(f"✅ Tabuľka 'window_settings' existuje")

        # Načítaj všetky záznamy
        cursor.execute("""
            SELECT id, user_id, window_name, x, y, width, height, updated_at
            FROM window_settings
            ORDER BY updated_at DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("\n⚠️  Tabuľka je PRÁZDNA - žiadne uložené nastavenia")
            print("\nDôvody:")
            print("  • Aplikácia bola spustená ale nebol uložený closeEvent")
            print("  • Chyba pri ukladaní (pozri logy)")
            print("  • Databáza bola vyčistená")
        else:
            print(f"\n✅ Nájdených {len(rows)} záznamov:")
            print("\n" + "-" * 80)

            for row in rows:
                id, user_id, window_name, x, y, width, height, updated_at = row
                print(f"ID:          {id}")
                print(f"User:        {user_id}")
                print(f"Window:      {window_name}")
                print(f"Position:    x={x}, y={y}")
                print(f"Size:        {width} x {height}")
                print(f"Updated:     {updated_at}")
                print("-" * 80)

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"❌ Chyba pri čítaní databázy: {e}")
        return False

    finally:
        print("\n" + "=" * 80)


if __name__ == "__main__":
    check_database()