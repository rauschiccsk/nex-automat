#!/usr/bin/env python3
"""
Diagnose Window Settings Database
==================================
Session: 2025-12-05
Location: scripts/03_diagnose_window_settings.py

Zobrazí kompletný stav window_settings databázy vrátane:
- Aký user_id používa aktuálny proces
- Všetky záznamy v databáze
- Validitu každej pozície
"""

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")

# Validačné limity
MIN_X = -3840  # Dual 4K monitor support
MIN_Y = 0
MIN_WIDTH = 400
MIN_HEIGHT = 300
MAX_WIDTH = 3840
MAX_HEIGHT = 2160


def get_current_user_id():
    """Vráti Windows username (rovnaké ako window_settings.py)"""
    return os.getenv('USERNAME', 'default_user')


def check_position_validity(x, y, width, height):
    """Skontroluje či je pozícia validná"""
    issues = []

    if x < MIN_X:
        issues.append(f"x={x} < {MIN_X}")
    if y < MIN_Y:
        issues.append(f"y={y} < {MIN_Y}")
    if width < MIN_WIDTH:
        issues.append(f"width={width} < {MIN_WIDTH}")
    if width > MAX_WIDTH:
        issues.append(f"width={width} > {MAX_WIDTH}")
    if height < MIN_HEIGHT:
        issues.append(f"height={height} < {MIN_HEIGHT}")
    if height > MAX_HEIGHT:
        issues.append(f"height={height} > {MAX_HEIGHT}")

    return len(issues) == 0, issues


def diagnose_database():
    """Diagnostika databázy"""

    print("=" * 80)
    print("WINDOW SETTINGS DATABASE DIAGNOSTICS")
    print("=" * 80)

    # 1. Aktuálny user
    current_user = get_current_user_id()
    print(f"\n1. Aktuálny user_id: '{current_user}'")
    print(f"   (Windows USERNAME: {os.getenv('USERNAME')})")

    # 2. Databáza existuje?
    print(f"\n2. Databáza: {DB_PATH}")
    if not DB_PATH.exists():
        print("   ❌ Databáza NEEXISTUJE")
        return

    print("   ✅ Databáza existuje")

    # 3. Pripojenie
    print("\n3. Pripájam sa na databázu...")
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        print("   ✅ Pripojené")
    except sqlite3.Error as e:
        print(f"   ❌ Chyba: {e}")
        return

    # 4. Načítaj všetky záznamy
    print("\n4. Načítavam záznamy...")
    try:
        cursor.execute("""
            SELECT id, user_id, window_name, x, y, width, height, window_state, updated_at
            FROM window_settings
            ORDER BY updated_at DESC
        """)
        rows = cursor.fetchall()
        print(f"   ✅ Nájdených {len(rows)} záznamov")
    except sqlite3.Error as e:
        print(f"   ❌ Chyba: {e}")
        conn.close()
        return

    # 5. Zobraziť všetky záznamy
    if not rows:
        print("\n5. Databáza je PRÁZDNA")
        conn.close()
        return

    print("\n5. Všetky záznamy v databáze:")
    print("   " + "-" * 76)

    valid_count = 0
    invalid_count = 0
    current_user_count = 0

    for row in rows:
        id, user_id, window_name, x, y, width, height, window_state, updated_at = row

        is_valid, issues = check_position_validity(x, y, width, height)
        status = "✅ VALID" if is_valid else "❌ INVALID"

        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1

        if user_id == current_user:
            current_user_count += 1
            user_marker = "← CURRENT USER"
        else:
            user_marker = ""

        print(f"\n   ID: {id} {status} {user_marker}")
        print(f"   User: {user_id}")
        print(f"   Window: {window_name}")
        print(f"   Position: ({x}, {y})")
        print(f"   Size: {width} x {height}")
        print(f"   Window State: {'Maximized' if window_state == 2 else 'Normal'} ({window_state})")
        print(f"   Window State: {'Maximized' if window_state == 2 else 'Normal'} ({window_state})")
        print(f"   Updated: {updated_at}")

        if not is_valid:
            print(f"   Issues: {', '.join(issues)}")

    print("\n   " + "-" * 76)

    # 6. Zhrnutie
    conn.close()

    print("\n6. Zhrnutie:")
    print(f"   • Celkom záznamov: {len(rows)}")
    print(f"   • Validné: {valid_count}")
    print(f"   • Nevalidné: {invalid_count}")
    print(f"   • Pre aktuálneho usera '{current_user}': {current_user_count}")

    print("\n" + "=" * 80)

    if invalid_count > 0:
        print("⚠️  AKCIA POTREBNÁ:")
        print("=" * 80)
        print("Databáza obsahuje nevalidné záznamy!")
        print("\nSpusti clean script:")
        print("  python scripts\\clean_invalid_window_positions.py")
    else:
        print("✅ VŠETKO V PORIADKU")
        print("=" * 80)
        print("Všetky záznamy sú validné.")

    print("=" * 80)


if __name__ == "__main__":
    diagnose_database()