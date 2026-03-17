"""Integration testy pre payment endpointy — 10 testov.

Tests:
  CALLBACK (6):
    1. test_payment_callback_paid — PAID → order status='paid', payment_status='paid'
    2. test_payment_callback_cancelled — CANCELLED → payment_status='failed'
    3. test_payment_callback_invalid_secret — zlý secret → stav sa nezmení
    4. test_payment_callback_invalid_merchant — zlý merchant → stav sa nezmení
    5. test_payment_callback_idempotent — 2× PAID → spracované len raz
    6. test_payment_callback_price_mismatch — iná cena → stav sa nezmení

  RETURN (2):
    7. test_payment_return_paid — GET s platným trans → 200
    8. test_payment_return_not_found — GET s neexistujúcim trans → 404

  ORDER CREATION (2):
    9. test_create_order_with_comgate — s Comgate creds → payment_url v response
    10. test_create_order_without_comgate — bez Comgate creds → payment_url=null
"""

import os
import sys

# Set JWT_SECRET_KEY before any app imports
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-payment-tests")

from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# Tenant dict — with comgate credentials
# ---------------------------------------------------------------------------

_TENANT_WITH_COMGATE = {
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
    "comgate_merchant_id": "12345",
    "comgate_secret": "test_secret",
    "comgate_test_mode": True,
}

_TENANT_NO_COMGATE = {
    "tenant_id": 2,
    "company_name": "No Comgate s.r.o.",
    "domain": "nocomgate.sk",
    "brand_name": "NOCOM",
    "logo_url": None,
    "primary_color": "#000000",
    "currency": "EUR",
    "vat_rate_default": 20.00,
    "default_lang": "sk",
    "is_active": True,
    "smtp_from": "noreply@nocomgate.sk",
    "admin_email": "admin@nocomgate.sk",
    "comgate_merchant_id": None,
    "comgate_secret": None,
    "comgate_test_mode": None,
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def payment_client(fake_db):
    """Test client with mocked DB — NO tenant override (callback has no auth)."""
    from fastapi.testclient import TestClient
    from database import get_db
    from main import app

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def eshop_client_comgate(fake_db):
    """Test client with mocked DB + tenant with Comgate credentials."""
    from fastapi.testclient import TestClient
    from database import get_db
    from eshop.dependencies import get_tenant_by_token
    from main import app

    def override_get_db():
        yield fake_db

    async def override_tenant():
        return _TENANT_WITH_COMGATE

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tenant_by_token] = override_tenant

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def eshop_client_no_comgate(fake_db):
    """Test client with mocked DB + tenant WITHOUT Comgate credentials."""
    from fastapi.testclient import TestClient
    from database import get_db
    from eshop.dependencies import get_tenant_by_token
    from main import app

    def override_get_db():
        yield fake_db

    async def override_tenant():
        return _TENANT_NO_COMGATE

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tenant_by_token] = override_tenant

    yield TestClient(app)

    app.dependency_overrides.clear()


# ===========================================================================
# CALLBACK TESTS (6)
# ===========================================================================


def test_payment_callback_paid(payment_client, fake_db):
    """#1: callback PAID → order status='paid', payment_status='paid'."""
    # Setup: order exists, tenant with comgate, status is 'new'
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order by refId (order_number)
            (
                1,  # order_id
                1,  # tenant_id
                Decimal("12.00"),  # total_amount_vat
                "EUR",  # currency
                "pending",  # payment_status
                "new",  # status
            ),
            # 2. Load tenant to verify secrets
            (
                1,  # tenant_id
                "12345",  # comgate_merchant_id
                "test_secret",  # comgate_secret
            ),
            # 3. Fetch tenant for email
            (
                "noreply@test.sk",  # smtp_from
                "admin@test.sk",  # admin_email
                "TEST",  # brand_name
                "test.sk",  # domain
                "#2E7D32",  # primary_color
                "EUR",  # currency
            ),
            # 4. Fetch order for email
            (
                "ORD-001",  # order_number
                "test@test.sk",  # customer_email
                "Test Customer",  # customer_name
                Decimal("12.00"),  # total_amount_vat
                "EUR",  # currency
                "credit_card",  # payment_method
            ),
        ]
    )
    fake_db.set_fetchall_sequence(
        [
            # items for email
            [("Test Product", 1, Decimal("12.00"))],
        ]
    )

    resp = payment_client.post(
        "/api/eshop/payment/callback",
        data={
            "merchant": "12345",
            "test": "true",
            "price": "1200",
            "curr": "EUR",
            "label": "ORD-001",
            "refId": "ORD-001",
            "transId": "TRANS-001",
            "secret": "test_secret",
            "status": "PAID",
            "email": "test@test.sk",
        },
    )
    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # Verify UPDATE queries were executed
    queries = [q[0] for q in fake_db._cursor.executed_queries]
    assert any("payment_status = 'paid'" in q for q in queries)
    assert any("status = 'paid'" in q for q in queries)


