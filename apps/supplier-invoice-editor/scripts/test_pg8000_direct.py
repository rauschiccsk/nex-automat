#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pg8000 directly"""

import pg8000.dbapi

print("Testing pg8000 connection...")

# Test 1: Direct connection
print("\nTest 1: Direct pg8000.dbapi.connect()")
try:
    conn = pg8000.dbapi.connect(
        host='localhost',
        port=5432,
        database='invoice_staging',
        user='postgres',
        password='Nex1968'
    )
    print("OK Connected!")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: With different parameters
print("\nTest 2: With timeout parameter")
try:
    conn = pg8000.dbapi.connect(
        host='localhost',
        port=5432,
        database='invoice_staging',
        user='postgres',
        password='Nex1968',
        timeout=10
    )
    print("OK Connected!")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Check PostgresClient implementation
print("\nTest 3: Check how PostgresClient builds connection")
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database.postgres_client import PostgresClient

config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'invoice_staging',
    'user': 'postgres',
    'password': 'Nex1968'
}

client = PostgresClient(config)
print(f"Connection params: {client.conn_params}")

try:
    with client.get_connection() as conn:
        print("OK Connected via PostgresClient!")
except Exception as e:
    print(f"ERROR: {e}")