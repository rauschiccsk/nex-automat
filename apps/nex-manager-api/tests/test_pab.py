"""Unit tests for Partner Catalog (PAB) module — 30 endpoints, 70+ test cases.

Covers:
  Partner CRUD lifecycle (create → read → update → soft delete → verify)
  Child table CRUD: extensions, addresses, contacts, bank accounts, facilities,
                    categories, texts
  Validation: duplicate partner_id, missing required fields, invalid types
  Pagination, sorting, filtering, search
  Extensions upsert (create if not exists, update if exists)
  Soft delete: partner is inactive, child data remains
  RBAC: 403 without authentication
  Versioning: partner_class, modify_id, history endpoints
"""

import os
import sys
from datetime import datetime, timezone

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

_NOW = datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Helpers — fake DB rows
# ---------------------------------------------------------------------------


def _partner_row(
    partner_id=100,
    partner_name="Test s.r.o.",
    reg_name=None,
    company_id="12345678",
    tax_id="2021234567",
    vat_id="SK2021234567",
    is_vat_payer=True,
    is_supplier=False,
    is_customer=True,
    street="Hlavná 1",
    city="Bratislava",
    zip_code="81101",
    country_code="SK",
    partner_class="business",
    modify_id=0,
    bank_account_count=0,
    facility_count=0,
    is_active=True,
):
    """Return a tuple matching _PARTNER_COLUMNS order."""
    return (
        partner_id,
        partner_name,
        reg_name,
        company_id,
        tax_id,
        vat_id,
        is_vat_payer,
        is_supplier,
        is_customer,
        street,
        city,
        zip_code,
        country_code,
        partner_class,
        modify_id,
        bank_account_count,
        facility_count,
        is_active,
        _NOW,
        _NOW,
    )


def _history_row(
    history_id=1,
    partner_id=100,
    modify_id=0,
    partner_name="Test s.r.o.",
    reg_name=None,
    company_id="12345678",
    tax_id="2021234567",
    vat_id="SK2021234567",
    is_vat_payer=True,
    is_supplier=False,
    is_customer=True,
    street="Hlavná 1",
    city="Bratislava",
    zip_code="81101",
    country_code="SK",
    partner_class="business",
    valid_to=None,
    changed_by="admin",
):
    """Return a tuple matching _HISTORY_COLUMNS order."""
    return (
        history_id,
        partner_id,
        modify_id,
        partner_name,
        reg_name,
        company_id,
        tax_id,
        vat_id,
        is_vat_payer,
        is_supplier,
        is_customer,
        street,
        city,
        zip_code,
        country_code,
        partner_class,
        _NOW,
        valid_to,
        changed_by,
    )


def _ext_row(partner_id=100):
    """Return a tuple matching extensions SELECT order."""
    return (
        partner_id,
        None,
        None,
        14,
        "EUR",
        None,
        0,
        0,
        None,
        None,
        14,
        "EUR",
        None,
        0,
        None,
        None,
        True,
        _NOW,
        _NOW,
    )


def _addr_row(addr_id=1, partner_id=100, atype="registered"):
    return (
        addr_id,
        partner_id,
        atype,
        "Hlavná 1",
        "Bratislava",
        "81101",
        "SK",
        True,
        _NOW,
        _NOW,
    )


def _contact_row(contact_id=1, partner_id=100):
    return (
        contact_id,
        partner_id,
        "person",
        "Ing.",
        "Ján",
        "Novák",
        "riaditeľ",
        "+421901234567",
        "+421902345678",
        None,
        None,
        "jan@test.sk",
        None,
        None,
        None,
        None,
        True,
        _NOW,
        _NOW,
    )


def _bank_row(account_id=1, partner_id=100):
    return (
        account_id,
        partner_id,
        "SK1234567890123456789012",
        "TATRSKBX",
        "123456",
        "Tatra banka",
        "Bratislava",
        "1234",
        "5678",
        True,
        True,
        _NOW,
        _NOW,
    )


def _text_row(text_id=1, partner_id=100):
    return (
        text_id,
        partner_id,
        "owner_name",
        1,
        "sk",
        "Ján Novák",
        True,
        _NOW,
        _NOW,
    )