def test_payment_callback_cancelled(payment_client, fake_db):
    """#2: callback CANCELLED → payment_status='failed'."""
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order
            (1, 1, Decimal("12.00"), "EUR", "pending", "new"),
            # 2. Load tenant
            (1, "12345", "test_secret"),
            # 3. Tenant for email
            (
                "noreply@test.sk",
                "admin@test.sk",
                "TEST",
                "test.sk",
                "#2E7D32",
                "EUR",
            ),
            # 4. Order for email
            (
                "ORD-002",
                "test@test.sk",
                "Test Customer",
                Decimal("12.00"),
                "EUR",
                "credit_card",
                "TRANS-002",
            ),
        ]
    )

    resp = payment_client.post(
        "/api/eshop/payment/callback",
        data={
            "merchant": "12345",
            "test": "true",
            "price": "1200",
            "curr": "EUR",
            "label": "ORD-002",
            "refId": "ORD-002",
            "transId": "TRANS-002",
            "secret": "test_secret",
            "status": "CANCELLED",
            "email": "test@test.sk",
        },
    )
    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # Verify payment_status='failed' UPDATE was called
    queries = [q[0] for q in fake_db._cursor.executed_queries]
    assert any("payment_status = 'failed'" in q for q in queries)


def test_payment_callback_invalid_secret(payment_client, fake_db):
    """#3: callback so zlým secretom → stav sa nezmení."""
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order
            (1, 1, Decimal("12.00"), "EUR", "pending", "new"),
            # 2. Load tenant (correct secret is 'test_secret')
            (1, "12345", "test_secret"),
        ]
    )

    resp = payment_client.post(
        "/api/eshop/payment/callback",
        data={
            "merchant": "12345",
            "test": "true",
            "price": "1200",
            "curr": "EUR",
            "label": "ORD-003",
            "refId": "ORD-003",
            "transId": "TRANS-003",
            "secret": "wrong_secret",
            "status": "PAID",
            "email": "test@test.sk",
        },
    )
    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # Verify NO status UPDATE was executed (only SELECT queries)
    queries = [q[0] for q in fake_db._cursor.executed_queries]
    assert not any("UPDATE" in q for q in queries)


def test_payment_callback_invalid_merchant(payment_client, fake_db):
    """#4: callback so zlým merchant ID → stav sa nezmení."""
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order
            (1, 1, Decimal("12.00"), "EUR", "pending", "new"),
            # 2. Load tenant
            (1, "12345", "test_secret"),
        ]
    )

    resp = payment_client.post(
        "/api/eshop/payment/callback",
        data={
            "merchant": "99999",  # wrong merchant
            "test": "true",
            "price": "1200",
            "curr": "EUR",
            "label": "ORD-004",
            "refId": "ORD-004",
            "transId": "TRANS-004",
            "secret": "test_secret",
            "status": "PAID",
            "email": "test@test.sk",
        },
    )
    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # Verify NO status UPDATE was executed
    queries = [q[0] for q in fake_db._cursor.executed_queries]
    assert not any("UPDATE" in q for q in queries)


def test_payment_callback_idempotent(payment_client, fake_db):
    """#5: 2× PAID callback → spracované len raz (idempotency)."""
    # First callback: order already has payment_status='paid'
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order (already paid)
            (1, 1, Decimal("12.00"), "EUR", "paid", "paid"),
            # 2. Load tenant
            (1, "12345", "test_secret"),
        ]
    )

    resp = payment_client.post(
        "/api/eshop/payment/callback",
        data={
            "merchant": "12345",
            "test": "true",
            "price": "1200",
            "curr": "EUR",
            "label": "ORD-005",
            "refId": "ORD-005",
            "transId": "TRANS-005",
            "secret": "test_secret",
            "status": "PAID",
            "email": "test@test.sk",
        },
    )
    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # Verify NO UPDATE was executed (idempotent — already paid)
    queries = [q[0] for q in fake_db._cursor.executed_queries]
    assert not any("UPDATE" in q for q in queries)


def test_payment_callback_price_mismatch(payment_client, fake_db):
    """#6: callback s inou cenou → stav sa nezmení."""
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order — total_amount_vat = 12.00 → expected price_cents = 1200
            (1, 1, Decimal("12.00"), "EUR", "pending", "new"),
            # 2. Load tenant
            (1, "12345", "test_secret"),
        ]
    )

    resp = payment_client.post(
        "/api/eshop/payment/callback",
        data={
            "merchant": "12345",
            "test": "true",
            "price": "9999",  # wrong price (expected 1200)
            "curr": "EUR",
            "label": "ORD-006",
            "refId": "ORD-006",
            "transId": "TRANS-006",
            "secret": "test_secret",
            "status": "PAID",
            "email": "test@test.sk",
        },
    )
    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # Verify NO status UPDATE was executed
    queries = [q[0] for q in fake_db._cursor.executed_queries]
    assert not any("UPDATE" in q for q in queries)


# ===========================================================================
# RETURN TESTS (2)
# ===========================================================================


