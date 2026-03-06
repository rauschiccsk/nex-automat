"""Partner Catalog (PAB) API endpoints — 25 endpoints for partner_catalog + child tables.

Endpoints:
  Partners (CRUD):
    GET    /api/pab/partners                              — list with filter/search/pagination/sort
    GET    /api/pab/partners/{partner_id}                 — detail with all child data
    POST   /api/pab/partners                              — create
    PUT    /api/pab/partners/{partner_id}                 — update
    DELETE /api/pab/partners/{partner_id}                 — soft delete

  Extensions (1:1 upsert):
    GET    /api/pab/partners/{partner_id}/extensions
    PUT    /api/pab/partners/{partner_id}/extensions      — upsert

  Addresses (CRUD):
    GET    /api/pab/partners/{partner_id}/addresses
    POST   /api/pab/partners/{partner_id}/addresses
    PUT    /api/pab/partners/{partner_id}/addresses/{address_type}
    DELETE /api/pab/partners/{partner_id}/addresses/{address_type}

  Contacts (CRUD):
    GET    /api/pab/partners/{partner_id}/contacts
    POST   /api/pab/partners/{partner_id}/contacts
    PUT    /api/pab/partners/{partner_id}/contacts/{contact_id}
    DELETE /api/pab/partners/{partner_id}/contacts/{contact_id}

  Bank Accounts (CRUD):
    GET    /api/pab/partners/{partner_id}/bank-accounts
    POST   /api/pab/partners/{partner_id}/bank-accounts
    PUT    /api/pab/partners/{partner_id}/bank-accounts/{account_id}
    DELETE /api/pab/partners/{partner_id}/bank-accounts/{account_id}

  Categories (assign/unassign):
    GET    /api/pab/partners/{partner_id}/categories
    POST   /api/pab/partners/{partner_id}/categories
    DELETE /api/pab/partners/{partner_id}/categories/{category_id}

  Texts (upsert):
    GET    /api/pab/partners/{partner_id}/texts
    PUT    /api/pab/partners/{partner_id}/texts           — upsert

  Facilities (CRUD):
    GET    /api/pab/partners/{partner_id}/facilities
    POST   /api/pab/partners/{partner_id}/facilities
    PUT    /api/pab/partners/{partner_id}/facilities/{facility_id}
    DELETE /api/pab/partners/{partner_id}/facilities/{facility_id}
"""

import json
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.dependencies import require_permission
from database import get_db
from nex_config.limits import DEFAULT_PAGE_SIZE

from .schemas import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
    BankAccountCreate,
    BankAccountResponse,
    BankAccountUpdate,
    CategoryAssign,
    CategoryMappingResponse,
    ContactCreate,
    ContactResponse,
    ContactUpdate,
    ExtensionsResponse,
    ExtensionsUpsert,
    FacilityCreate,
    FacilityResponse,
    FacilityUpdate,
    PartnerCatalogCreate,
    PartnerCatalogListResponse,
    PartnerCatalogResponse,
    PartnerCatalogUpdate,
    TextResponse,
    TextUpsert,
)

router = APIRouter(prefix="/api/pab", tags=["PAB - Partner Catalog"])


# ---------------------------------------------------------------------------
# Column definitions
# ---------------------------------------------------------------------------

_PARTNER_COLUMNS = (
    "partner_id, partner_code, partner_name, reg_name, "
    "company_id, tax_id, vat_id, is_vat_payer, "
    "is_supplier, is_customer, "
    "street, city, zip_code, country_code, "
    "bank_account_count, facility_count, "
    "is_active, created_at, updated_at"
)

_SORT_COLUMNS = frozenset(
    {"partner_id", "partner_code", "partner_name", "city", "created_at"}
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _dec(v):
    """Convert Decimal to float for JSON serialization."""
    return float(v) if isinstance(v, Decimal) else v


def _row_to_partner(row: tuple) -> PartnerCatalogResponse:
    """Map a database row to PartnerCatalogResponse."""
    return PartnerCatalogResponse(
        partner_id=row[0],
        partner_code=row[1],
        partner_name=row[2],
        reg_name=row[3],
        company_id=row[4],
        tax_id=row[5],
        vat_id=row[6],
        is_vat_payer=row[7],
        is_supplier=row[8],
        is_customer=row[9],
        street=row[10],
        city=row[11],
        zip_code=row[12],
        country_code=row[13],
        bank_account_count=row[14],
        facility_count=row[15],
        is_active=row[16],
        created_at=row[17],
        updated_at=row[18],
    )


def _ensure_partner_exists(cur, partner_id: int) -> None:
    """Raise 404 if partner_catalog record does not exist."""
    cur.execute(
        "SELECT partner_id FROM partner_catalog WHERE partner_id = %s",
        (partner_id,),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partner {partner_id} nebol nájdený",
        )


def _write_audit_log(
    cur,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
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
            entity_id,
            json.dumps(details) if details else None,
        ),
    )


# ===================================================================
# 1–5  PARTNER CATALOG — CRUD
# ===================================================================


