"""ESHOP API endpoints — Public, Admin, Payment, and MuFis integration.

Public endpoints (X-Eshop-Token auth):
  GET    /api/eshop/products                    — list active products
  GET    /api/eshop/products/{sku}              — single product
  POST   /api/eshop/orders                      — create order
  GET    /api/eshop/orders/{order_number}        — order status

Payment endpoints (NO auth — called by Comgate / customer browser):
  POST   /api/eshop/payment/callback            — Comgate payment notification
  GET    /api/eshop/payment/return              — customer return from gateway

Admin endpoints (JWT auth):
  GET    /api/eshop/admin/orders                — paginated order list
  GET    /api/eshop/admin/orders/{order_id}     — order detail
  PATCH  /api/eshop/admin/orders/{order_id}     — update order
  GET    /api/eshop/admin/products              — all products
  POST   /api/eshop/admin/products              — create product
  PATCH  /api/eshop/admin/products/{product_id} — update product
  DELETE /api/eshop/admin/products/{product_id} — soft delete product
  GET    /api/eshop/admin/tenants               — list tenants
  GET    /api/eshop/admin/tenants/{tenant_id}   — tenant detail

MuFis endpoints (API-KEY auth, form-urlencoded):
  POST   /api/eshop/mufis/getOrder              — list orders
  POST   /api/eshop/mufis/setOrder              — update orders
  POST   /api/eshop/mufis/getProduct            — list products
  POST   /api/eshop/mufis/setProduct            — update stock
"""

import asyncio
import hmac
import json
import logging
import math
import os
import re
import secrets
from decimal import Decimal
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Header,
    HTTPException,
    Query,
    Response,
    status,
)

logger = logging.getLogger(__name__)

from auth.dependencies import require_permission
from database import get_db

from .dependencies import get_tenant_by_mufis_key, get_tenant_by_token
from .mufis_auth import verify_mufis_access
from .mufis_status import map_mufis_status
from .mufis_webhook import notify_mufis_order_change
from .comgate import ComgateError, get_comgate_client
from .email_service import EshopEmailService
from .schemas import (
    AdminOrderDetailResponse,
    AdminOrderListItem,
    AdminOrderListResponse,
    AdminOrderUpdateRequest,
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
    AdminStatusHistoryItem,
    AdminTenantResponse,
    CustomerLoginRequest,
    CustomerLoginResponse,
    CustomerProfileResponse,
    CustomerRegisterRequest,
    EshopProductListResponse,
    EshopProductResponse,
    LeadRegisterRequest,
    LeadRegisterResponse,
    LeadValidateResponse,
    OrderCreateRequest,
    OrderCreateResponse,
    OrderItemResponse,
    OrderStatusResponse,
    PaymentReturnResponse,
)
from .utils import generate_order_number

router = APIRouter(prefix="/api/eshop", tags=["ESHOP"])

# MuFis pagination constant
MUFIS_PAGE_SIZE = 50


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _dec(v):
    """Convert Decimal to float for JSON serialization."""
    return float(v) if isinstance(v, Decimal) else v


# ============================================================================
# PUBLIC — Products
# ============================================================================


