"""Unified invoice models for ANDROS multi-supplier API integration.

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

    # Základné údaje položky
    line_number: int
    product_code: str  # Kód od dodávateľa
    product_code_type: str  # "ean", "marso_code", "continental_code"
    product_name: str
    quantity: float
    unit: str
    unit_price: float
    total_price: float
    vat_rate: float
    vat_amount: float

    # Voliteľné - alternatívne kódy
    ean: str | None = None
    supplier_product_code: str | None = None

    # NEX Genesis mapovanie (vyplnené po product matching)
    nex_product_id: str | None = None
    nex_product_code: str | None = None
    match_confidence: float | None = None


@dataclass
class UnifiedInvoice:
    """Normalized invoice model - common for PDF and API sources."""

    # Zdroj
    source_type: str  # "api" alebo "pdf"
    supplier_id: str  # napr. "marso", "continental"
    supplier_name: str

    # Hlavička faktúry
    invoice_number: str
    invoice_date: datetime
    external_invoice_id: str  # ID v systéme dodávateľa

    # Sumy
    total_without_vat: float
    total_vat: float
    total_with_vat: float

    # Položky
    items: list[InvoiceItem]

    # Metadata
    fetched_at: datetime
    status: InvoiceStatus

    # Voliteľné - dátumy
    due_date: datetime | None = None
    delivery_date: datetime | None = None

    # Voliteľné - identifikátory dodávateľa
    supplier_ico: str | None = None
    supplier_dic: str | None = None
    supplier_ic_dph: str | None = None

    # Voliteľné - mena
    currency: str = "EUR"

    # Voliteľné - archív pôvodných dát
    raw_xml: str | None = None
    raw_pdf_path: str | None = None
