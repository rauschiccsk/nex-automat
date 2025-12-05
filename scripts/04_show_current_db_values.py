"""
Zobrazí aktuálne hodnoty v DB a skutočné rozmery monitoru
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")


def main():
    print("=" * 80)
    print("AKTUÁLNE HODNOTY V DATABÁZE")
    print("=" * 80)

    if not DB_PATH.exists():
        print(f"❌ Databáza neexistuje: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Načítaj všetky záznamy
    cursor.execute("""
        SELECT user_id, window_name, x, y, width, height, window_state, updated_at
        FROM window_settings
        ORDER BY updated_at DESC
    """)

    rows = cursor.fetchall()

    if not rows:
        print("❌ Žiadne záznamy v databáze")
        conn.close()
        return

    print(f"\n✅ Nájdených {len(rows)} záznamov:\n")

    for row in rows:
        user_id, win_name, x, y, width, height, state, updated = row
        print(f"Window: {win_name}")
        print(f"  User ID: {user_id}")
        print(f"  Position: x={x}, y={y}")
        print(f"  Size: {width}x{height}")
        print(f"  State: {state} {'(MAXIMIZED)' if state == 2 else '(NORMAL)'}")
        print(f"  Updated: {updated}")
        print()

    conn.close()

    # Skús zistiť rozmery monitoru pomocou PyQt5
    print("=" * 80)
    print("ROZMERY MONITOROV (PyQt5)")
    print("=" * 80)

    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        import sys

        app = QApplication(sys.argv)
        desktop = app.desktop()

        screen_count = desktop.screenCount()
        print(f"\n✅ Počet obrazoviek: {screen_count}\n")

        for i in range(screen_count):
            screen_geom = desktop.screenGeometry(i)
            print(f"Monitor {i}:")
            print(f"  Position: x={screen_geom.x()}, y={screen_geom.y()}")
            print(f"  Size: {screen_geom.width()}x{screen_geom.height()}")
            print(f"  Right edge: {screen_geom.x() + screen_geom.width()}")
            print(f"  Bottom edge: {screen_geom.y() + screen_geom.height()}")
            print()

    except Exception as e:
        print(f"⚠️  Nepodarilo sa získať info o monitoroch: {e}")

    print("=" * 80)
    print("ANALÝZA")
    print("=" * 80)
    print("\nAk je Y hodnota záporná alebo veľmi blízka 0,")
    print("hlavička okna môže byť mimo obrazovky.")
    print("\nODPORÚČANIE:")
    print("DELETE záznam z DB a nechaj aplikáciu vytvoriť nový s default pozíciou.")
    print("=" * 80)


if __name__ == '__main__':
    main()