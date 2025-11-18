#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Show table structure"""

import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config import Config
from database.postgres_client import PostgresClient

config_obj = Config(Path('config/config.yaml'))

db_config = {
    'host': config_obj.get('database.postgres.host'),
    'port': int(config_obj.get('database.postgres.port')),
    'database': config_obj.get('database.postgres.database'),
    'user': config_obj.get('database.postgres.user'),
    'password': os.getenv('POSTGRES_PASSWORD', config_obj.get('database.postgres.password', ''))
}

table_name = sys.argv[1] if len(sys.argv) > 1 else 'invoices_pending'

print(f"Table: {table_name}")
print("=" * 100)

db = PostgresClient(db_config)

with db.get_connection() as conn:
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            column_name, 
            data_type, 
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))

    columns = cursor.fetchall()

    print(f"\nColumns ({len(columns)}):\n")
    print(f"{'Column':<30} {'Type':<20} {'Nullable':<10} {'Default':<30}")
    print("-" * 100)

    for col_name, data_type, nullable, default in columns:
        print(f"{col_name:<30} {data_type:<20} {nullable:<10} {str(default or ''):<30}")

    cursor.close()

print("\n" + "=" * 100)