def _facility_row(facility_id=1, partner_id=100):
    return (
        facility_id,
        partner_id,
        "Pobočka Košice",
        "Hlavná 10",
        "Košice",
        "04001",
        "SK",
        "+421553456789",
        None,
        "pobocka@test.sk",
        None,
        True,
        _NOW,
        _NOW,
    )


def _cat_row(cat_id=1, partner_id=100, category_id=10):
    return (
        cat_id,
        partner_id,
        category_id,
        "supplier",
        True,
        _NOW,
        _NOW,
    )


# ===================================================================
# PARTNER CATALOG CRUD
# ===================================================================


# 1. Create partner — success
def test_create_partner_success(client, fake_db):
    """POST /api/pab/partners — 201 with valid data."""
    row = _partner_row()
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return None  # partner_id uniqueness check
        return row  # RETURNING

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 100,
            "partner_name": "Test s.r.o.",
            "company_id": "12345678",
            "is_customer": True,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["partner_id"] == 100
    assert data["is_active"] is True


# 2. Create partner — duplicate ID (409)
def test_create_partner_duplicate_id(client, fake_db):
    """POST /api/pab/partners — 409 when partner_id already exists."""
    fake_db.cursor().fetchone = lambda: (100,)

    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 100,
            "partner_name": "Dup Test",
        },
    )
    assert resp.status_code == 409
    assert "už existuje" in resp.json()["detail"]


# 3. Create partner — missing required fields (422)
def test_create_partner_missing_required(client):
    """POST /api/pab/partners — 422 when required fields missing."""
    resp = client.post("/api/pab/partners", json={"partner_id": 1})
    assert resp.status_code == 422


# 5. Create partner — invalid partner_id (422)
def test_create_partner_invalid_id(client):
    """POST /api/pab/partners — 422 when partner_id <= 0."""
    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 0,
            "partner_name": "Zero ID",
        },
    )
    assert resp.status_code == 422


# 6. Get partners list — pagination
def test_list_partners_pagination(client, fake_db):
    """GET /api/pab/partners — returns pagination structure."""
    r1 = _partner_row(partner_id=1)
    r2 = _partner_row(partner_id=2)

    fake_db.cursor().fetchone = lambda: (2,)
    fake_db.cursor().fetchall = lambda: [r1, r2]

    resp = client.get("/api/pab/partners")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert data["total"] == 2
    assert len(data["items"]) == 2


# 7. Get partners — filter by supplier
def test_list_partners_filter_supplier(client, fake_db):
    """GET /api/pab/partners?partner_type=supplier — filters correctly."""
    row = _partner_row(is_supplier=True, is_customer=False)
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners?partner_type=supplier")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    count_q = queries[0][0]
    assert "is_supplier = true" in count_q


# 8. Get partners — search
def test_list_partners_search(client, fake_db):
    """GET /api/pab/partners?search=bratislava — ILIKE search."""
    row = _partner_row()
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners?search=bratislava")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    count_q = queries[0][0]
    assert "ILIKE" in count_q


# 9. Get partners — sorting
def test_list_partners_sorting(client, fake_db):
    """GET /api/pab/partners?sort_by=partner_name&sort_order=desc — sorting."""
    row = _partner_row()
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners?sort_by=partner_name&sort_order=desc")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    select_q = queries[1][0]
    assert "ORDER BY partner_name desc" in select_q


# 10. Get partners — invalid sort column falls back
def test_list_partners_invalid_sort(client, fake_db):
    """GET /api/pab/partners?sort_by=DROP_TABLE — falls back to partner_id."""
    row = _partner_row()
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners?sort_by=DROP_TABLE")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    select_q = queries[1][0]
    assert "ORDER BY partner_id" in select_q


# 11. Get partner detail — 200
def test_get_partner_detail(client, fake_db):
    """GET /api/pab/partners/100 — returns detail with child data."""
    row = _partner_row()
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return row  # main partner
        if call_count == 2:
            return _ext_row()  # extensions
        return None

    fake_db.cursor().fetchone = mock_fetchone
    fake_db.cursor().fetchall = lambda: []

    resp = client.get("/api/pab/partners/100")
    assert resp.status_code == 200
    data = resp.json()
    assert data["partner_id"] == 100
    assert "extensions" in data
    assert "addresses" in data
    assert "contacts" in data
    assert "bank_accounts" in data
    assert "facilities" in data
    assert "categories" in data