def test_payment_return_paid(payment_client, fake_db):
    """#7: GET payment/return s paid trans → 200."""
    fake_db.set_fetchone_sequence(
        [
            # payment_return: SELECT order_number, status, payment_status
            ("ORD-007", "paid", "paid"),
        ]
    )

    resp = payment_client.get("/api/eshop/payment/return?id=TRANS-007")
    assert resp.status_code == 200

    data = resp.json()
    assert data["order_number"] == "ORD-007"
    assert data["status"] == "paid"
    assert data["payment_status"] == "paid"


def test_payment_return_not_found(payment_client, fake_db):
    """#8: GET payment/return s neexistujúcim trans → 404."""
    fake_db.set_fetchone_sequence(
        [
            None,  # no order found
        ]
    )

    resp = payment_client.get("/api/eshop/payment/return?id=NEEXISTUJE")
    assert resp.status_code == 404


# ===========================================================================
# ORDER CREATION TESTS (2)
# ===========================================================================


@patch("eshop.comgate.ComgateClient.create_payment", new_callable=AsyncMock)
@patch(
    "eshop.email_service.EshopEmailService.send_order_confirmation",
    new_callable=AsyncMock,
)
@patch(
    "eshop.email_service.EshopEmailService.send_admin_new_order", new_callable=AsyncMock
)
def test_create_order_with_comgate(
    mock_admin_email,
    mock_order_email,
    mock_create_payment,
    eshop_client_comgate,
    fake_db,
):
    """#9: POST order s Comgate credentials → payment_url v response."""
    # Setup mock Comgate response
    mock_create_payment.return_value = {
        "transId": "COMGATE-TRANS-001",
        "redirect_url": "https://payments.comgate.cz/client/instructions/index?id=COMGATE-TRANS-001",
    }
    mock_order_email.return_value = None
    mock_admin_email.return_value = None

    # DB sequence for create_order:
    fake_db.set_fetchone_sequence(
        [
            # 1. Product lookup (sku check)
            (
                1,  # product_id
                "SKU-001",  # sku
                "Test Product",  # name
                Decimal("10.00"),  # price
                Decimal("12.00"),  # price_vat
                Decimal("20.00"),  # vat_rate
                True,  # is_active
            ),
            # 2. generate_order_number: advisory lock (returns None-ish)
            None,
            # 3. generate_order_number: SELECT MAX
            (None,),
            # 4. INSERT order RETURNING order_id
            (1,),
            # 5. No discount code lookup (discount_code is None)
            # 6. UPDATE comgate_transaction_id RETURNING
        ]
    )

    resp = eshop_client_comgate.post(
        "/api/eshop/orders",
        json={
            "customer_email": "test@test.sk",
            "customer_name": "Test Customer",
            "billing_name": "Test Customer",
            "billing_street": "Hlavná 1",
            "billing_city": "Bratislava",
            "billing_zip": "81101",
            "billing_country": "SK",
            "items": [{"sku": "SKU-001", "quantity": 1}],
            "payment_method": "credit_card",
        },
        headers={"X-Eshop-Token": "test-token"},
    )
    assert resp.status_code == 200

    data = resp.json()
    assert data["payment_url"] is not None
    assert "comgate.cz" in data["payment_url"]

    # Verify Comgate create_payment was called
    mock_create_payment.assert_called_once()


@patch(
    "eshop.email_service.EshopEmailService.send_order_confirmation",
    new_callable=AsyncMock,
)
@patch(
    "eshop.email_service.EshopEmailService.send_admin_new_order", new_callable=AsyncMock
)
def test_create_order_without_comgate(
    mock_admin_email,
    mock_order_email,
    eshop_client_no_comgate,
    fake_db,
):
    """#10: POST order bez Comgate credentials → payment_url=null."""
    mock_order_email.return_value = None
    mock_admin_email.return_value = None

    # DB sequence for create_order:
    fake_db.set_fetchone_sequence(
        [
            # 1. Product lookup
            (
                1,
                "SKU-001",
                "Test Product",
                Decimal("10.00"),
                Decimal("12.00"),
                Decimal("20.00"),
                True,
            ),
            # 2. generate_order_number: advisory lock
            None,
            # 3. generate_order_number: SELECT MAX
            (None,),
            # 4. INSERT order RETURNING order_id
            (1,),
        ]
    )

    resp = eshop_client_no_comgate.post(
        "/api/eshop/orders",
        json={
            "customer_email": "test@test.sk",
            "customer_name": "Test Customer",
            "billing_name": "Test Customer",
            "billing_street": "Hlavná 1",
            "billing_city": "Bratislava",
            "billing_zip": "81101",
            "billing_country": "SK",
            "items": [{"sku": "SKU-001", "quantity": 1}],
            "payment_method": "bank_transfer",
        },
        headers={"X-Eshop-Token": "test-token"},
    )
    assert resp.status_code == 200

    data = resp.json()
    assert data["payment_url"] is None
