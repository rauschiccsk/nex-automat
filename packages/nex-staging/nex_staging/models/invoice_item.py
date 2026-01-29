"""Invoice item model."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class InvoiceItem(BaseModel):
    """Supplier invoice item model."""

    id: int
    invoice_head_id: int

    # XML extracted fields
    xml_line_number: int | None = None
    xml_seller_code: str | None = None
    xml_ean: str | None = None
    xml_product_name: str | None = None
    xml_quantity: Decimal | None = None
    xml_unit: str | None = None
    xml_unit_price: Decimal | None = None
    xml_unit_price_vat: Decimal | None = None
    xml_total_price: Decimal | None = None
    xml_total_price_vat: Decimal | None = None
    xml_vat_rate: Decimal | None = None

    # NEX Genesis matched fields
    nex_product_id: int | None = None
    nex_product_name: str | None = None
    nex_ean: str | None = None
    nex_stock_code: str | None = None
    nex_stock_id: int | None = None

    # Matching info
    matched: bool = False
    matched_by: str | None = None
    match_confidence: Decimal | None = None

    # Editing
    edited_unit_price: Decimal | None = None

    # Status
    validation_status: str | None = None

    # Timestamps
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
