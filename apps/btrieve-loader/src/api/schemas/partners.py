"""
Partner schemas (PAB table).

Based on nexdata.models.pab.PABRecord
"""

from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, Field

from .common import PaginatedResponse


class PartnerType(IntEnum):
    """Partner type enumeration."""

    SUPPLIER = 1
    CUSTOMER = 2
    BOTH = 3


class PartnerBase(BaseModel):
    """Base partner fields."""

    # Basic info
    name1: str = Field(..., max_length=100, description="Company name (line 1)")
    name2: str = Field(default="", max_length=100, description="Company name (line 2)")
    short_name: str = Field(default="", max_length=40, description="Short name")

    # Address
    street: str = Field(default="", max_length=80, description="Street address")
    city: str = Field(default="", max_length=50, description="City")
    zip_code: str = Field(default="", max_length=10, description="ZIP/Postal code")
    country: str = Field(default="", max_length=50, description="Country")

    # Contact
    phone: str = Field(default="", max_length=30, description="Phone number")
    fax: str = Field(default="", max_length=30, description="Fax number")
    email: str = Field(default="", max_length=60, description="Email address")
    web: str = Field(default="", max_length=60, description="Website URL")
    contact_person: str = Field(default="", max_length=50, description="Contact person")

    # Tax info
    ico: str = Field(default="", max_length=20, description="Company ID (IČO)")
    dic: str = Field(default="", max_length=20, description="Tax ID (DIČ)")
    ic_dph: str = Field(default="", max_length=30, description="VAT ID (IČ DPH)")

    # Bank info
    bank_account: str = Field(default="", max_length=30, description="Bank account number")
    bank_code: str = Field(default="", max_length=10, description="Bank code")
    bank_name: str = Field(default="", max_length=60, description="Bank name")
    iban: str = Field(default="", max_length=40, description="IBAN")
    swift: str = Field(default="", max_length=20, description="SWIFT/BIC")

    # Business info
    partner_type: PartnerType = Field(default=PartnerType.BOTH, description="Partner type")
    payment_terms: int = Field(default=14, ge=0, description="Payment terms (days)")
    credit_limit: float = Field(default=0.0, ge=0, description="Credit limit")
    discount_percent: float = Field(default=0.0, ge=0, le=100, description="Discount %")

    # Status
    active: bool = Field(default=True, description="Is active")
    vat_payer: bool = Field(default=True, description="Is VAT payer")

    # Notes
    note: str = Field(default="", max_length=200, description="Note")


class PartnerCreate(PartnerBase):
    """Schema for creating a partner."""

    pab_code: int | None = Field(default=None, description="Partner code (auto-generated if not provided)")


class Partner(PartnerBase):
    """Full partner schema (read)."""

    pab_code: int = Field(..., description="Partner code")
    mod_user: str = Field(default="", description="Last modified by")
    mod_date: datetime | None = Field(default=None, description="Last modified date")

    class Config:
        from_attributes = True

    @classmethod
    def from_pab_record(cls, record) -> "Partner":
        """Create Partner from PABRecord."""
        return cls(
            pab_code=record.pab_code,
            name1=record.name1,
            name2=record.name2,
            short_name=record.short_name,
            street=record.street,
            city=record.city,
            zip_code=record.zip_code,
            country=record.country,
            phone=record.phone,
            fax=record.fax,
            email=record.email,
            web=record.web,
            contact_person=record.contact_person,
            ico=record.ico,
            dic=record.dic,
            ic_dph=record.ic_dph,
            bank_account=record.bank_account,
            bank_code=record.bank_code,
            bank_name=record.bank_name,
            iban=record.iban,
            swift=record.swift,
            partner_type=PartnerType(record.partner_type) if record.partner_type in [1, 2, 3] else PartnerType.BOTH,
            payment_terms=record.payment_terms,
            credit_limit=record.credit_limit,
            discount_percent=record.discount_percent,
            active=record.active,
            vat_payer=record.vat_payer,
            note=record.note,
            mod_user=record.mod_user,
            mod_date=record.mod_date,
        )

    @property
    def full_name(self) -> str:
        """Get full company name."""
        if self.name2:
            return f"{self.name1} {self.name2}".strip()
        return self.name1

    @property
    def full_address(self) -> str:
        """Get full address as single line."""
        parts = [self.street, self.city, self.zip_code, self.country]
        return ", ".join([p for p in parts if p])

    @property
    def is_supplier(self) -> bool:
        """Check if partner is supplier."""
        return self.partner_type in [PartnerType.SUPPLIER, PartnerType.BOTH]

    @property
    def is_customer(self) -> bool:
        """Check if partner is customer."""
        return self.partner_type in [PartnerType.CUSTOMER, PartnerType.BOTH]


class PartnerList(PaginatedResponse[Partner]):
    """Paginated list of partners."""

    pass


class PartnerSearch(BaseModel):
    """Partner search parameters."""

    query: str | None = Field(default=None, description="Search query (name, ICO, etc.)")
    partner_type: PartnerType | None = Field(default=None, description="Filter by type")
    city: str | None = Field(default=None, description="Filter by city")
    active: bool | None = Field(default=None, description="Filter by active status")
