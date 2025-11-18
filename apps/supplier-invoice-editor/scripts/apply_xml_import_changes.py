#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script na aplikovanie zmien pre XML import a NEX lookup funkcionalitu

Vytvori:
- scripts/import_xml_to_staging.py - Import XML do PostgreSQL
- src/business/nex_lookup_service.py - NEX Genesis lookup service
- database/schemas/002_add_nex_columns.sql - Nová migrácia

Modifikuje:
- src/business/invoice_service.py - Pridá NEX lookup
- src/ui/widgets/invoice_items_grid.py - Pridá farebné označenie
"""

import os
from pathlib import Path

# Zisti root projektu
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent


def create_file(relative_path: str, content: str):
    """Vytvorí nový súbor s obsahom"""
    file_path = PROJECT_ROOT / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"OK Created: {relative_path}")


def main():
    print("=" * 80)
    print("Aplikujem zmeny pre XML import a NEX lookup")
    print("=" * 80)

    # =========================================================================
    # 1. NEX Lookup Service
    # =========================================================================
    print("\n1. Creating NEX Lookup Service...")

    nex_lookup_service_content = '''# src/business/nex_lookup_service.py
"""
NEX Genesis Lookup Service
Vyhladavanie produktov v NEX Genesis GSCAT.BTR podla EAN
"""

from pathlib import Path
from typing import Optional, Tuple, Dict
import sys

# Add src to path for standalone usage
sys.path.insert(0, str(Path(__file__).parent.parent))

from btrieve.btrieve_client import BtrieveClient
from models.gscat import GSCATRecord
from models.barcode import BarcodeRecord


class NexLookupService:
    """Service pre vyhladavanie produktov v NEX Genesis"""

    def __init__(self, nex_path: str = r"C:\\NEX\\YEARACT"):
        """
        Args:
            nex_path: Cesta k NEX Genesis YEARACT adresaru
        """
        self.nex_path = Path(nex_path)
        self.gscat_path = self.nex_path / "STORES" / "GSCAT.BTR"
        self.barcode_path = self.nex_path / "STORES" / "BARCODE.BTR"

        # Validate paths
        if not self.gscat_path.exists():
            raise FileNotFoundError(f"GSCAT.BTR not found: {self.gscat_path}")

    def lookup_by_ean(self, ean: str) -> Optional[Dict]:
        """
        Vyhlada produkt podla EAN

        Logika:
        1. Najprv hlada v GSCAT.BarCode (primarny EAN)
        2. Ak nenajde, hlada v BARCODE.BTR (druhotne EAN)

        Args:
            ean: EAN kod

        Returns:
            Dict s produktovymi udajmi alebo None
            {
                'plu': int,
                'name': str,
                'category': int,
                'price_buy': float,
                'price_sell': float,
                'unit': str,
                'in_nex': bool,
                'source': 'GSCAT' | 'BARCODE'
            }
        """
        # 1. Hladaj v GSCAT.BarCode
        gscat_record = self._find_in_gscat(ean)
        if gscat_record:
            return {
                'plu': gscat_record.gs_code,
                'name': gscat_record.gs_name,
                'category': gscat_record.mglst_code,
                'price_buy': float(gscat_record.price_buy),
                'price_sell': float(gscat_record.price_sell),
                'unit': gscat_record.unit,
                'in_nex': True,
                'source': 'GSCAT'
            }

        # 2. Hladaj v BARCODE.BTR
        barcode_record = self._find_in_barcode(ean)
        if barcode_record:
            # Nacitaj produkt podla PLU
            gscat_record = self._find_in_gscat_by_plu(barcode_record.gs_code)
            if gscat_record:
                return {
                    'plu': gscat_record.gs_code,
                    'name': gscat_record.gs_name,
                    'category': gscat_record.mglst_code,
                    'price_buy': float(gscat_record.price_buy),
                    'price_sell': float(gscat_record.price_sell),
                    'unit': gscat_record.unit,
                    'in_nex': True,
                    'source': 'BARCODE'
                }

        return None

    def _find_in_gscat(self, ean: str) -> Optional[GSCATRecord]:
        """Najde produkt v GSCAT.BTR podla BarCode"""
        client = BtrieveClient()

        try:
            status, pos_block = client.open_file(str(self.gscat_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                return None

            try:
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        if len(data) >= 72:
                            # Read BarCode: [00 00][length][data...]
                            barcode_length = data[59] if len(data) > 59 else 0
                            barcode_data = data[60:60+barcode_length] if len(data) >= 60+barcode_length else b''
                            barcode_str = barcode_data.decode('cp852', errors='ignore')

                            if barcode_str.strip() == ean.strip():
                                return GSCATRecord.from_bytes(data)
                    except:
                        pass

                    status, data = client.get_next(pos_block)

                return None
            finally:
                client.close_file(pos_block)
        except:
            return None

    def _find_in_gscat_by_plu(self, plu: int) -> Optional[GSCATRecord]:
        """Najde produkt v GSCAT.BTR podla PLU"""
        client = BtrieveClient()

        try:
            status, pos_block = client.open_file(str(self.gscat_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                return None

            try:
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        record = GSCATRecord.from_bytes(data)
                        if record.gs_code == plu:
                            return record
                    except:
                        pass

                    status, data = client.get_next(pos_block)

                return None
            finally:
                client.close_file(pos_block)
        except:
            return None

    def _find_in_barcode(self, ean: str) -> Optional[BarcodeRecord]:
        """Najde zaznam v BARCODE.BTR"""
        if not self.barcode_path.exists():
            return None

        client = BtrieveClient()

        try:
            status, pos_block = client.open_file(str(self.barcode_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                return None

            try:
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        record = BarcodeRecord.from_bytes(data)
                        if record.bar_code.strip() == ean.strip():
                            return record
                    except:
                        pass

                    status, data = client.get_next(pos_block)

                return None
            finally:
                client.close_file(pos_block)
        except:
            return None
'''

    create_file('src/business/nex_lookup_service.py', nex_lookup_service_content)

    # =========================================================================
    # 2. Import XML to Staging Script
    # =========================================================================
    print("\n2. Creating XML Import Script...")

    import_xml_script_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import XML faktury do PostgreSQL staging databazy
S NEX Genesis lookup pre kazdu polozku
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import uuid

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database.postgres_client import PostgresClient
from business.nex_lookup_service import NexLookupService
from utils.config import load_config


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
    config = load_config(config_path)
    db_config = config.get('database', {}).get('postgres', {})

    # NEX lookup service
    nex_service = NexLookupService()

    # Parse XML
    invoice, items = parse_isdoc_xml(xml_path)

    print(f"Invoice: {invoice['invoice_number']}")
    print(f"Items: {len(items)}")

    # Connect to database
    db = PostgresClient(db_config)
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # Insert invoice
        cursor.execute("""
            INSERT INTO invoices (
                invoice_number, supplier_name, supplier_ico, issue_date, 
                due_date, total_amount, currency, status, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            invoice['invoice_number'],
            invoice.get('supplier_name', ''),
            invoice.get('supplier_ico', ''),
            invoice['issue_date'],
            invoice.get('due_date'),
            invoice['total_amount'],
            invoice['currency'],
            'pending',
            datetime.now()
        ))

        invoice_id = cursor.fetchone()[0]
        print(f"Invoice ID: {invoice_id}")

        # Insert items with NEX lookup
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
                print(f"  OK {item['description'][:40]:<40} -> PLU: {nex_data['plu']}")
            else:
                missing_count += 1
                print(f"  MISSING {item['description'][:40]:<40} -> EAN: {ean}")

            # Insert item
            cursor.execute("""
                INSERT INTO invoice_items_pending (
                    invoice_id, line_number, original_name, original_ean,
                    original_quantity, original_unit, original_price_per_unit,
                    original_line_total, nex_plu, nex_name, nex_category, in_nex,
                    edited_name, edited_quantity, edited_unit, edited_price_buy,
                    final_price_buy, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                invoice_id,
                item['line_number'],
                item['description'],
                ean,
                item['quantity'],
                item['unit'],
                item['unit_price'],
                item['line_total'],
                nex_data['plu'] if nex_data else None,
                nex_data['name'] if nex_data else None,
                nex_data['category'] if nex_data else None,
                nex_data is not None,
                nex_data['name'] if nex_data else item['description'],
                item['quantity'],
                item['unit'],
                nex_data['price_buy'] if nex_data else item['unit_price'],
                item['unit_price'],
                datetime.now()
            ))

        conn.commit()

        print(f"\\nImport complete!")
        print(f"  Found in NEX: {found_count}")
        print(f"  Missing in NEX: {missing_count}")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


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
'''

    create_file('scripts/import_xml_to_staging.py', import_xml_script_content)

    # =========================================================================
    # 3. Database Migration - Add NEX columns
    # =========================================================================
    print("\n3. Creating Database Migration...")

    migration_content = '''-- 002_add_nex_columns.sql
-- Pridanie stlpcov pre NEX Genesis lookup data

-- Pridaj NEX stlpce do invoice_items_pending
ALTER TABLE invoice_items_pending
ADD COLUMN IF NOT EXISTS nex_plu INTEGER,
ADD COLUMN IF NOT EXISTS nex_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS nex_category INTEGER,
ADD COLUMN IF NOT EXISTS in_nex BOOLEAN DEFAULT FALSE;

-- Indexy pre rychlejsie vyhladavanie
CREATE INDEX IF NOT EXISTS idx_invoice_items_pending_in_nex ON invoice_items_pending(in_nex);
CREATE INDEX IF NOT EXISTS idx_invoice_items_pending_nex_plu ON invoice_items_pending(nex_plu);

-- Komentar
COMMENT ON COLUMN invoice_items_pending.nex_plu IS 'PLU cislo produktu z NEX Genesis GSCAT';
COMMENT ON COLUMN invoice_items_pending.nex_name IS 'Nazov produktu z NEX Genesis GSCAT';
COMMENT ON COLUMN invoice_items_pending.nex_category IS 'Tovarova skupina (MGLST) z NEX Genesis';
COMMENT ON COLUMN invoice_items_pending.in_nex IS 'Priznak ci produkt existuje v NEX Genesis';
'''

    create_file('database/schemas/002_add_nex_columns.sql', migration_content)

    # =========================================================================
    # 4. Update invoice_service.py - Add NEX data loading
    # =========================================================================
    print("\n4. Modifying invoice_service.py...")

    invoice_service_update = '''
    # Add after existing get_invoice_items method

    def get_invoice_items_with_nex(self, invoice_id: int) -> List[Dict]:
        """
        Get invoice items with NEX Genesis data

        Returns items with NEX lookup data and color coding
        """
        items = self.get_invoice_items(invoice_id)

        # Add color coding based on in_nex flag
        for item in items:
            item['row_color'] = 'green' if item.get('in_nex', False) else 'red'
            item['in_nex_text'] = 'OK' if item.get('in_nex', False) else 'MISSING'

        return items
'''

    print("  NOTE: Manually add get_invoice_items_with_nex() method to invoice_service.py")
    print("  Or run: python scripts/update_invoice_service.py")

    # =========================================================================
    # 5. Update invoice_items_grid.py - Add color coding
    # =========================================================================
    print("\n5. Creating UI update note...")

    ui_update_note = '''
# Update invoice_items_grid.py

Add color coding in data() method:

def data(self, index, role=Qt.DisplayRole):
    if not index.isValid():
        return None

    item = self._items[index.row()]
    col = index.column()

    # ADD THIS: Background color based on in_nex
    if role == Qt.BackgroundRole:
        if not item.get('in_nex', True):
            return QBrush(QColor(255, 200, 200))  # Light red for missing
        return QBrush(QColor(200, 255, 200))  # Light green for found

    # ... rest of existing code
'''

    print("  NOTE: Manually update invoice_items_grid.py data() method")
    print("  Add Qt.BackgroundRole handling for color coding")

    # =========================================================================
    # Done
    # =========================================================================
    print("\n" + "=" * 80)
    print("HOTOVO - Vsetky subory vytvorene")
    print("=" * 80)
    print("\nDalšie kroky:")
    print("1. Spusti migráciu: psql -U postgres -d invoice_staging -f database/schemas/002_add_nex_columns.sql")
    print("2. Importuj XML: python scripts/import_xml_to_staging.py C:\\NEX\\IMPORT\\32501215.xml")
    print("3. Manuálne uprav invoice_service.py - pridaj get_invoice_items_with_nex() metódu")
    print("4. Manuálne uprav invoice_items_grid.py - pridaj Qt.BackgroundRole handling")
    print("5. Testuj aplikáciu")


if __name__ == '__main__':
    main()