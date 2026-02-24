"""
Document schemas (TSH/TSI tables).

Based on nexdata.models.tsh.TSHRecord and nexdata.models.tsi.TSIRecord
"""

from datetime import date, datetime
from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel, Field

from .common import PaginatedResponse


class DocumentType(IntEnum):
    """Document type enumeration."""

    RECEIPT = 1  # Príjem
    ISSUE = 2  # Výdaj
    TRANSFER = 3  # Transfer


class DocumentStatus(IntEnum):
    """Document status enumeration."""

    DRAFT = 1
    CONFIRMED = 2
    SHIPPED = 3
    CANCELLED = 4


class PaymentMethod(IntEnum):
    """Payment method enumeration."""

    CASH = 1
    TRANSFER = 2
    CARD = 3


class DocumentHeaderBase(BaseModel):
    """Base document header fields."""

    doc_type: DocumentType = Field(
        default=DocumentType.RECEIPT, description="Document type"
    )
    doc_date: date | None = Field(default=None, description="Document date")
    delivery_date: date | None = Field(default=None, description="Delivery date")
    due_date: date | None = Field(default=None, description="Due date")

    # Partner
    pab_code: int = Field(..., description="Partner code")
    pab_name: str = Field(
        default="", max_length=100, description="Partner name (cached)"
    )
    pab_address: str = Field(
        default="", max_length=150, description="Partner address (cached)"
    )
    pab_ico: str = Field(default="", max_length=20, description="Partner ICO (cached)")
    pab_dic: str = Field(default="", max_length=20, description="Partner DIC (cached)")

    # Financial
    currency: str = Field(default="EUR", max_length=4, description="Currency code")
    exchange_rate: Decimal = Field(default=Decimal("1.0"), description="Exchange rate")

    # References
    invoice_number: str = Field(default="", max_length=30, description="Invoice number")
    order_number: str = Field(default="", max_length=30, description="Order number")
    internal_note: str = Field(default="", max_length=200, description="Internal note")
    public_note: str = Field(default="", max_length=200, description="Public note")

    # Payment
    payment_method: PaymentMethod = Field(
        default=PaymentMethod.TRANSFER, description="Payment method"
    )
    payment_terms: int = Field(default=14, ge=0, description="Payment terms (days)")

    # Warehouse
    warehouse_code: int = Field(default=1, description="Warehouse code")


class DocumentHeader(DocumentHeaderBase):
    """Full document header schema (read)."""

    doc_number: str = Field(..., max_length=20, description="Document number")

    # Amounts (calculated)
    amount_base: Decimal = Field(default=Decimal("0.00"), description="Base amount")
    amount_vat: Decimal = Field(default=Decimal("0.00"), description="VAT amount")
    amount_total: Decimal = Field(default=Decimal("0.00"), description="Total amount")

    # VAT breakdown
    vat_20_base: Decimal = Field(default=Decimal("0.00"), description="VAT 20% base")
    vat_20_amount: Decimal = Field(
        default=Decimal("0.00"), description="VAT 20% amount"
    )
    vat_10_base: Decimal = Field(default=Decimal("0.00"), description="VAT 10% base")
    vat_10_amount: Decimal = Field(
        default=Decimal("0.00"), description="VAT 10% amount"
    )
    vat_0_base: Decimal = Field(default=Decimal("0.00"), description="VAT 0% base")

    # Status
    status: DocumentStatus = Field(
        default=DocumentStatus.DRAFT, description="Document status"
    )
    locked: bool = Field(default=False, description="Is locked")
    posted: bool = Field(default=False, description="Is posted")
    paid: bool = Field(default=False, description="Is paid")
    paid_date: date | None = Field(default=None, description="Payment date")
    paid_amount: Decimal = Field(default=Decimal("0.00"), description="Paid amount")

    # Audit
    mod_user: str = Field(default="", description="Last modified by")
    mod_date: datetime | None = Field(default=None, description="Last modified date")

    class Config:
        from_attributes = True

    @classmethod
    def from_tsh_record(cls, record) -> "DocumentHeader":
        """Create DocumentHeader from TSHRecord."""
        return cls(
            doc_number=record.doc_number,
            doc_type=DocumentType(record.doc_type)
            if record.doc_type in [1, 2, 3]
            else DocumentType.RECEIPT,
            doc_date=record.doc_date,
            delivery_date=record.delivery_date,
            due_date=record.due_date,
            pab_code=record.pab_code,
            pab_name=record.pab_name,
            pab_address=record.pab_address,
            pab_ico=record.pab_ico,
            pab_dic=record.pab_dic,
            pab_ic_dph=record.pab_ic_dph if hasattr(record, "pab_ic_dph") else "",
            currency=record.currency,
            exchange_rate=record.exchange_rate,
            amount_base=record.amount_base,
            amount_vat=record.amount_vat,
            amount_total=record.amount_total,
            vat_20_base=record.vat_20_base,
            vat_20_amount=record.vat_20_amount,
            vat_10_base=record.vat_10_base,
            vat_10_amount=record.vat_10_amount,
            vat_0_base=record.vat_0_base,
            payment_method=PaymentMethod(record.payment_method)
            if record.payment_method in [1, 2, 3]
            else PaymentMethod.TRANSFER,
            payment_terms=record.payment_terms,
            paid=record.paid,
            paid_date=record.paid_date,
            paid_amount=record.paid_amount,
            invoice_number=record.invoice_number,
            order_number=record.order_number,
            internal_note=record.internal_note,
            public_note=record.public_note,
            status=DocumentStatus(record.status)
            if hasattr(record, "status") and record.status in [1, 2, 3, 4]
            else DocumentStatus.DRAFT,
            locked=record.locked if hasattr(record, "locked") else False,
            posted=record.posted if hasattr(record, "posted") else False,
            warehouse_code=record.warehouse_code,
            mod_user=record.mod_user if hasattr(record, "mod_user") else "",
            mod_date=record.mod_date if hasattr(record, "mod_date") else None,
        )


