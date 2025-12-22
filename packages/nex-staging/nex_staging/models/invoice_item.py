"""Invoice item model."""

from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class InvoiceItem(BaseModel):
    """Supplier invoice item model."""

    id: int
    invoice_head_id: int

    # XML extracted fields
    xml_line_number: Optional[int] = None
    xml_seller_code: Optional[str] = None
    xml_ean: Optional[str] = None
    xml_product_name: Optional[str] = None
    xml_quantity: Optional[Decimal] = None
    xml_unit: Optional[str] = None
    xml_unit_price: Optional[Decimal] = None
    xml_unit_price_vat: Optional[Decimal] = None
    xml_total_price: Optional[Decimal] = None
    xml_total_price_vat: Optional[Decimal] = None
    xml_vat_rate: Optional[Decimal] = None

    # NEX Genesis matched fields
    nex_product_id: Optional[int] = None
    nex_product_name: Optional[str] = None
    nex_ean: Optional[str] = None
    nex_stock_code: Optional[str] = None
    nex_stock_id: Optional[int] = None

    # Matching info
    matched: bool = False
    matched_by: Optional[str] = None
    match_confidence: Optional[Decimal] = None

    # Editing
    edited_unit_price: Optional[Decimal] = None

    # Status
    validation_status: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