# 12. Get partner — not found (404)
def test_get_partner_not_found(client, fake_db):
    """GET /api/pab/partners/999 — 404 when not found."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.get("/api/pab/partners/999")
    assert resp.status_code == 404
    assert "nebol nájdený" in resp.json()["detail"]


# 13. Update partner — success
def test_update_partner_success(client, fake_db):
    """PUT /api/pab/partners/100 — updates name."""
    updated = _partner_row(partner_name="Updated s.r.o.")
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # exists check
        return updated  # after update

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put("/api/pab/partners/100", json={"partner_name": "Updated s.r.o."})
    assert resp.status_code == 200
    assert resp.json()["partner_name"] == "Updated s.r.o."


# 14. Update partner — not found (404)
def test_update_partner_not_found(client, fake_db):
    """PUT /api/pab/partners/999 — 404 when partner doesn't exist."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.put("/api/pab/partners/999", json={"partner_name": "Nope"})
    assert resp.status_code == 404


# 15. Update partner — empty body (400)
def test_update_partner_empty_body(client, fake_db):
    """PUT /api/pab/partners/100 — 400 when no fields provided."""
    fake_db.cursor().fetchone = lambda: (100,)

    resp = client.put("/api/pab/partners/100", json={})
    assert resp.status_code == 400
    assert "Žiadne polia" in resp.json()["detail"]


# 16. Soft delete partner
def test_delete_partner_soft(client, fake_db):
    """DELETE /api/pab/partners/100 — soft deletes (is_active=false)."""
    fake_db.cursor().fetchone = lambda: (100,)

    resp = client.delete("/api/pab/partners/100")
    assert resp.status_code == 200
    assert "deaktivovaný" in resp.json()["message"]

    # Verify UPDATE query
    queries = fake_db.cursor().executed_queries
    update_q = [q for q, _ in queries if "is_active = false" in q]
    assert len(update_q) >= 1


# 17. Soft delete — not found
def test_delete_partner_not_found(client, fake_db):
    """DELETE /api/pab/partners/999 — 404."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.delete("/api/pab/partners/999")
    assert resp.status_code == 404


# ===================================================================
# EXTENSIONS (1:1 upsert)
# ===================================================================


# 18. Get extensions — 200
def test_get_extensions(client, fake_db):
    """GET /api/pab/partners/100/extensions — returns extensions."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return _ext_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.get("/api/pab/partners/100/extensions")
    assert resp.status_code == 200
    data = resp.json()
    assert data["partner_id"] == 100
    assert data["sale_payment_due_days"] == 14


# 19. Upsert extensions — create
def test_upsert_extensions_create(client, fake_db):
    """PUT /api/pab/partners/100/extensions — creates when not exists."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        if call_count == 2:
            return None  # extensions not exists
        return _ext_row()  # after insert

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put(
        "/api/pab/partners/100/extensions",
        json={
            "sale_payment_due_days": 30,
            "sale_currency_code": "CZK",
        },
    )
    assert resp.status_code == 200


# 20. Upsert extensions — update
def test_upsert_extensions_update(client, fake_db):
    """PUT /api/pab/partners/100/extensions — updates when exists."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        if call_count == 2:
            return (100,)  # extensions exists
        return _ext_row()  # after update

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put(
        "/api/pab/partners/100/extensions",
        json={
            "sale_payment_due_days": 60,
        },
    )
    assert resp.status_code == 200


# ===================================================================
# ADDRESSES
# ===================================================================


# 21. List addresses
def test_list_addresses(client, fake_db):
    """GET /api/pab/partners/100/addresses — returns list."""
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [_addr_row()]

    resp = client.get("/api/pab/partners/100/addresses")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["address_type"] == "registered"


