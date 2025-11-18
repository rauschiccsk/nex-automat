"""
Invoice Service - Business logic for invoice operations
Provides data access layer between UI and database
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
            self.logger.info("PostgreSQL client initialized")
        except ImportError:
            self.logger.warning(
                "psycopg2 not installed - using stub data. "
                "Install psycopg2-binary to connect to PostgreSQL."
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            self.logger.warning("Using stub data")

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
        """Get invoices from PostgreSQL (not implemented yet)"""
        # TODO: Implement actual database query
        # For now, return stub data
        self.logger.info("Database query not yet implemented, using stub data")
        return self._get_stub_invoices()

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
            },
            {
                'id': 2,
                'invoice_number': 'FAV-2025-002',
                'invoice_date': '2025-11-11',
                'supplier_name': 'Iný Dodávateľ a.s.',
                'supplier_ico': '87654321',
                'total_amount': Decimal('850.50'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 3,
                'invoice_number': 'FAV-2025-003',
                'invoice_date': '2025-11-10',
                'supplier_name': 'ABC Trading s.r.o.',
                'supplier_ico': '11223344',
                'total_amount': Decimal('2450.75'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 4,
                'invoice_number': 'FAV-2025-004',
                'invoice_date': '2025-11-09',
                'supplier_name': 'XYZ Company a.s.',
                'supplier_ico': '55667788',
                'total_amount': Decimal('675.25'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 5,
                'invoice_number': 'FAV-2025-005',
                'invoice_date': '2025-11-08',
                'supplier_name': 'Slovak Suppliers s.r.o.',
                'supplier_ico': '99887766',
                'total_amount': Decimal('3125.00'),
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
        invoices = self.get_pending_invoices()
        for invoice in invoices:
            if invoice['id'] == invoice_id:
                return invoice
        return None

    def get_invoice_items(self, invoice_id: int) -> List[Dict]:
        """
        Get invoice line items

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
        """Get items from PostgreSQL (not implemented yet)"""
        # TODO: Implement actual database query
        # SELECT * FROM invoice_items_pending WHERE invoice_id = ?
        self.logger.info(f"Database query for items not yet implemented, using stub data")
        return self._get_stub_items(invoice_id)

    def _get_stub_items(self, invoice_id: int) -> List[Dict]:
        """Get stub item data for testing"""
        self.logger.info(f"Using stub items for invoice {invoice_id}")

        # Different items per invoice
        if invoice_id == 1:
            return [
                {
                    'id': 1,
                    'invoice_id': 1,
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
                    'id': 2,
                    'invoice_id': 1,
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
        elif invoice_id == 2:
            return [
                {
                    'id': 3,
                    'invoice_id': 2,
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
        else:
            # Default items for other invoices
            return [
                {
                    'id': 100 + invoice_id,
                    'invoice_id': invoice_id,
                    'plu_code': f'{1000 + invoice_id}',
                    'item_name': f'Test položka {invoice_id}',
                    'category_code': '01',
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
        Save invoice items

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
        """Save items to PostgreSQL (not implemented yet)"""
        # TODO: Implement actual database update
        # UPDATE invoice_items_pending SET ... WHERE id = ?
        self.logger.info("Database save not yet implemented, using stub mode")
        return True

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
