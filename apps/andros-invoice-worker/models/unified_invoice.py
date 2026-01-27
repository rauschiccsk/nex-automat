"""Unified invoice models for ANDROS multi-supplier API integration.

These models provide a normalized representation of invoices from various sources
(API, PDF) and suppliers (MARSO, CONTINENTAL, etc.).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class InvoiceStatus(Enum):
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
    ean: Optional[str] = None
    supplier_product_code: Optional[str] = None

    # NEX Genesis mapovanie (vyplnené po product matching)
    nex_product_id: Optional[str] = None
    nex_product_code: Optional[str] = None
    match_confidence: Optional[float] = None


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
    due_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None

    # Voliteľné - identifikátory dodávateľa
    supplier_ico: Optional[str] = None
    supplier_dic: Optional[str] = None
    supplier_ic_dph: Optional[str] = None

    # Voliteľné - mena
    currency: str = "EUR"

    # Voliteľné - archív pôvodných dát
    raw_xml: Optional[str] = None
    raw_pdf_path: Optional[str] = None