@router.get("/partners", response_model=PartnerCatalogListResponse)
def list_partners(
    partner_type: Optional[str] = Query(
        None, description="Filter: supplier or customer"
    ),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(
        None, description="Search in partner_code, partner_name, company_id, city"
    ),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=10000, description="Limit"),
    offset: int = Query(0, ge=0, description="Offset"),
    sort_by: str = Query(
        "partner_id",
        description="Sort column: partner_id, partner_code, partner_name, city, created_at",
    ),
    sort_order: str = Query("asc", description="Sort direction: asc, desc"),
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List partners from partner_catalog with filtering, search, pagination, sorting."""
    if sort_by not in _SORT_COLUMNS:
        sort_by = "partner_id"
    if sort_order not in ("asc", "desc"):
        sort_order = "asc"

    conditions: list[str] = []
    params: list = []

    if partner_type == "supplier":
        conditions.append("is_supplier = true")
    elif partner_type == "customer":
        conditions.append("is_customer = true")

    if is_active is not None:
        conditions.append("is_active = %s")
        params.append(is_active)

    if search:
        s = search.strip()
        if s:
            conditions.append(
                "(partner_code ILIKE %s OR partner_name ILIKE %s "
                "OR company_id ILIKE %s OR city ILIKE %s)"
            )
            like = f"%{s}%"
            params.extend([like, like, like, like])

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    cur = db.cursor()

    # Total count
    cur.execute(f"SELECT COUNT(*) FROM partner_catalog {where}", params)
    total = cur.fetchone()[0]

    # Fetch page — sort_by validated against whitelist
    cur.execute(
        f"SELECT {_PARTNER_COLUMNS} FROM partner_catalog {where} "
        f"ORDER BY {sort_by} {sort_order} LIMIT %s OFFSET %s",
        params + [limit, offset],
    )
    rows = cur.fetchall()

    return PartnerCatalogListResponse(
        items=[_row_to_partner(r) for r in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/partners/{partner_id}", response_model=PartnerCatalogResponse)
def get_partner(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """Get partner detail with all child data aggregated."""
    cur = db.cursor()
    cur.execute(
        f"SELECT {_PARTNER_COLUMNS} FROM partner_catalog WHERE partner_id = %s",
        (partner_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partner {partner_id} nebol nájdený",
        )

    partner = _row_to_partner(row)

    # --- Extensions ---
    cur.execute(
        "SELECT partner_id, sale_payment_method_id, sale_transport_method_id, "
        "sale_payment_due_days, sale_currency_code, sale_price_category, "
        "sale_discount_percent, sale_credit_limit, "
        "purchase_payment_method_id, purchase_transport_method_id, "
        "purchase_payment_due_days, purchase_currency_code, "
        "purchase_price_category, purchase_discount_percent, "
        "last_sale_date, last_purchase_date, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_extensions WHERE partner_id = %s",
        (partner_id,),
    )
    ext_row = cur.fetchone()
    if ext_row:
        partner.extensions = ExtensionsResponse(
            partner_id=ext_row[0],
            sale_payment_method_id=ext_row[1],
            sale_transport_method_id=ext_row[2],
            sale_payment_due_days=ext_row[3],
            sale_currency_code=ext_row[4],
            sale_price_category=ext_row[5],
            sale_discount_percent=_dec(ext_row[6]),
            sale_credit_limit=_dec(ext_row[7]),
            purchase_payment_method_id=ext_row[8],
            purchase_transport_method_id=ext_row[9],
            purchase_payment_due_days=ext_row[10],
            purchase_currency_code=ext_row[11],
            purchase_price_category=ext_row[12],
            purchase_discount_percent=_dec(ext_row[13]),
            last_sale_date=str(ext_row[14]) if ext_row[14] else None,
            last_purchase_date=str(ext_row[15]) if ext_row[15] else None,
            is_active=ext_row[16],
            created_at=ext_row[17],
            updated_at=ext_row[18],
        )

    # --- Addresses ---
    cur.execute(
        "SELECT id, partner_id, address_type, street, city, zip_code, "
        "country_code, is_active, created_at, updated_at "
        "FROM partner_catalog_addresses WHERE partner_id = %s ORDER BY address_type",
        (partner_id,),
    )
    partner.addresses = [
        AddressResponse(
            id=r[0],
            partner_id=r[1],
            address_type=r[2],
            street=r[3],
            city=r[4],
            zip_code=r[5],
            country_code=r[6],
            is_active=r[7],
            created_at=r[8],
            updated_at=r[9],
        )
        for r in cur.fetchall()
    ]

    # --- Contacts ---
    cur.execute(
        "SELECT contact_id, partner_id, contact_type, title, first_name, last_name, "
        "function_name, phone_work, phone_mobile, phone_private, fax, email, "
        "street, city, zip_code, country_code, is_active, created_at, updated_at "
        "FROM partner_catalog_contacts WHERE partner_id = %s ORDER BY contact_id",
        (partner_id,),
    )
    partner.contacts = [
        ContactResponse(
            contact_id=r[0],
            partner_id=r[1],
            contact_type=r[2],
            title=r[3],
            first_name=r[4],
            last_name=r[5],
            function_name=r[6],
            phone_work=r[7],
            phone_mobile=r[8],
            phone_private=r[9],
            fax=r[10],
            email=r[11],
            street=r[12],
            city=r[13],
            zip_code=r[14],
            country_code=r[15],
            is_active=r[16],
            created_at=r[17],
            updated_at=r[18],
        )
        for r in cur.fetchall()
    ]

    # --- Texts ---
    cur.execute(
        "SELECT text_id, partner_id, text_type, line_number, language, "
        "text_content, is_active, created_at, updated_at "
        "FROM partner_catalog_texts WHERE partner_id = %s "
        "ORDER BY text_type, line_number",
        (partner_id,),
    )
    partner.texts = [
        TextResponse(
            text_id=r[0],
            partner_id=r[1],
            text_type=r[2],
            line_number=r[3],
            language=r[4],
            text_content=r[5],
            is_active=r[6],
            created_at=r[7],
            updated_at=r[8],
        )
        for r in cur.fetchall()
    ]

    # --- Bank Accounts ---
    cur.execute(
        "SELECT account_id, partner_id, iban_code, swift_code, account_number, "
        "bank_name, bank_seat, vs_sale, vs_purchase, is_primary, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_bank_accounts WHERE partner_id = %s ORDER BY account_id",
        (partner_id,),
    )
    partner.bank_accounts = [
        BankAccountResponse(
            account_id=r[0],
            partner_id=r[1],
            iban_code=r[2],
            swift_code=r[3],
            account_number=r[4],
            bank_name=r[5],
            bank_seat=r[6],
            vs_sale=r[7],
            vs_purchase=r[8],
            is_primary=r[9],
            is_active=r[10],
            created_at=r[11],
            updated_at=r[12],
        )
        for r in cur.fetchall()
    ]

    # --- Facilities ---
    cur.execute(
        "SELECT facility_id, partner_id, facility_name, street, city, zip_code, "
        "country_code, phone, fax, email, transport_method_id, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_facilities WHERE partner_id = %s ORDER BY facility_id",
        (partner_id,),
    )
    partner.facilities = [
        FacilityResponse(
            facility_id=r[0],
            partner_id=r[1],
            facility_name=r[2],
            street=r[3],
            city=r[4],
            zip_code=r[5],
            country_code=r[6],
            phone=r[7],
            fax=r[8],
            email=r[9],
            transport_method_id=r[10],
            is_active=r[11],
            created_at=r[12],
            updated_at=r[13],
        )
        for r in cur.fetchall()
    ]

    # --- Categories ---
    cur.execute(
        "SELECT id, partner_id, category_id, category_type, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_categories WHERE partner_id = %s ORDER BY id",
        (partner_id,),
    )
    partner.categories = [
        CategoryMappingResponse(
            id=r[0],
            partner_id=r[1],
            category_id=r[2],
            category_type=r[3],
            is_active=r[4],
            created_at=r[5],
            updated_at=r[6],
        )
        for r in cur.fetchall()
    ]

    return partner


@router.post(
    "/partners",
    response_model=PartnerCatalogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_partner(
    body: PartnerCatalogCreate,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Create a new partner in partner_catalog."""
    cur = db.cursor()

    # Check partner_id uniqueness
    cur.execute(
        "SELECT partner_id FROM partner_catalog WHERE partner_id = %s",
        (body.partner_id,),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Partner s ID {body.partner_id} už existuje",
        )

    # Check partner_code uniqueness
    cur.execute(
        "SELECT partner_id FROM partner_catalog WHERE partner_code = %s",
        (body.partner_code,),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Partner s kódom '{body.partner_code}' už existuje",
        )

    cur.execute(
        f"INSERT INTO partner_catalog ("
        "partner_id, partner_code, partner_name, reg_name, "
        "company_id, tax_id, vat_id, is_vat_payer, "
        "is_supplier, is_customer, "
        "street, city, zip_code, country_code, "
        "is_active, created_by, updated_by"
        f") VALUES ("
        "%s, %s, %s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, "
        "%s, %s, %s, %s, "
        "%s, %s, %s"
        f") RETURNING {_PARTNER_COLUMNS}",
        (
            body.partner_id,
            body.partner_code,
            body.partner_name,
            body.reg_name,
            body.company_id,
            body.tax_id,
            body.vat_id,
            body.is_vat_payer,
            body.is_supplier,
            body.is_customer,
            body.street,
            body.city,
            body.zip_code,
            body.country_code,
            body.is_active,
            current_user["login_name"],
            current_user["login_name"],
        ),
    )
    new_row = cur.fetchone()

    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="create",
        entity_type="PAB",
        entity_id=body.partner_id,
        details={"message": f"Created partner_catalog {body.partner_code}"},
    )

    db.commit()
    return _row_to_partner(new_row)


