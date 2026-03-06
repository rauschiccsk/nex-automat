"""Pydantic models for Partner Catalog (PAB) module endpoints."""

import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, field_validator


# ---------------------------------------------------------------------------
# Partner Catalog — main table
# ---------------------------------------------------------------------------


class PartnerCatalogCreate(BaseModel):
    """Request body for creating a new partner in partner_catalog."""

    partner_id: int
    partner_code: str
    partner_name: str
    reg_name: Optional[str] = None

    company_id: Optional[str] = None  # IČO
    tax_id: Optional[str] = None  # DIČ
    vat_id: Optional[str] = None  # IČ DPH
    is_vat_payer: bool = False

    is_supplier: bool = False
    is_customer: bool = True

    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: str = "SK"

    is_active: bool = True

    @field_validator("partner_code")
    @classmethod
    def code_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Kód partnera je povinný")
        if len(v) > 30:
            raise ValueError("Kód partnera môže mať maximálne 30 znakov")
        return v

    @field_validator("partner_name")
    @classmethod
    def name_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Názov partnera je povinný")
        if len(v) > 100:
            raise ValueError("Názov partnera môže mať maximálne 100 znakov")
        return v

    @field_validator("company_id")
    @classmethod
    def company_id_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if not re.match(r"^\d+$", v):
            raise ValueError("IČO musí obsahovať len čísla")
        if len(v) > 20:
            raise ValueError("IČO môže mať maximálne 20 znakov")
        return v

    @field_validator("partner_id")
    @classmethod
    def partner_id_valid(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("partner_id musí byť kladné číslo")
        return v


class PartnerCatalogUpdate(BaseModel):
    """Request body for updating a partner. partner_id and partner_code are readonly."""

    partner_name: Optional[str] = None
    reg_name: Optional[str] = None

    company_id: Optional[str] = None
    tax_id: Optional[str] = None
    vat_id: Optional[str] = None
    is_vat_payer: Optional[bool] = None

    is_supplier: Optional[bool] = None
    is_customer: Optional[bool] = None

    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None

    is_active: Optional[bool] = None

    @field_validator("partner_name")
    @classmethod
    def name_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Názov partnera je povinný")
        if len(v) > 100:
            raise ValueError("Názov partnera môže mať maximálne 100 znakov")
        return v


class PartnerCatalogResponse(BaseModel):
    """Partner catalog record returned from API."""

    partner_id: int
    partner_code: str
    partner_name: str
    reg_name: str | None = None

    company_id: str | None = None
    tax_id: str | None = None
    vat_id: str | None = None
    is_vat_payer: bool

    is_supplier: bool
    is_customer: bool

    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_code: str | None = None

    bank_account_count: int = 0
    facility_count: int = 0

    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Aggregated child data (only in detail endpoint)
    extensions: Optional["ExtensionsResponse"] = None
    addresses: Optional[list["AddressResponse"]] = None
    contacts: Optional[list["ContactResponse"]] = None
    texts: Optional[list["TextResponse"]] = None
    bank_accounts: Optional[list["BankAccountResponse"]] = None
    facilities: Optional[list["FacilityResponse"]] = None
    categories: Optional[list["CategoryMappingResponse"]] = None


class PartnerCatalogListResponse(BaseModel):
    """Paginated list of partners from partner_catalog."""

    items: list[PartnerCatalogResponse]
    total: int
    limit: int
    offset: int


# ---------------------------------------------------------------------------
# Extensions (1:1)
# ---------------------------------------------------------------------------


class ExtensionsUpsert(BaseModel):
    """Request body for upserting partner extensions."""

    sale_payment_method_id: Optional[int] = None
    sale_transport_method_id: Optional[int] = None
    sale_payment_due_days: int = 14
    sale_currency_code: str = "EUR"
    sale_price_category: Optional[str] = None
    sale_discount_percent: float = 0
    sale_credit_limit: float = 0

    purchase_payment_method_id: Optional[int] = None
    purchase_transport_method_id: Optional[int] = None
    purchase_payment_due_days: int = 14
    purchase_currency_code: str = "EUR"
    purchase_price_category: Optional[str] = None
    purchase_discount_percent: float = 0

    last_sale_date: Optional[str] = None
    last_purchase_date: Optional[str] = None

    @field_validator("sale_discount_percent", "purchase_discount_percent")
    @classmethod
    def discount_valid(cls, v: float) -> float:
        if v < 0 or v > 100:
            raise ValueError("Zľava musí byť 0-100%")
        return v

    @field_validator("sale_credit_limit")
    @classmethod
    def credit_limit_valid(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Kreditný limit musí byť >= 0")
        return v


class ExtensionsResponse(BaseModel):
    """Extensions record returned from API."""

    partner_id: int
    sale_payment_method_id: int | None = None
    sale_transport_method_id: int | None = None
    sale_payment_due_days: int | None = None
    sale_currency_code: str | None = None
    sale_price_category: str | None = None
    sale_discount_percent: float | None = None
    sale_credit_limit: float | None = None

    purchase_payment_method_id: int | None = None
    purchase_transport_method_id: int | None = None
    purchase_payment_due_days: int | None = None
    purchase_currency_code: str | None = None
    purchase_price_category: str | None = None
    purchase_discount_percent: float | None = None

    last_sale_date: str | None = None
    last_purchase_date: str | None = None

    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


# ---------------------------------------------------------------------------
# Addresses
# ---------------------------------------------------------------------------

_ADDRESS_TYPES = Literal["registered", "correspondence", "invoice"]


class AddressCreate(BaseModel):
    """Request body for creating an address."""

    address_type: _ADDRESS_TYPES
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: str = "SK"


class AddressUpdate(BaseModel):
    """Request body for updating an address."""

    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None


class AddressResponse(BaseModel):
    """Address record returned from API."""

    id: int
    partner_id: int
    address_type: str
    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_code: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------

_CONTACT_TYPES = Literal["address", "person"]


class ContactCreate(BaseModel):
    """Request body for creating a contact."""

    contact_type: _CONTACT_TYPES
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    function_name: Optional[str] = None
    phone_work: Optional[str] = None
    phone_mobile: Optional[str] = None
    phone_private: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None


class ContactUpdate(BaseModel):
    """Request body for updating a contact."""

    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    function_name: Optional[str] = None
    phone_work: Optional[str] = None
    phone_mobile: Optional[str] = None
    phone_private: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None


class ContactResponse(BaseModel):
    """Contact record returned from API."""

    contact_id: int
    partner_id: int
    contact_type: str
    title: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    function_name: str | None = None
    phone_work: str | None = None
    phone_mobile: str | None = None
    phone_private: str | None = None
    fax: str | None = None
    email: str | None = None
    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_code: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Bank Accounts
# ---------------------------------------------------------------------------


class BankAccountCreate(BaseModel):
    """Request body for creating a bank account."""

    iban_code: Optional[str] = None
    swift_code: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_seat: Optional[str] = None
    vs_sale: Optional[str] = None
    vs_purchase: Optional[str] = None
    is_primary: bool = False


class BankAccountUpdate(BaseModel):
    """Request body for updating a bank account."""

    iban_code: Optional[str] = None
    swift_code: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_seat: Optional[str] = None
    vs_sale: Optional[str] = None
    vs_purchase: Optional[str] = None
    is_primary: Optional[bool] = None


class BankAccountResponse(BaseModel):
    """Bank account record returned from API."""

    account_id: int
    partner_id: int
    iban_code: str | None = None
    swift_code: str | None = None
    account_number: str | None = None
    bank_name: str | None = None
    bank_seat: str | None = None
    vs_sale: str | None = None
    vs_purchase: str | None = None
    is_primary: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Categories (M:N mapping)
# ---------------------------------------------------------------------------


class CategoryAssign(BaseModel):
    """Request body for assigning a category to a partner."""

    category_id: int
    category_type: Literal["supplier", "customer"]


class CategoryMappingResponse(BaseModel):
    """Category mapping record returned from API."""

    id: int
    partner_id: int
    category_id: int
    category_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Texts
# ---------------------------------------------------------------------------


class TextUpsert(BaseModel):
    """Request body for upserting texts."""

    text_type: Literal["owner_name", "description", "notice"]
    line_number: int = 1
    language: str = "sk"
    text_content: Optional[str] = None

    @field_validator("line_number")
    @classmethod
    def line_number_valid(cls, v: int) -> int:
        if v < 1:
            raise ValueError("line_number musí byť >= 1")
        return v


class TextResponse(BaseModel):
    """Text record returned from API."""

    text_id: int
    partner_id: int
    text_type: str
    line_number: int
    language: str
    text_content: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Facilities
# ---------------------------------------------------------------------------


class FacilityCreate(BaseModel):
    """Request body for creating a facility."""

    facility_name: str
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: str = "SK"
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    transport_method_id: Optional[int] = None

    @field_validator("facility_name")
    @classmethod
    def name_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Názov prevádzky je povinný")
        if len(v) > 100:
            raise ValueError("Názov prevádzky môže mať maximálne 100 znakov")
        return v


class FacilityUpdate(BaseModel):
    """Request body for updating a facility."""

    facility_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    transport_method_id: Optional[int] = None


class FacilityResponse(BaseModel):
    """Facility record returned from API."""

    facility_id: int
    partner_id: int
    facility_name: str
    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_code: str | None = None
    phone: str | None = None
    fax: str | None = None
    email: str | None = None
    transport_method_id: int | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
