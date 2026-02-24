#!/usr/bin/env python
"""Check what tables exist in database"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database.postgres_client import PostgresClient
from utils.config import Config

config_obj = Config(Path("config/config.yaml"))

db_config = {
    "host": config_obj.get("database.postgres.host"),
    "port": int(config_obj.get("database.postgres.port")),
    "database": config_obj.get("database.postgres.database"),
    "user": config_obj.get("database.postgres.user"),
    "password": os.getenv(
        "POSTGRES_PASSWORD", config_obj.get("database.postgres.password", "")
    ),
}

print(f"Checking database: {db_config['database']}")
print("=" * 80)

db = PostgresClient(db_config)

with db.get_connection() as conn:
    cursor = conn.cursor()

    # List all tables
    cursor.execute("""
        SELECT table_schema, table_name 
        FROM information_schema.tables 
        WHERE table_type = 'BASE TABLE'
        ORDER BY table_schema, table_name
    """)

    tables = cursor.fetchall()

    print(f"\nFound {len(tables)} tables:\n")
    for schema, table in tables:
        print(f"  {schema}.{table}")

    cursor.close()

print("\n" + "=" * 80)