@router.put("/partners/{partner_id}", response_model=PartnerCatalogResponse)
def update_partner(
    partner_id: int,
    body: PartnerCatalogUpdate,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Update an existing partner. partner_id and partner_code are NOT editable."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

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
        params.append(value)

    set_parts.append("updated_by = %s")
    params.append(current_user["login_name"])
    params.append(partner_id)

    cur.execute(
        f"UPDATE partner_catalog SET {', '.join(set_parts)} WHERE partner_id = %s",
        params,
    )

    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="update",
        entity_type="PAB",
        entity_id=partner_id,
        details={"message": f"Updated partner_catalog {partner_id}"},
    )

    db.commit()

    cur.execute(
        f"SELECT {_PARTNER_COLUMNS} FROM partner_catalog WHERE partner_id = %s",
        (partner_id,),
    )
    return _row_to_partner(cur.fetchone())


@router.delete("/partners/{partner_id}")
def delete_partner(
    partner_id: int,
    current_user=Depends(require_permission("PAB", "can_delete")),
    db=Depends(get_db),
):
    """Soft delete a partner (set is_active = false)."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

    cur.execute(
        "UPDATE partner_catalog SET is_active = false, updated_by = %s "
        "WHERE partner_id = %s",
        (current_user["login_name"], partner_id),
    )

    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="soft_delete",
        entity_type="PAB",
        entity_id=partner_id,
        details={"message": f"Soft deleted partner_catalog {partner_id}"},
    )

    db.commit()
    return {"message": f"Partner {partner_id} deaktivovaný"}


# ===================================================================
# 6–7  EXTENSIONS (1:1 upsert)
# ===================================================================


@router.get(
    "/partners/{partner_id}/extensions",
    response_model=ExtensionsResponse | None,
)
def get_extensions(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """Get partner extensions (1:1)."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

    cur.execute(
        "SELECT partner_id, sale_payment_method_id, sale_transport_method_id, "
        "sale_payment_due_days, sale_currency_code, sale_price_category, "
        "sale_discount_percent, sale_credit_limit, "
        "purchase_payment_method_id, purchase_transport_method_id, "
        "purchase_payment_due_days, purchase_currency_code, "
        "purchase_price_category, purchase_discount_percent, "
        "last_sale_date, last_purchase_date, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_extensions WHERE partner_id = %s",
        (partner_id,),
    )
    r = cur.fetchone()
    if not r:
        return None

    return ExtensionsResponse(
        partner_id=r[0],
        sale_payment_method_id=r[1],
        sale_transport_method_id=r[2],
        sale_payment_due_days=r[3],
        sale_currency_code=r[4],
        sale_price_category=r[5],
        sale_discount_percent=_dec(r[6]),
        sale_credit_limit=_dec(r[7]),
        purchase_payment_method_id=r[8],
        purchase_transport_method_id=r[9],
        purchase_payment_due_days=r[10],
        purchase_currency_code=r[11],
        purchase_price_category=r[12],
        purchase_discount_percent=_dec(r[13]),
        last_sale_date=str(r[14]) if r[14] else None,
        last_purchase_date=str(r[15]) if r[15] else None,
        is_active=r[16],
        created_at=r[17],
        updated_at=r[18],
    )


