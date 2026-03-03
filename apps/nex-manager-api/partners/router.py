"""Partner management API endpoints — CRUD with pagination, sorting, RBAC, audit."""

import json
import math
from decimal import Decimal
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.dependencies import require_permission
from database import get_db

from .schemas import (
    PartnerCreate,
    PartnerListResponse,
    PartnerResponse,
    PartnerUpdate,
)

router = APIRouter(prefix="/api/partners", tags=["partners"])


# ---------------------------------------------------------------------------
# Column mapping — DB column order for SELECT
# ---------------------------------------------------------------------------

_PARTNER_COLUMNS = (
    "id, code, name, partner_type, is_supplier, is_customer, "
    "company_id, tax_id, vat_id, is_vat_payer, "
    "street, city, zip_code, country_code, "
    "billing_street, billing_city, billing_zip_code, billing_country_code, "
    "shipping_street, shipping_city, shipping_zip_code, shipping_country_code, "
    "phone, mobile, email, website, contact_person, "
    "payment_due_days, credit_limit, discount_percent, price_category, "
    "payment_method, currency, "
    "iban, bank_name, swift_bic, "
    "notes, is_active, created_at, updated_at"
)

# Whitelist of sortable columns to prevent SQL injection
_SORT_COLUMNS = frozenset({"code", "name", "city", "created_at"})


def _row_to_partner(row: tuple, warnings: list[str] | None = None) -> PartnerResponse:
    """Map a database row to PartnerResponse."""
    return PartnerResponse(
        id=row[0],
        code=row[1],
        name=row[2],
        partner_type=row[3],
        is_supplier=row[4],
        is_customer=row[5],
        company_id=row[6],
        tax_id=row[7],
        vat_id=row[8],
        is_vat_payer=row[9],
        street=row[10],
        city=row[11],
        zip_code=row[12],
        country_code=row[13],
        billing_street=row[14],
        billing_city=row[15],
        billing_zip_code=row[16],
        billing_country_code=row[17],
        shipping_street=row[18],
        shipping_city=row[19],
        shipping_zip_code=row[20],
        shipping_country_code=row[21],
        phone=row[22],
        mobile=row[23],
        email=row[24],
        website=row[25],
        contact_person=row[26],
        payment_due_days=row[27],
        credit_limit=float(row[28]) if isinstance(row[28], Decimal) else row[28],
        discount_percent=float(row[29]) if isinstance(row[29], Decimal) else row[29],
        price_category=row[30],
        payment_method=row[31],
        currency=row[32],
        iban=row[33],
        bank_name=row[34],
        swift_bic=row[35],
        notes=row[36],
        is_active=row[37],
        created_at=row[38],
        updated_at=row[39],
        warnings=warnings,
    )


def _write_audit_log(
    cur,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    details: dict | None = None,
) -> None:
    """Insert an audit log entry."""
    cur.execute(
        "INSERT INTO audit_log (user_id, action, entity_type, entity_id, details) "
        "VALUES (%s, %s, %s, %s, %s)",
        (
            user_id,
            action,
            entity_type,
            None,  # entity_id is INTEGER in audit_log, partner id is UUID
            json.dumps(
                {**(details or {}), "partner_uuid": str(entity_id)}
                if entity_id
                else details
            )
            if details or entity_id
            else None,
        ),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=PartnerListResponse)
