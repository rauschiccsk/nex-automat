"""02: Check database content vs repository."""
import sqlite3
import json
from pathlib import Path

DB_PATH = Path.home() / ".nex-automat" / "settings.db"

print(f"Database: {DB_PATH}")
print("=" * 60)

# Direct DB query
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    SELECT id, window_name, grid_name, settings, updated_at 
    FROM grid_settings 
    WHERE window_name='supplier_invoice_staging_main' 
    AND grid_name='invoice_list'
""")
rows = cursor.fetchall()
conn.close()

print(f"Found {len(rows)} row(s) in database:\n")
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Window: {row[1]}")
    print(f"Grid: {row[2]}")
    print(f"Updated: {row[4]}")
    settings = json.loads(row[3])
    print(f"Column widths: {settings.get('column_widths')}")
    print()

print("=" * 60)
print("Via SettingsRepository:")
print()

from shared_pyside6.database import SettingsRepository
repo = SettingsRepository()
loaded = repo.load_grid_settings('supplier_invoice_staging_main', 'invoice_list', 'default')
if loaded:
    print(f"Column widths: {loaded.get('column_widths')}")
else:
    print("No settings loaded!")