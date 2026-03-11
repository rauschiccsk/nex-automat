"""Unit tests for E-shop Customer endpoints — register, login, profile, orders, company orders.

6 test cases covering:
1. Customer registration — success (201)
2. Customer registration — duplicate email (409)
3. Customer login — correct password → 200 + token
4. Customer login — wrong password → 401
5. Customer profile — valid token → 200
6. Customer orders — valid token → 200 + list
7. Order with company data — is_company_order=True
8. Order with account creation — create_account=True
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TENANT_ROW = (
    1,            # tenant_id
    "Test s.r.o.", # company_name
    "test.sk",    # domain
    "TEST",       # brand_name
    None,         # logo_url
    "#2E7D32",    # primary_color
    "EUR",        # currency
    20.00,        # vat_rate_default
    "sk",         # default_lang
    True,         # is_active
    "noreply@test.sk",  # smtp_from
    "admin@test.sk",    # admin_email
)


def _make_customer_row(
    customer_id=1,
    email="customer@test.sk",
    password_hash="$2b$12$hashedpassword",
    first_name="Ján",
    last_name="Testovač",
):
    """Build a fake eshop_customers DB row."""
    return (
        customer_id,     # id
        1,               # tenant_id
        email,           # email
        password_hash,   # password_hash
        first_name,      # first_name
        last_name,       # last_name
        "+421901234567", # phone
        "Hlavná 1",     # street
        "Bratislava",   # city
        "81101",        # postal_code
        "SK",           # country
        False,          # is_company
        None,           # company_name
        None,           # company_ico
        None,           # company_dic
        None,           # company_ic_dph
    )


def _make_customer_profile_row(customer_id=1, email="customer@test.sk"):
    """Build a row matching _get_customer_from_token SELECT."""
    return (
        customer_id,     # id
        1,               # tenant_id
        email,           # email
        "Ján",          # first_name
        "Testovač",     # last_name
        "+421901234567", # phone
        "Hlavná 1",     # street
        "Bratislava",   # city
        "81101",        # postal_code
        "SK",           # country
        False,          # is_company
        None,           # company_name
        None,           # company_ico
        None,           # company_dic
        None,           # company_ic_dph
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def eshop_client(fake_db):
    """Test client with mocked DB, X-Eshop-Token resolved to test tenant."""
    from fastapi.testclient import TestClient
    from database import get_db
    from eshop.dependencies import get_tenant_by_token
    from auth.dependencies import get_current_user, require_permission
    from main import app

    def override_get_db():
        yield fake_db

    async def override_tenant():
        return {
            "tenant_id": 1,
            "company_name": "Test s.r.o.",
            "domain": "test.sk",
            "brand_name": "TEST",
            "logo_url": None,
            "primary_color": "#2E7D32",
            "currency": "EUR",
            "vat_rate_default": 20.00,
            "default_lang": "sk",
            "is_active": True,
            "smtp_from": "noreply@test.sk",
            "admin_email": "admin@test.sk",
        }

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tenant_by_token] = override_tenant

    yield TestClient(app)

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# 1. Customer registration — success (201)
# ---------------------------------------------------------------------------
def test_customer_register(eshop_client, fake_db):
    """POST /api/eshop/customers/register — 201 with valid data."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # Uniqueness check → not found
            return None
        # INSERT RETURNING id
        return (42,)

    fake_db.cursor().fetchone = mock_fetchone

    resp = eshop_client.post(
        "/api/eshop/customers/register",
        json={
            "email": "new@test.sk",
            "password": "SecurePass123!",
            "first_name": "Nový",
            "last_name": "Zákazník",
        },
        headers={"X-Eshop-Token": "test-token"},
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["customer_id"] == 42
    assert data["email"] == "new@test.sk"


# ---------------------------------------------------------------------------
# 2. Customer registration — duplicate email (409)
# ---------------------------------------------------------------------------
def test_customer_register_duplicate(eshop_client, fake_db):
    """POST /api/eshop/customers/register — 409 when email already registered."""
    # Uniqueness check returns existing customer
    fake_db.cursor().fetchone = lambda: (1,)

    resp = eshop_client.post(
        "/api/eshop/customers/register",
        json={
            "email": "existing@test.sk",
            "password": "SecurePass123!",
            "first_name": "Existujúci",
            "last_name": "Zákazník",
        },
        headers={"X-Eshop-Token": "test-token"},
    )

    assert resp.status_code == 409
    assert "zaregistrovaný" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 3. Customer login — correct password → 200 + token
# ---------------------------------------------------------------------------
def test_customer_login(eshop_client, fake_db):
    """POST /api/eshop/customers/login — 200 with correct credentials."""
    import bcrypt

    pw_hash = bcrypt.hashpw(b"CorrectPassword1!", bcrypt.gensalt()).decode()

    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # SELECT customer
            return (1, "customer@test.sk", pw_hash, "Ján", "Testovač")
        return None

    fake_db.cursor().fetchone = mock_fetchone

    resp = eshop_client.post(
        "/api/eshop/customers/login",
        json={
            "email": "customer@test.sk",
            "password": "CorrectPassword1!",
        },
        headers={"X-Eshop-Token": "test-token"},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["customer_id"] == 1
    assert data["email"] == "customer@test.sk"


# ---------------------------------------------------------------------------
# 4. Customer login — wrong password → 401
# ---------------------------------------------------------------------------
def test_customer_login_wrong_password(eshop_client, fake_db):
    """POST /api/eshop/customers/login — 401 with wrong password."""
    import bcrypt

    pw_hash = bcrypt.hashpw(b"CorrectPassword1!", bcrypt.gensalt()).decode()

    fake_db.cursor().fetchone = lambda: (
        1, "customer@test.sk", pw_hash, "Ján", "Testovač"
    )

    resp = eshop_client.post(
        "/api/eshop/customers/login",
        json={
            "email": "customer@test.sk",
            "password": "WrongPassword!!",
        },
        headers={"X-Eshop-Token": "test-token"},
    )

    assert resp.status_code == 401
    assert "Nesprávny" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 5. Customer profile — valid token → 200
# ---------------------------------------------------------------------------
def test_customer_profile(eshop_client, fake_db):
    """GET /api/eshop/customers/profile — 200 with valid Bearer token."""
    from jose import jwt
    from auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

    token = jwt.encode(
        {
            "customer_id": 1,
            "tenant_id": 1,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    fake_db.cursor().fetchone = lambda: _make_customer_profile_row()

    resp = eshop_client.get(
        "/api/eshop/customers/profile",
        headers={
            "X-Eshop-Token": "test-token",
            "Authorization": f"Bearer {token}",
        },
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["email"] == "customer@test.sk"
    assert data["first_name"] == "Ján"


# ---------------------------------------------------------------------------
# 6. Customer orders — valid token → 200 + list
# ---------------------------------------------------------------------------
def test_customer_orders(eshop_client, fake_db):
    """GET /api/eshop/customers/orders — 200 with order list."""
    from jose import jwt
    from auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

    token = jwt.encode(
        {
            "customer_id": 1,
            "tenant_id": 1,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        # _get_customer_from_token SELECT
        return _make_customer_profile_row()

    now = datetime.now()

    fake_db.cursor().fetchone = mock_fetchone
    fake_db.cursor().fetchall = lambda: [
        (1, "TEST-2026-001", "new", "pending", 49.90, "EUR", now),
    ]

    resp = eshop_client.get(
        "/api/eshop/customers/orders",
        headers={
            "X-Eshop-Token": "test-token",
            "Authorization": f"Bearer {token}",
        },
    )

    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data
    assert len(data["orders"]) == 1
    assert data["orders"][0]["order_number"] == "TEST-2026-001"
