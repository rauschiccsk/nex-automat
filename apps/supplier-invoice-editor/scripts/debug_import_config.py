#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug config loading"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config import Config

config_obj = Config(Path('config/config.yaml'))

env_password = os.getenv('POSTGRES_PASSWORD', '')
config_password = config_obj.get('database.postgres.password', '')

db_config = {
    'host': config_obj.get('database.postgres.host'),
    'port': int(config_obj.get('database.postgres.port')),
    'database': config_obj.get('database.postgres.database'),
    'user': config_obj.get('database.postgres.user'),
    'password': env_password or config_password
}

print("Password sources:")
print(f"  ENV POSTGRES_PASSWORD: {'***' if env_password else 'NOT SET'} (length: {len(env_password)})")
print(f"  Config file password:  {'***' if config_password else 'NOT SET'} (length: {len(config_password)})")
print(f"  Using:                 {'ENV' if env_password else 'CONFIG'}")

print("\nDB Config:")
for key, value in db_config.items():
    if key == 'password':
        # Show password with repr to see hidden chars
        print(f"  {key}: {repr(value)}")
    else:
        print(f"  {key}: {value} (type: {type(value).__name__})")

# Try to connect
from database.postgres_client import PostgresClient

print(f"\nTest 1: Trying with current password...")
try:
    db = PostgresClient(db_config)
    with db.get_connection() as conn:
        print("OK Connected successfully!")
except Exception as e:
    print(f"ERROR: {e}")

# Try with stripped password
print(f"\nTest 2: Trying with stripped password...")
db_config['password'] = db_config['password'].strip()
try:
    db = PostgresClient(db_config)
    with db.get_connection() as conn:
        print("OK Connected successfully!")
except Exception as e:
    print(f"ERROR: {e}")

print("\nSuggestion: Try to connect manually:")
print(f"  psql -h {db_config['host']} -p {db_config['port']} -U {db_config['user']} -d {db_config['database']}")
print("  Enter the same password you use in the script")