@router.put("/partners/{partner_id}/extensions", response_model=ExtensionsResponse)
def upsert_extensions(
    partner_id: int,
    body: ExtensionsUpsert,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Upsert partner extensions (create if not exists, update if exists)."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

    # Check if exists
    cur.execute(
        "SELECT partner_id FROM partner_catalog_extensions WHERE partner_id = %s",
        (partner_id,),
    )
    exists = cur.fetchone() is not None
    login = current_user["login_name"]

    if exists:
        cur.execute(
            "UPDATE partner_catalog_extensions SET "
            "sale_payment_method_id = %s, sale_transport_method_id = %s, "
            "sale_payment_due_days = %s, sale_currency_code = %s, "
            "sale_price_category = %s, sale_discount_percent = %s, "
            "sale_credit_limit = %s, "
            "purchase_payment_method_id = %s, purchase_transport_method_id = %s, "
            "purchase_payment_due_days = %s, purchase_currency_code = %s, "
            "purchase_price_category = %s, purchase_discount_percent = %s, "
            "last_sale_date = %s, last_purchase_date = %s, "
            "updated_by = %s "
            "WHERE partner_id = %s",
            (
                body.sale_payment_method_id,
                body.sale_transport_method_id,
                body.sale_payment_due_days,
                body.sale_currency_code,
                body.sale_price_category,
                body.sale_discount_percent,
                body.sale_credit_limit,
                body.purchase_payment_method_id,
                body.purchase_transport_method_id,
                body.purchase_payment_due_days,
                body.purchase_currency_code,
                body.purchase_price_category,
                body.purchase_discount_percent,
                body.last_sale_date,
                body.last_purchase_date,
                login,
                partner_id,
            ),
        )
    else:
        cur.execute(
            "INSERT INTO partner_catalog_extensions ("
            "partner_id, sale_payment_method_id, sale_transport_method_id, "
            "sale_payment_due_days, sale_currency_code, sale_price_category, "
            "sale_discount_percent, sale_credit_limit, "
            "purchase_payment_method_id, purchase_transport_method_id, "
            "purchase_payment_due_days, purchase_currency_code, "
            "purchase_price_category, purchase_discount_percent, "
            "last_sale_date, last_purchase_date, "
            "created_by, updated_by"
            ") VALUES ("
            "%s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
            ")",
            (
                partner_id,
                body.sale_payment_method_id,
                body.sale_transport_method_id,
                body.sale_payment_due_days,
                body.sale_currency_code,
                body.sale_price_category,
                body.sale_discount_percent,
                body.sale_credit_limit,
                body.purchase_payment_method_id,
                body.purchase_transport_method_id,
                body.purchase_payment_due_days,
                body.purchase_currency_code,
                body.purchase_price_category,
                body.purchase_discount_percent,
                body.last_sale_date,
                body.last_purchase_date,
                login,
                login,
            ),
        )

    db.commit()

    cur.execute(
        "SELECT partner_id, sale_payment_method_id, sale_transport_method_id, "
        "sale_payment_due_days, sale_currency_code, sale_price_category, "
        "sale_discount_percent, sale_credit_limit, "
        "purchase_payment_method_id, purchase_transport_method_id, "
        "purchase_payment_due_days, purchase_currency_code, "
        "purchase_price_category, purchase_discount_percent, "
        "last_sale_date, last_purchase_date, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_extensions WHERE partner_id = %s",
        (partner_id,),
    )
    r = cur.fetchone()
    return ExtensionsResponse(
        partner_id=r[0],
        sale_payment_method_id=r[1],
        sale_transport_method_id=r[2],
        sale_payment_due_days=r[3],
        sale_currency_code=r[4],
        sale_price_category=r[5],
        sale_discount_percent=_dec(r[6]),
        sale_credit_limit=_dec(r[7]),
        purchase_payment_method_id=r[8],
        purchase_transport_method_id=r[9],
        purchase_payment_due_days=r[10],
        purchase_currency_code=r[11],
        purchase_price_category=r[12],
        purchase_discount_percent=_dec(r[13]),
        last_sale_date=str(r[14]) if r[14] else None,
        last_purchase_date=str(r[15]) if r[15] else None,
        is_active=r[16],
        created_at=r[17],
        updated_at=r[18],
    )


# ===================================================================
# 8–11  ADDRESSES
# ===================================================================


@router.get("/partners/{partner_id}/addresses", response_model=list[AddressResponse])
def list_addresses(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List addresses for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    cur.execute(
        "SELECT id, partner_id, address_type, street, city, zip_code, "
        "country_code, is_active, created_at, updated_at "
        "FROM partner_catalog_addresses WHERE partner_id = %s ORDER BY address_type",
        (partner_id,),
    )
    return [
        AddressResponse(
            id=r[0],
            partner_id=r[1],
            address_type=r[2],
            street=r[3],
            city=r[4],
            zip_code=r[5],
            country_code=r[6],
            is_active=r[7],
            created_at=r[8],
            updated_at=r[9],
        )
        for r in cur.fetchall()
    ]


@router.post(
    "/partners/{partner_id}/addresses",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    partner_id: int,
    body: AddressCreate,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Create an address for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

    # Check uniqueness (partner_id, address_type)
    cur.execute(
        "SELECT id FROM partner_catalog_addresses "
        "WHERE partner_id = %s AND address_type = %s",
        (partner_id, body.address_type),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Adresa typu '{body.address_type}' už existuje pre partnera {partner_id}",
        )

    login = current_user["login_name"]
    cur.execute(
        "INSERT INTO partner_catalog_addresses ("
        "partner_id, address_type, street, city, zip_code, country_code, "
        "created_by, updated_by"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        "RETURNING id, partner_id, address_type, street, city, zip_code, "
        "country_code, is_active, created_at, updated_at",
        (
            partner_id,
            body.address_type,
            body.street,
            body.city,
            body.zip_code,
            body.country_code,
            login,
            login,
        ),
    )
    r = cur.fetchone()
    db.commit()
    return AddressResponse(
        id=r[0],
        partner_id=r[1],
        address_type=r[2],
        street=r[3],
        city=r[4],
        zip_code=r[5],
        country_code=r[6],
        is_active=r[7],
        created_at=r[8],
        updated_at=r[9],
    )


@router.put(
    "/partners/{partner_id}/addresses/{address_type}",
    response_model=AddressResponse,
)
def update_address(
    partner_id: int,
    address_type: str,
    body: AddressUpdate,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Update an address by partner_id and address_type."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

    body_data = body.model_dump(exclude_unset=True)
    if not body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    set_parts = [f"{k} = %s" for k in body_data]
    params = list(body_data.values())
    set_parts.append("updated_by = %s")
    params.append(current_user["login_name"])
    params.extend([partner_id, address_type])

    cur.execute(
        f"UPDATE partner_catalog_addresses SET {', '.join(set_parts)} "
        "WHERE partner_id = %s AND address_type = %s "
        "RETURNING id, partner_id, address_type, street, city, zip_code, "
        "country_code, is_active, created_at, updated_at",
        params,
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Adresa typu '{address_type}' nenájdená",
        )
    db.commit()
    return AddressResponse(
        id=r[0],
        partner_id=r[1],
        address_type=r[2],
        street=r[3],
        city=r[4],
        zip_code=r[5],
        country_code=r[6],
        is_active=r[7],
        created_at=r[8],
        updated_at=r[9],
    )


@router.delete("/partners/{partner_id}/addresses/{address_type}")
def delete_address(
    partner_id: int,
    address_type: str,
    _current_user=Depends(require_permission("PAB", "can_delete")),
    db=Depends(get_db),
):
    """Delete an address by partner_id and address_type."""
    cur = db.cursor()
    cur.execute(
        "DELETE FROM partner_catalog_addresses "
        "WHERE partner_id = %s AND address_type = %s RETURNING id",
        (partner_id, address_type),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Adresa typu '{address_type}' nenájdená",
        )
    db.commit()
    return {"message": "Adresa odstránená"}


# ===================================================================
# 12–15  CONTACTS
# ===================================================================


@router.get("/partners/{partner_id}/contacts", response_model=list[ContactResponse])
def list_contacts(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List contacts for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    cur.execute(
        "SELECT contact_id, partner_id, contact_type, title, first_name, last_name, "
        "function_name, phone_work, phone_mobile, phone_private, fax, email, "
        "street, city, zip_code, country_code, is_active, created_at, updated_at "
        "FROM partner_catalog_contacts WHERE partner_id = %s ORDER BY contact_id",
        (partner_id,),
    )
    return [
        ContactResponse(
            contact_id=r[0],
            partner_id=r[1],
            contact_type=r[2],
            title=r[3],
            first_name=r[4],
            last_name=r[5],
            function_name=r[6],
            phone_work=r[7],
            phone_mobile=r[8],
            phone_private=r[9],
            fax=r[10],
            email=r[11],
            street=r[12],
            city=r[13],
            zip_code=r[14],
            country_code=r[15],
            is_active=r[16],
            created_at=r[17],
            updated_at=r[18],
        )
        for r in cur.fetchall()
    ]


@router.post(
    "/partners/{partner_id}/contacts",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact(
    partner_id: int,
    body: ContactCreate,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Create a contact for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    login = current_user["login_name"]

    cur.execute(
        "INSERT INTO partner_catalog_contacts ("
        "partner_id, contact_type, title, first_name, last_name, function_name, "
        "phone_work, phone_mobile, phone_private, fax, email, "
        "street, city, zip_code, country_code, created_by, updated_by"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "RETURNING contact_id, partner_id, contact_type, title, first_name, last_name, "
        "function_name, phone_work, phone_mobile, phone_private, fax, email, "
        "street, city, zip_code, country_code, is_active, created_at, updated_at",
        (
            partner_id,
            body.contact_type,
            body.title,
            body.first_name,
            body.last_name,
            body.function_name,
            body.phone_work,
            body.phone_mobile,
            body.phone_private,
            body.fax,
            body.email,
            body.street,
            body.city,
            body.zip_code,
            body.country_code,
            login,
            login,
        ),
    )
    r = cur.fetchone()
    db.commit()
    return ContactResponse(
        contact_id=r[0],
        partner_id=r[1],
        contact_type=r[2],
        title=r[3],
        first_name=r[4],
        last_name=r[5],
        function_name=r[6],
        phone_work=r[7],
        phone_mobile=r[8],
        phone_private=r[9],
        fax=r[10],
        email=r[11],
        street=r[12],
        city=r[13],
        zip_code=r[14],
        country_code=r[15],
        is_active=r[16],
        created_at=r[17],
        updated_at=r[18],
    )


@router.put(
    "/partners/{partner_id}/contacts/{contact_id}",
    response_model=ContactResponse,
)
def update_contact(
    partner_id: int,
    contact_id: int,
    body: ContactUpdate,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Update a contact."""
    cur = db.cursor()
    body_data = body.model_dump(exclude_unset=True)
    if not body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    set_parts = [f"{k} = %s" for k in body_data]
    params = list(body_data.values())
    set_parts.append("updated_by = %s")
    params.append(current_user["login_name"])
    params.extend([partner_id, contact_id])

    cur.execute(
        f"UPDATE partner_catalog_contacts SET {', '.join(set_parts)} "
        "WHERE partner_id = %s AND contact_id = %s "
        "RETURNING contact_id, partner_id, contact_type, title, first_name, "
        "last_name, function_name, phone_work, phone_mobile, phone_private, "
        "fax, email, street, city, zip_code, country_code, "
        "is_active, created_at, updated_at",
        params,
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kontakt {contact_id} nenájdený",
        )
    db.commit()
    return ContactResponse(
        contact_id=r[0],
        partner_id=r[1],
        contact_type=r[2],
        title=r[3],
        first_name=r[4],
        last_name=r[5],
        function_name=r[6],
        phone_work=r[7],
        phone_mobile=r[8],
        phone_private=r[9],
        fax=r[10],
        email=r[11],
        street=r[12],
        city=r[13],
        zip_code=r[14],
        country_code=r[15],
        is_active=r[16],
        created_at=r[17],
        updated_at=r[18],
    )


@router.delete("/partners/{partner_id}/contacts/{contact_id}")
def delete_contact(
    partner_id: int,
    contact_id: int,
    _current_user=Depends(require_permission("PAB", "can_delete")),
    db=Depends(get_db),
):
    """Delete a contact."""
    cur = db.cursor()
    cur.execute(
        "DELETE FROM partner_catalog_contacts "
        "WHERE partner_id = %s AND contact_id = %s RETURNING contact_id",
        (partner_id, contact_id),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kontakt {contact_id} nenájdený",
        )
    db.commit()
    return {"message": "Kontakt odstránený"}


# ===================================================================
# 16–19  BANK ACCOUNTS
# ===================================================================


@router.get(
    "/partners/{partner_id}/bank-accounts",
    response_model=list[BankAccountResponse],
)
def list_bank_accounts(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List bank accounts for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    cur.execute(
        "SELECT account_id, partner_id, iban_code, swift_code, account_number, "
        "bank_name, bank_seat, vs_sale, vs_purchase, is_primary, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_bank_accounts WHERE partner_id = %s ORDER BY account_id",
        (partner_id,),
    )
    return [
        BankAccountResponse(
            account_id=r[0],
            partner_id=r[1],
            iban_code=r[2],
            swift_code=r[3],
            account_number=r[4],
            bank_name=r[5],
            bank_seat=r[6],
            vs_sale=r[7],
            vs_purchase=r[8],
            is_primary=r[9],
            is_active=r[10],
            created_at=r[11],
            updated_at=r[12],
        )
        for r in cur.fetchall()
    ]


@router.post(
    "/partners/{partner_id}/bank-accounts",
    response_model=BankAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bank_account(
    partner_id: int,
    body: BankAccountCreate,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Create a bank account for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    login = current_user["login_name"]

    cur.execute(
        "INSERT INTO partner_catalog_bank_accounts ("
        "partner_id, iban_code, swift_code, account_number, bank_name, "
        "bank_seat, vs_sale, vs_purchase, is_primary, created_by, updated_by"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "RETURNING account_id, partner_id, iban_code, swift_code, account_number, "
        "bank_name, bank_seat, vs_sale, vs_purchase, is_primary, "
        "is_active, created_at, updated_at",
        (
            partner_id,
            body.iban_code,
            body.swift_code,
            body.account_number,
            body.bank_name,
            body.bank_seat,
            body.vs_sale,
            body.vs_purchase,
            body.is_primary,
            login,
            login,
        ),
    )
    r = cur.fetchone()
    db.commit()
    return BankAccountResponse(
        account_id=r[0],
        partner_id=r[1],
        iban_code=r[2],
        swift_code=r[3],
        account_number=r[4],
        bank_name=r[5],
        bank_seat=r[6],
        vs_sale=r[7],
        vs_purchase=r[8],
        is_primary=r[9],
        is_active=r[10],
        created_at=r[11],
        updated_at=r[12],
    )


@router.put(
    "/partners/{partner_id}/bank-accounts/{account_id}",
    response_model=BankAccountResponse,
)
def update_bank_account(
    partner_id: int,
    account_id: int,
    body: BankAccountUpdate,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Update a bank account."""
    cur = db.cursor()
    body_data = body.model_dump(exclude_unset=True)
    if not body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    set_parts = [f"{k} = %s" for k in body_data]
    params = list(body_data.values())
    set_parts.append("updated_by = %s")
    params.append(current_user["login_name"])
    params.extend([partner_id, account_id])

    cur.execute(
        f"UPDATE partner_catalog_bank_accounts SET {', '.join(set_parts)} "
        "WHERE partner_id = %s AND account_id = %s "
        "RETURNING account_id, partner_id, iban_code, swift_code, account_number, "
        "bank_name, bank_seat, vs_sale, vs_purchase, is_primary, "
        "is_active, created_at, updated_at",
        params,
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bankový účet {account_id} nenájdený",
        )
    db.commit()
    return BankAccountResponse(
        account_id=r[0],
        partner_id=r[1],
        iban_code=r[2],
        swift_code=r[3],
        account_number=r[4],
        bank_name=r[5],
        bank_seat=r[6],
        vs_sale=r[7],
        vs_purchase=r[8],
        is_primary=r[9],
        is_active=r[10],
        created_at=r[11],
        updated_at=r[12],
    )


@router.delete("/partners/{partner_id}/bank-accounts/{account_id}")
def delete_bank_account(
    partner_id: int,
    account_id: int,
    _current_user=Depends(require_permission("PAB", "can_delete")),
    db=Depends(get_db),
):
    """Delete a bank account."""
    cur = db.cursor()
    cur.execute(
        "DELETE FROM partner_catalog_bank_accounts "
        "WHERE partner_id = %s AND account_id = %s RETURNING account_id",
        (partner_id, account_id),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bankový účet {account_id} nenájdený",
        )
    db.commit()
    return {"message": "Bankový účet odstránený"}


# ===================================================================
# 20–22  CATEGORIES (assign / unassign)
# ===================================================================


@router.get(
    "/partners/{partner_id}/categories",
    response_model=list[CategoryMappingResponse],
)
def list_categories(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List category mappings for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    cur.execute(
        "SELECT id, partner_id, category_id, category_type, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_categories WHERE partner_id = %s ORDER BY id",
        (partner_id,),
    )
    return [
        CategoryMappingResponse(
            id=r[0],
            partner_id=r[1],
            category_id=r[2],
            category_type=r[3],
            is_active=r[4],
            created_at=r[5],
            updated_at=r[6],
        )
        for r in cur.fetchall()
    ]


@router.post(
    "/partners/{partner_id}/categories",
    response_model=CategoryMappingResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_category(
    partner_id: int,
    body: CategoryAssign,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Assign a category to a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)

    # Check uniqueness
    cur.execute(
        "SELECT id FROM partner_catalog_categories "
        "WHERE partner_id = %s AND category_id = %s",
        (partner_id, body.category_id),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Kategória {body.category_id} je už priradená partneru {partner_id}",
        )

    login = current_user["login_name"]
    cur.execute(
        "INSERT INTO partner_catalog_categories ("
        "partner_id, category_id, category_type, created_by, updated_by"
        ") VALUES (%s, %s, %s, %s, %s) "
        "RETURNING id, partner_id, category_id, category_type, "
        "is_active, created_at, updated_at",
        (partner_id, body.category_id, body.category_type, login, login),
    )
    r = cur.fetchone()
    db.commit()
    return CategoryMappingResponse(
        id=r[0],
        partner_id=r[1],
        category_id=r[2],
        category_type=r[3],
        is_active=r[4],
        created_at=r[5],
        updated_at=r[6],
    )


@router.delete("/partners/{partner_id}/categories/{category_id}")
def unassign_category(
    partner_id: int,
    category_id: int,
    _current_user=Depends(require_permission("PAB", "can_delete")),
    db=Depends(get_db),
):
    """Unassign a category from a partner."""
    cur = db.cursor()
    cur.execute(
        "DELETE FROM partner_catalog_categories "
        "WHERE partner_id = %s AND category_id = %s RETURNING id",
        (partner_id, category_id),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mapovanie kategórie {category_id} nenájdené",
        )
    db.commit()
    return {"message": "Kategória odpriradená"}


# ===================================================================
# 23–24  TEXTS (upsert)
# ===================================================================


@router.get("/partners/{partner_id}/texts", response_model=list[TextResponse])
def list_texts(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List texts for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    cur.execute(
        "SELECT text_id, partner_id, text_type, line_number, language, "
        "text_content, is_active, created_at, updated_at "
        "FROM partner_catalog_texts WHERE partner_id = %s "
        "ORDER BY text_type, line_number",
        (partner_id,),
    )
    return [
        TextResponse(
            text_id=r[0],
            partner_id=r[1],
            text_type=r[2],
            line_number=r[3],
            language=r[4],
            text_content=r[5],
            is_active=r[6],
            created_at=r[7],
            updated_at=r[8],
        )
        for r in cur.fetchall()
    ]


@router.put("/partners/{partner_id}/texts", response_model=TextResponse)
def upsert_text(
    partner_id: int,
    body: TextUpsert,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Upsert a text entry (create if not exists, update if exists)."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    login = current_user["login_name"]

    # Check if exists
    cur.execute(
        "SELECT text_id FROM partner_catalog_texts "
        "WHERE partner_id = %s AND text_type = %s "
        "AND line_number = %s AND language = %s",
        (partner_id, body.text_type, body.line_number, body.language),
    )
    existing = cur.fetchone()

    if existing:
        cur.execute(
            "UPDATE partner_catalog_texts SET text_content = %s, updated_by = %s "
            "WHERE text_id = %s "
            "RETURNING text_id, partner_id, text_type, line_number, language, "
            "text_content, is_active, created_at, updated_at",
            (body.text_content, login, existing[0]),
        )
    else:
        cur.execute(
            "INSERT INTO partner_catalog_texts ("
            "partner_id, text_type, line_number, language, text_content, "
            "created_by, updated_by"
            ") VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "RETURNING text_id, partner_id, text_type, line_number, language, "
            "text_content, is_active, created_at, updated_at",
            (
                partner_id,
                body.text_type,
                body.line_number,
                body.language,
                body.text_content,
                login,
                login,
            ),
        )

    r = cur.fetchone()
    db.commit()
    return TextResponse(
        text_id=r[0],
        partner_id=r[1],
        text_type=r[2],
        line_number=r[3],
        language=r[4],
        text_content=r[5],
        is_active=r[6],
        created_at=r[7],
        updated_at=r[8],
    )


# ===================================================================
# 25–28  FACILITIES
# ===================================================================


@router.get(
    "/partners/{partner_id}/facilities",
    response_model=list[FacilityResponse],
)
def list_facilities(
    partner_id: int,
    _current_user=Depends(require_permission("PAB", "can_view")),
    db=Depends(get_db),
):
    """List facilities for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    cur.execute(
        "SELECT facility_id, partner_id, facility_name, street, city, zip_code, "
        "country_code, phone, fax, email, transport_method_id, "
        "is_active, created_at, updated_at "
        "FROM partner_catalog_facilities WHERE partner_id = %s ORDER BY facility_id",
        (partner_id,),
    )
    return [
        FacilityResponse(
            facility_id=r[0],
            partner_id=r[1],
            facility_name=r[2],
            street=r[3],
            city=r[4],
            zip_code=r[5],
            country_code=r[6],
            phone=r[7],
            fax=r[8],
            email=r[9],
            transport_method_id=r[10],
            is_active=r[11],
            created_at=r[12],
            updated_at=r[13],
        )
        for r in cur.fetchall()
    ]


@router.post(
    "/partners/{partner_id}/facilities",
    response_model=FacilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_facility(
    partner_id: int,
    body: FacilityCreate,
    current_user=Depends(require_permission("PAB", "can_create")),
    db=Depends(get_db),
):
    """Create a facility for a partner."""
    cur = db.cursor()
    _ensure_partner_exists(cur, partner_id)
    login = current_user["login_name"]

    cur.execute(
        "INSERT INTO partner_catalog_facilities ("
        "partner_id, facility_name, street, city, zip_code, country_code, "
        "phone, fax, email, transport_method_id, created_by, updated_by"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "RETURNING facility_id, partner_id, facility_name, street, city, zip_code, "
        "country_code, phone, fax, email, transport_method_id, "
        "is_active, created_at, updated_at",
        (
            partner_id,
            body.facility_name,
            body.street,
            body.city,
            body.zip_code,
            body.country_code,
            body.phone,
            body.fax,
            body.email,
            body.transport_method_id,
            login,
            login,
        ),
    )
    r = cur.fetchone()
    db.commit()
    return FacilityResponse(
        facility_id=r[0],
        partner_id=r[1],
        facility_name=r[2],
        street=r[3],
        city=r[4],
        zip_code=r[5],
        country_code=r[6],
        phone=r[7],
        fax=r[8],
        email=r[9],
        transport_method_id=r[10],
        is_active=r[11],
        created_at=r[12],
        updated_at=r[13],
    )


@router.put(
    "/partners/{partner_id}/facilities/{facility_id}",
    response_model=FacilityResponse,
)
def update_facility(
    partner_id: int,
    facility_id: int,
    body: FacilityUpdate,
    current_user=Depends(require_permission("PAB", "can_edit")),
    db=Depends(get_db),
):
    """Update a facility."""
    cur = db.cursor()
    body_data = body.model_dump(exclude_unset=True)
    if not body_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Žiadne polia na aktualizáciu",
        )

    set_parts = [f"{k} = %s" for k in body_data]
    params = list(body_data.values())
    set_parts.append("updated_by = %s")
    params.append(current_user["login_name"])
    params.extend([partner_id, facility_id])

    cur.execute(
        f"UPDATE partner_catalog_facilities SET {', '.join(set_parts)} "
        "WHERE partner_id = %s AND facility_id = %s "
        "RETURNING facility_id, partner_id, facility_name, street, city, zip_code, "
        "country_code, phone, fax, email, transport_method_id, "
        "is_active, created_at, updated_at",
        params,
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prevádzka {facility_id} nenájdená",
        )
    db.commit()
    return FacilityResponse(
        facility_id=r[0],
        partner_id=r[1],
        facility_name=r[2],
        street=r[3],
        city=r[4],
        zip_code=r[5],
        country_code=r[6],
        phone=r[7],
        fax=r[8],
        email=r[9],
        transport_method_id=r[10],
        is_active=r[11],
        created_at=r[12],
        updated_at=r[13],
    )


@router.delete("/partners/{partner_id}/facilities/{facility_id}")
def delete_facility(
    partner_id: int,
    facility_id: int,
    _current_user=Depends(require_permission("PAB", "can_delete")),
    db=Depends(get_db),
):
    """Delete a facility."""
    cur = db.cursor()
    cur.execute(
        "DELETE FROM partner_catalog_facilities "
        "WHERE partner_id = %s AND facility_id = %s RETURNING facility_id",
        (partner_id, facility_id),
    )
    if not cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prevádzka {facility_id} nenájdená",
        )
    db.commit()
    return {"message": "Prevádzka odstránená"}
