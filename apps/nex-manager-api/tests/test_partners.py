"""Unit tests for Partners (PAB) module — CRUD, validation, pagination, sorting, RBAC.

14+ test cases covering:
1. Create partner success
2. Create partner duplicate code (409)
3. Create partner missing required fields (422)
4. Get partners list (pagination structure)
5. Get partners filter by type
6. Get partners search
7. Get partners sorting
8. Get partner detail (200)
9. Get partner not found (404)
10. Update partner success
11. Update partner code readonly (400)
12. Partner validation — IČO format
13. Partner validation — email format
14. Partner RBAC — no permission (403)
"""

import os
import sys
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SAMPLE_UUID = uuid4()
_NOW = datetime.now(timezone.utc)


def _make_partner_row(
    partner_id=None,
    code="TEST001",
    name="Test Partner s.r.o.",
    partner_type="customer",
    is_supplier=False,
    is_customer=True,
    company_id="12345678",
    city="Bratislava",
    email="test@example.sk",
):
    """Build a fake DB row matching _PARTNER_COLUMNS order."""
    pid = partner_id or _SAMPLE_UUID
    return (
        pid,  # id
        code,  # code
        name,  # name
        partner_type,  # partner_type
        is_supplier,  # is_supplier
        is_customer,  # is_customer
        company_id,  # company_id
        "2021234567",  # tax_id
        "SK2021234567",  # vat_id
        True,  # is_vat_payer
        "Hlavná 1",  # street
        city,  # city
        "81101",  # zip_code
        "SK",  # country_code
        None,  # billing_street
        None,  # billing_city
        None,  # billing_zip_code
        None,  # billing_country_code
        None,  # shipping_street
        None,  # shipping_city
        None,  # shipping_zip_code
        None,  # shipping_country_code
        "+421901234567",  # phone
        None,  # mobile
        email,  # email
        None,  # website
        None,  # contact_person
        14,  # payment_due_days
        Decimal("0.00"),  # credit_limit
        Decimal("0.00"),  # discount_percent
        None,  # price_category
        "transfer",  # payment_method
        "EUR",  # currency
        None,  # iban
        None,  # bank_name
        None,  # swift_bic
        None,  # notes
        True,  # is_active
        _NOW,  # created_at
        _NOW,  # updated_at
    )


# ---------------------------------------------------------------------------
# 1. Create partner — success
# ---------------------------------------------------------------------------
def test_create_partner_success(client, fake_db):
    """POST /api/partners — 201 with valid data."""
    row = _make_partner_row()

    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            # First call: code uniqueness check → not found
            # Second call: company_id uniqueness check → not found
            return None
        # Third call: RETURNING from INSERT
        return row

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/partners",
        json={
            "code": "TEST001",
            "name": "Test Partner s.r.o.",
            "partner_type": "customer",
            "company_id": "12345678",
            "city": "Bratislava",
            "email": "test@example.sk",
        },
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["code"] == "TEST001"
    assert data["name"] == "Test Partner s.r.o."
    assert data["partner_type"] == "customer"
    assert data["is_active"] is True


# ---------------------------------------------------------------------------
# 2. Create partner — duplicate code (409)
# ---------------------------------------------------------------------------
def test_create_partner_duplicate_code(client, fake_db):
    """POST /api/partners — 409 when code already exists."""
    # Code uniqueness check returns existing partner
    fake_db.cursor().fetchone = lambda: (_SAMPLE_UUID,)

    resp = client.post(
        "/api/partners",
        json={
            "code": "EXISTING",
            "name": "Duplicate Partner",
        },
    )

    assert resp.status_code == 409
    assert "už existuje" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 3. Create partner — missing required fields (422)
# ---------------------------------------------------------------------------
def test_create_partner_missing_required(client):
    """POST /api/partners — 422 when code or name missing."""
    # Missing code
    resp = client.post("/api/partners", json={"name": "Only Name"})
    assert resp.status_code == 422

    # Missing name
    resp = client.post("/api/partners", json={"code": "ONLY_CODE"})
    assert resp.status_code == 422

    # Empty body
    resp = client.post("/api/partners", json={})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# 4. Get partners list — pagination structure
# ---------------------------------------------------------------------------
def test_get_partners_list(client, fake_db):
    """GET /api/partners — verify pagination response structure."""
    row1 = _make_partner_row(partner_id=uuid4(), code="A001")
    row2 = _make_partner_row(partner_id=uuid4(), code="A002")

    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        return (2,)  # total count

    def mock_fetchall():
        return [row1, row2]

    fake_db.cursor().fetchone = mock_fetchone
    fake_db.cursor().fetchall = mock_fetchall

    resp = client.get("/api/partners")

    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data
    assert data["total"] == 2
    assert data["page"] == 1
    assert len(data["items"]) == 2


# ---------------------------------------------------------------------------
# 5. Get partners — filter by type
# ---------------------------------------------------------------------------
def test_get_partners_filter_by_type(client, fake_db):
    """GET /api/partners?partner_type=supplier — filter works."""
    row = _make_partner_row(
        partner_type="supplier", is_supplier=True, is_customer=False
    )

    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/partners?partner_type=supplier")

    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["partner_type"] == "supplier"

    # Verify the query contained partner_type filter
    queries = fake_db.cursor().executed_queries
    count_query = queries[0][0]
    assert "partner_type = %s" in count_query


