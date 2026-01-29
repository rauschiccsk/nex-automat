"""Invoice head model."""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class FileStatus(str, Enum):
    """File status enum matching database constraint."""

    RECEIVED = "received"
    STAGED = "staged"
    ARCHIVED = "archived"


class InvoiceHead(BaseModel):
    """Supplier invoice head model."""

    id: int

    # XML extracted fields
    xml_invoice_number: str | None = None
    xml_variable_symbol: str | None = None
    xml_issue_date: date | None = None
    xml_tax_point_date: date | None = None
    xml_due_date: date | None = None
    xml_currency: str | None = None
    xml_supplier_ico: str | None = None
    xml_supplier_name: str | None = None
    xml_supplier_dic: str | None = None
    xml_supplier_ic_dph: str | None = None
    xml_iban: str | None = None
    xml_swift: str | None = None
    xml_total_without_vat: Decimal | None = None
    xml_total_vat: Decimal | None = None
    xml_total_with_vat: Decimal | None = None

    # NEX Genesis fields
    nex_supplier_id: int | None = None
    nex_supplier_modify_id: int | None = None
    nex_iban: str | None = None
    nex_swift: str | None = None
    nex_stock_id: int | None = None
    nex_book_num: int | None = None
    nex_payment_method_id: int | None = None
    nex_price_list_id: int | None = None
    nex_document_id: int | None = None
    nex_invoice_doc_id: int | None = None
    nex_delivery_doc_id: int | None = None

    # Status fields
    status: str | None = None
    file_status: FileStatus = FileStatus.RECEIVED

    # File paths (correct column names)
    pdf_file_path: str | None = None
    xml_file_path: str | None = None
    file_basename: str | None = None

    # Matching stats
    item_count: int = 0
    items_matched: int = 0
    match_percent: Decimal | None = None
    validation_status: str | None = None
    validation_errors: str | None = None

    # Timestamps
    created_at: datetime | None = None
    updated_at: datetime | None = None
    processed_at: datetime | None = None
    imported_at: datetime | None = None

    class Config:
        from_attributes = True
