#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import XML faktury do PostgreSQL staging databazy
S NEX Genesis lookup pre kazdu polozku
FIXED: Null byte sanitization for NEX data
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database.postgres_client import PostgresClient
from business.nex_lookup_service import NexLookupService
from utils.config import Config


def clean_string(value):
    """
    Odstrani null bytes a control characters z retazcov
    NEX Genesis Btrieve polia obsahuju \x00 padding
    """
    if value is None:
        return None

    if not isinstance(value, str):
        return value

    # Remove null bytes
    cleaned = value.replace('\x00', '')

    # Remove other control characters (except newline, tab)
    cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\t')

    # Strip excess whitespace
    cleaned = cleaned.strip()

    return cleaned if cleaned else None


def parse_isdoc_xml(xml_path: str):
    """Parse ISDOC XML fakturu"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    ns = {'isdoc': 'http://isdoc.cz/namespace/2013'}

    # Header
    invoice = {
        'invoice_number': root.find('.//isdoc:ID', ns).text,
        'uuid': root.find('.//isdoc:UUID', ns).text,
        'issue_date': root.find('.//isdoc:IssueDate', ns).text,
        'due_date': None,
        'total_amount': Decimal(root.find('.//isdoc:LegalMonetaryTotal/isdoc:TaxInclusiveAmount', ns).text),
        'currency': 'EUR'
    }

    # Due date
    payment = root.find('.//isdoc:PaymentMeans/isdoc:Payment', ns)
    if payment is not None:
        due_date_elem = payment.find('.//isdoc:PaymentDueDate', ns)
        if due_date_elem is not None:
            invoice['due_date'] = due_date_elem.text

    # Supplier
    supplier_party = root.find('.//isdoc:AccountingSupplierParty/isdoc:Party', ns)
    if supplier_party is not None:
        invoice['supplier_name'] = supplier_party.find('.//isdoc:PartyName/isdoc:Name', ns).text
        invoice['supplier_ico'] = supplier_party.find('.//isdoc:PartyIdentification/isdoc:ID', ns).text

    # Items
    items = []
    for idx, line in enumerate(root.findall('.//isdoc:InvoiceLine', ns), 1):
        item = {
            'line_number': idx,
            'description': line.find('.//isdoc:Item/isdoc:Description', ns).text,
            'ean': '',
            'quantity': Decimal('0'),
            'unit': 'ks',
            'unit_price': Decimal('0'),
            'line_total': Decimal('0')
        }

        # EAN
        std_item = line.find('.//isdoc:Item/isdoc:StandardItemIdentification', ns)
        if std_item is not None:
            ean_elem = std_item.find('.//isdoc:ID', ns)
            if ean_elem is not None:
                item['ean'] = ean_elem.text

        # Quantity
        qty_elem = line.find('.//isdoc:InvoicedQuantity', ns)
        if qty_elem is not None:
            item['quantity'] = Decimal(qty_elem.text)
            item['unit'] = qty_elem.get('unitCode', 'ks')

        # Prices
        price_elem = line.find('.//isdoc:UnitPrice', ns)
        if price_elem is not None:
            item['unit_price'] = Decimal(price_elem.text)

        total_elem = line.find('.//isdoc:LineExtensionAmount', ns)
        if total_elem is not None:
            item['line_total'] = Decimal(total_elem.text)

        items.append(item)

    return invoice, items


def import_to_database(xml_path: str, config_path: str = 'config/config.yaml'):
    """Importuj XML fakturu do databazy"""
    print(f"Importing: {xml_path}")

    # Load config
    config_obj = Config(Path(config_path))

    # Build DB config dict
    db_config = {
        'host': config_obj.get('database.postgres.host'),
        'port': config_obj.get('database.postgres.port'),
        'database': config_obj.get('database.postgres.database'),
        'user': config_obj.get('database.postgres.user'),
        'password': os.getenv('POSTGRES_PASSWORD', config_obj.get('database.postgres.password', ''))
    }

    print(f"Connecting to: {db_config['host']}:{db_config['port']}/{db_config['database']}")

    # NEX lookup service
    print("Initializing NEX lookup service...")
    nex_service = NexLookupService()

    # Parse XML
    print("Parsing XML...")
    invoice, items = parse_isdoc_xml(xml_path)

    print(f"Invoice: {invoice['invoice_number']}")
    print(f"Items: {len(items)}")

    # Connect to database
    print("Connecting to database...")
    db = PostgresClient(db_config)

    with db.get_connection() as conn:
        cursor = conn.cursor()

        try:
            # Insert invoice
            print("Inserting invoice...")
            cursor.execute("""
                INSERT INTO invoices_pending (
                    invoice_number, supplier_name, supplier_ico, invoice_date, 
                    due_date, total_amount, currency, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                invoice['invoice_number'],
                clean_string(invoice.get('supplier_name', '')),
                clean_string(invoice.get('supplier_ico', '')),
                invoice['issue_date'],
                invoice.get('due_date'),
                invoice['total_amount'],
                invoice['currency'],
                'pending'
            ))

            invoice_id = cursor.fetchone()[0]
            print(f"Invoice ID: {invoice_id}")

            # Insert items with NEX lookup
            print("\nProcessing items with NEX lookup...")
            found_count = 0
            missing_count = 0

            for item in items:
                ean = item['ean']

                # NEX lookup
                nex_data = None
                if ean:
                    nex_data = nex_service.lookup_by_ean(ean)

                if nex_data:
                    found_count += 1
                    # Clean NEX data - CRITICAL FIX!
                    nex_name_clean = clean_string(nex_data.get('name', ''))
                    nex_category_clean = clean_string(nex_data.get('category', ''))
                    print(f"  OK {item['description'][:40]:<40} -> PLU: {nex_data['plu']}")
                else:
                    missing_count += 1
                    nex_name_clean = None
                    nex_category_clean = None
                    print(f"  MISSING {item['description'][:40]:<40} -> EAN: {ean}")

                # Clean XML description too
                description_clean = clean_string(item['description'])

                # Fallback name
                edited_name = nex_name_clean if nex_name_clean else description_clean

                # Insert item
                cursor.execute("""
                    INSERT INTO invoice_items_pending (
                        invoice_id, line_number, original_name, original_ean,
                        original_quantity, original_unit, original_price_per_unit,
                        nex_plu, nex_name, nex_category, in_nex,
                        edited_name, edited_price_buy, final_price_buy
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    invoice_id,
                    item['line_number'],
                    description_clean,
                    ean,
                    item['quantity'],
                    item['unit'],
                    item['unit_price'],
                    nex_data['plu'] if nex_data else None,
                    nex_name_clean,
                    nex_category_clean,
                    nex_data is not None,
                    edited_name,
                    nex_data['price_buy'] if nex_data else item['unit_price'],
                    item['unit_price']
                ))

            conn.commit()

            print(f"\nImport complete!")
            print(f"  Found in NEX: {found_count}")
            print(f"  Missing in NEX: {missing_count}")
            print(f"\nYou can now view the invoice in the application.")

        except Exception as e:
            conn.rollback()
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            cursor.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_xml_to_staging.py <xml_path>")
        return 1

    xml_path = sys.argv[1]

    if not Path(xml_path).exists():
        print(f"ERROR: File not found: {xml_path}")
        return 1

    import_to_database(xml_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())