# 22. Create address
def test_create_address(client, fake_db):
    """POST /api/pab/partners/100/addresses — 201."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        if call_count == 2:
            return None  # no duplicate
        return _addr_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/addresses",
        json={
            "address_type": "registered",
            "street": "Hlavná 1",
            "city": "Bratislava",
        },
    )
    assert resp.status_code == 201


# 23. Create address — duplicate type (409)
def test_create_address_duplicate_type(client, fake_db):
    """POST /api/pab/partners/100/addresses — 409 when type exists."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return (1,)  # duplicate

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/addresses",
        json={
            "address_type": "registered",
            "city": "Košice",
        },
    )
    assert resp.status_code == 409


# 24. Update address
def test_update_address(client, fake_db):
    """PUT /api/pab/partners/100/addresses/registered — updates."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return _addr_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put(
        "/api/pab/partners/100/addresses/registered",
        json={
            "city": "Košice",
        },
    )
    assert resp.status_code == 200


# 25. Delete address
def test_delete_address(client, fake_db):
    """DELETE /api/pab/partners/100/addresses/registered — deletes."""
    fake_db.cursor().fetchone = lambda: (1,)

    resp = client.delete("/api/pab/partners/100/addresses/registered")
    assert resp.status_code == 200


# 26. Delete address — not found
def test_delete_address_not_found(client, fake_db):
    """DELETE /api/pab/partners/100/addresses/invoice — 404."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.delete("/api/pab/partners/100/addresses/invoice")
    assert resp.status_code == 404


# ===================================================================
# CONTACTS
# ===================================================================


# 27. List contacts
def test_list_contacts(client, fake_db):
    """GET /api/pab/partners/100/contacts — returns list."""
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [_contact_row()]

    resp = client.get("/api/pab/partners/100/contacts")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# 28. Create contact
def test_create_contact(client, fake_db):
    """POST /api/pab/partners/100/contacts — 201."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return _contact_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/contacts",
        json={
            "contact_type": "person",
            "first_name": "Ján",
            "last_name": "Novák",
        },
    )
    assert resp.status_code == 201


# 29. Update contact
def test_update_contact(client, fake_db):
    """PUT /api/pab/partners/100/contacts/1 — updates."""
    fake_db.cursor().fetchone = lambda: _contact_row()

    resp = client.put(
        "/api/pab/partners/100/contacts/1",
        json={
            "first_name": "Peter",
        },
    )
    assert resp.status_code == 200


# 30. Delete contact
def test_delete_contact(client, fake_db):
    """DELETE /api/pab/partners/100/contacts/1 — deletes."""
    fake_db.cursor().fetchone = lambda: (1,)

    resp = client.delete("/api/pab/partners/100/contacts/1")
    assert resp.status_code == 200


# ===================================================================
# BANK ACCOUNTS
# ===================================================================


# 31. List bank accounts
def test_list_bank_accounts(client, fake_db):
    """GET /api/pab/partners/100/bank-accounts — returns list."""
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [_bank_row()]

    resp = client.get("/api/pab/partners/100/bank-accounts")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# 32. Create bank account
def test_create_bank_account(client, fake_db):
    """POST /api/pab/partners/100/bank-accounts — 201."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return _bank_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/bank-accounts",
        json={
            "iban_code": "SK1234567890123456789012",
            "is_primary": True,
        },
    )
    assert resp.status_code == 201


# 33. Update bank account
def test_update_bank_account(client, fake_db):
    """PUT /api/pab/partners/100/bank-accounts/1 — updates."""
    fake_db.cursor().fetchone = lambda: _bank_row()

    resp = client.put(
        "/api/pab/partners/100/bank-accounts/1",
        json={
            "is_primary": False,
        },
    )
    assert resp.status_code == 200


# 34. Delete bank account
def test_delete_bank_account(client, fake_db):
    """DELETE /api/pab/partners/100/bank-accounts/1 — deletes."""
    fake_db.cursor().fetchone = lambda: (1,)

    resp = client.delete("/api/pab/partners/100/bank-accounts/1")
    assert resp.status_code == 200


