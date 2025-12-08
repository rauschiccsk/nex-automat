#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration Script: v2.3 - Migrate invoice-shared to nex-shared
- Create text_utils.py in nex-shared/utils
- Create postgres_staging.py in nex-shared/database
- Update __init__.py exports
- Update imports in supplier-invoice-loader
"""
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
NEX_SHARED = DEV_ROOT / "packages" / "nex-shared"
LOADER_APP = DEV_ROOT / "apps" / "supplier-invoice-loader"

print("=" * 80)
print("Migration Script v2.3: invoice-shared → nex-shared")
print("=" * 80)

# ============================================================================
# 1. CREATE text_utils.py in nex-shared/utils
# ============================================================================
print("\n[1/5] Creating nex-shared/utils/text_utils.py...")

text_utils_content = '''"""
NEX Shared - Text Utilities
Utility functions for text processing and cleaning.
"""


def clean_string(value):
    """
    Odstráni null bytes a control characters z reťazcov.
    NEX Genesis Btrieve polia obsahujú \\\\x00 padding.

    Args:
        value: String alebo iná hodnota na vyčistenie

    Returns:
        Vyčistený string alebo None/original value
    """
    if value is None:
        return None
    if not isinstance(value, str):
        return value

    # Remove null bytes
    cleaned = value.replace('\\x00', '')

    # Remove other control characters (except newline, tab)
    cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\\n\\t')

    # Strip excess whitespace
    cleaned = cleaned.strip()

    return cleaned if cleaned else None
'''

text_utils_file = NEX_SHARED / "utils" / "text_utils.py"
text_utils_file.parent.mkdir(parents=True, exist_ok=True)
text_utils_file.write_text(text_utils_content, encoding='utf-8')
print(f"   ✅ Created: {text_utils_file}")

# ============================================================================
# 2. CREATE postgres_staging.py in nex-shared/database
# ============================================================================
print("\n[2/5] Creating nex-shared/database/postgres_staging.py...")

postgres_staging_content = '''"""
NEX Shared - PostgreSQL Staging Client
Database client for invoice staging operations.
"""
import logging
from typing import Optional, Dict, List, Any
from contextlib import contextmanager

try:
    import pg8000
    import pg8000.dbapi
    PG8000_AVAILABLE = True
except ImportError:
    PG8000_AVAILABLE = False
    pg8000 = None

logger = logging.getLogger(__name__)


class PostgresStagingClient:
    """
    PostgreSQL client for invoice staging operations.

    Usage:
        config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'invoice_staging',
            'user': 'postgres',
            'password': 'secret'
        }

        with PostgresStagingClient(config) as client:
            is_dup = client.check_duplicate_invoice(ico, number)
            invoice_id = client.insert_invoice_with_items(invoice_data, items_data, xml)
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PostgreSQL staging client.

        Args:
            config: Connection configuration dict with keys:
                    host, port, database, user, password
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._conn = None

        if not PG8000_AVAILABLE:
            raise ImportError(
                "pg8000 not installed. "
                "Install with: pip install pg8000"
            )

        # Get connection parameters
        self.conn_params = {
            'host': config.get('host', 'localhost'),
            'port': config.get('port', 5432),
            'database': config.get('database', 'invoice_staging'),
            'user': config.get('user', 'postgres'),
            'password': config.get('password', '')
        }

        self.logger.info(
            f"PostgresStagingClient initialized: "
            f"{self.conn_params['host']}:{self.conn_params['port']}"
            f"/{self.conn_params['database']}"
        )

    def __enter__(self):
        """Context manager entry - establish connection."""
        self._conn = pg8000.dbapi.connect(**self.conn_params)
        self.logger.debug("Database connection established")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection."""
        if self._conn:
            if exc_type is not None:
                # Error occurred, rollback
                self._conn.rollback()
                self.logger.error(f"Transaction rolled back due to error: {exc_val}")
            else:
                # Success, commit
                self._conn.commit()
                self.logger.debug("Transaction committed")

            self._conn.close()
            self._conn = None
            self.logger.debug("Database connection closed")

        # Don't suppress exceptions
        return False

    def check_duplicate_invoice(
        self, 
        supplier_ico: str, 
        invoice_number: str
    ) -> bool:
        """
        Check if invoice already exists in staging database.

        Args:
            supplier_ico: Supplier ICO (tax ID)
            invoice_number: Invoice number

        Returns:
            True if invoice exists, False otherwise
        """
        if not self._conn:
            raise RuntimeError("Not in context manager - use 'with PostgresStagingClient(...) as client:'")

        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM invoices_pending 
                WHERE supplier_ico = %s 
                  AND invoice_number = %s
            """, (supplier_ico, invoice_number))

            count = cursor.fetchone()[0]
            cursor.close()

            exists = count > 0
            if exists:
                self.logger.info(
                    f"Duplicate invoice found: {supplier_ico}/{invoice_number}"
                )

            return exists

        except Exception as e:
            self.logger.exception("Failed to check duplicate invoice")
            raise

    def insert_invoice_with_items(
        self,
        invoice_data: Dict[str, Any],
        items_data: List[Dict[str, Any]],
        isdoc_xml: Optional[str] = None
    ) -> Optional[int]:
        """
        Insert invoice with items into staging database.

        Args:
            invoice_data: Invoice header data dict with keys:
                - supplier_ico (required)
                - supplier_name
                - supplier_dic
                - invoice_number (required)
                - invoice_date (required)
                - due_date
                - total_amount (required)
                - total_vat
                - total_without_vat
                - currency (default: EUR)

            items_data: List of item dicts with keys:
                - line_number (required)
                - name (required)
                - quantity (required)
                - unit
                - price_per_unit (required)
                - ean
                - vat_rate

            isdoc_xml: Optional ISDOC XML string

        Returns:
            Invoice ID if successful, None otherwise
        """
        if not self._conn:
            raise RuntimeError("Not in context manager - use 'with PostgresStagingClient(...) as client:'")

        try:
            cursor = self._conn.cursor()

            # Insert invoice header
            cursor.execute("""
                INSERT INTO invoices_pending (
                    supplier_ico,
                    supplier_name,
                    supplier_dic,
                    invoice_number,
                    invoice_date,
                    due_date,
                    total_amount,
                    total_vat,
                    total_without_vat,
                    currency,
                    isdoc_xml,
                    status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, (
                invoice_data['supplier_ico'],
                invoice_data.get('supplier_name'),
                invoice_data.get('supplier_dic'),
                invoice_data['invoice_number'],
                invoice_data['invoice_date'],
                invoice_data.get('due_date'),
                invoice_data['total_amount'],
                invoice_data.get('total_vat'),
                invoice_data.get('total_without_vat'),
                invoice_data.get('currency', 'EUR'),
                isdoc_xml,
                'pending'
            ))

            invoice_id = cursor.fetchone()[0]
            self.logger.info(f"Inserted invoice: id={invoice_id}")

            # Insert invoice items
            for item in items_data:
                cursor.execute("""
                    INSERT INTO invoice_items_pending (
                        invoice_id,
                        line_number,
                        original_name,
                        original_quantity,
                        original_unit,
                        original_price_per_unit,
                        original_ean,
                        original_vat_rate,
                        edited_name,
                        edited_price_buy,
                        final_price_buy
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    invoice_id,
                    item['line_number'],
                    item['name'],
                    item['quantity'],
                    item.get('unit'),
                    item['price_per_unit'],
                    item.get('ean'),
                    item.get('vat_rate'),
                    item['name'],  # edited_name = original by default
                    item['price_per_unit'],  # edited_price_buy = original
                    item['price_per_unit']   # final_price_buy = original
                ))

            cursor.close()

            self.logger.info(
                f"Inserted {len(items_data)} items for invoice {invoice_id}"
            )

            return invoice_id

        except Exception as e:
            self.logger.exception("Failed to insert invoice with items")
            raise
