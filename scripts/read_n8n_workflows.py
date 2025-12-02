"""
Read n8n workflows from SQLite database
"""
import sqlite3
import sys
from pathlib import Path


def read_n8n_workflows(db_path):
    """Read workflows from n8n database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]

        print("=" * 80)
        print("n8n DATABASE TABLES:")
        print("=" * 80)
        for table in tables:
            print(f"  - {table}")

        # Find workflow table
        workflow_table = None
        if 'workflow_entity' in tables:
            workflow_table = 'workflow_entity'
        elif 'workflows' in tables:
            workflow_table = 'workflows'

        if not workflow_table:
            print("\n❌ Workflow tabuľka nenájdená!")
            print(f"   Dostupné tabuľky: {', '.join(tables)}")
            return

        # Read workflows
        cursor.execute(f"SELECT id, name, active, createdAt, updatedAt FROM {workflow_table}")
        workflows = cursor.fetchall()

        print(f"\n{'=' * 80}")
        print(f"n8n WORKFLOWS ({len(workflows)} total):")
        print("=" * 80)

        if not workflows:
            print("\n❌ Žiadne workflows v databáze!")
        else:
            for wf_id, name, active, created, updated in workflows:
                status = "🟢 ACTIVE" if active else "🔴 INACTIVE"
                print(f"\n{status} {name}")
                print(f"   ID: {wf_id}")
                print(f"   Created: {created}")
                print(f"   Updated: {updated}")

        # Read credentials count
        cred_table = None
        if 'credentials_entity' in tables:
            cred_table = 'credentials_entity'
        elif 'credentials' in tables:
            cred_table = 'credentials'

        if cred_table:
            cursor.execute(f"SELECT COUNT(*) FROM {cred_table}")
            cred_count = cursor.fetchone()[0]
            print(f"\n{'=' * 80}")
            print(f"CREDENTIALS: {cred_count} total")

            cursor.execute(f"SELECT id, name, type FROM {cred_table}")
            creds = cursor.fetchall()
            for cred_id, name, cred_type in creds:
                print(f"  - {name} ({cred_type})")

        print("\n" + "=" * 80)

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Chyba pri čítaní databázy: {e}")
        sys.exit(1)


if __name__ == "__main__":
    db_path = Path(r"C:\Users\ZelenePC\.n8n\database.sqlite")

    if not db_path.exists():
        print(f"❌ Databáza nenájdená: {db_path}")
        sys.exit(1)

    print(f"📂 Databáza: {db_path}")
    print(f"📊 Veľkosť: {db_path.stat().st_size / 1024 / 1024:.1f} MB\n")
    read_n8n_workflows(db_path)