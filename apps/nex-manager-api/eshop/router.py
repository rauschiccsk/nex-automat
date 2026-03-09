"""ESHOP API endpoints — Public, Admin, and MuFis integration.

Public endpoints (X-Eshop-Token auth):
  GET    /api/eshop/products                    — list active products
  GET    /api/eshop/products/{sku}              — single product
  POST   /api/eshop/orders                      — create order
  GET    /api/eshop/orders/{order_number}        — order status

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

import json
import math
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Response, status

from auth.dependencies import require_permission
from database import get_db

from .dependencies import get_tenant_by_mufis_key, get_tenant_by_token
from .schemas import (
    AdminOrderDetailResponse,
    AdminOrderListItem,
    AdminOrderListResponse,
    AdminOrderUpdateRequest,
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
    AdminStatusHistoryItem,
    AdminTenantResponse,
    EshopProductListResponse,
    EshopProductResponse,
    OrderCreateRequest,
    OrderCreateResponse,
    OrderItemResponse,
    OrderStatusResponse,
)
from .utils import generate_order_number

router = APIRouter(prefix="/api/eshop", tags=["ESHOP"])


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
def create_order(
    body: OrderCreateRequest,
    tenant=Depends(get_tenant_by_token),
    db=Depends(get_db),
):
    """Create a new order. Prices are always taken from DB, never from request."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

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

        order_items.append({
            "product_id": product[0],
            "sku": product[1],
            "name": product[2],
            "quantity": item.quantity,
            "unit_price": product_price,
            "unit_price_vat": product_price_vat,
            "vat_rate": product_vat_rate,
        })

    # Add shipping price
    shipping_price = Decimal("0")
    if body.shipping_type:
        # Shipping price could come from a config table in the future
        pass
    total_amount_vat += shipping_price
    total_amount += shipping_price

    # Generate order number
    order_number = generate_order_number(tenant_id, tenant["brand_name"], db)

    # Insert order
    cur.execute(
        "INSERT INTO eshop_orders ("
        "tenant_id, order_number, customer_email, customer_name, customer_phone, "
        "lang, billing_name, billing_name2, billing_street, billing_city, "
        "billing_zip, billing_country, shipping_name, shipping_name2, "
        "shipping_street, shipping_city, shipping_zip, shipping_country, "
        "ico, dic, eu_vat_number, total_amount, total_amount_vat, "
        "currency, payment_method, shipping_type, shipping_price, note, "
        "delivery_point_group, delivery_point_id, status, payment_status"
        ") VALUES ("
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s"
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

    # Insert initial status history
    cur.execute(
        "INSERT INTO eshop_order_status_history ("
        "order_id, old_status, new_status, changed_by, note"
        ") VALUES (%s, %s, %s, %s, %s)",
        (order_id, None, "new", "system", ""),
    )

    db.commit()

    return OrderCreateResponse(
        order_number=order_number,
        status="new",
        total_amount_vat=total_amount_vat,
        currency=tenant["currency"],
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
            sku=ir[0], name=ir[1], quantity=ir[2],
            unit_price_vat=ir[3], vat_rate=ir[4],
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
            old_status=hr[0], new_status=hr[1],
            changed_by=hr[2], note=hr[3] or "", created_at=hr[4],
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
def admin_update_order(
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
    if body.status is not None and body.status != old_status:
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
        products.append({
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
        })

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
    page: int = Form(1),
    order_number: Optional[str] = Form(None),
    order_id: Optional[int] = Form(None),
    updated_at_min: Optional[str] = Form(None),
    status_filter: Optional[str] = Form(None, alias="status"),
    date_from: Optional[str] = Form(None),
    date_to: Optional[str] = Form(None),
):
    """MuFis: get orders with filtering."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()
    per_page = 50

    conditions: list[str] = ["tenant_id = %s"]
    params: list = [tenant_id]

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
        conditions.append("status = %s")
        params.append(status_filter)
    if date_from:
        conditions.append("created_at >= %s")
        params.append(date_from)
    if date_to:
        conditions.append("created_at <= %s")
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
        f"created_at, updated_at "
        f"FROM eshop_orders {where} ORDER BY order_id DESC "
        f"LIMIT %s OFFSET %s",
        params + [per_page, offset],
    )
    order_rows = cur.fetchall()

    # Payment method mapping
    pm_map = {
        "credit_card": "CARD",
        "bank_transfer": "BANK",
        "cod": "COD",
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
        items = [
            {
                "sku": ir[0],
                "name": ir[1],
                "quantity": ir[2],
                "unit_price": _dec(ir[3]),
                "unit_price_vat": _dec(ir[4]),
                "vat_rate": _dec(ir[5]),
                "item_type": ir[6],
            }
            for ir in cur.fetchall()
        ]

        payment_method_raw = r[25] or ""
        payment_method_mapped = pm_map.get(payment_method_raw, "OTHER")

        orders.append({
            "order_id": r[0],
            "order_number": r[1],
            "customer_email": r[3],
            "customer_name": r[4],
            "customer_phone": r[5] or "",
            "lang": r[6] or "sk",
            "billing_name": r[7] or "",
            "billing_name2": r[8] or "",
            "billing_street": r[9] or "",
            "billing_city": r[10] or "",
            "billing_zip": r[11] or "",
            "billing_country": r[12] or "",
            "shipping_name": r[13] or "",
            "shipping_name2": r[14] or "",
            "shipping_street": r[15] or "",
            "shipping_city": r[16] or "",
            "shipping_zip": r[17] or "",
            "shipping_country": r[18] or "",
            "ico": r[19] or "",
            "dic": r[20] or "",
            "eu_vat_number": r[21] or "",
            "total_amount": _dec(r[22]),
            "total_amount_vat": _dec(r[23]),
            "currency": r[24],
            "payment_method": payment_method_mapped,
            "payment_status": r[26] or "",
            "shipping_type": r[27] or "",
            "shipping_price": _dec(r[28]),
            "delivery_point_group": r[29] or "",
            "delivery_point_id": r[30] or "",
            "tracking_number": r[31] or "",
            "tracking_link": r[32] or "",
            "multiple_packages": r[33],
            "status": r[34],
            "note": r[35] or "",
            "created_at": r[36].isoformat() if r[36] else "",
            "updated_at": r[37].isoformat() if r[37] else "",
            "items": items,
        })

    return {
        "total_pages": total_pages,
        "page": page,
        "orders": orders,
    }


# ============================================================================
# MUFIS — setOrder
# ============================================================================


@router.post("/mufis/setOrder")
async def mufis_set_order(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
    order_number: Optional[str] = Form(None),
    status_val: Optional[str] = Form(None, alias="status"),
    package_number: Optional[str] = Form(None),
    tracking_link: Optional[str] = Form(None),
    multiple_packages: Optional[bool] = Form(None),
    data: Optional[str] = Form(None),
):
    """MuFis: update order status/tracking. Supports batch via 'data' param."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    items_to_process = []

    if data:
        # Batch mode — parse JSON list
        try:
            batch = json.loads(data)
            if isinstance(batch, list):
                items_to_process = batch
            else:
                items_to_process = [batch]
        except (json.JSONDecodeError, TypeError):
            return {"ok": 0, "error": "Neplatný JSON v 'data' parametri"}
    elif order_number:
        items_to_process = [{
            "order_number": order_number,
            "status": status_val,
            "package_number": package_number,
            "tracking_link": tracking_link,
            "multiple_packages": multiple_packages,
        }]
    else:
        return {"ok": 0, "error": "Chýba order_number alebo data parameter"}

    for item in items_to_process:
        on = item.get("order_number")
        if not on:
            continue

        # Get current order
        cur.execute(
            "SELECT order_id, status FROM eshop_orders "
            "WHERE order_number = %s AND tenant_id = %s",
            (on, tenant_id),
        )
        order = cur.fetchone()
        if not order:
            continue

        order_id_val = order[0]
        old_status = order[1]

        set_parts: list[str] = []
        params: list = []

        new_status = item.get("status")
        if new_status:
            set_parts.append("status = %s")
            params.append(new_status)

        pkg = item.get("package_number")
        if pkg:
            set_parts.append("tracking_number = %s")
            params.append(pkg)

        tl = item.get("tracking_link")
        if tl:
            set_parts.append("tracking_link = %s")
            params.append(tl)

        mp = item.get("multiple_packages")
        if mp is not None:
            set_parts.append("multiple_packages = %s")
            params.append(mp)

        if set_parts:
            params.append(order_id_val)
            cur.execute(
                f"UPDATE eshop_orders SET {', '.join(set_parts)} "
                f"WHERE order_id = %s",
                params,
            )

        # Status history
        if new_status and new_status != old_status:
            cur.execute(
                "INSERT INTO eshop_order_status_history ("
                "order_id, old_status, new_status, changed_by, note"
                ") VALUES (%s, %s, %s, %s, %s)",
                (order_id_val, old_status, new_status, "mufis", ""),
            )

    db.commit()
    return {"ok": 1}


# ============================================================================
# MUFIS — getProduct
# ============================================================================


@router.post("/mufis/getProduct")
async def mufis_get_product(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
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
        f"FROM eshop_products {where} ORDER BY product_id "
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


@router.post("/mufis/setProduct")
async def mufis_set_product(
    tenant=Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
    sku: Optional[str] = Form(None),
    stock_quantity: Optional[int] = Form(None),
    data: Optional[str] = Form(None),
):
    """MuFis: update product stock. Supports batch via 'data' param."""
    tenant_id = tenant["tenant_id"]
    cur = db.cursor()

    items_to_process = []

    if data:
        try:
            batch = json.loads(data)
            if isinstance(batch, list):
                items_to_process = batch
            else:
                items_to_process = [batch]
        except (json.JSONDecodeError, TypeError):
            return {"ok": 0, "error": "Neplatný JSON v 'data' parametri"}
    elif sku and stock_quantity is not None:
        items_to_process = [{"sku": sku, "stock_quantity": stock_quantity}]
    else:
        return {"ok": 0, "error": "Chýba sku/stock_quantity alebo data parameter"}

    for item in items_to_process:
        item_sku = item.get("sku")
        item_qty = item.get("stock_quantity")
        if item_sku is None or item_qty is None:
            continue

        cur.execute(
            "UPDATE eshop_products SET stock_quantity = %s "
            "WHERE tenant_id = %s AND sku = %s",
            (item_qty, tenant_id, item_sku),
        )

    db.commit()
    return {"ok": 1}