def list_partners(
    partner_type: Optional[str] = Query(
        None, description="Filter: customer/supplier/both"
    ),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(
        None, description="Search in code, name, company_id, city, email"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    sort_by: str = Query(
        "code", description="Sort column: code, name, city, created_at"
    ),
    sort_order: str = Query("asc", description="Sort direction: asc, desc"),
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List partners with pagination, sorting, and filtering."""
    # Validate sort_by
    if sort_by not in _SORT_COLUMNS:
        sort_by = "code"
    if sort_order not in ("asc", "desc"):
        sort_order = "asc"

    conditions: list[str] = []
    params: list = []

    if partner_type is not None:
        conditions.append("partner_type = %s")
        params.append(partner_type)

    if is_active is not None:
        conditions.append("is_active = %s")
        params.append(is_active)

    if search is not None:
        search_val = search.strip()
        if search_val:
            conditions.append(
                "(code ILIKE %s OR name ILIKE %s OR company_id ILIKE %s "
                "OR city ILIKE %s OR email ILIKE %s)"
            )
            like_val = f"%{search_val}%"
            params.extend([like_val, like_val, like_val, like_val, like_val])

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    cur = db.cursor()

    # Count total
    cur.execute(f"SELECT COUNT(*) FROM partners {where_clause}", params)
    total = cur.fetchone()[0]

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    offset = (page - 1) * page_size

    # Fetch page — sort_by is validated against whitelist above
    cur.execute(
        f"SELECT {_PARTNER_COLUMNS} FROM partners {where_clause} "
        f"ORDER BY {sort_by} {sort_order} "
        f"LIMIT %s OFFSET %s",
        params + [page_size, offset],
    )
    rows = cur.fetchall()

    items = [_row_to_partner(row) for row in rows]
    return PartnerListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{partner_id}", response_model=PartnerResponse)
def get_partner(
    partner_id: UUID,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """Get a single partner by UUID."""
    cur = db.cursor()
    cur.execute(
        f"SELECT {_PARTNER_COLUMNS} FROM partners WHERE id = %s",
        (str(partner_id),),
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner nebol nájdený",
        )

    return _row_to_partner(row)


@router.post("", response_model=PartnerResponse, status_code=status.HTTP_201_CREATED)
def create_partner(
    body: PartnerCreate,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Create a new partner."""
    cur = db.cursor()
    warnings: list[str] = []

    # Check code uniqueness
    cur.execute("SELECT id FROM partners WHERE code = %s", (body.code,))
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Partner s kódom '{body.code}' už existuje",
        )

    # Check company_id (IČO) uniqueness — warning only, not error
    if body.company_id:
        cur.execute(
            "SELECT code FROM partners WHERE company_id = %s",
            (body.company_id,),
        )
        existing_ico = cur.fetchone()
        if existing_ico:
            warnings.append(
                f"IČO '{body.company_id}' sa už používa u partnera '{existing_ico[0]}'"
            )

    # Derive is_supplier / is_customer from partner_type
    is_supplier = body.partner_type in ("supplier", "both")
    is_customer = body.partner_type in ("customer", "both")

    # INSERT
    cur.execute(
        f"INSERT INTO partners ("
        "code, name, partner_type, is_supplier, is_customer, "
        "company_id, tax_id, vat_id, is_vat_payer, "
        "street, city, zip_code, country_code, "
        "billing_street, billing_city, billing_zip_code, billing_country_code, "
        "shipping_street, shipping_city, shipping_zip_code, shipping_country_code, "
        "phone, mobile, email, website, contact_person, "
        "payment_due_days, credit_limit, discount_percent, price_category, "
        "payment_method, currency, "
        "iban, bank_name, swift_bic, "
        "notes, is_active, created_by, updated_by"
        f") VALUES ("
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, "
        "%s, %s, %s, "
        "%s, %s, %s, %s"
        f") RETURNING {_PARTNER_COLUMNS}",
        (
            body.code,
            body.name,
            body.partner_type,
            is_supplier,
            is_customer,
            body.company_id,
            body.tax_id,
            body.vat_id,
            body.is_vat_payer,
            body.street,
            body.city,
            body.zip_code,
            body.country_code,
            body.billing_street,
            body.billing_city,
            body.billing_zip_code,
            body.billing_country_code,
            body.shipping_street,
            body.shipping_city,
            body.shipping_zip_code,
            body.shipping_country_code,
            body.phone,
            body.mobile,
            body.email,
            body.website,
            body.contact_person,
            body.payment_due_days,
            body.credit_limit,
            body.discount_percent,
            body.price_category,
            body.payment_method,
            body.currency,
            body.iban,
            body.bank_name,
            body.swift_bic,
            body.notes,
            body.is_active,
            current_user["login_name"],
            current_user["login_name"],
        ),
    )
    new_row = cur.fetchone()

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="create",
        entity_type="PAB",
        entity_id=str(new_row[0]),
        details={"message": f"Created partner {body.code}"},
    )

    db.commit()
    return _row_to_partner(new_row, warnings=warnings if warnings else None)


@router.put("/{partner_id}", response_model=PartnerResponse)
def update_partner(
    partner_id: UUID,
    body: PartnerUpdate,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Update an existing partner. Code is NOT editable."""
    cur = db.cursor()

    # Check partner exists
    cur.execute(
        "SELECT code FROM partners WHERE id = %s",
        (str(partner_id),),
    )
    existing = cur.fetchone()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner nebol nájdený",
        )
    partner_code = existing[0]

    # Build dynamic UPDATE — iterate over provided fields
    body_data = body.model_dump(exclude_unset=True)

    # Reject 'code' in update body (code is readonly after creation)
    if "code" in body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kód partnera nie je možné zmeniť po vytvorení",
        )

    if not body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    set_parts: list[str] = []
    params: list = []

    # If partner_type changes, derive is_supplier/is_customer
    if "partner_type" in body_data:
        pt = body_data["partner_type"]
        body_data["is_supplier"] = pt in ("supplier", "both")
        body_data["is_customer"] = pt in ("customer", "both")

    for field, value in body_data.items():
        set_parts.append(f"{field} = %s")
        params.append(value)

    # Always update audit fields
    set_parts.append("updated_by = %s")
    params.append(current_user["login_name"])

    params.append(str(partner_id))
    cur.execute(
        f"UPDATE partners SET {', '.join(set_parts)} WHERE id = %s",
        params,
    )

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="update",
        entity_type="PAB",
        entity_id=str(partner_id),
        details={"message": f"Updated partner {partner_code}"},
    )

    db.commit()

    # Return updated partner
    cur.execute(
        f"SELECT {_PARTNER_COLUMNS} FROM partners WHERE id = %s",
        (str(partner_id),),
    )
    row = cur.fetchone()
    return _row_to_partner(row)