@router.get("/products", response_model=EshopProductListResponse)
def list_products(
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """List active products for tenant."""
    cur = db.cursor()
    cur.execute(
        "SELECT product_id, sku, name, short_description, description, "
        "price, price_vat, vat_rate, stock_quantity, image_url, weight, is_active "
        "FROM eshop_products "
        "WHERE tenant_id = %s AND is_active = TRUE "
        "ORDER BY sort_order",
        (tenant["tenant_id"],),
    )
    products = [
        EshopProductResponse(
            product_id=r[0],
            sku=r[1],
            name=r[2],
            short_description=r[3],
            description=r[4],
            price=r[5],
            price_vat=r[6],
            vat_rate=r[7],
            stock_quantity=r[8],
            image_url=r[9],
            weight=r[10],
            is_active=r[11],
        )
        for r in cur.fetchall()
    ]
    return EshopProductListResponse(products=products)


@router.get("/products/{sku}", response_model=EshopProductResponse)
def get_product(
    sku: str,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Get single product by SKU."""
    cur = db.cursor()
    cur.execute(
        "SELECT product_id, sku, name, short_description, description, "
        "price, price_vat, vat_rate, stock_quantity, image_url, weight, is_active "
        "FROM eshop_products "
        "WHERE tenant_id = %s AND sku = %s AND is_active = TRUE",
        (tenant["tenant_id"], sku),
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt '{sku}' nebol nájdený",
        )
    return EshopProductResponse(
        product_id=r[0],
        sku=r[1],
        name=r[2],
        short_description=r[3],
        description=r[4],
        price=r[5],
        price_vat=r[6],
        vat_rate=r[7],
        stock_quantity=r[8],
        image_url=r[9],
        weight=r[10],
        is_active=r[11],
    )


# ============================================================================
# PUBLIC — Orders
# ============================================================================


@router.post("/orders", response_model=OrderCreateResponse)
async def create_order(
    body: OrderCreateRequest,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
    auth_header: str = Header(None, alias="Authorization"),
):
    """Create a new order. Prices are always taken from DB, never from request."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    # --- Resolve customer_id from Bearer token or account creation ---
    customer_id = None

    # 1. If Bearer token provided, link order to that customer
    if auth_header and auth_header.startswith("Bearer "):
        try:
            customer = _get_customer_from_token(auth_header, db)
            customer_id = customer["id"]
        except HTTPException:
            pass  # Ignore invalid token — order can proceed without customer

    # 2. If create_account requested, create customer first
    if body.create_account and body.account_password and customer_id is None:
        import bcrypt

        # Check uniqueness
        cur.execute(
            "SELECT id FROM eshop_customers "
            "WHERE tenant_id = %s AND email = %s AND is_active = TRUE",
            (tenant_id, body.customer_email),
        )
        existing = cur.fetchone()
        if existing:
            customer_id = existing[0]
        else:
            pw_hash = bcrypt.hashpw(
                body.account_password.encode(), bcrypt.gensalt()
            ).decode()
            cur.execute(
                "INSERT INTO eshop_customers ("
                "tenant_id, email, password_hash, first_name, last_name"
                ") VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (
                    tenant_id,
                    body.customer_email,
                    pw_hash,
                    body.customer_name.split(" ", 1)[0] if body.customer_name else "",
                    body.customer_name.split(" ", 1)[1]
                    if body.customer_name and " " in body.customer_name
                    else "",
                ),
            )
            customer_id = cur.fetchone()[0]

    # Validate items and collect product data from DB
    order_items = []
    total_amount = Decimal("0")
    total_amount_vat = Decimal("0")

    for item in body.items:
        cur.execute(
            "SELECT product_id, sku, name, price, price_vat, vat_rate, is_active "
            "FROM eshop_products "
            "WHERE tenant_id = %s AND sku = %s",
            (tenant_id, item.sku),
        )
        product = cur.fetchone()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Produkt so SKU '{item.sku}' nebol nájdený",
            )
        if not product[6]:  # is_active
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Produkt '{item.sku}' nie je aktívny",
            )

        product_price = Decimal(str(product[3]))
        product_price_vat = Decimal(str(product[4]))
        product_vat_rate = Decimal(str(product[5]))

        total_amount += product_price * item.quantity
        total_amount_vat += product_price_vat * item.quantity

        order_items.append(
            {
                "product_id": product[0],
                "sku": product[1],
                "name": product[2],
                "quantity": item.quantity,
                "unit_price": product_price,
                "unit_price_vat": product_price_vat,
                "vat_rate": product_vat_rate,
            }
        )

    # Add shipping price
    shipping_price = Decimal("0")
    if body.shipping_type:
        # Shipping price could come from a config table in the future
        pass
    total_amount_vat += shipping_price
    total_amount += shipping_price

    # Generate order number
    order_number = generate_order_number(tenant_id, tenant["brand_name"], db)

    # Insert order (including company fields and customer_id)
    cur.execute(
        "INSERT INTO eshop_orders ("
        "tenant_id, order_number, customer_email, customer_name, customer_phone, "
        "lang, billing_name, billing_name2, billing_street, billing_city, "
        "billing_zip, billing_country, shipping_name, shipping_name2, "
        "shipping_street, shipping_city, shipping_zip, shipping_country, "
        "ico, dic, eu_vat_number, total_amount, total_amount_vat, "
        "currency, payment_method, shipping_type, shipping_price, note, "
        "delivery_point_group, delivery_point_id, status, payment_status, "
        "is_company_order, company_name, company_ico, company_dic, "
        "company_ic_dph, billing_postal_code, customer_id"
        ") VALUES ("
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s"
        ") RETURNING order_id",
        (
            tenant_id,
            order_number,
            body.customer_email,
            body.customer_name,
            body.customer_phone or "",
            body.lang or "sk",
            body.billing_name,
            body.billing_name2 or "",
            body.billing_street,
            body.billing_city,
            body.billing_zip,
            body.billing_country,
            body.shipping_name or "",
            body.shipping_name2 or "",
            body.shipping_street or "",
            body.shipping_city or "",
            body.shipping_zip or "",
            body.shipping_country or "",
            body.ico or "",
            body.dic or "",
            body.eu_vat_number or "",
            float(total_amount),
            float(total_amount_vat),
            tenant["currency"],
            body.payment_method,
            body.shipping_type or "",
            float(shipping_price),
            body.note or "",
            body.delivery_point_group or "",
            body.delivery_point_id or "",
            "new",
            "pending",
            body.is_company_order,
            body.company_name if body.is_company_order else None,
            body.company_ico if body.is_company_order else None,
            body.company_dic if body.is_company_order else None,
            body.company_ic_dph if body.is_company_order else None,
            body.billing_postal_code,
            customer_id,
        ),
    )
    order_row = cur.fetchone()
    order_id = order_row[0]

    # Insert order items
    for oi in order_items:
        cur.execute(
            "INSERT INTO eshop_order_items ("
            "order_id, product_id, sku, name, quantity, "
            "unit_price, unit_price_vat, vat_rate, item_type"
            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                order_id,
                oi["product_id"],
                oi["sku"],
                oi["name"],
                oi["quantity"],
                float(oi["unit_price"]),
                float(oi["unit_price_vat"]),
                float(oi["vat_rate"]),
                "product",
            ),
        )

    # --- Discount code processing ---
    discount_code_applied = None
    if body.discount_code:
        cur.execute(
            "SELECT lead_id, discount_percentage, expires_at, is_active, "
            "first_order_id "
            "FROM eshop_leads "
            "WHERE discount_code = %s AND tenant_id = %s",
            (body.discount_code, tenant_id),
        )
        lead = cur.fetchone()
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Neplatný zľavový kód",
            )
        if not lead[3]:  # is_active
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Zľavový kód nie je aktívny",
            )
        if lead[4] is not None:  # first_order_id
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Zľavový kód už bol použitý",
            )

        from datetime import datetime, timezone

        now_utc = datetime.now(timezone.utc)
        if lead[2] <= now_utc:  # expires_at
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Zľavový kód expiroval",
            )

        discount_percentage = float(lead[1])
        total_products_price = float(total_amount_vat)
        discount_amount = round(total_products_price * (discount_percentage / 100), 2)

        cur.execute(
            "INSERT INTO eshop_order_items ("
            "order_id, product_id, sku, name, quantity, "
            "unit_price, unit_price_vat, vat_rate, item_type"
            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                order_id,
                None,
                "DISCOUNT",
                f"Zľava {discount_percentage}% (kód: {body.discount_code})",
                1,
                float(-discount_amount),
                float(-discount_amount),
                0,
                "discount",
            ),
        )

        # Adjust totals
        total_amount_vat -= Decimal(str(discount_amount))
        total_amount -= Decimal(str(discount_amount))

        # Update order totals
        cur.execute(
            "UPDATE eshop_orders SET total_amount = %s, total_amount_vat = %s "
            "WHERE order_id = %s",
            (float(total_amount), float(total_amount_vat), order_id),
        )

        discount_code_applied = body.discount_code

    # Insert initial status history
    cur.execute(
        "INSERT INTO eshop_order_status_history ("
        "order_id, old_status, new_status, changed_by, note"
        ") VALUES (%s, %s, %s, %s, %s)",
        (order_id, None, "new", "system", ""),
    )

    db.commit()

    # --- Update lead with first_order_id ---
    if discount_code_applied:
        cur.execute(
            "UPDATE eshop_leads SET first_order_id = %s WHERE discount_code = %s",
            (order_id, discount_code_applied),
        )
        db.commit()

    # --- Comgate payment integration ---
    payment_url = None
    comgate_client = get_comgate_client(tenant)

    if comgate_client is not None:
        try:
            price_cents = int(Decimal(str(total_amount_vat)) * 100)
            result = await comgate_client.create_payment(
                price_cents=price_cents,
                currency=tenant["currency"],
                order_number=order_number,
                customer_email=body.customer_email,
                label=tenant["brand_name"][:16],
                country=body.billing_country or "SK",
                lang=body.lang or "sk",
            )
            # Store Comgate transaction ID
            cur.execute(
                "UPDATE eshop_orders SET comgate_transaction_id = %s "
                "WHERE order_id = %s",
                (result["transId"], order_id),
            )
            db.commit()
            payment_url = result["redirect_url"]
        except ComgateError:
            logger.exception(
                "Comgate payment creation failed for order %s", order_number
            )
        except Exception:
            logger.exception(
                "Unexpected error creating Comgate payment for order %s",
                order_number,
            )
    else:
        logger.warning("Comgate not configured for tenant %s", tenant_id)

    # --- Email notifications (fire-and-forget) ---
    try:
        order_data = {
            "order_number": order_number,
            "customer_email": body.customer_email,
            "customer_name": body.customer_name,
            "customer_phone": body.customer_phone or "",
            "billing_name": body.billing_name,
            "billing_name2": body.billing_name2 or "",
            "billing_street": body.billing_street,
            "billing_city": body.billing_city,
            "billing_zip": body.billing_zip,
            "billing_country": body.billing_country,
            "shipping_name": body.shipping_name or "",
            "shipping_name2": body.shipping_name2 or "",
            "shipping_street": body.shipping_street or "",
            "shipping_city": body.shipping_city or "",
            "shipping_zip": body.shipping_zip or "",
            "shipping_country": body.shipping_country or "",
            "total_amount_vat": float(total_amount_vat),
            "currency": tenant["currency"],
            "payment_method": body.payment_method,
            "note": body.note or "",
        }
        items_data = [
            {
                "name": oi["name"],
                "quantity": oi["quantity"],
                "unit_price_vat": float(oi["unit_price_vat"]),
                "currency": tenant["currency"],
            }
            for oi in order_items
        ]
        email_svc = EshopEmailService(tenant)
        await email_svc.send_order_confirmation(order_data, items_data)
        await email_svc.send_admin_new_order(order_data, items_data)
    except Exception as e:
        logger.error("Email notification failed for order %s: %s", order_number, e)

    # Notify MuFis about new order (fire-and-forget)
    asyncio.create_task(notify_mufis_order_change())

    return OrderCreateResponse(
        order_number=order_number,
        status="new",
        total_amount_vat=total_amount_vat,
        currency=tenant["currency"],
        payment_url=payment_url,
    )


