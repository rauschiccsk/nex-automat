"""Unified invoice models for multi-supplier API integration.

These models provide a normalized representation of invoices from various sources
(API, PDF) and suppliers (MARSO, CONTINENTAL, etc.).
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class InvoiceStatus(str, Enum):
    """Status of an invoice in the processing pipeline."""

    PENDING = "pending"
    FETCHED = "fetched"
    PROCESSED = "processed"
    ACKNOWLEDGED = "acknowledged"
    ERROR = "error"


@dataclass
class InvoiceItem:
    """Single line item on an invoice."""

    line_number: int
    product_code: str
    product_code_type: str
    product_name: str
    quantity: float
    unit: str
    unit_price: float
    total_price: float
    vat_rate: float
    vat_amount: float

    ean: str | None = None
    supplier_product_code: str | None = None

    nex_product_id: str | None = None
    nex_product_code: str | None = None
    match_confidence: float | None = None


@dataclass
class UnifiedInvoice:
    """Normalized invoice model - common for PDF and API sources."""

    source_type: str
    supplier_id: str
    supplier_name: str

    invoice_number: str
    invoice_date: datetime
    external_invoice_id: str

    total_without_vat: float
    total_vat: float
    total_with_vat: float

    items: list[InvoiceItem]

    fetched_at: datetime
    status: InvoiceStatus

    due_date: datetime | None = None
    delivery_date: datetime | None = None

    supplier_ico: str | None = None
    supplier_dic: str | None = None
    supplier_ic_dph: str | None = None

    currency: str = "EUR"

    raw_xml: str | None = None
    raw_pdf_path: str | None = None