'''

postgres_staging_file = NEX_SHARED / "database" / "postgres_staging.py"
postgres_staging_file.parent.mkdir(parents=True, exist_ok=True)
postgres_staging_file.write_text(postgres_staging_content, encoding='utf-8')
print(f"   ✅ Created: {postgres_staging_file}")

# ============================================================================
# 3. UPDATE nex-shared/__init__.py exports
# ============================================================================
print("\n[3/5] Updating nex-shared exports...")

# Update utils/__init__.py
utils_init = NEX_SHARED / "utils" / "__init__.py"
utils_init_content = '''"""NEX Shared - Utils Package"""
from .grid_settings import GridSettings
from .text_utils import clean_string

__all__ = ['GridSettings', 'clean_string']
'''
utils_init.write_text(utils_init_content, encoding='utf-8')
print(f"   ✅ Updated: {utils_init}")

# Update database/__init__.py
db_init = NEX_SHARED / "database" / "__init__.py"
db_init_content = '''"""NEX Shared - Database Package"""
from .window_settings_db import WindowSettingsDB
from .postgres_staging import PostgresStagingClient

__all__ = ['WindowSettingsDB', 'PostgresStagingClient']
'''
db_init.write_text(db_init_content, encoding='utf-8')
print(f"   ✅ Updated: {db_init}")

# ============================================================================
# 4. UPDATE imports in supplier-invoice-loader
# ============================================================================
print("\n[4/5] Updating supplier-invoice-loader imports...")

# Update main.py
main_file = LOADER_APP / "main.py"
main_content = main_file.read_text(encoding='utf-8')

# Replace imports
main_content = main_content.replace(
    'from invoice_shared.utils.text_utils import clean_string',
    'from nex_shared.utils import clean_string'
)
main_content = main_content.replace(
    'from invoice_shared.database.postgres_staging import PostgresStagingClient',
    'from nex_shared.database import PostgresStagingClient'
)

main_file.write_text(main_content, encoding='utf-8')
print(f"   ✅ Updated: {main_file}")

# Update test file if exists
test_file = LOADER_APP / "scripts" / "test_invoice_integration.py"
if test_file.exists():
    test_content = test_file.read_text(encoding='utf-8')

    test_content = test_content.replace(
        'from invoice_shared.database.postgres_staging import PostgresStagingClient',
        'from nex_shared.database import PostgresStagingClient'
    )

    test_file.write_text(test_content, encoding='utf-8')
    print(f"   ✅ Updated: {test_file}")

# ============================================================================
# 5. SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ Migration v2.3 Complete!")
print("=" * 80)
print("\nFiles created:")
print(f"  - {text_utils_file}")
print(f"  - {postgres_staging_file}")
print("\nFiles updated:")
print(f"  - {utils_init}")
print(f"  - {db_init}")
print(f"  - {main_file}")
if test_file.exists():
    print(f"  - {test_file}")

print("\nNext steps:")
print("  1. cd packages\\nex-shared")
print("  2. pip install -e .")
print("  3. cd ..\\..\\apps\\supplier-invoice-loader")
print("  4. python main.py  # Test loader")
print("  5. git add .")
print("  6. git commit -m 'v2.3: Migrate invoice-shared to nex-shared'")
print("  7. git tag v2.3")

print("\n" + "=" * 80)