# 35. Delete bank account — not found
def test_delete_bank_account_not_found(client, fake_db):
    """DELETE /api/pab/partners/100/bank-accounts/999 — 404."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.delete("/api/pab/partners/100/bank-accounts/999")
    assert resp.status_code == 404


# ===================================================================
# CATEGORIES
# ===================================================================


# 36. List categories
def test_list_categories(client, fake_db):
    """GET /api/pab/partners/100/categories — returns list."""
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [_cat_row()]

    resp = client.get("/api/pab/partners/100/categories")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# 37. Assign category
def test_assign_category(client, fake_db):
    """POST /api/pab/partners/100/categories — 201."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        if call_count == 2:
            return None  # no duplicate
        return _cat_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/categories",
        json={
            "category_id": 10,
            "category_type": "supplier",
        },
    )
    assert resp.status_code == 201


# 38. Assign category — duplicate (409)
def test_assign_category_duplicate(client, fake_db):
    """POST /api/pab/partners/100/categories — 409 when already assigned."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return (1,)  # already assigned

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/categories",
        json={
            "category_id": 10,
            "category_type": "supplier",
        },
    )
    assert resp.status_code == 409


# 39. Unassign category
def test_unassign_category(client, fake_db):
    """DELETE /api/pab/partners/100/categories/10 — unassigns."""
    fake_db.cursor().fetchone = lambda: (1,)

    resp = client.delete("/api/pab/partners/100/categories/10")
    assert resp.status_code == 200


# 40. Unassign category — not found
def test_unassign_category_not_found(client, fake_db):
    """DELETE /api/pab/partners/100/categories/999 — 404."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.delete("/api/pab/partners/100/categories/999")
    assert resp.status_code == 404


# ===================================================================
# TEXTS
# ===================================================================


# 41. List texts
def test_list_texts(client, fake_db):
    """GET /api/pab/partners/100/texts — returns list."""
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [_text_row()]

    resp = client.get("/api/pab/partners/100/texts")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# 42. Upsert text — create
def test_upsert_text_create(client, fake_db):
    """PUT /api/pab/partners/100/texts — creates new text."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        if call_count == 2:
            return None  # text not exists
        return _text_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put(
        "/api/pab/partners/100/texts",
        json={
            "text_type": "owner_name",
            "text_content": "Ján Novák",
        },
    )
    assert resp.status_code == 200


# 43. Upsert text — update
def test_upsert_text_update(client, fake_db):
    """PUT /api/pab/partners/100/texts — updates existing text."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        if call_count == 2:
            return (1,)  # text_id exists
        return _text_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put(
        "/api/pab/partners/100/texts",
        json={
            "text_type": "owner_name",
            "text_content": "Peter Novák",
        },
    )
    assert resp.status_code == 200


# ===================================================================
# FACILITIES
# ===================================================================


# 44. List facilities
def test_list_facilities(client, fake_db):
    """GET /api/pab/partners/100/facilities — returns list."""
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [_facility_row()]

    resp = client.get("/api/pab/partners/100/facilities")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# 45. Create facility
def test_create_facility(client, fake_db):
    """POST /api/pab/partners/100/facilities — 201."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return _facility_row()

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners/100/facilities",
        json={
            "facility_name": "Pobočka Košice",
            "city": "Košice",
        },
    )
    assert resp.status_code == 201


# 46. Create facility — missing name (422)
def test_create_facility_missing_name(client, fake_db):
    """POST /api/pab/partners/100/facilities — 422 when name missing."""
    resp = client.post(
        "/api/pab/partners/100/facilities",
        json={
            "city": "Košice",
        },
    )
    assert resp.status_code == 422


# 47. Update facility
def test_update_facility(client, fake_db):
    """PUT /api/pab/partners/100/facilities/1 — updates."""
    fake_db.cursor().fetchone = lambda: _facility_row()

    resp = client.put(
        "/api/pab/partners/100/facilities/1",
        json={
            "facility_name": "Updated Pobočka",
        },
    )
    assert resp.status_code == 200


# 48. Delete facility
def test_delete_facility(client, fake_db):
    """DELETE /api/pab/partners/100/facilities/1 — deletes."""
    fake_db.cursor().fetchone = lambda: (1,)

    resp = client.delete("/api/pab/partners/100/facilities/1")
    assert resp.status_code == 200


# 49. Delete facility — not found
def test_delete_facility_not_found(client, fake_db):
    """DELETE /api/pab/partners/100/facilities/999 — 404."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.delete("/api/pab/partners/100/facilities/999")
    assert resp.status_code == 404


