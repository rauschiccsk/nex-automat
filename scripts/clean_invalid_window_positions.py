#!/usr/bin/env python3
"""
Clean Invalid Window Positions
===============================

Location: scripts/04_clean_invalid_window_positions.py

Vymaže nevalidné pozície okien z databázy.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")

# Validačné limity (rovnaké ako v window_settings.py)
MIN_X = -50
MIN_Y = 0
MIN_WIDTH = 400
MIN_HEIGHT = 300
MAX_WIDTH = 3840
MAX_HEIGHT = 2160


def clean_invalid_positions():
    """Vymaže nevalidné záznamy z databázy."""

    print("=" * 80)
    print("CLEAN INVALID WINDOW POSITIONS")
    print("=" * 80)

    print(f"\nValidačné pravidlá:")
    print(f"  X >= {MIN_X}")
    print(f"  Y >= {MIN_Y}")
    print(f"  Width: {MIN_WIDTH}-{MAX_WIDTH}")
    print(f"  Height: {MIN_HEIGHT}-{MAX_HEIGHT}")

    # 1. Pripoj sa na databázu
    print(f"\n1. Pripájam sa na databázu: {DB_PATH}")

    if not DB_PATH.exists():
        print("❌ Databáza neexistuje")
        return False

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # 2. Načítaj všetky záznamy
        print(f"\n2. Načítavam záznamy...")

        cursor.execute("""
            SELECT id, user_id, window_name, x, y, width, height
            FROM window_settings
        """)

        rows = cursor.fetchall()
        print(f"✅ Nájdených {len(rows)} záznamov")

        # 3. Identifikuj nevalidné
        print(f"\n3. Kontrolujem validitu...")

        invalid_ids = []

        for row in rows:
            id, user_id, window_name, x, y, width, height = row

            is_valid = True
            reasons = []

            if x < MIN_X:
                is_valid = False
                reasons.append(f"x={x} < {MIN_X}")

            if y < MIN_Y:
                is_valid = False
                reasons.append(f"y={y} < {MIN_Y}")

            if width < MIN_WIDTH or width > MAX_WIDTH:
                is_valid = False
                reasons.append(f"width={width} mimo {MIN_WIDTH}-{MAX_WIDTH}")

            if height < MIN_HEIGHT or height > MAX_HEIGHT:
                is_valid = False
                reasons.append(f"height={height} mimo {MIN_HEIGHT}-{MAX_HEIGHT}")

            if not is_valid:
                invalid_ids.append(id)
                print(f"\n  ❌ ID {id}: {window_name} ({user_id})")
                print(f"     Position: x={x}, y={y}")
                print(f"     Size: {width}x{height}")
                print(f"     Dôvody: {', '.join(reasons)}")

        if not invalid_ids:
            print("\n  ✅ Všetky záznamy sú VALIDNÉ")
            conn.close()
            return True

        # 4. Vymaž nevalidné záznamy
        print(f"\n4. Mažem {len(invalid_ids)} nevalidných záznamov...")

        placeholders = ','.join('?' * len(invalid_ids))
        cursor.execute(f"""
            DELETE FROM window_settings
            WHERE id IN ({placeholders})
        """, invalid_ids)

        conn.commit()
        deleted_count = cursor.rowcount

        print(f"✅ Vymazaných {deleted_count} záznamov")

        # 5. Zhrnutie
        cursor.execute("SELECT COUNT(*) FROM window_settings")
        remaining = cursor.fetchone()[0]

        conn.close()

        print("\n" + "=" * 80)
        print("✅ HOTOVO - Invalid Positions CLEANED")
        print("=" * 80)
        print(f"\nVýsledok:")
        print(f"  • Vymazaných: {deleted_count}")
        print(f"  • Zostalo: {remaining}")

        print("\n" + "=" * 80)
        print("ĎALŠÍ KROK:")
        print("=" * 80)
        print("1. Spusti aplikáciu - použije default pozíciu")
        print("2. Presuň okno a zmeň veľkosť")
        print("3. Zatvor aplikáciu (ESC)")
        print("4. Spusti znovu - malo by zapamätať pozíciu")
        print("5. Overiť: python scripts\\03_check_window_settings_db.py")
        print("=" * 80)

        return True

    except sqlite3.Error as e:
        print(f"\n❌ Chyba databázy: {e}")
        return False


if __name__ == "__main__":
    success = clean_invalid_positions()
    exit(0 if success else 1)