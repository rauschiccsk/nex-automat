#!/usr/bin/env python3
"""
Insert Test Data - Populate database with test invoices
"""

import sys
from pathlib import Path
from decimal import Decimal

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import Config
from database.postgres_client import PostgresClient


def insert_test_invoices(client: PostgresClient):
    """Insert test invoices"""
    print("\nInserting test invoices...")

    invoices = [
        {
            'invoice_number': 'FAV-2025-001',
            'invoice_date': '2025-11-12',
            'supplier_name': 'Test Dodávateľ s.r.o.',
            'supplier_ico': '12345678',
            'total_amount': Decimal('253.75'),
            'currency': 'EUR',
            'status': 'pending'
        },
        {
            'invoice_number': 'FAV-2025-002',
            'invoice_date': '2025-11-11',
            'supplier_name': 'Iný Dodávateľ a.s.',
            'supplier_ico': '87654321',
            'total_amount': Decimal('217.92'),
            'currency': 'EUR',
            'status': 'pending'
        },
        {
            'invoice_number': 'FAV-2025-003',
            'invoice_date': '2025-11-10',
            'supplier_name': 'ABC Trading s.r.o.',
            'supplier_ico': '11223344',
            'total_amount': Decimal('0.00'),
            'currency': 'EUR',
            'status': 'pending'
        }
    ]

    query = """
        INSERT INTO invoices_pending 
        (invoice_number, invoice_date, supplier_name, supplier_ico, total_amount, currency, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """

    invoice_ids = []

    for invoice in invoices:
        params = (
            invoice['invoice_number'],
            invoice['invoice_date'],
            invoice['supplier_name'],
            invoice['supplier_ico'],
            invoice['total_amount'],
            invoice['currency'],
            invoice['status']
        )

        result = client.execute_query(query, params, fetch=True)
        invoice_id = result[0]['id']
        invoice_ids.append(invoice_id)

        print(f"  ✓ Inserted invoice {invoice['invoice_number']} (ID: {invoice_id})")

    return invoice_ids


def insert_test_items(client: PostgresClient, invoice_ids: list):
    """Insert test invoice items"""
    print("\nInserting test items...")

    # Items for invoice 1
    items_1 = [
        {
            'invoice_id': invoice_ids[0],
            'plu_code': '1001',
            'item_name': 'Produkt A',
            'category_code': '01',
            'unit': 'ks',
            'quantity': Decimal('10.000'),
            'unit_price': Decimal('15.00'),
            'rabat_percent': Decimal('10.0'),
            'price_after_rabat': Decimal('13.50'),
            'total_price': Decimal('135.00')
        },
        {
            'invoice_id': invoice_ids[0],
            'plu_code': '1002',
            'item_name': 'Produkt B',
            'category_code': '02',
            'unit': 'ks',
            'quantity': Decimal('5.000'),
            'unit_price': Decimal('25.00'),
            'rabat_percent': Decimal('5.0'),
            'price_after_rabat': Decimal('23.75'),
            'total_price': Decimal('118.75')
        }
    ]

    # Items for invoice 2
    items_2 = [
        {
            'invoice_id': invoice_ids[1],
            'plu_code': '2001',
            'item_name': 'Tovar X',
            'category_code': '03',
            'unit': 'kg',
            'quantity': Decimal('20.500'),
            'unit_price': Decimal('12.50'),
            'rabat_percent': Decimal('15.0'),
            'price_after_rabat': Decimal('10.63'),
            'total_price': Decimal('217.92')
        }
    ]

    # Items for invoice 3
    items_3 = [
        {
            'invoice_id': invoice_ids[2],
            'plu_code': '3001',
            'item_name': 'Test položka C',
            'category_code': '01',
            'unit': 'ks',
            'quantity': Decimal('1.000'),
            'unit_price': Decimal('100.00'),
            'rabat_percent': Decimal('0.0'),
            'price_after_rabat': Decimal('100.00'),
            'total_price': Decimal('100.00')
        }
    ]

    all_items = items_1 + items_2 + items_3

    query = """
        INSERT INTO invoice_items_pending
        (invoice_id, plu_code, item_name, category_code, unit, quantity, 
         unit_price, rabat_percent, price_after_rabat, total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params_list = []
    for item in all_items:
        params = (
            item['invoice_id'],
            item['plu_code'],
            item['item_name'],
            item['category_code'],
            item['unit'],
            item['quantity'],
            item['unit_price'],
            item['rabat_percent'],
            item['price_after_rabat'],
            item['total_price']
        )
        params_list.append(params)

    count = client.execute_many(query, params_list)
    print(f"  ✓ Inserted {count} items")

    # Update invoice totals
    print("\nUpdating invoice totals...")
    update_query = """
        UPDATE invoices_pending
        SET total_amount = (
            SELECT SUM(total_price)
            FROM invoice_items_pending
            WHERE invoice_id = invoices_pending.id
        )
    """
    client.execute_query(update_query, fetch=False)
    print("  ✓ Updated totals")


def clear_existing_data(client: PostgresClient):
    """Clear existing test data"""
    print("\nClearing existing test data...")

    # Delete items first (foreign key constraint)
    client.execute_query("DELETE FROM invoice_items_pending WHERE invoice_id IN (SELECT id FROM invoices_pending WHERE invoice_number LIKE 'FAV-2025-%')", fetch=False)
    print("  ✓ Cleared items")

    # Delete invoices
    client.execute_query("DELETE FROM invoices_pending WHERE invoice_number LIKE 'FAV-2025-%'", fetch=False)
    print("  ✓ Cleared invoices")


def main():
    """Main function"""
    print("=" * 60)
    print("INSERT TEST DATA")
    print("=" * 60)

    try:
        # Load config
        config = Config()
        print("\n✓ Configuration loaded")

        # Connect to database
        client = PostgresClient(config)
        print("✓ Connected to PostgreSQL")

        # Test connection
        if not client.test_connection():
            print("\n✗ Database connection test failed!")
            return 1

        print("✓ Connection test successful")

        # Clear existing data
        clear_existing_data(client)

        # Insert test data
        invoice_ids = insert_test_invoices(client)
        insert_test_items(client, invoice_ids)

        print("\n" + "=" * 60)
        print("TEST DATA INSERTED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nInserted {len(invoice_ids)} invoices with items")
        print("\nYou can now:")
        print("  1. Run: python main.py")
        print("  2. See invoices in list")
        print("  3. Double-click to edit")
        print("  4. Save changes to database")

        # Close connection
        client.close()

        return 0

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
