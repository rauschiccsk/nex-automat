"""Pydantic models for partner management endpoints."""

import re
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class PartnerCreate(BaseModel):
    """Request body for creating a new partner."""

    code: str
    name: str

    partner_type: Literal["customer", "supplier", "both"] = "customer"

    # Identifikácia
    company_id: Optional[str] = None  # IČO
    tax_id: Optional[str] = None  # DIČ
    vat_id: Optional[str] = None  # IČ DPH
    is_vat_payer: bool = False

    # Sídlo
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: str = "SK"

    # Fakturačná adresa
    billing_street: Optional[str] = None
    billing_city: Optional[str] = None
    billing_zip_code: Optional[str] = None
    billing_country_code: Optional[str] = None

    # Dodacia adresa
    shipping_street: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_zip_code: Optional[str] = None
    shipping_country_code: Optional[str] = None

    # Kontakt
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None

    # Obchodné podmienky
    payment_due_days: int = 14
    credit_limit: float = 0
    discount_percent: float = 0
    price_category: Optional[str] = None
    payment_method: Literal["transfer", "cash", "cod"] = "transfer"
    currency: str = "EUR"

    # Banka
    iban: Optional[str] = None
    bank_name: Optional[str] = None
    swift_bic: Optional[str] = None

    # Poznámky
    notes: Optional[str] = None

    is_active: bool = True

    @field_validator("code")
    @classmethod
    def code_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Kód partnera je povinný")
        if len(v) > 30:
            raise ValueError("Kód partnera môže mať maximálne 30 znakov")
        return v

    @field_validator("name")
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

    @field_validator("vat_id")
    @classmethod
    def vat_id_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if not re.match(r"^[A-Z]{2}\d{8,10}$", v):
            raise ValueError("IČ DPH musí byť vo formáte SK/CZ (napr. SK2021234567)")
        return v

    @field_validator("iban")
    @classmethod
    def iban_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.replace(" ", "").strip()
        if not v:
            return None
        if len(v) > 34:
            raise ValueError("IBAN môže mať maximálne 34 znakov")
        return v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if "@" not in v or "." not in v:
            raise ValueError("Neplatný formát emailu")
        return v

    @field_validator("payment_due_days")
    @classmethod
    def payment_due_days_valid(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Splatnosť musí byť >= 0")
        return v

    @field_validator("credit_limit")
    @classmethod
    def credit_limit_valid(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Kreditný limit musí byť >= 0")
        return v

    @field_validator("discount_percent")
    @classmethod
    def discount_percent_valid(cls, v: float) -> float:
        if v < 0 or v > 100:
            raise ValueError("Zľava musí byť 0-100%")
        return v

    @field_validator("currency")
    @classmethod
    def currency_valid(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) > 3:
            raise ValueError("Kód meny môže mať maximálne 3 znaky")
        return v


class PartnerUpdate(BaseModel):
    """Request body for updating a partner. Code is NOT editable."""

    # Code is captured here so we can detect it and reject with 400.
    # It will never reach the DB update — router rejects it.
    code: Optional[str] = None

    name: Optional[str] = None

    partner_type: Optional[Literal["customer", "supplier", "both"]] = None

    # Identifikácia
    company_id: Optional[str] = None
    tax_id: Optional[str] = None
    vat_id: Optional[str] = None
    is_vat_payer: Optional[bool] = None

    # Sídlo
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None

    # Fakturačná adresa
    billing_street: Optional[str] = None
    billing_city: Optional[str] = None
    billing_zip_code: Optional[str] = None
    billing_country_code: Optional[str] = None

    # Dodacia adresa
    shipping_street: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_zip_code: Optional[str] = None
    shipping_country_code: Optional[str] = None

    # Kontakt
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None

    # Obchodné podmienky
    payment_due_days: Optional[int] = None
    credit_limit: Optional[float] = None
    discount_percent: Optional[float] = None
    price_category: Optional[str] = None
    payment_method: Optional[Literal["transfer", "cash", "cod"]] = None
    currency: Optional[str] = None

    # Banka
    iban: Optional[str] = None
    bank_name: Optional[str] = None
    swift_bic: Optional[str] = None

    # Poznámky
    notes: Optional[str] = None

    is_active: Optional[bool] = None

    @field_validator("name")
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

    @field_validator("vat_id")
    @classmethod
    def vat_id_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if not re.match(r"^[A-Z]{2}\d{8,10}$", v):
            raise ValueError("IČ DPH musí byť vo formáte SK/CZ (napr. SK2021234567)")
        return v

    @field_validator("iban")
    @classmethod
    def iban_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.replace(" ", "").strip()
        if not v:
            return None
        if len(v) > 34:
            raise ValueError("IBAN môže mať maximálne 34 znakov")
        return v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if "@" not in v or "." not in v:
            raise ValueError("Neplatný formát emailu")
        return v

    @field_validator("payment_due_days")
    @classmethod
    def payment_due_days_valid(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("Splatnosť musí byť >= 0")
        return v

    @field_validator("credit_limit")
    @classmethod
    def credit_limit_valid(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("Kreditný limit musí byť >= 0")
        return v

    @field_validator("discount_percent")
    @classmethod
    def discount_percent_valid(cls, v: float | None) -> float | None:
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Zľava musí byť 0-100%")
        return v

    @field_validator("currency")
    @classmethod
    def currency_valid(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().upper()
        if len(v) > 3:
            raise ValueError("Kód meny môže mať maximálne 3 znaky")
        return v


class PartnerResponse(BaseModel):
    """Partner returned from API."""

    id: UUID
    code: str
    name: str

    partner_type: str
    is_supplier: bool
    is_customer: bool

    company_id: str | None = None
    tax_id: str | None = None
    vat_id: str | None = None
    is_vat_payer: bool

    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_code: str | None = None

    billing_street: str | None = None
    billing_city: str | None = None
    billing_zip_code: str | None = None
    billing_country_code: str | None = None

    shipping_street: str | None = None
    shipping_city: str | None = None
    shipping_zip_code: str | None = None
    shipping_country_code: str | None = None

    phone: str | None = None
    mobile: str | None = None
    email: str | None = None
    website: str | None = None
    contact_person: str | None = None

    payment_due_days: int
    credit_limit: float
    discount_percent: float
    price_category: str | None = None
    payment_method: str
    currency: str

    iban: str | None = None
    bank_name: str | None = None
    swift_bic: str | None = None

    notes: str | None = None

    is_active: bool
    created_at: datetime
    updated_at: datetime

    warnings: list[str] | None = None


class PartnerListResponse(BaseModel):
    """Paginated list of partners."""

    items: list[PartnerResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PartnerListParams(BaseModel):
    """Query parameters for partner list."""

    partner_type: Optional[Literal["customer", "supplier", "both"]] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 50
    sort_by: Literal["code", "name", "city", "created_at"] = "code"
    sort_order: Literal["asc", "desc"] = "asc"

    @field_validator("page")
    @classmethod
    def page_valid(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Stránka musí byť >= 1")
        return v

    @field_validator("page_size")
    @classmethod
    def page_size_valid(cls, v: int) -> int:
        if v < 1 or v > 10000:
            raise ValueError("Veľkosť stránky musí byť 1-10000")
        return v