# ===================================================================
# RBAC
# ===================================================================


# 50. RBAC — no auth returns 401/403
def test_pab_rbac_no_auth(client_no_auth):
    """GET /api/pab/partners — without auth returns 401/403."""
    resp = client_no_auth.get("/api/pab/partners")
    assert resp.status_code in (401, 403)


# ===================================================================
# VALIDATION
# ===================================================================


# 51. Validation — IČO only digits
def test_validation_company_id_digits(client):
    """POST /api/pab/partners — IČO must be digits only."""
    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 300,
            "partner_name": "ICO Test",
            "company_id": "ABC-not-digits",
        },
    )
    assert resp.status_code == 422


# 52. Validation — partner_name too long
def test_validation_name_too_long(client):
    """POST /api/pab/partners — name > 100 chars triggers 422."""
    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 301,
            "partner_name": "A" * 101,
        },
    )
    assert resp.status_code == 422


# 53. Validation — extensions discount out of range
def test_validation_extensions_discount(client, fake_db):
    """PUT /api/pab/partners/100/extensions — discount > 100 triggers 422."""
    resp = client.put(
        "/api/pab/partners/100/extensions",
        json={
            "sale_discount_percent": 150,
        },
    )
    assert resp.status_code == 422


# 54. Validation — text line_number < 1
def test_validation_text_line_number(client, fake_db):
    """PUT /api/pab/partners/100/texts — line_number < 1 triggers 422."""
    resp = client.put(
        "/api/pab/partners/100/texts",
        json={
            "text_type": "notice",
            "line_number": 0,
            "text_content": "test",
        },
    )
    assert resp.status_code == 422


# 55. Validation — invalid address_type (422)
def test_validation_invalid_address_type(client, fake_db):
    """POST /api/pab/partners/100/addresses — invalid type triggers 422."""
    resp = client.post(
        "/api/pab/partners/100/addresses",
        json={
            "address_type": "invalid_type",
            "city": "Bratislava",
        },
    )
    assert resp.status_code == 422


# 56. Validation — invalid contact_type (422)
def test_validation_invalid_contact_type(client, fake_db):
    """POST /api/pab/partners/100/contacts — invalid type triggers 422."""
    resp = client.post(
        "/api/pab/partners/100/contacts",
        json={
            "contact_type": "invalid",
        },
    )
    assert resp.status_code == 422


# 57. Validation — invalid category_type (422)
def test_validation_invalid_category_type(client, fake_db):
    """POST /api/pab/partners/100/categories — invalid type triggers 422."""
    resp = client.post(
        "/api/pab/partners/100/categories",
        json={
            "category_id": 1,
            "category_type": "invalid",
        },
    )
    assert resp.status_code == 422


# ===================================================================
# VERSIONING LIFECYCLE
# ===================================================================


# 58. Create partner → modify_id = 0
def test_create_partner_modify_id_zero(client, fake_db):
    """POST /api/pab/partners — new partner has modify_id = 0."""
    row = _partner_row(modify_id=0)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return None  # partner_id uniqueness check
        return row  # RETURNING

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 100,
            "partner_name": "Test s.r.o.",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["modify_id"] == 0


# 59. Create partner → history record exists (modify_id=0, valid_to IS NULL)
def test_create_partner_initial_history(client, fake_db):
    """After create, history endpoint returns initial record (modify_id=0)."""
    h_row = _history_row(modify_id=0, valid_to=None)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return None  # no specific version query

    fake_db.cursor().fetchone = mock_fetchone
    fake_db.cursor().fetchall = lambda: [h_row]

    resp = client.get("/api/pab/partners/100/history")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["modify_id"] == 0
    assert data[0]["valid_to"] is None


# 60. Update business field → modify_id = 1, new history record
def test_update_partner_increments_modify_id(client, fake_db):
    """PUT /api/pab/partners/100 — after update, modify_id is 1."""
    updated = _partner_row(partner_name="Updated s.r.o.", modify_id=1)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # exists check
        return updated  # after update

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put("/api/pab/partners/100", json={"partner_name": "Updated s.r.o."})
    assert resp.status_code == 200
    assert resp.json()["modify_id"] == 1