@router.get("/orders/{order_number}", response_model=OrderStatusResponse)
def get_order_status(
    order_number: str,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Get order status with items."""
    cur = db.cursor()
    cur.execute(
        "SELECT order_number, status, payment_status, tracking_number, "
        "tracking_link, created_at "
        "FROM eshop_orders "
        "WHERE order_number = %s AND tenant_id = %s",
        (order_number, tenant["tenant_id"]),
    )
    order = cur.fetchone()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Objednávka '{order_number}' nebola nájdená",
        )

    # Fetch items
    cur.execute(
        "SELECT oi.sku, oi.name, oi.quantity, oi.unit_price_vat, oi.vat_rate "
        "FROM eshop_order_items oi "
        "JOIN eshop_orders o ON oi.order_id = o.order_id "
        "WHERE o.order_number = %s AND o.tenant_id = %s",
        (order_number, tenant["tenant_id"]),
    )
    items = [
        OrderItemResponse(
            sku=r[0],
            name=r[1],
            quantity=r[2],
            unit_price_vat=r[3],
            vat_rate=r[4],
        )
        for r in cur.fetchall()
    ]

    return OrderStatusResponse(
        order_number=order[0],
        status=order[1],
        payment_status=order[2],
        tracking_number=order[3] or "",
        tracking_link=order[4] or "",
        created_at=order[5],
        items=items,
    )


# ============================================================================
# PUBLIC — Customer Registration, Login, Profile, Orders
# ============================================================================


def _get_customer_from_token(authorization: str, db) -> dict:
    """Parse Bearer token, decode JWT, return customer dict or raise 401."""
    from jose import jwt, JWTError
    from auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chýba alebo neplatný Authorization header",
        )
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný alebo expirovaný token",
        )
    customer_id = payload.get("customer_id")
    tenant_id = payload.get("tenant_id")
    if not customer_id or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný token — chýba customer_id alebo tenant_id",
        )
    cur = db.cursor()
    cur.execute(
        "SELECT id, tenant_id, email, first_name, last_name, phone, "
        "street, city, postal_code, country, is_company, company_name, "
        "company_ico, company_dic, company_ic_dph "
        "FROM eshop_customers WHERE id = %s AND tenant_id = %s AND is_active = TRUE",
        (customer_id, tenant_id),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Zákazník nebol nájdený alebo nie je aktívny",
        )
    return {
        "id": row[0],
        "tenant_id": row[1],
        "email": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "phone": row[5],
        "street": row[6],
        "city": row[7],
        "postal_code": row[8],
        "country": row[9],
        "is_company": row[10],
        "company_name": row[11],
        "company_ico": row[12],
        "company_dic": row[13],
        "company_ic_dph": row[14],
    }


@router.post(
    "/customers/register",
    status_code=status.HTTP_201_CREATED,
)
def register_customer(
    body: CustomerRegisterRequest,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Register a new customer for the tenant."""
    import bcrypt

    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    # Check uniqueness (tenant_id, email)
    cur.execute(
        "SELECT id FROM eshop_customers "
        "WHERE tenant_id = %s AND email = %s AND is_active = TRUE",
        (tenant_id, body.email),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail je už zaregistrovaný",
        )

    # Hash password
    password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

    # Insert customer
    cur.execute(
        "INSERT INTO eshop_customers ("
        "tenant_id, email, password_hash, first_name, last_name, phone, "
        "street, city, postal_code, country, is_company, "
        "company_name, company_ico, company_dic, company_ic_dph"
        ") VALUES ("
        "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
        ") RETURNING id",
        (
            tenant_id,
            body.email,
            password_hash,
            body.first_name,
            body.last_name,
            body.phone,
            body.street,
            body.city,
            body.postal_code,
            body.country,
            body.is_company,
            body.company_name,
            body.company_ico,
            body.company_dic,
            body.company_ic_dph,
        ),
    )
    customer_id = cur.fetchone()[0]
    db.commit()

    return {"customer_id": customer_id, "email": body.email}


@router.post("/customers/login", response_model=CustomerLoginResponse)
def login_customer(
    body: CustomerLoginRequest,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Authenticate customer and return JWT token."""
    import bcrypt
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    cur.execute(
        "SELECT id, email, password_hash, first_name, last_name "
        "FROM eshop_customers "
        "WHERE tenant_id = %s AND email = %s AND is_active = TRUE",
        (tenant_id, body.email),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nesprávny e-mail alebo heslo",
        )

    customer_id = row[0]
    stored_hash = row[2]

    if not bcrypt.checkpw(body.password.encode(), stored_hash.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nesprávny e-mail alebo heslo",
        )

    # Update last_login_at
    cur.execute(
        "UPDATE eshop_customers SET last_login_at = NOW() WHERE id = %s",
        (customer_id,),
    )
    db.commit()

    # Generate JWT
    token = jwt.encode(
        {
            "customer_id": customer_id,
            "tenant_id": tenant_id,
            "exp": datetime.now(timezone.utc) + timedelta(days=30),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return CustomerLoginResponse(
        token=token,
        customer_id=customer_id,
        email=row[1],
        first_name=row[3] or "",
        last_name=row[4] or "",
    )


@router.get("/customers/profile", response_model=CustomerProfileResponse)
def get_customer_profile(
    auth_header: str = Header(..., alias="Authorization"),
    db=Depends(get_db),
):
    """Get customer profile from Bearer token."""
    customer = _get_customer_from_token(auth_header, db)
    return CustomerProfileResponse(**customer)


@router.get("/customers/orders")
def get_customer_orders(
    auth_header: str = Header(None, alias="Authorization"),
    db=Depends(get_db),
):
    """Get customer's orders from Bearer token."""
    customer = _get_customer_from_token(auth_header, db)
    cur = db.cursor()
    cur.execute(
        "SELECT order_id, order_number, status, payment_status, "
        "total_amount_vat, currency, created_at "
        "FROM eshop_orders "
        "WHERE customer_id = %s ORDER BY created_at DESC",
        (customer["id"],),
    )
    orders = [
        {
            "order_id": r[0],
            "order_number": r[1],
            "status": r[2],
            "payment_status": r[3],
            "total_amount_vat": _dec(r[4]),
            "currency": r[5],
            "created_at": r[6].isoformat() if r[6] else None,
        }
        for r in cur.fetchall()
    ]
    return {"orders": orders}


# ============================================================================
# PUBLIC — Lead Capture
# ============================================================================

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@router.post(
    "/leads",
    response_model=LeadRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_lead(
    body: LeadRegisterRequest,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Register a new lead and generate a discount code."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    # Validate email format
    if not body.email or not EMAIL_REGEX.match(body.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Neplatný formát e-mailovej adresy",
        )

    # Validate GDPR consent
    if not body.gdpr_consent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GDPR súhlas je povinný",
        )

    # Check duplicate email for tenant
    cur.execute(
        "SELECT lead_id FROM eshop_leads WHERE tenant_id = %s AND email = %s",
        (tenant_id, body.email),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail je už zaregistrovaný",
        )

    # Generate unique discount code (max 3 attempts)
    discount_code = None
    for _ in range(3):
        code = f"OASIS-{secrets.token_hex(4).upper()}"
        cur.execute(
            "SELECT lead_id FROM eshop_leads WHERE discount_code = %s",
            (code,),
        )
        if not cur.fetchone():
            discount_code = code
            break

    if not discount_code:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Nepodarilo sa vygenerovať unikátny kód",
        )

    # Insert lead
    cur.execute(
        "INSERT INTO eshop_leads ("
        "tenant_id, email, first_name, last_name, phone, "
        "discount_code, discount_percentage, "
        "expires_at, gdpr_consent, gdpr_consent_at"
        ") VALUES ("
        "%s, %s, %s, %s, %s, %s, %s, "
        "NOW() + INTERVAL '3 months', %s, NOW()"
        ") RETURNING lead_id, expires_at",
        (
            tenant_id,
            body.email,
            body.first_name,
            body.last_name,
            body.phone,
            discount_code,
            50.00,
            True,
        ),
    )
    result = cur.fetchone()
    lead_id = result[0]
    expires_at = result[1]
    db.commit()

    # Send welcome email (fire-and-forget)
    try:
        lead_data = {
            "email": body.email,
            "first_name": body.first_name,
            "discount_code": discount_code,
            "expires_at": expires_at,
        }
        email_svc = EshopEmailService(tenant)
        await email_svc.send_lead_welcome_email(tenant, lead_data)
    except Exception as e:
        logger.error("Lead welcome email failed for %s: %s", body.email, e)

    return LeadRegisterResponse(
        lead_id=lead_id,
        email=body.email,
        discount_code=discount_code,
        discount_percentage=50.0,
        expires_at=expires_at.isoformat()
        if hasattr(expires_at, "isoformat")
        else str(expires_at),
        message="Registrácia úspešná. Zľavový kód bol odoslaný na váš e-mail.",
    )


@router.get("/leads/validate/{discount_code}", response_model=LeadValidateResponse)
def validate_discount_code(
    discount_code: str,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Validate a discount code."""
    cur = db.cursor()
    cur.execute(
        "SELECT discount_percentage, expires_at, is_active, first_order_id "
        "FROM eshop_leads "
        "WHERE discount_code = %s AND tenant_id = %s",
        (discount_code, tenant["tenant_id"]),
    )
    lead = cur.fetchone()
    if not lead:
        return LeadValidateResponse(valid=False, message="Neplatný zľavový kód")

    discount_percentage = float(lead[0])
    expires_at = lead[1]
    is_active = lead[2]
    first_order_id = lead[3]

    if not is_active:
        return LeadValidateResponse(valid=False, message="Zľavový kód nie je aktívny")

    if first_order_id is not None:
        return LeadValidateResponse(valid=False, message="Zľavový kód už bol použitý")

    from datetime import datetime, timezone

    now_utc = datetime.now(timezone.utc)
    if expires_at <= now_utc:
        return LeadValidateResponse(valid=False, message="Zľavový kód expiroval")

    return LeadValidateResponse(
        valid=True,
        discount_percentage=discount_percentage,
        expires_at=expires_at.isoformat()
        if hasattr(expires_at, "isoformat")
        else str(expires_at),
        message="Kód je platný",
    )


# ============================================================================
# PAYMENT — Comgate Callback & Return
# ============================================================================


@router.post("/payment/callback")
async def payment_callback(
    merchant: str = Form(...),
    test: str = Form(...),
    price: str = Form(...),
    curr: str = Form(...),
    label: str = Form(...),
    refId: str = Form(...),
    transId: str = Form(...),
    secret: str = Form(...),
    email: str = Form(...),
    status_val: str = Form(..., alias="status"),
    db=Depends(get_db),
):
    """Comgate payment callback — NO authentication required.

    Comgate sends POST with form-urlencoded data when payment status changes.
    MUST always return HTTP 200 with body 'code=0&message=OK'.
    """
    ok_response = Response(content="code=0&message=OK", media_type="text/plain")
    cur = db.cursor()

    # 1. Find order by refId (order_number)
    cur.execute(
        "SELECT order_id, tenant_id, total_amount_vat, currency, "
        "payment_status, status "
        "FROM eshop_orders WHERE order_number = %s",
        (refId,),
    )
    order = cur.fetchone()
    if not order:
        logger.error("Comgate callback: order '%s' not found", refId)
        return ok_response

    order_id = order[0]
    tenant_id = order[1]
    order_total_vat = order[2]
    order_currency = order[3]
    current_payment_status = order[4]
    current_order_status = order[5]

    # 2. Load tenant to verify secrets
    cur.execute(
        "SELECT tenant_id, comgate_merchant_id, comgate_secret "
        "FROM eshop_tenants WHERE tenant_id = %s",
        (tenant_id,),
    )
    tenant_row = cur.fetchone()
    if not tenant_row:
        logger.error("Comgate callback: tenant %s not found", tenant_id)
        return ok_response

    tenant_merchant_id = tenant_row[1] or ""
    tenant_secret = tenant_row[2] or ""

    # 3. Verify callback authenticity
    if not hmac.compare_digest(secret, tenant_secret):
        logger.error("Comgate callback: secret mismatch for order %s", refId)
        return ok_response

    if merchant != tenant_merchant_id:
        logger.error(
            "Comgate callback: merchant mismatch for order %s (got %s, expected %s)",
            refId,
            merchant,
            tenant_merchant_id,
        )
        return ok_response

    # 4. Verify price and currency
    expected_price_cents = int(Decimal(str(order_total_vat)) * 100)
    if int(price) != expected_price_cents:
        logger.error(
            "Comgate callback: price mismatch for order %s (got %s, expected %s)",
            refId,
            price,
            expected_price_cents,
        )
        return ok_response

    if curr != order_currency:
        logger.error(
            "Comgate callback: currency mismatch for order %s (got %s, expected %s)",
            refId,
            curr,
            order_currency,
        )
        return ok_response

    # 5. Process status
    if status_val == "PAID":
        # Idempotency: if already paid, don't change anything
        if current_payment_status == "paid":
            return ok_response

        cur.execute(
            "UPDATE eshop_orders SET payment_status = 'paid', "
            "comgate_transaction_id = %s WHERE order_id = %s",
            (transId, order_id),
        )

        # If order status is 'new', advance to 'paid'
        if current_order_status == "new":
            cur.execute(
                "UPDATE eshop_orders SET status = 'paid' WHERE order_id = %s",
                (order_id,),
            )
            cur.execute(
                "INSERT INTO eshop_order_status_history ("
                "order_id, old_status, new_status, changed_by, note"
                ") VALUES (%s, %s, %s, %s, %s)",
                (order_id, current_order_status, "paid", "comgate", ""),
            )
        else:
            # Just record payment status change in history
            cur.execute(
                "INSERT INTO eshop_order_status_history ("
                "order_id, old_status, new_status, changed_by, note"
                ") VALUES (%s, %s, %s, %s, %s)",
                (
                    order_id,
                    current_order_status,
                    current_order_status,
                    "comgate",
                    "payment_status: paid",
                ),
            )

        # --- Email: payment confirmation ---
        try:
            cur.execute(
                "SELECT smtp_from, admin_email, brand_name, domain, primary_color, "
                "currency FROM eshop_tenants WHERE tenant_id = %s",
                (tenant_id,),
            )
            t_email = cur.fetchone()
            if t_email:
                tenant_for_email = {
                    "smtp_from": t_email[0],
                    "admin_email": t_email[1],
                    "brand_name": t_email[2],
                    "domain": t_email[3],
                    "primary_color": t_email[4],
                    "currency": t_email[5],
                }
                # Fetch order details for email
                cur.execute(
                    "SELECT order_number, customer_email, customer_name, "
                    "total_amount_vat, currency, payment_method "
                    "FROM eshop_orders WHERE order_id = %s",
                    (order_id,),
                )
                o_row = cur.fetchone()
                if o_row:
                    order_for_email = {
                        "order_number": o_row[0],
                        "customer_email": o_row[1],
                        "customer_name": o_row[2],
                        "total_amount_vat": float(o_row[3]),
                        "currency": o_row[4],
                        "payment_method": o_row[5],
                    }
                    # Fetch items
                    cur.execute(
                        "SELECT name, quantity, unit_price_vat "
                        "FROM eshop_order_items WHERE order_id = %s",
                        (order_id,),
                    )
                    items_for_email = [
                        {
                            "name": ir[0],
                            "quantity": ir[1],
                            "unit_price_vat": float(ir[2]),
                        }
                        for ir in cur.fetchall()
                    ]
                    email_svc = EshopEmailService(tenant_for_email)
                    await email_svc.send_payment_confirmation(
                        order_for_email, items_for_email
                    )
        except Exception as e:
            logger.error("Email notification failed for PAID callback %s: %s", refId, e)

    elif status_val == "CANCELLED":
        cur.execute(
            "UPDATE eshop_orders SET payment_status = 'failed' WHERE order_id = %s",
            (order_id,),
        )
        cur.execute(
            "INSERT INTO eshop_order_status_history ("
            "order_id, old_status, new_status, changed_by, note"
            ") VALUES (%s, %s, %s, %s, %s)",
            (
                order_id,
                current_order_status,
                current_order_status,
                "comgate",
                "payment_status: failed (CANCELLED)",
            ),
        )

        # --- Email: admin payment failed ---
        try:
            cur.execute(
                "SELECT smtp_from, admin_email, brand_name, domain, primary_color, "
                "currency FROM eshop_tenants WHERE tenant_id = %s",
                (tenant_id,),
            )
            t_email = cur.fetchone()
            if t_email:
                tenant_for_email = {
                    "smtp_from": t_email[0],
                    "admin_email": t_email[1],
                    "brand_name": t_email[2],
                    "domain": t_email[3],
                    "primary_color": t_email[4],
                    "currency": t_email[5],
                }
                cur.execute(
                    "SELECT order_number, customer_email, customer_name, "
                    "total_amount_vat, currency, payment_method, "
                    "comgate_transaction_id "
                    "FROM eshop_orders WHERE order_id = %s",
                    (order_id,),
                )
                o_row = cur.fetchone()
                if o_row:
                    order_for_email = {
                        "order_number": o_row[0],
                        "customer_email": o_row[1],
                        "customer_name": o_row[2],
                        "total_amount_vat": float(o_row[3]),
                        "currency": o_row[4],
                        "payment_method": o_row[5],
                        "comgate_transaction_id": o_row[6],
                    }
                    email_svc = EshopEmailService(tenant_for_email)
                    await email_svc.send_admin_payment_failed(order_for_email)
        except Exception as e:
            logger.error(
                "Email notification failed for CANCELLED callback %s: %s", refId, e
            )

    elif status_val == "AUTHORIZED":
        cur.execute(
            "UPDATE eshop_orders SET payment_status = 'authorized' WHERE order_id = %s",
            (order_id,),
        )
        cur.execute(
            "INSERT INTO eshop_order_status_history ("
            "order_id, old_status, new_status, changed_by, note"
            ") VALUES (%s, %s, %s, %s, %s)",
            (
                order_id,
                current_order_status,
                current_order_status,
                "comgate",
                "payment_status: authorized",
            ),
        )

    db.commit()
    return ok_response


@router.get("/payment/return", response_model=PaymentReturnResponse)
def payment_return(
    id: str = Query(..., description="Comgate transaction ID"),
    db=Depends(get_db),
):
    """Payment return — customer browser redirected here after payment.

    NO authentication — called by customer browser.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT order_number, status, payment_status "
        "FROM eshop_orders WHERE comgate_transaction_id = %s",
        (id,),
    )
    order = cur.fetchone()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objednávka pre túto transakciu nebola nájdená",
        )

    return PaymentReturnResponse(
        order_number=order[0],
        status=order[1],
        payment_status=order[2],
    )


# ============================================================================
# ADMIN — Orders
# ============================================================================


@router.get("/admin/orders", response_model=AdminOrderListResponse)
def admin_list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    tenant_id: Optional[int] = Query(None),
    _current_user=Depends(require_permission("ESHOP", "can_view")),
    db=Depends(get_db),
):
    """Admin: list orders with filtering and pagination."""
    cur = db.cursor()

    conditions: list[str] = []
    params: list = []

    if tenant_id is not None:
        conditions.append("tenant_id = %s")
        params.append(tenant_id)
    if status_filter:
        conditions.append("status = %s")
        params.append(status_filter)
    if date_from:
        conditions.append("created_at >= %s")
        params.append(date_from)
    if date_to:
        conditions.append("created_at <= %s")
        params.append(date_to)

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    # Count
    cur.execute(f"SELECT COUNT(*) FROM eshop_orders {where}", params)
    total = cur.fetchone()[0]

    # Fetch page
    offset = (page - 1) * page_size
    cur.execute(
        f"SELECT order_id, order_number, customer_name, customer_email, "
        f"total_amount_vat, currency, status, payment_status, "
        f"created_at, updated_at "
        f"FROM eshop_orders {where} "
        f"ORDER BY created_at DESC LIMIT %s OFFSET %s",
        params + [page_size, offset],
    )
    orders = [
        AdminOrderListItem(
            order_id=r[0],
            order_number=r[1],
            customer_name=r[2],
            customer_email=r[3],
            total_amount_vat=r[4],
            currency=r[5],
            status=r[6],
            payment_status=r[7],
            created_at=r[8],
            updated_at=r[9],
        )
        for r in cur.fetchall()
    ]

    return AdminOrderListResponse(
        orders=orders,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/admin/orders/{order_id}", response_model=AdminOrderDetailResponse)
def admin_get_order(
    order_id: int,
    _current_user=Depends(require_permission("ESHOP", "can_view")),
    db=Depends(get_db),
):
    """Admin: get order detail with items and status history."""
    cur = db.cursor()
    cur.execute(
        "SELECT order_id, order_number, tenant_id, customer_email, customer_name, "
        "customer_phone, lang, billing_name, billing_name2, billing_street, "
        "billing_city, billing_zip, billing_country, shipping_name, shipping_name2, "
        "shipping_street, shipping_city, shipping_zip, shipping_country, "
        "ico, dic, eu_vat_number, total_amount, total_amount_vat, currency, "
        "payment_method, payment_status, comgate_transaction_id, shipping_type, "
        "shipping_price, delivery_point_group, delivery_point_id, "
        "tracking_number, tracking_link, multiple_packages, status, note, "
        "created_at, updated_at "
        "FROM eshop_orders WHERE order_id = %s",
        (order_id,),
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Objednávka {order_id} nebola nájdená",
        )

    # Items
    cur.execute(
        "SELECT sku, name, quantity, unit_price_vat, vat_rate "
        "FROM eshop_order_items WHERE order_id = %s",
        (order_id,),
    )
    items = [
        OrderItemResponse(
            sku=ir[0],
            name=ir[1],
            quantity=ir[2],
            unit_price_vat=ir[3],
            vat_rate=ir[4],
        )
        for ir in cur.fetchall()
    ]

    # Status history
    cur.execute(
        "SELECT old_status, new_status, changed_by, note, created_at "
        "FROM eshop_order_status_history WHERE order_id = %s "
        "ORDER BY created_at",
        (order_id,),
    )
    history = [
        AdminStatusHistoryItem(
            old_status=hr[0],
            new_status=hr[1],
            changed_by=hr[2],
            note=hr[3] or "",
            created_at=hr[4],
        )
        for hr in cur.fetchall()
    ]

    return AdminOrderDetailResponse(
        order_id=r[0],
        order_number=r[1],
        tenant_id=r[2],
        customer_email=r[3],
        customer_name=r[4],
        customer_phone=r[5],
        lang=r[6],
        billing_name=r[7],
        billing_name2=r[8] or "",
        billing_street=r[9],
        billing_city=r[10],
        billing_zip=r[11],
        billing_country=r[12],
        shipping_name=r[13] or "",
        shipping_name2=r[14] or "",
        shipping_street=r[15] or "",
        shipping_city=r[16] or "",
        shipping_zip=r[17] or "",
        shipping_country=r[18] or "",
        ico=r[19] or "",
        dic=r[20] or "",
        eu_vat_number=r[21] or "",
        total_amount=r[22],
        total_amount_vat=r[23],
        currency=r[24],
        payment_method=r[25],
        payment_status=r[26],
        comgate_transaction_id=r[27],
        shipping_type=r[28] or "",
        shipping_price=r[29],
        delivery_point_group=r[30] or "",
        delivery_point_id=r[31] or "",
        tracking_number=r[32] or "",
        tracking_link=r[33] or "",
        multiple_packages=r[34],
        status=r[35],
        note=r[36] or "",
        created_at=r[37],
        updated_at=r[38],
        items=items,
        status_history=history,
    )


@router.patch("/admin/orders/{order_id}")
async def admin_update_order(
    order_id: int,
    body: AdminOrderUpdateRequest,
    current_user=Depends(require_permission("ESHOP", "can_edit")),
    db=Depends(get_db),
):
    """Admin: update order status/note."""
    cur = db.cursor()

    # Check exists and get current status
    cur.execute(
        "SELECT status FROM eshop_orders WHERE order_id = %s",
        (order_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Objednávka {order_id} nebola nájdená",
        )

    old_status = row[0]
    set_parts: list[str] = []
    params: list = []

    if body.status is not None:
        set_parts.append("status = %s")
        params.append(body.status)
    if body.note is not None:
        set_parts.append("note = %s")
        params.append(body.note)

    if not set_parts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    params.append(order_id)
    cur.execute(
        f"UPDATE eshop_orders SET {', '.join(set_parts)} WHERE order_id = %s",
        params,
    )

    # Status history if status changed
    status_changed = body.status is not None and body.status != old_status
    if status_changed:
        cur.execute(
            "INSERT INTO eshop_order_status_history ("
            "order_id, old_status, new_status, changed_by, note"
            ") VALUES (%s, %s, %s, %s, %s)",
            (
                order_id,
                old_status,
                body.status,
                current_user["login_name"],
                body.note or "",
            ),
        )

    db.commit()

    # Notify MuFis about order status change (fire-and-forget)
    if status_changed:
        asyncio.create_task(notify_mufis_order_change())

    return {"message": f"Objednávka {order_id} aktualizovaná"}


# ============================================================================
# ADMIN — Products
# ============================================================================


@router.get("/admin/products")
def admin_list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    tenant_id: Optional[int] = Query(None),
    include_inactive: bool = Query(True),
    _current_user=Depends(require_permission("ESHOP", "can_view")),
    db=Depends(get_db),
):
    """Admin: list all products with pagination."""
    cur = db.cursor()

    conditions: list[str] = []
    params: list = []

    if tenant_id is not None:
        conditions.append("tenant_id = %s")
        params.append(tenant_id)
    if not include_inactive:
        conditions.append("is_active = TRUE")

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    cur.execute(f"SELECT COUNT(*) FROM eshop_products {where}", params)
    total = cur.fetchone()[0]

    offset = (page - 1) * page_size
    cur.execute(
        f"SELECT product_id, tenant_id, sku, barcode, name, short_description, "
        f"description, image_url, price, price_vat, vat_rate, stock_quantity, "
        f"weight, is_active, sort_order, created_at, updated_at "
        f"FROM eshop_products {where} ORDER BY sort_order LIMIT %s OFFSET %s",
        params + [page_size, offset],
    )
    products = []
    for r in cur.fetchall():
        products.append(
            {
                "product_id": r[0],
                "tenant_id": r[1],
                "sku": r[2],
                "barcode": r[3],
                "name": r[4],
                "short_description": r[5],
                "description": r[6],
                "image_url": r[7],
                "price": _dec(r[8]),
                "price_vat": _dec(r[9]),
                "vat_rate": _dec(r[10]),
                "stock_quantity": r[11],
                "weight": _dec(r[12]),
                "is_active": r[13],
                "sort_order": r[14],
                "created_at": r[15].isoformat() if r[15] else None,
                "updated_at": r[16].isoformat() if r[16] else None,
            }
        )

    return {
        "products": products,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post(
    "/admin/products",
    status_code=status.HTTP_201_CREATED,
)
def admin_create_product(
    body: AdminProductCreateRequest,
    tenant_id: int = Query(...),
    _current_user=Depends(require_permission("ESHOP", "can_create")),
    db=Depends(get_db),
):
    """Admin: create a new product."""
    cur = db.cursor()
    cur.execute(
        "INSERT INTO eshop_products ("
        "tenant_id, sku, barcode, name, short_description, description, "
        "image_url, price, price_vat, vat_rate, stock_quantity, weight, "
        "is_active, sort_order"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "RETURNING product_id, tenant_id, sku, barcode, name, short_description, "
        "description, image_url, price, price_vat, vat_rate, stock_quantity, "
        "weight, is_active, sort_order, created_at, updated_at",
        (
            tenant_id,
            body.sku,
            body.barcode,
            body.name,
            body.short_description,
            body.description,
            body.image_url,
            float(body.price),
            float(body.price_vat),
            float(body.vat_rate),
            body.stock_quantity,
            float(body.weight) if body.weight is not None else None,
            body.is_active,
            body.sort_order,
        ),
    )
    r = cur.fetchone()
    db.commit()

    return {
        "product_id": r[0],
        "tenant_id": r[1],
        "sku": r[2],
        "barcode": r[3],
        "name": r[4],
        "short_description": r[5],
        "description": r[6],
        "image_url": r[7],
        "price": _dec(r[8]),
        "price_vat": _dec(r[9]),
        "vat_rate": _dec(r[10]),
        "stock_quantity": r[11],
        "weight": _dec(r[12]),
        "is_active": r[13],
        "sort_order": r[14],
        "created_at": r[15].isoformat() if r[15] else None,
        "updated_at": r[16].isoformat() if r[16] else None,
    }


@router.patch("/admin/products/{product_id}")
def admin_update_product(
    product_id: int,
    body: AdminProductUpdateRequest,
    _current_user=Depends(require_permission("ESHOP", "can_edit")),
    db=Depends(get_db),
):
    """Admin: partial update a product."""
    cur = db.cursor()

    body_data = body.model_dump(exclude_unset=True)
    if not body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    set_parts: list[str] = []
    params: list = []
    for field, value in body_data.items():
        set_parts.append(f"{field} = %s")
        if isinstance(value, Decimal):
            params.append(float(value))
        else:
            params.append(value)

    params.append(product_id)
    cur.execute(
        f"UPDATE eshop_products SET {', '.join(set_parts)} WHERE product_id = %s "
        "RETURNING product_id, tenant_id, sku, barcode, name, short_description, "
        "description, image_url, price, price_vat, vat_rate, stock_quantity, "
        "weight, is_active, sort_order, created_at, updated_at",
        params,
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt {product_id} nebol nájdený",
        )
    db.commit()

    return {
        "product_id": r[0],
        "tenant_id": r[1],
        "sku": r[2],
        "barcode": r[3],
        "name": r[4],
        "short_description": r[5],
        "description": r[6],
        "image_url": r[7],
        "price": _dec(r[8]),
        "price_vat": _dec(r[9]),
        "vat_rate": _dec(r[10]),
        "stock_quantity": r[11],
        "weight": _dec(r[12]),
        "is_active": r[13],
        "sort_order": r[14],
        "created_at": r[15].isoformat() if r[15] else None,
        "updated_at": r[16].isoformat() if r[16] else None,
    }


@router.delete("/admin/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_product(
    product_id: int,
    _current_user=Depends(require_permission("ESHOP", "can_delete")),
    db=Depends(get_db),
):
    """Admin: soft-delete a product (set is_active = FALSE)."""
    cur = db.cursor()
    cur.execute(
        "UPDATE eshop_products SET is_active = FALSE WHERE product_id = %s "
        "RETURNING product_id",
        (product_id,),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt {product_id} nebol nájdený",
        )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============================================================================
# ADMIN — Tenants
# ============================================================================


@router.get("/admin/tenants")
def admin_list_tenants(
    _current_user=Depends(require_permission("ESHOP", "can_view")),
    db=Depends(get_db),
):
    """Admin: list tenants (sanitized — no secrets)."""
    cur = db.cursor()
    cur.execute(
        "SELECT tenant_id, company_name, domain, brand_name, logo_url, "
        "primary_color, currency, vat_rate_default, default_lang, is_active, "
        "created_at "
        "FROM eshop_tenants ORDER BY tenant_id",
    )
    tenants = [
        AdminTenantResponse(
            tenant_id=r[0],
            company_name=r[1],
            domain=r[2],
            brand_name=r[3],
            logo_url=r[4],
            primary_color=r[5],
            currency=r[6],
            vat_rate_default=r[7],
            default_lang=r[8],
            is_active=r[9],
            created_at=r[10],
        ).model_dump()
        for r in cur.fetchall()
    ]
    return {"tenants": tenants}


@router.get("/admin/tenants/{tenant_id}")
def admin_get_tenant(
    tenant_id: int,
    _current_user=Depends(require_permission("ESHOP", "can_view")),
    db=Depends(get_db),
):
    """Admin: get tenant detail (sanitized)."""
    cur = db.cursor()
    cur.execute(
        "SELECT tenant_id, company_name, domain, brand_name, logo_url, "
        "primary_color, currency, vat_rate_default, default_lang, is_active, "
        "created_at "
        "FROM eshop_tenants WHERE tenant_id = %s",
        (tenant_id,),
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant {tenant_id} nebol nájdený",
        )
    return AdminTenantResponse(
        tenant_id=r[0],
        company_name=r[1],
        domain=r[2],
        brand_name=r[3],
        logo_url=r[4],
        primary_color=r[5],
        currency=r[6],
        vat_rate_default=r[7],
        default_lang=r[8],
        is_active=r[9],
        created_at=r[10],
    ).model_dump()


# ============================================================================
# MUFIS — getOrder
# ============================================================================


@router.post("/mufis/getOrder")
async def mufis_get_order(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
    mufis_access=Depends(verify_mufis_access),
    page: int = Form(1),
    order_number: Optional[str] = Form(None),
    order_id: Optional[int] = Form(None),
    updated_at_min: Optional[str] = Form(None),
    status_filter: Optional[str] = Form(None, alias="status"),
    date_from: Optional[str] = Form(None),
    date_to: Optional[str] = Form(None),
):
    """MuFis: get orders with filtering.

    Default filter: status='paid' AND mufis_synced_at IS NULL (new orders for MuFis).
    When MUFIS_DRY_RUN=true (default), orders are NOT marked as synced.
    """
    mufis_dry_run = os.environ.get("MUFIS_DRY_RUN", "true").lower() == "true"
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()
    per_page = MUFIS_PAGE_SIZE

    conditions: list[str] = ["tenant_id = %s"]
    params: list = [tenant_id]

    # Default: only paid, unsynced orders (unless explicit filters provided)
    has_explicit_filter = any(
        [order_number, order_id, status_filter, updated_at_min, date_from, date_to]
    )
    if not has_explicit_filter:
        conditions.append("status = %s")
        params.append("paid")
        conditions.append("mufis_synced_at IS NULL")

    if order_number:
        conditions.append("order_number = %s")
        params.append(order_number)
    if order_id:
        conditions.append("order_id = %s")
        params.append(order_id)
    if updated_at_min:
        conditions.append("updated_at >= %s")
        params.append(updated_at_min)
    if status_filter:
        statuses = [s.strip() for s in status_filter.split(",")]
        if len(statuses) == 1:
            conditions.append("status = %s")
            params.append(statuses[0])
        else:
            placeholders = ", ".join(["%s"] * len(statuses))
            conditions.append(f"status IN ({placeholders})")
            params.extend(statuses)
    if date_from:
        conditions.append("created_at::date >= %s")
        params.append(date_from)
    if date_to:
        conditions.append("created_at::date <= %s")
        params.append(date_to)

    where = "WHERE " + " AND ".join(conditions)

    # Count
    cur.execute(f"SELECT COUNT(*) FROM eshop_orders {where}", params)
    total = cur.fetchone()[0]
    total_pages = max(1, math.ceil(total / per_page))

    offset = (page - 1) * per_page
    cur.execute(
        f"SELECT order_id, order_number, tenant_id, customer_email, customer_name, "
        f"customer_phone, lang, billing_name, billing_name2, billing_street, "
        f"billing_city, billing_zip, billing_country, "
        f"shipping_name, shipping_name2, shipping_street, shipping_city, "
        f"shipping_zip, shipping_country, "
        f"ico, dic, eu_vat_number, total_amount, total_amount_vat, currency, "
        f"payment_method, payment_status, shipping_type, shipping_price, "
        f"delivery_point_group, delivery_point_id, "
        f"tracking_number, tracking_link, multiple_packages, status, note, "
        f"created_at, updated_at, "
        f"comgate_transaction_id, company_ic_dph, "
        f"delivery_method, packeta_point_id, packeta_point_name "
        f"FROM eshop_orders {where} ORDER BY order_id DESC "
        f"LIMIT %s OFFSET %s",
        params + [per_page, offset],
    )
    order_rows = cur.fetchall()

    # Payment type mapping (MuFis API v1.2 spec)
    PAYMENT_TYPE_MAP = {
        "credit_card": "CARD",
        "card": "CARD",
        "CARD": "CARD",
        "bank_transfer": "BANK",
        "bank": "BANK",
        "BANK": "BANK",
        "cod": "COD",
        "COD": "COD",
        "paypal": "PAYPAL",
        "PAYPAL": "PAYPAL",
    }

    # Shipping type mapping (MuFis API v1.2 spec)
    SHIPPING_TYPE_MAP = {
        "courier": "Kuriér na adresu",
        "packeta_point": "Výdajné miesto Packeta",
        "packeta_box": "Packeta Box",
    }

    orders = []
    for r in order_rows:
        oid = r[0]
        # Fetch items for this order
        cur.execute(
            "SELECT sku, name, quantity, unit_price, unit_price_vat, vat_rate, item_type "
            "FROM eshop_order_items WHERE order_id = %s",
            (oid,),
        )
        order_items = []
        for ir in cur.fetchall():
            order_items.append(
                {
                    "sku": ir[0],
                    "name": ir[1],
                    "quantity": ir[2],
                    "unit_price": _dec(ir[3]),
                    "unit_price_vat": _dec(ir[4]),
                    "vat_rate": _dec(ir[5]),
                    "price_type": "with_vat",
                    "item_type": ir[6],
                }
            )

        payment_method_raw = r[25] or ""
        payment_type = PAYMENT_TYPE_MAP.get(payment_method_raw, "OTHER")

        # Shipping type mapping
        shipping_type_raw = r[27] or ""
        delivery_method = r[40] or ""  # from migration 011
        # Use delivery_method for mapping if available, fallback to shipping_type
        shipping_type_source = delivery_method or shipping_type_raw
        shipping_type = SHIPPING_TYPE_MAP.get(
            shipping_type_source, shipping_type_source
        )

        # Delivery point (Packeta specific)
        delivery_point_group = r[29] or ""
        delivery_point_id = r[30] or ""
        packeta_point_id = r[41] or ""
        packeta_point_name = r[42] or ""
        # Enrich from packeta fields if delivery_method is packeta
        if delivery_method == "packeta_point" and packeta_point_id:
            if not delivery_point_group:
                delivery_point_group = "packeta"
            if not delivery_point_id:
                delivery_point_id = packeta_point_id

        # EU VAT number (company orders)
        eu_vat_number = r[21] or ""
        company_ic_dph = r[39] or ""
        if not eu_vat_number and company_ic_dph:
            vat = str(company_ic_dph)
            if not vat.startswith("SK"):
                vat = f"SK{vat}"
            eu_vat_number = vat

        # Comgate transaction ID
        comgate_transaction_id = r[38] or ""

        # Meta data (additional info)
        meta_data = []
        if comgate_transaction_id:
            meta_data.append(
                {"key": "comgate_transaction_id", "value": comgate_transaction_id}
            )
        if packeta_point_name:
            meta_data.append({"key": "packeta_point_name", "value": packeta_point_name})

        # date_mod: use updated_at (reflects last change), fallback to created_at
        created_at = r[36]
        updated_at = r[37]
        date_mod = (
            updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if updated_at
            else (created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "")
        )
        order_date = created_at.strftime("%Y-%m-%d") if created_at else ""

        # Billing streetnum (concat street + zip for MuFis)
        billing_streetnum = r[9] or ""

        # Shipping: fallback to billing if empty
        shipping_name = r[13] or r[4] or ""
        shipping_streetnum = r[15] or billing_streetnum
        shipping_city = r[16] or r[10] or ""
        shipping_zip = r[17] or r[11] or ""
        shipping_country = r[18] or r[12] or "SK"

        orders.append(
            {
                "order_id": r[0],
                "order_number": r[1],
                "order_date": order_date,
                "date_mod": date_mod,
                "customer_email": r[3],
                "customer_name": r[4],
                "customer_phone": r[5] or "",
                "email": r[3],
                "phone": r[5] or "",
                "lang": r[6] or "sk",
                "billing_name": r[7] or "",
                "billing_name2": r[8] or "",
                "billing_streetnum": billing_streetnum,
                "billing_city": r[10] or "",
                "billing_zip": r[11] or "",
                "billing_country": r[12] or "SK",
                "shipping_name": shipping_name,
                "shipping_name2": r[14] or "",
                "shipping_streetnum": shipping_streetnum,
                "shipping_city": shipping_city,
                "shipping_zip": shipping_zip,
                "shipping_country": shipping_country,
                "ico": r[19] or "",
                "dic": r[20] or "",
                "eu_vat_number": eu_vat_number,
                "total_amount": _dec(r[22]),
                "total_amount_vat": _dec(r[23]),
                "total_price": _dec(r[23]),
                "currency": r[24],
                "payment_type": payment_type,
                "payment_method": payment_type,
                "payment_status": r[26] or "",
                "shipping_type": shipping_type,
                "shipping_price": _dec(r[28]),
                "delivery_point_group": delivery_point_group,
                "delivery_point_id": delivery_point_id,
                "tracking_number": r[31] or "",
                "tracking_link": r[32] or "",
                "multiple_packages": r[33],
                "status": r[34],
                "note": r[35] or "",
                "created_at": created_at.isoformat() if created_at else "",
                "updated_at": updated_at.isoformat() if updated_at else "",
                "order_items": order_items,
                "items": order_items,
                "meta_data": meta_data,
            }
        )

    # Mark orders as synced (unless dry-run)
    if orders and not mufis_dry_run and not has_explicit_filter:
        synced_ids = [o["order_id"] for o in orders]
        placeholders = ", ".join(["%s"] * len(synced_ids))
        cur.execute(
            f"UPDATE eshop_orders SET mufis_synced_at = NOW() "
            f"WHERE order_id IN ({placeholders})",
            synced_ids,
        )
        db.commit()
        logger.info(
            "MuFis getOrder: marked %d orders as synced (tenant=%s)",
            len(synced_ids),
            tenant_id,
        )
    elif orders and mufis_dry_run:
        logger.info(
            "MuFis getOrder DRY-RUN: returning %d orders WITHOUT marking synced (tenant=%s)",
            len(orders),
            tenant_id,
        )

    return {
        "total_pages": total_pages,
        "page": page,
        "orders": orders,
    }


# ============================================================================
# MUFIS — setOrder
# ============================================================================


async def _process_set_order(
    cur,
    tenant: dict,
    item: dict,
    email_svc_factory=None,
) -> dict:
    """Process single setOrder update.

    Returns:
        {"ok": 1, "error": ""} on success
        {"ok": 0, "error": "description"} on failure

    Never raises — all errors are caught and returned in the dict.
    """
    tenant_id = tenant["tenant_id"]
    on = item.get("order_number")
    if not on:
        return {"ok": 0, "error": "Missing order_number"}

    mufis_hungarian_status = item.get("status")
    if not mufis_hungarian_status:
        return {"ok": 0, "error": "Missing status"}

    # Get current order
    try:
        cur.execute(
            "SELECT order_id, status FROM eshop_orders "
            "WHERE order_number = %s AND tenant_id = %s",
            (on, tenant_id),
        )
        order = cur.fetchone()
        if not order:
            return {"ok": 0, "error": f"Order {on} not found"}
    except Exception as e:
        return {"ok": 0, "error": f"Database error: {e}"}

    order_id_val = order[0]
    old_status = order[1]

    set_parts: list[str] = []
    params: list = []

    internal_status = map_mufis_status(mufis_hungarian_status)
    set_parts.append("status = %s")
    params.append(internal_status)
    set_parts.append("mufis_status = %s")
    params.append(mufis_hungarian_status)

    # --- multiple_packages support ---
    mp = item.get("multiple_packages")
    is_multiple = str(mp) == "1" or mp is True

    pkg = item.get("package_number")
    tl = item.get("tracking_link")

    if is_multiple and pkg:
        # Parse JSON arrays for multi-package orders
        try:
            pkg_list = json.loads(pkg) if isinstance(pkg, str) else [pkg]
        except (json.JSONDecodeError, TypeError):
            pkg_list = [pkg]
        try:
            trk_list = (
                json.loads(tl) if isinstance(tl, str) and tl else ([tl] if tl else [])
            )
        except (json.JSONDecodeError, TypeError):
            trk_list = [tl] if tl else []

        tracking_number_val = ",".join(str(p) for p in pkg_list if p)
        tracking_url_val = ",".join(str(t) for t in trk_list if t)
    else:
        tracking_number_val = pkg
        tracking_url_val = tl

    if tracking_number_val:
        set_parts.append("tracking_number = %s")
        params.append(tracking_number_val)
        set_parts.append("mufis_tracking_number = %s")
        params.append(tracking_number_val)

    if tracking_url_val:
        set_parts.append("tracking_link = %s")
        params.append(tracking_url_val)
        set_parts.append("mufis_tracking_url = %s")
        params.append(tracking_url_val)

    item_carrier = item.get("carrier")
    if item_carrier:
        set_parts.append("mufis_carrier = %s")
        params.append(item_carrier)

    if mp is not None:
        set_parts.append("multiple_packages = %s")
        params.append(is_multiple)

    mufis_oid = item.get("mufis_order_id")
    if mufis_oid:
        set_parts.append("mufis_order_id = %s")
        params.append(mufis_oid)

    try:
        if set_parts:
            params.append(order_id_val)
            cur.execute(
                f"UPDATE eshop_orders SET {', '.join(set_parts)} WHERE order_id = %s",
                params,
            )

        # Status history with source tracking
        if internal_status and internal_status != old_status:
            cur.execute(
                "INSERT INTO eshop_order_status_history ("
                "order_id, old_status, new_status, changed_by, note, "
                "source, mufis_original_status"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    order_id_val,
                    old_status,
                    internal_status,
                    "mufis",
                    "",
                    "mufis",
                    mufis_hungarian_status,
                ),
            )

        # --- Email: shipping notification ---
        if internal_status == "shipped" and (tracking_number_val or tracking_url_val):
            try:
                cur.execute(
                    "SELECT o.order_number, o.customer_email, o.customer_name, "
                    "o.tracking_number, o.tracking_link "
                    "FROM eshop_orders o WHERE o.order_id = %s",
                    (order_id_val,),
                )
                o_row = cur.fetchone()
                if o_row and email_svc_factory:
                    order_for_email = {
                        "order_number": o_row[0],
                        "customer_email": o_row[1],
                        "customer_name": o_row[2],
                        "tracking_number": o_row[3] or "",
                        "tracking_link": o_row[4] or "",
                    }
                    email_svc = email_svc_factory(tenant)
                    await email_svc.send_shipping_notification(order_for_email)
            except Exception as e:
                logger.error(
                    "Email notification failed for shipped order %s: %s", on, e
                )

        return {"ok": 1, "error": ""}

    except Exception as e:
        logger.error("Failed to update order %s: %s", on, e)
        return {"ok": 0, "error": f"Update failed: {e}"}


@router.post("/mufis/setOrder")
async def mufis_set_order(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
    mufis_access=Depends(verify_mufis_access),
    order_number: Optional[str] = Form(None),
    status_val: Optional[str] = Form(None, alias="status"),
    package_number: Optional[str] = Form(None),
    tracking_link: Optional[str] = Form(None),
    carrier: Optional[str] = Form(None),
    multiple_packages: Optional[str] = Form(None),
    data: Optional[str] = Form(None),
):
    """MuFis: update order status/tracking.

    Modes:
    - Single: order_number, status, package_number, tracking_link, multiple_packages
    - Batch: data (JSON array with above fields per order)

    Response:
    - Single: {"ok": 1, "error": ""} or {"ok": 0, "error": "..."}
    - Batch: {"orders": [{"order_number": "...", "ok": 1, "error": ""}, ...]}
    """
    cur = db.cursor()

    if data:
        # BATCH mode — parse JSON list
        try:
            batch = json.loads(data)
            if not isinstance(batch, list):
                return {
                    "orders": [
                        {
                            "order_number": "",
                            "ok": 0,
                            "error": "data must be JSON array",
                        }
                    ]
                }
        except (json.JSONDecodeError, TypeError) as e:
            return {
                "orders": [
                    {
                        "order_number": "",
                        "ok": 0,
                        "error": f"Invalid JSON in data parameter: {e}",
                    }
                ]
            }

        results = []
        for item in batch:
            if not isinstance(item, dict):
                results.append(
                    {
                        "order_number": "",
                        "ok": 0,
                        "error": "Each item must be an object",
                    }
                )
                continue

            result = await _process_set_order(
                cur, tenant, item, email_svc_factory=EshopEmailService
            )
            result["order_number"] = item.get("order_number", "")
            results.append(result)

        db.commit()
        return {"orders": results}

    else:
        # SINGLE mode
        if not order_number:
            return {"ok": 0, "error": "Chýba order_number alebo data parameter"}

        item = {
            "order_number": order_number,
            "status": status_val,
            "package_number": package_number,
            "tracking_link": tracking_link,
            "carrier": carrier,
            "multiple_packages": multiple_packages,
        }
        result = await _process_set_order(
            cur, tenant, item, email_svc_factory=EshopEmailService
        )
        db.commit()
        return result


# ============================================================================
# MUFIS — getProduct
# ============================================================================


@router.post("/mufis/getProduct")
async def mufis_get_product(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
    mufis_access=Depends(verify_mufis_access),
    page: int = Form(1),
    product_id: Optional[int] = Form(None),
    sku: Optional[str] = Form(None),
    active: Optional[int] = Form(None),
):
    """MuFis: get products with filtering."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()
    per_page = 50

    conditions: list[str] = ["tenant_id = %s"]
    params: list = [tenant_id]

    if product_id:
        conditions.append("product_id = %s")
        params.append(product_id)
    if sku:
        # Support comma-separated SKUs
        skus = [s.strip() for s in sku.split(",") if s.strip()]
        if len(skus) == 1:
            conditions.append("sku = %s")
            params.append(skus[0])
        elif skus:
            placeholders = ", ".join(["%s"] * len(skus))
            conditions.append(f"sku IN ({placeholders})")
            params.extend(skus)
    if active is not None:
        conditions.append("is_active = %s")
        params.append(active == 1)

    where = "WHERE " + " AND ".join(conditions)

    cur.execute(f"SELECT COUNT(*) FROM eshop_products {where}", params)
    total = cur.fetchone()[0]
    total_pages = max(1, math.ceil(total / per_page))

    offset = (page - 1) * per_page
    cur.execute(
        f"SELECT product_id, sku, barcode, name, short_description, description, "
        f"image_url, price, price_vat, vat_rate, stock_quantity, weight, "
        f"is_active, sort_order "
        f"FROM eshop_products {where} ORDER BY product_id DESC "
        f"LIMIT %s OFFSET %s",
        params + [per_page, offset],
    )

    products = [
        {
            "product_id": r[0],
            "sku": r[1],
            "barcode": r[2] or "",
            "name": r[3],
            "short_description": r[4] or "",
            "description": r[5] or "",
            "image_url": r[6] or "",
            "price": _dec(r[7]),
            "price_vat": _dec(r[8]),
            "vat_rate": _dec(r[9]),
            "stock_quantity": r[10],
            "weight": _dec(r[11]) if r[11] is not None else 0,
            "active": 1 if r[12] else 0,
            "sort_order": r[13],
        }
        for r in cur.fetchall()
    ]

    return {
        "total_pages": total_pages,
        "page": page,
        "products": products,
    }


# ============================================================================
# MUFIS — setProduct
# ============================================================================


def _process_set_product(cur, tenant_id: int, sku: str, stock_quantity) -> dict:
    """Process single setProduct update.

    Returns:
        {"ok": 1, "error": ""} on success
        {"ok": 0, "error": "description"} on failure

    Never raises — all errors are caught and returned in the dict.
    """
    if not sku:
        return {"ok": 0, "error": "Missing sku"}
    if stock_quantity is None:
        return {"ok": 0, "error": "Missing stock_quantity"}

    try:
        qty = int(stock_quantity)
    except (ValueError, TypeError):
        return {"ok": 0, "error": f"Invalid stock_quantity: {stock_quantity}"}

    try:
        cur.execute(
            "UPDATE eshop_products SET stock_quantity = %s, updated_at = CURRENT_TIMESTAMP "
            "WHERE tenant_id = %s AND sku = %s",
            (qty, tenant_id, sku),
        )
        return {"ok": 1, "error": ""}
    except Exception as e:
        logger.error("Failed to update product %s: %s", sku, e)
        return {"ok": 0, "error": f"Update failed: {e}"}


@router.post("/mufis/setProduct")
async def mufis_set_product(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
    mufis_access=Depends(verify_mufis_access),
    sku: Optional[str] = Form(None),
    stock_quantity: Optional[str] = Form(None),
    data: Optional[str] = Form(None),
):
    """MuFis: update product stock.

    Modes:
    - Single: sku, stock_quantity
    - Batch: data (JSON array with sku + stock_quantity per product)

    Response:
    - Single: {"ok": 1, "error": ""} or {"ok": 0, "error": "..."}
    - Batch: {"products": [{"sku": "...", "ok": 1, "error": ""}, ...]}
    """
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    if data:
        # BATCH mode — parse JSON list
        try:
            products_data = json.loads(data)
            if not isinstance(products_data, list):
                return {
                    "products": [
                        {
                            "sku": "",
                            "ok": 0,
                            "error": "data must be JSON array",
                        }
                    ]
                }
        except (json.JSONDecodeError, TypeError) as e:
            return {
                "products": [
                    {
                        "sku": "",
                        "ok": 0,
                        "error": f"Invalid JSON in data parameter: {e}",
                    }
                ]
            }

        results = []
        for item in products_data:
            if not isinstance(item, dict):
                results.append(
                    {"sku": "", "ok": 0, "error": "Each item must be an object"}
                )
                continue

            result = _process_set_product(
                cur, tenant_id, item.get("sku"), item.get("stock_quantity")
            )
            result["sku"] = item.get("sku", "")
            results.append(result)

        db.commit()
        return {"products": results}

    else:
        # SINGLE mode
        if not sku and stock_quantity is None:
            return {"ok": 0, "error": "Chýba sku/stock_quantity alebo data parameter"}

        result = _process_set_product(cur, tenant_id, sku, stock_quantity)
        db.commit()
        return result
