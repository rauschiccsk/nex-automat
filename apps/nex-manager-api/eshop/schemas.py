"""ESHOP Pydantic schemas — Public, Admin, and MuFis API models."""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================================
# PUBLIC API — Products
# ============================================================================


class EshopProductResponse(BaseModel):
    """Single product response."""

    product_id: int
    sku: str
    name: str
    short_description: Optional[str] = None
    description: Optional[str] = None
    price: Decimal
    price_vat: Decimal
    vat_rate: Decimal
    stock_quantity: int
    image_url: Optional[str] = None
    weight: Optional[Decimal] = None
    is_active: bool


class EshopProductListResponse(BaseModel):
    """List of products."""

    products: List[EshopProductResponse]


# ============================================================================
# PUBLIC API — Orders
# ============================================================================


class OrderItemRequest(BaseModel):
    """Single order item in create request."""

    sku: str
    quantity: int = Field(..., ge=1)


class OrderCreateRequest(BaseModel):
    """Create order request."""

    customer_email: str
    customer_name: str
    customer_phone: Optional[str] = None
    billing_name: str
    billing_name2: Optional[str] = ""
    billing_street: str
    billing_city: str
    billing_zip: str
    billing_country: str = "SK"
    shipping_name: Optional[str] = ""
    shipping_name2: Optional[str] = ""
    shipping_street: Optional[str] = ""
    shipping_city: Optional[str] = ""
    shipping_zip: Optional[str] = ""
    shipping_country: Optional[str] = ""
    ico: Optional[str] = ""
    dic: Optional[str] = ""
    eu_vat_number: Optional[str] = ""
    items: List[OrderItemRequest] = Field(..., min_length=1)
    payment_method: str
    shipping_type: Optional[str] = ""
    note: Optional[str] = ""
    lang: Optional[str] = "sk"
    delivery_point_group: Optional[str] = ""
    delivery_point_id: Optional[str] = ""
    discount_code: Optional[str] = None
    is_company_order: bool = False
    company_name: str | None = None
    company_ico: str | None = None
    company_dic: str | None = None
    company_ic_dph: str | None = None
    billing_postal_code: str | None = None
    create_account: bool = False
    account_password: str | None = None


class OrderCreateResponse(BaseModel):
    """Order creation response."""

    order_number: str
    status: str
    total_amount_vat: Decimal
    currency: str
    payment_url: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Order item in status response."""

    sku: str
    name: str
    quantity: int
    unit_price_vat: Decimal
    vat_rate: Decimal


class OrderStatusResponse(BaseModel):
    """Order status response."""

    order_number: str
    status: str
    payment_status: str
    tracking_number: str
    tracking_link: str
    created_at: datetime
    items: List[OrderItemResponse]


# ============================================================================
# ADMIN API — Orders
# ============================================================================


class AdminOrderListItem(BaseModel):
    """Admin order list item."""

    order_id: int
    order_number: str
    customer_name: str
    customer_email: str
    total_amount_vat: Decimal
    currency: str
    status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime


class AdminOrderListResponse(BaseModel):
    """Admin order list with pagination."""

    orders: List[AdminOrderListItem]
    total: int
    page: int
    page_size: int


class AdminStatusHistoryItem(BaseModel):
    """Status history entry."""

    old_status: Optional[str] = None
    new_status: str
    changed_by: Optional[str] = None
    note: Optional[str] = ""
    created_at: datetime


class AdminOrderDetailResponse(BaseModel):
    """Admin order detail with items and history."""

    order_id: int
    order_number: str
    tenant_id: int
    customer_email: str
    customer_name: str
    customer_phone: Optional[str] = None
    lang: str
    billing_name: str
    billing_name2: str
    billing_street: str
    billing_city: str
    billing_zip: str
    billing_country: str
    shipping_name: str
    shipping_name2: str
    shipping_street: str
    shipping_city: str
    shipping_zip: str
    shipping_country: str
    ico: str
    dic: str
    eu_vat_number: str
    total_amount: Decimal
    total_amount_vat: Decimal
    currency: str
    payment_method: Optional[str] = None
    payment_status: str
    comgate_transaction_id: Optional[str] = None
    shipping_type: str
    shipping_price: Decimal
    delivery_point_group: str
    delivery_point_id: str
    tracking_number: str
    tracking_link: str
    multiple_packages: bool
    status: str
    note: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]
    status_history: List[AdminStatusHistoryItem]


class AdminOrderUpdateRequest(BaseModel):
    """Admin order update request."""

    status: Optional[str] = None
    note: Optional[str] = None


# ============================================================================
# ADMIN API — Products
# ============================================================================


class AdminProductCreateRequest(BaseModel):
    """Admin product create request."""

    sku: str
    name: str
    barcode: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Decimal
    price_vat: Decimal
    vat_rate: Decimal
    stock_quantity: int = 0
    weight: Optional[Decimal] = None
    is_active: bool = True
    sort_order: int = 0


class AdminProductUpdateRequest(BaseModel):
    """Admin product update — all fields optional."""

    sku: Optional[str] = None
    name: Optional[str] = None
    barcode: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[Decimal] = None
    price_vat: Optional[Decimal] = None
    vat_rate: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    weight: Optional[Decimal] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


# ============================================================================
# ADMIN API — Tenants
# ============================================================================


class AdminTenantResponse(BaseModel):
    """Admin tenant response — sanitized (no secrets)."""

    tenant_id: int
    company_name: str
    domain: str
    brand_name: str
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    currency: str
    vat_rate_default: Decimal
    default_lang: str
    is_active: bool
    created_at: datetime


# ============================================================================
# MUFIS API
# ============================================================================


class MufisSetResponse(BaseModel):
    """MuFis set operation response."""

    ok: int
    error: Optional[str] = None


# ============================================================================
# PAYMENT — Comgate
# ============================================================================


class PaymentReturnResponse(BaseModel):
    """Payment return page response — shown after customer returns from gateway."""

    order_number: str
    status: str
    payment_status: str


# ============================================================================
# LEAD CAPTURE
# ============================================================================


class LeadRegisterRequest(BaseModel):
    """Lead registration request."""

    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    gdpr_consent: bool


class LeadRegisterResponse(BaseModel):
    """Lead registration response."""

    lead_id: int
    email: str
    discount_code: str
    discount_percentage: float
    expires_at: str
    message: str


class LeadValidateResponse(BaseModel):
    """Discount code validation response."""

    valid: bool
    discount_percentage: float | None = None
    expires_at: str | None = None
    message: str


class DiscountApplyRequest(BaseModel):
    """Discount code for order."""

    discount_code: str | None = None


# ============================================================================
# CUSTOMER API — Registration, Login, Profile
# ============================================================================


class CustomerRegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str = "SK"
    is_company: bool = False
    company_name: str | None = None
    company_ico: str | None = None
    company_dic: str | None = None
    company_ic_dph: str | None = None


class CustomerLoginRequest(BaseModel):
    email: str
    password: str


class CustomerLoginResponse(BaseModel):
    token: str
    customer_id: int
    email: str
    first_name: str
    last_name: str


class CustomerProfileResponse(BaseModel):
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    street: str | None
    city: str | None
    postal_code: str | None
    country: str
    is_company: bool
    company_name: str | None
    company_ico: str | None
    company_dic: str | None
    company_ic_dph: str | None