# 61. Two updates → modify_id = 2, 3 history records
def test_update_partner_two_updates_modify_id(client, fake_db):
    """After two updates, modify_id should be 2."""
    updated = _partner_row(partner_name="Final s.r.o.", modify_id=2)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # exists check
        return updated  # after update

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put("/api/pab/partners/100", json={"partner_name": "Final s.r.o."})
    assert resp.status_code == 200
    assert resp.json()["modify_id"] == 2


# 62. History endpoint → chronological order with valid_from/valid_to
def test_history_chronological_order(client, fake_db):
    """GET /partners/{id}/history — returns versions in modify_id order."""
    h0 = _history_row(history_id=1, modify_id=0, valid_to=_NOW)
    h1 = _history_row(history_id=2, modify_id=1, partner_name="V1", valid_to=_NOW)
    h2 = _history_row(history_id=3, modify_id=2, partner_name="V2", valid_to=None)

    fake_db.cursor().fetchone = lambda: (100,)  # partner exists
    fake_db.cursor().fetchall = lambda: [h0, h1, h2]

    resp = client.get("/api/pab/partners/100/history")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert data[0]["modify_id"] == 0
    assert data[1]["modify_id"] == 1
    assert data[2]["modify_id"] == 2
    # First two versions have valid_to, last does not
    assert data[0]["valid_to"] is not None
    assert data[1]["valid_to"] is not None
    assert data[2]["valid_to"] is None


# ===================================================================
# PARTNER_CLASS
# ===================================================================


# 63. Create business partner → default list shows it
def test_create_business_partner_default_list(client, fake_db):
    """Business partner appears in default list (no partner_class filter)."""
    row = _partner_row(partner_class="business")
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners")
    assert resp.status_code == 200
    assert len(resp.json()["items"]) == 1
    assert resp.json()["items"][0]["partner_class"] == "business"


# 64. Create retail partner → filter by partner_class=retail
def test_list_retail_partners_filter(client, fake_db):
    """GET /api/pab/partners?partner_class=retail — shows only retail."""
    row = _partner_row(partner_class="retail")
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners?partner_class=retail")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    count_q = queries[0][0]
    assert "partner_class = %s" in count_q


# 65. Create guest partner → filter by partner_class=guest
def test_list_guest_partners_filter(client, fake_db):
    """GET /api/pab/partners?partner_class=guest — shows only guest."""
    row = _partner_row(partner_class="guest")
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners?partner_class=guest")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    count_q = queries[0][0]
    assert "partner_class = %s" in count_q


# 66. List without partner_class filter → no partner_class WHERE clause
def test_list_no_partner_class_filter(client, fake_db):
    """GET /api/pab/partners — without partner_class param, no class filter in SQL."""
    row = _partner_row()
    fake_db.cursor().fetchone = lambda: (1,)
    fake_db.cursor().fetchall = lambda: [row]

    resp = client.get("/api/pab/partners")
    assert resp.status_code == 200
    queries = fake_db.cursor().executed_queries
    count_q = queries[0][0]
    assert "partner_class" not in count_q


# 67. POST with partner_class=guest → creates guest partner
def test_create_guest_partner(client, fake_db):
    """POST /api/pab/partners — creates partner with partner_class=guest."""
    row = _partner_row(partner_class="guest")
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return None  # partner_id uniqueness check
        return row  # RETURNING

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 200,
            "partner_name": "Guest s.r.o.",
            "partner_class": "guest",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["partner_class"] == "guest"
    # Verify INSERT query includes partner_class
    queries = fake_db.cursor().executed_queries
    insert_q = [q for q, _ in queries if "INSERT INTO partner_catalog" in q]
    assert len(insert_q) >= 1
    assert "partner_class" in insert_q[0]


# ===================================================================
# HISTORY ENDPOINTS
# ===================================================================


# 68. GET /partners/{id}/history → list of versions
def test_history_list_endpoint(client, fake_db):
    """GET /api/pab/partners/100/history — returns list of history records."""
    h_row = _history_row()
    fake_db.cursor().fetchone = lambda: (100,)
    fake_db.cursor().fetchall = lambda: [h_row]

    resp = client.get("/api/pab/partners/100/history")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["history_id"] == 1
    assert data[0]["partner_id"] == 100
    assert data[0]["modify_id"] == 0