class DocumentHeaderList(PaginatedResponse[DocumentHeader]):
    """Paginated list of document headers."""

    pass


class DocumentItemBase(BaseModel):
    """Base document item fields."""

    gs_code: int = Field(..., description="Product code")
    gs_name: str = Field(default="", max_length=80, description="Product name (cached)")
    bar_code: str = Field(default="", max_length=15, description="Barcode used")

    quantity: Decimal = Field(..., gt=0, description="Quantity")
    unit: str = Field(default="ks", max_length=10, description="Unit of measure")
    unit_coef: Decimal = Field(default=Decimal("1.0"), description="Unit coefficient")

    price_unit: Decimal = Field(..., ge=0, description="Unit price (excl. VAT)")
    price_unit_vat: Decimal = Field(
        default=Decimal("0.00"), ge=0, description="Unit price (incl. VAT)"
    )
    vat_rate: Decimal = Field(
        default=Decimal("20.0"), ge=0, le=100, description="VAT rate %"
    )
    discount_percent: Decimal = Field(
        default=Decimal("0.0"), ge=0, le=100, description="Discount %"
    )

    warehouse_code: int = Field(default=1, description="Warehouse code")
    batch_number: str = Field(default="", max_length=30, description="Batch number")
    serial_number: str = Field(default="", max_length=30, description="Serial number")
    note: str = Field(default="", max_length=100, description="Item note")
    supplier_item_code: str = Field(
        default="", max_length=30, description="Supplier item code"
    )


class DocumentItem(DocumentItemBase):
    """Full document item schema (read)."""

    doc_number: str = Field(..., max_length=20, description="Document number")
    line_number: int = Field(..., ge=1, description="Line number")

    # Calculated totals
    line_base: Decimal = Field(default=Decimal("0.00"), description="Line base amount")
    line_vat: Decimal = Field(default=Decimal("0.00"), description="Line VAT amount")
    line_total: Decimal = Field(
        default=Decimal("0.00"), description="Line total amount"
    )

    status: int = Field(default=1, description="Item status")
    mod_user: str = Field(default="", description="Last modified by")
    mod_date: datetime | None = Field(default=None, description="Last modified date")

    class Config:
        from_attributes = True

    @classmethod
    def from_tsi_record(cls, record) -> "DocumentItem":
        """Create DocumentItem from TSIRecord."""
        return cls(
            doc_number=record.doc_number,
            line_number=record.line_number,
            gs_code=record.gs_code,
            gs_name=record.gs_name,
            bar_code=record.bar_code,
            quantity=record.quantity,
            unit=record.unit,
            unit_coef=record.unit_coef,
            price_unit=record.price_unit,
            price_unit_vat=record.price_unit_vat,
            vat_rate=record.vat_rate,
            discount_percent=record.discount_percent,
            line_base=record.line_base,
            line_vat=record.line_vat,
            line_total=record.line_total,
            warehouse_code=record.warehouse_code,
            batch_number=record.batch_number,
            serial_number=record.serial_number,
            note=record.note,
            supplier_item_code=record.supplier_item_code,
            status=record.status,
            mod_user=record.mod_user if hasattr(record, "mod_user") else "",
            mod_date=record.mod_date if hasattr(record, "mod_date") else None,
        )


class DocumentItemList(PaginatedResponse[DocumentItem]):
    """Paginated list of document items."""

    pass


class DocumentWithItems(BaseModel):
    """Complete document with header and items."""

    header: DocumentHeader
    items: list[DocumentItem] = Field(default_factory=list)

    @property
    def item_count(self) -> int:
        """Number of items."""
        return len(self.items)