# ---------------------------------------------------------------------------
# 6. Get partners — search
# ---------------------------------------------------------------------------
def test_get_partners_search(client, fake_db):
    """GET /api/partners?search=bratislava — search across 5 fields."""
    row = _make_partner_row(city="Bratislava")

    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/partners?search=bratislava")

    assert resp.status_code == 200

    # Verify ILIKE search was applied
    queries = fake_db.cursor().executed_queries
    count_query = queries[0][0]
    assert "ILIKE" in count_query
    assert "code ILIKE" in count_query
    assert "name ILIKE" in count_query
    assert "company_id ILIKE" in count_query
    assert "city ILIKE" in count_query
    assert "email ILIKE" in count_query


# ---------------------------------------------------------------------------
# 7. Get partners — sorting
# ---------------------------------------------------------------------------
def test_get_partners_sorting(client, fake_db):
    """GET /api/partners?sort_by=name&sort_order=desc — sorting works."""
    row = _make_partner_row()

    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/partners?sort_by=name&sort_order=desc")

    assert resp.status_code == 200

    # Verify ORDER BY in query
    queries = fake_db.cursor().executed_queries
    select_query = queries[1][0]
    assert "ORDER BY name desc" in select_query


# ---------------------------------------------------------------------------
# 8. Get partner detail — 200
# ---------------------------------------------------------------------------
def test_get_partner_detail(client, fake_db):
    """GET /api/partners/{id} — 200 with data."""
    row = _make_partner_row()
    fake_db.cursor().fetchone = lambda: row

    resp = client.get(f"/api/partners/{_SAMPLE_UUID}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "TEST001"
    assert data["name"] == "Test Partner s.r.o."


# ---------------------------------------------------------------------------
# 9. Get partner not found — 404
# ---------------------------------------------------------------------------
def test_get_partner_not_found(client, fake_db):
    """GET /api/partners/{id} — 404 when not found."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.get(f"/api/partners/{uuid4()}")

    assert resp.status_code == 404
    assert "nebol nájdený" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 10. Update partner — success
# ---------------------------------------------------------------------------
def test_update_partner_success(client, fake_db):
    """PUT /api/partners/{id} — update name, verify response."""
    updated_row = _make_partner_row(name="Updated Name s.r.o.")

    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # Exists check
            return ("TEST001",)
        # After UPDATE — return updated row
        return updated_row

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put(
        f"/api/partners/{_SAMPLE_UUID}",
        json={
            "name": "Updated Name s.r.o.",
        },
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated Name s.r.o."


# ---------------------------------------------------------------------------
# 11. Update partner — code readonly (400)
# ---------------------------------------------------------------------------
def test_update_partner_code_readonly(client, fake_db):
    """PUT /api/partners/{id} — code cannot be changed, returns 400."""
    fake_db.cursor().fetchone = lambda: ("TEST001",)

    resp = client.put(
        f"/api/partners/{_SAMPLE_UUID}",
        json={
            "code": "NEWCODE",
            "name": "Updated Name",
        },
    )

    assert resp.status_code == 400
    assert "nie je možné zmeniť" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 12. Partner validation — IČO format
# ---------------------------------------------------------------------------
def test_partner_validation_ico(client):
    """POST /api/partners — invalid IČO format triggers 422."""
    resp = client.post(
        "/api/partners",
        json={
            "code": "V001",
            "name": "Validation Test",
            "company_id": "ABC-not-a-number",
        },
    )

    assert resp.status_code == 422
    body = resp.json()
    assert any("IČO" in str(e) or "čísla" in str(e) for e in body.get("detail", []))


# ---------------------------------------------------------------------------
# 13. Partner validation — email format
# ---------------------------------------------------------------------------
def test_partner_validation_email(client):
    """POST /api/partners — invalid email format triggers 422."""
    resp = client.post(
        "/api/partners",
        json={
            "code": "V002",
            "name": "Validation Email",
            "email": "not-an-email",
        },
    )

    assert resp.status_code == 422
    body = resp.json()
    assert any("email" in str(e).lower() for e in body.get("detail", []))


# ---------------------------------------------------------------------------
# 14. Partner RBAC — no permission (403)
# ---------------------------------------------------------------------------
def test_partner_rbac(client_no_auth):
    """GET /api/partners — without auth token returns 403 (or 401)."""
    resp = client_no_auth.get("/api/partners")

    # Without auth header, HTTPBearer raises 403
    assert resp.status_code in (401, 403)


# ---------------------------------------------------------------------------
# 15. Create partner — IČO duplicate warning (not error)
# ---------------------------------------------------------------------------
def test_create_partner_ico_warning(client, fake_db):
    """POST /api/partners — duplicate IČO produces warning, not error."""
    row = _make_partner_row(code="W001")

    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # Code uniqueness → not found
            return None
        if call_count == 2:
            # IČO uniqueness → found existing
            return ("EXISTING01",)
        # INSERT RETURNING
        return row

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/partners",
        json={
            "code": "W001",
            "name": "Warning Test",
            "company_id": "12345678",
        },
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["warnings"] is not None
    assert len(data["warnings"]) > 0
    assert "IČO" in data["warnings"][0]


# ---------------------------------------------------------------------------
# 16. Partner validation — discount percent out of range
# ---------------------------------------------------------------------------
def test_partner_validation_discount_range(client):
    """POST /api/partners — discount_percent > 100 triggers 422."""
    resp = client.post(
        "/api/partners",
        json={
            "code": "V003",
            "name": "Discount Test",
            "discount_percent": 150.0,
        },
    )

    assert resp.status_code == 422