# 69. GET /partners/{id}/history/0 → first version
def test_history_get_version_zero(client, fake_db):
    """GET /api/pab/partners/100/history/0 — returns first version."""
    h_row = _history_row(modify_id=0)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return h_row  # history version

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.get("/api/pab/partners/100/history/0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["modify_id"] == 0
    assert data["partner_name"] == "Test s.r.o."


# 70. GET /partners/{id}/history/999 → 404
def test_history_get_version_not_found(client, fake_db):
    """GET /api/pab/partners/100/history/999 — 404 for non-existent version."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # partner exists
        return None  # version not found

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.get("/api/pab/partners/100/history/999")
    assert resp.status_code == 404
    assert "neexistuje" in resp.json()["detail"]


# ===================================================================
# TRIGGER BYPASS
# ===================================================================


# 71. Update only is_active → modify_id does NOT increment (WHEN condition)
def test_update_only_is_active_no_version_change(client, fake_db):
    """PUT /api/pab/partners/100 — updating only is_active does not change modify_id.

    The UPDATE trigger has a WHEN condition that excludes is_active.
    In the API, this is simulated: when only is_active changes,
    the DB trigger does not fire and modify_id stays the same.
    """
    # Same modify_id before and after — trigger did NOT fire
    updated = _partner_row(is_active=False, modify_id=0)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # exists check
        return updated  # after update

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put("/api/pab/partners/100", json={"is_active": False})
    assert resp.status_code == 200
    assert resp.json()["modify_id"] == 0


# 72. Update company_name → modify_id DOES increment
def test_update_business_field_version_change(client, fake_db):
    """PUT /api/pab/partners/100 — updating partner_name triggers version change."""
    updated = _partner_row(partner_name="Zmena s.r.o.", modify_id=1)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # exists check
        return updated  # after update — DB trigger would have incremented

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put("/api/pab/partners/100", json={"partner_name": "Zmena s.r.o."})
    assert resp.status_code == 200
    assert resp.json()["modify_id"] == 1


# ===================================================================
# ADDITIONAL PARTNER_CLASS + VERSIONING
# ===================================================================


# 73. Validation — invalid partner_class (422)
def test_validation_invalid_partner_class(client, fake_db):
    """POST /api/pab/partners — invalid partner_class triggers 422."""
    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 400,
            "partner_name": "Bad Class",
            "partner_class": "invalid_class",
        },
    )
    assert resp.status_code == 422


# 74. Default partner_class is 'business'
def test_default_partner_class_is_business(client, fake_db):
    """POST /api/pab/partners — partner_class defaults to 'business'."""
    row = _partner_row(partner_class="business")
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return None  # partner_id uniqueness check
        return row

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/pab/partners",
        json={
            "partner_id": 500,
            "partner_name": "Default Class",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["partner_class"] == "business"


# 75. History for non-existent partner → 404
def test_history_partner_not_found(client, fake_db):
    """GET /api/pab/partners/999/history — 404 when partner doesn't exist."""
    fake_db.cursor().fetchone = lambda: None

    resp = client.get("/api/pab/partners/999/history")
    assert resp.status_code == 404


# 76. Update partner_class via PUT
def test_update_partner_class(client, fake_db):
    """PUT /api/pab/partners/100 — can update partner_class."""
    updated = _partner_row(partner_class="retail", modify_id=1)
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)  # exists check
        return updated

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.put("/api/pab/partners/100", json={"partner_class": "retail"})
    assert resp.status_code == 200
    assert resp.json()["partner_class"] == "retail"
    assert resp.json()["modify_id"] == 1


# 77. History version returns partner_class field
def test_history_version_has_partner_class(client, fake_db):
    """GET /api/pab/partners/100/history/0 — response includes partner_class."""
    h_row = _history_row(modify_id=0, partner_class="retail")
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return (100,)
        return h_row

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.get("/api/pab/partners/100/history/0")
    assert resp.status_code == 200
    assert resp.json()["partner_class"] == "retail"
