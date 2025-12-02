"""
Read n8n user email from SQLite database
"""
import sqlite3
import sys
from pathlib import Path


def read_n8n_email(db_path):
    """Read email from n8n database"""
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Read user email
        cursor.execute("SELECT email, firstName, lastName FROM user")
        users = cursor.fetchall()

        if not users:
            print("❌ Žiadny používateľ nenájdený v databáze")
            return

        print("=" * 60)
        print("n8n POUŽÍVATELIA:")
        print("=" * 60)

        for i, (email, first_name, last_name) in enumerate(users, 1):
            name = f"{first_name or ''} {last_name or ''}".strip()
            print(f"\n{i}. Email: {email}")
            if name:
                print(f"   Meno:  {name}")

        print("\n" + "=" * 60)
        print(f"\nCelkom používateľov: {len(users)}")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Chyba pri čítaní databázy: {e}")
        sys.exit(1)


if __name__ == "__main__":
    db_path = Path(r"C:\Users\ZelenePC\.n8n\database.sqlite")

    if not db_path.exists():
        print(f"❌ Databáza nenájdená: {db_path}")
        sys.exit(1)

    print(f"📂 Databáza: {db_path}\n")
    read_n8n_email(db_path)