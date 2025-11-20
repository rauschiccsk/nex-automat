#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnose Editor Database Connection
Location: C:/Development/nex-automat/diagnose_editor_db.py
"""

import os
import sys
from pathlib import Path

# Add editor to path
sys.path.insert(0, str(Path(__file__).parent / "apps" / "supplier-invoice-editor"))

print("=" * 70)
print("DIAGNOSE: Supplier Invoice Editor Database")
print("=" * 70)
print()

# Step 1: Check pg8000
print("1️⃣ Checking pg8000...")
try:
    import pg8000

    print(f"   ✅ pg8000 {pg8000.__version__} nainštalované")
except ImportError:
    print("   ❌ pg8000 NIE JE nainštalované")
    print()
    print("   Inštaluj: pip install pg8000")
    print()
    sys.exit(1)

# Step 2: Check config
print()
print("2️⃣ Loading config...")
try:
    from src.utils.config import Config

    config = Config()
    print("   ✅ Config načítaný")

    db_config = config.get('database.postgres', {})
    print(f"   Host: {db_config.get('host')}")
    print(f"   Port: {db_config.get('port')}")
    print(f"   Database: {db_config.get('database')}")
    print(f"   User: {db_config.get('user')}")

    if db_config.get('password'):
        print(f"   Password: {'*' * len(db_config.get('password'))}")
    else:
        print("   ❌ Password NIE JE nastavené")

except Exception as e:
    print(f"   ❌ Chyba pri načítaní config: {e}")
    sys.exit(1)

# Step 3: Test PostgreSQL connection
print()
print("3️⃣ Testing PostgreSQL connection...")
try:
    from src.database.postgres_client import PostgresClient

    db_client = PostgresClient(config)

    if db_client.test_connection():
        print("   ✅ PostgreSQL pripojenie OK")
    else:
        print("   ❌ PostgreSQL pripojenie FAILED")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ Chyba pri pripojení: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

# Step 4: Check invoices_pending table
print()
print("4️⃣ Checking invoices_pending table...")
try:
    query = """
        SELECT COUNT(*) as total,
               COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count
        FROM invoices_pending
    """
    result = db_client.execute_query(query)

    if result:
        total = result[0]['total']
        pending = result[0]['pending_count']
        print(f"   ✅ Tabuľka existuje")
        print(f"   Total faktúr: {total}")
        print(f"   Pending faktúr: {pending}")

        if pending == 0:
            print()
            print("   ⚠️  Žiadne faktúry so statusom 'pending'!")
            print("   Editor zobrazuje len pending faktúry.")
    else:
        print("   ❌ Tabuľka je prázdna")

except Exception as e:
    print(f"   ❌ Chyba pri query: {e}")
    import traceback

    traceback.print_exc()

# Step 5: Test InvoiceService
print()
print("5️⃣ Testing InvoiceService...")
try:
    from src.business.invoice_service import InvoiceService

    service = InvoiceService(config)

    if service.db_client:
        print("   ✅ InvoiceService má DB client")
    else:
        print("   ❌ InvoiceService NEMÁ DB client (používa stub data)")

    invoices = service.get_pending_invoices()
    print(f"   Načítaných faktúr: {len(invoices)}")

    if invoices:
        print()
        print("   Prvá faktúra:")
        inv = invoices[0]
        print(f"   ID: {inv.get('id')}")
        print(f"   Číslo: {inv.get('invoice_number')}")
        print(f"   Dodávateľ: {inv.get('supplier_name')}")
        print(f"   Status: {inv.get('status')}")

except Exception as e:
    print(f"   ❌ Chyba v InvoiceService: {e}")
    import traceback

    traceback.print_exc()

# Summary
print()
print("=" * 70)
print("DIAGNÓZA DOKONČENÁ")
print("=" * 70)
print()