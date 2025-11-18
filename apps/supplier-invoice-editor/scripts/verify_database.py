#!/usr/bin/env python3
"""
Verify Database - Check PostgreSQL connection and data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import Config
from database.postgres_client import PostgresClient


def verify_connection(client: PostgresClient):
    """Verify database connection"""
    print("\n1. Testing connection...")
    if client.test_connection():
        print("   ✓ Connection successful")
        return True
    else:
        print("   ✗ Connection failed")
        return False


def verify_tables(client: PostgresClient):
    """Verify required tables exist"""
    print("\n2. Checking tables...")

    required_tables = [
        'invoices_pending',
        'invoice_items_pending',
        'invoice_log'
    ]

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = %s
    """

    all_exist = True
    for table in required_tables:
        result = client.execute_query(query, (table,))
        if result:
            print(f"   ✓ {table}")
        else:
            print(f"   ✗ {table} - MISSING!")
            all_exist = False

    return all_exist


def verify_invoices(client: PostgresClient):
    """Verify invoices data"""
    print("\n3. Checking invoices...")

    query = """
        SELECT COUNT(*) as count
        FROM invoices_pending
        WHERE status = 'pending'
    """

    result = client.execute_query(query)
    count = result[0]['count'] if result else 0

    if count > 0:
        print(f"   ✓ Found {count} pending invoices")

        # Show sample
        sample_query = """
            SELECT invoice_number, supplier_name, total_amount
            FROM invoices_pending
            WHERE status = 'pending'
            LIMIT 3
        """
        samples = client.execute_query(sample_query)

        print("\n   Sample invoices:")
        for inv in samples:
            print(f"     • {inv['invoice_number']} - {inv['supplier_name']} - {inv['total_amount']} EUR")

        return True
    else:
        print("   ⚠ No pending invoices found")
        print("   Run: python scripts/insert_test_data.py")
        return False


def verify_items(client: PostgresClient):
    """Verify invoice items data"""
    print("\n4. Checking invoice items...")

    query = """
        SELECT COUNT(*) as count
        FROM invoice_items_pending
    """

    result = client.execute_query(query)
    count = result[0]['count'] if result else 0

    if count > 0:
        print(f"   ✓ Found {count} invoice items")
        return True
    else:
        print("   ⚠ No invoice items found")
        print("   Run: python scripts/insert_test_data.py")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)

    try:
        # Load config
        config = Config()
        print("\n✓ Configuration loaded")

        # Connect to database
        print("\nConnecting to PostgreSQL...")
        client = PostgresClient(config)
        print("✓ PostgreSQL client initialized")

        # Run verifications
        results = []
        results.append(verify_connection(client))
        results.append(verify_tables(client))
        results.append(verify_invoices(client))
        results.append(verify_items(client))

        # Summary
        print("\n" + "=" * 60)
        if all(results):
            print("✓ ALL CHECKS PASSED")
            print("=" * 60)
            print("\nDatabase is ready!")
            print("Run: python main.py")
        else:
            print("⚠ SOME CHECKS FAILED")
            print("=" * 60)
            print("\nPlease fix the issues above before running the application.")

        # Close connection
        client.close()

        return 0 if all(results) else 1

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
