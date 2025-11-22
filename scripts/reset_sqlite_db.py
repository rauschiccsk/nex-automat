"""
Reset SQLite database for testing
"""

from pathlib import Path
import shutil

project_root = Path(__file__).parent.parent
sqlite_db = project_root / "apps" / "supplier-invoice-loader" / "config" / "invoices.db"

print("=" * 80)
print("RESET SQLITE DATABASE")
print("=" * 80)
print()

if not sqlite_db.exists():
    print(f"SQLite database not found: {sqlite_db}")
    print("[OK] No database to reset")
else:
    # Create backup
    backup_db = sqlite_db.with_suffix('.db.backup')

    print(f"Database: {sqlite_db}")
    print(f"Size: {sqlite_db.stat().st_size / 1024:.1f} KB")
    print()

    # Backup
    print(f"Creating backup: {backup_db.name}")
    shutil.copy2(sqlite_db, backup_db)
    print("[OK] Backup created")
    print()

    # Delete
    print("Deleting database...")
    sqlite_db.unlink()
    print("[OK] Database deleted")
    print()

    print("The application will create a new empty database on next request.")

print()
print("=" * 80)
print("Next steps:")
print("1. Run E2E test: python scripts\\test_e2e_workflow.py")
print("=" * 80)