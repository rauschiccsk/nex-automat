"""
Invoice Service - Business logic for invoice operations
Adapted for production database schema from supplier_invoice_loader
"""

import logging
from typing import List, Dict, Optional
from decimal import Decimal


class InvoiceService:
    """Service for invoice operations"""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Try to initialize PostgreSQL client
        self.db_client = None
        self._init_database()

    def _init_database(self):
        """Initialize database connection"""
        try:
            from database.postgres_client import PostgresClient
            self.db_client = PostgresClient(self.config)

            # Test connection
            if self.db_client.test_connection():
                self.logger.info("PostgreSQL client initialized and connected")
            else:
                self.logger.warning("PostgreSQL connection test failed - using stub data")
                self.db_client = None

        except ImportError:
            self.logger.warning(
                "pg8000 not installed - using stub data. "
                "Install with: pip install pg8000"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            self.logger.warning("Using stub data")
            self.db_client = None

    def get_pending_invoices(self) -> List[Dict]:
        """
        Get list of pending invoices

        Returns:
            List of invoice dictionaries
        """
        if self.db_client:
            try:
                return self._get_invoices_from_database()
            except Exception as e:
                self.logger.error(f"Database query failed: {e}")
                self.logger.warning("Falling back to stub data")

        return self._get_stub_invoices()

    def _get_invoices_from_database(self) -> List[Dict]:
        """Get invoices from PostgreSQL"""
        query = """
            SELECT 
                id,
                invoice_number,
                invoice_date::text as invoice_date,
                supplier_name,
                supplier_ico,
                total_amount,
                currency,
                status
            FROM invoices_pending
            WHERE status = 'pending'
            ORDER BY invoice_date DESC, id DESC
        """

        results = self.db_client.execute_query(query)
        self.logger.info(f"Loaded {len(results)} pending invoices from database")

        return results

    def _get_stub_invoices(self) -> List[Dict]:
        """Get stub invoice data for testing"""
        self.logger.info("Using stub invoice data")

        return [
            {
                'id': 1,
                'invoice_number': 'FAV-2025-001',
                'invoice_date': '2025-11-12',
                'supplier_name': 'Test Dodávateľ s.r.o.',
                'supplier_ico': '12345678',
                'total_amount': Decimal('1200.00'),
                'currency': 'EUR',
                'status': 'pending'
            }
        ]

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Dict]:
        """
        Get single invoice by ID

        Args:
            invoice_id: Invoice ID

        Returns:
            Invoice dictionary or None
        """
        if self.db_client:
            try:
                query = """
                    SELECT 
                        id,
                        invoice_number,
                        invoice_date::text as invoice_date,
                        supplier_name,
                        supplier_ico,
                        total_amount,
                        currency,
                        status
                    FROM invoices_pending
                    WHERE id = %s
                """
                results = self.db_client.execute_query(query, (invoice_id,))

                if results:
                    self.logger.info(f"Loaded invoice {invoice_id} from database")
                    return results[0]
                else:
                    self.logger.warning(f"Invoice {invoice_id} not found in database")
                    return None

            except Exception as e:
                self.logger.error(f"Failed to load invoice {invoice_id}: {e}")

        # Fallback to stub data
        invoices = self._get_stub_invoices()
        for invoice in invoices:
            if invoice['id'] == invoice_id:
                return invoice
        return None

    def get_invoice_items(self, invoice_id: int) -> List[Dict]:
        """
        Get invoice line items - ADAPTED FOR PRODUCTION SCHEMA

        Args:
            invoice_id: Invoice ID

        Returns:
            List of item dictionaries
        """
        if self.db_client:
            try:
                return self._get_items_from_database(invoice_id)
            except Exception as e:
                self.logger.error(f"Database query failed: {e}")
                self.logger.warning("Falling back to stub data")

        return self._get_stub_items(invoice_id)

    def _get_items_from_database(self, invoice_id: int) -> List[Dict]:
        """
        Get items from PostgreSQL - ADAPTED FOR PRODUCTION SCHEMA

        Maps production columns to UI expected columns:
        - edited_name OR original_name → item_name
        - edited_mglst_code → category_code
        - original_unit → unit
        - original_quantity → quantity
        - edited_price_buy OR original_price_per_unit → unit_price
        - edited_discount_percent → rabat_percent
        - final_price_buy → price_after_rabat
        - (final_price_buy * original_quantity) → total_price
        - original_ean OR nex_gs_code → plu_code
        """
        query = """
            SELECT 
                id,
                invoice_id,
                line_number,
                COALESCE(edited_name, original_name) as item_name,
                COALESCE(edited_mglst_code, 0) as category_code,
                original_unit as unit,
                original_quantity as quantity,
                COALESCE(edited_price_buy, original_price_per_unit) as unit_price,
                COALESCE(edited_discount_percent, 0.00) as rabat_percent,
                COALESCE(final_price_buy, edited_price_buy, original_price_per_unit) as price_after_rabat,
                (COALESCE(final_price_buy, edited_price_buy, original_price_per_unit) * original_quantity) as total_price,
                COALESCE(CAST(nex_gs_code AS VARCHAR), original_ean, '') as plu_code,
                original_ean,
                was_edited,
                validation_status
            FROM invoice_items_pending
            WHERE invoice_id = %s
            ORDER BY line_number
        """

        results = self.db_client.execute_query(query, (invoice_id,))
        self.logger.info(f"Loaded {len(results)} items for invoice {invoice_id} from database")

        return results

    def _get_stub_items(self, invoice_id: int) -> List[Dict]:
        """Get stub item data for testing"""
        self.logger.info(f"Using stub items for invoice {invoice_id}")

        return [
            {
                'id': 100 + invoice_id,
                'invoice_id': invoice_id,
                'plu_code': f'{1000 + invoice_id}',
                'item_name': f'Test položka {invoice_id}',
                'category_code': '1',
                'unit': 'ks',
                'quantity': Decimal('1.000'),
                'unit_price': Decimal('100.00'),
                'rabat_percent': Decimal('0.0'),
                'price_after_rabat': Decimal('100.00'),
                'total_price': Decimal('100.00')
            }
        ]

    def save_invoice(self, invoice_id: int, items: List[Dict]) -> bool:
        """
        Save invoice items - ADAPTED FOR PRODUCTION SCHEMA

        Args:
            invoice_id: Invoice ID
            items: List of item dictionaries

        Returns:
            True if saved successfully
        """
        try:
            self.logger.info(f"Saving invoice {invoice_id} with {len(items)} items")

            if self.db_client:
                return self._save_to_database(invoice_id, items)
            else:
                # Stub mode - just log
                self.logger.warning("Database not available - changes not saved (stub mode)")
                self.logger.info(f"Would save {len(items)} items:")
                for item in items:
                    self.logger.info(f"  - {item['item_name']}: {item['total_price']}")
                return True

        except Exception as e:
            self.logger.exception(f"Failed to save invoice {invoice_id}")
            return False

    def _save_to_database(self, invoice_id: int, items: List[Dict]) -> bool:
        """
        Save items to PostgreSQL - ADAPTED FOR PRODUCTION SCHEMA

        Maps UI columns back to production columns:
        - item_name → edited_name
        - category_code → edited_mglst_code
        - unit_price → edited_price_buy
        - rabat_percent → edited_discount_percent
        - price_after_rabat → final_price_buy
        """
        try:
            with self.db_client.transaction() as conn:
                cur = conn.cursor()

                # Update each item
                update_query = """
                    UPDATE invoice_items_pending
                    SET 
                        edited_name = %s,
                        edited_mglst_code = %s,
                        edited_price_buy = %s,
                        edited_discount_percent = %s,
                        final_price_buy = %s,
                        final_price_sell = %s,
                        was_edited = true,
                        edited_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND invoice_id = %s
                """

                for item in items:
                    # Calculate final_price_sell (with some margin, e.g. 50%)
                    final_price_buy = item['price_after_rabat']
                    final_price_sell = final_price_buy * Decimal('1.5')  # 50% margin

                    params = (
                        item['item_name'],
                        int(item.get('category_code', 0)),
                        item['unit_price'],
                        item['rabat_percent'],
                        final_price_buy,
                        final_price_sell,
                        item['id'],
                        invoice_id
                    )
                    cur.execute(update_query, params)

                # Update invoice total
                total_query = """
                    UPDATE invoices_pending
                    SET 
                        total_amount = (
                            SELECT SUM(final_price_buy * original_quantity)
                            FROM invoice_items_pending
                            WHERE invoice_id = %s
                        )
                    WHERE id = %s
                """
                cur.execute(total_query, (invoice_id, invoice_id))

                cur.close()

            self.logger.info(f"Successfully saved {len(items)} items to database")
            return True

        except Exception as e:
            self.logger.exception("Database save failed")
            return False

    def calculate_item_price(self, unit_price: Decimal, rabat_percent: Decimal, 
                            quantity: Decimal) -> tuple:
        """
        Calculate item prices

        Args:
            unit_price: Unit price
            rabat_percent: Rabat percentage (0-100)
            quantity: Quantity

        Returns:
            Tuple (price_after_rabat, total_price)
        """
        price_after_rabat = unit_price * (Decimal('1') - rabat_percent / Decimal('100'))
        price_after_rabat = price_after_rabat.quantize(Decimal('0.01'))

        total_price = price_after_rabat * quantity
        total_price = total_price.quantize(Decimal('0.01'))

        return (price_after_rabat, total_price)
