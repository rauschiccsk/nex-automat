"""Invoice head model."""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class FileStatus(str, Enum):
    """File status enum matching database constraint."""
    RECEIVED = "received"
    STAGED = "staged"
    ARCHIVED = "archived"


class InvoiceHead(BaseModel):
    """Supplier invoice head model."""

    id: int

    # XML extracted fields
    xml_invoice_number: Optional[str] = None
    xml_variable_symbol: Optional[str] = None
    xml_issue_date: Optional[date] = None
    xml_tax_point_date: Optional[date] = None
    xml_due_date: Optional[date] = None
    xml_currency: Optional[str] = None
    xml_supplier_ico: Optional[str] = None
    xml_supplier_name: Optional[str] = None
    xml_supplier_dic: Optional[str] = None
    xml_supplier_ic_dph: Optional[str] = None
    xml_iban: Optional[str] = None
    xml_swift: Optional[str] = None
    xml_total_without_vat: Optional[Decimal] = None
    xml_total_vat: Optional[Decimal] = None
    xml_total_with_vat: Optional[Decimal] = None

    # NEX Genesis fields
    nex_supplier_id: Optional[int] = None
    nex_supplier_modify_id: Optional[int] = None
    nex_iban: Optional[str] = None
    nex_swift: Optional[str] = None
    nex_stock_id: Optional[int] = None
    nex_book_num: Optional[int] = None
    nex_payment_method_id: Optional[int] = None
    nex_price_list_id: Optional[int] = None
    nex_document_id: Optional[int] = None
    nex_invoice_doc_id: Optional[int] = None
    nex_delivery_doc_id: Optional[int] = None

    # Status fields
    status: Optional[str] = None
    file_status: FileStatus = FileStatus.RECEIVED

    # File paths (correct column names)
    pdf_file_path: Optional[str] = None
    xml_file_path: Optional[str] = None
    file_basename: Optional[str] = None

    # Matching stats
    item_count: int = 0
    items_matched: int = 0
    match_percent: Optional[Decimal] = None
    validation_status: Optional[str] = None
    validation_errors: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    imported_at: Optional[datetime] = None

    class Config:
        from_attributes = True
