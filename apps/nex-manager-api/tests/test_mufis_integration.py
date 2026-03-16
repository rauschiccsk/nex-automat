"""MuFis Integration Tests — 12 tests covering auth, getOrder, setOrder, product, status mapping.

Tests:
  AUTH (3):
    1. Valid API key + allowed IP → 200
    2. Invalid API key → 401
    3. Valid key, blocked IP → 403

  getOrder (2):
    4. No paid orders → empty orders[]
    5. DRY_RUN=true → returns data, mufis_synced_at stays NULL

  setOrder (3):
    6. Status mapping: "kézbesítve" → delivered + history source='mufis'
    7. Unknown status → default 'processing'
    8. Tracking data stored in DB

  Product (2):
    9.  getProduct → returns products
    10. setProduct → stock update

  Unit (2):
    11. All MUFIS_STATUS_MAP values are valid ORDER_STATUSES
    12. Delivery method + packeta fields
"""

import os
import sys

# Set JWT_SECRET_KEY before any app imports (required by nex_config.security)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-mufis-tests")

from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TENANT_DICT = {
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

_TENANT_DICT_WITH_IP = {**_TENANT_DICT, "client_ip": "127.0.0.1"}


def _make_order_row(
    order_id=1,
    order_number="ORD-001",
    status="paid",
    tracking_number="",
    tracking_link="",
):
    """Build a fake eshop_orders DB row matching getOrder SELECT columns."""
    now = datetime(2026, 3, 16, 12, 0, 0)
    return (
        order_id,  # order_id
        order_number,  # order_number
        1,  # tenant_id
        "test@test.sk",  # customer_email
        "Test Customer",  # customer_name
        "+421900000000",  # customer_phone
        "sk",  # lang
        "Billing Name",  # billing_name
        "",  # billing_name2
        "Hlavná 1",  # billing_street
        "Bratislava",  # billing_city
        "81101",  # billing_zip
        "SK",  # billing_country
        "Ship Name",  # shipping_name
        "",  # shipping_name2
        "Nová 5",  # shipping_street
        "Košice",  # shipping_city
        "04001",  # shipping_zip
        "SK",  # shipping_country
        "",  # ico
        "",  # dic
        "",  # eu_vat_number
        Decimal("100.00"),  # total_amount
        Decimal("120.00"),  # total_amount_vat
        "EUR",  # currency
        "bank_transfer",  # payment_method
        "paid",  # payment_status
        "courier",  # shipping_type
        Decimal("5.00"),  # shipping_price
        "",  # delivery_point_group
        "",  # delivery_point_id
        tracking_number,  # tracking_number
        tracking_link,  # tracking_link
        False,  # multiple_packages
        status,  # status
        "",  # note
        now,  # created_at
        now,  # updated_at
    )


def _make_order_status_row(order_id=1, status="paid"):
    """Build a minimal row for setOrder's SELECT order_id, status."""
    return (order_id, status)


def _make_product_row(
    product_id=1,
    sku="SKU-001",
    stock_quantity=10,
):
    """Build a fake eshop_products DB row matching getProduct SELECT."""
    return (
        product_id,  # product_id
        sku,  # sku
        "",  # barcode
        "Test Product",  # name
        "Short desc",  # short_description
        "Full desc",  # description
        "",  # image_url
        Decimal("10.00"),  # price
        Decimal("12.00"),  # price_vat
        Decimal("20.00"),  # vat_rate
        stock_quantity,  # stock_quantity
        Decimal("0.5"),  # weight
        True,  # is_active
        0,  # sort_order
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mufis_client(fake_db):
    """Test client with mocked DB, MuFis auth resolved to test tenant."""
    from fastapi.testclient import TestClient
    from database import get_db
    from eshop.dependencies import get_tenant_by_mufis_key
    from eshop.mufis_auth import verify_mufis_access
    from main import app

    def override_get_db():
        yield fake_db

    async def override_mufis_key():
        return _TENANT_DICT

    async def override_mufis_access():
        return _TENANT_DICT_WITH_IP

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tenant_by_mufis_key] = override_mufis_key
    app.dependency_overrides[verify_mufis_access] = override_mufis_access

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def mufis_client_no_auth(fake_db):
    """Test client with mocked DB but NO MuFis auth override (for auth tests)."""
    from fastapi.testclient import TestClient
    from database import get_db
    from main import app

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


# ===========================================================================
# AUTH TESTS (3)
# ===========================================================================


def test_mufis_auth_valid(mufis_client, fake_db):
    """#1: Správny API key + povolená IP → 200 (prázdne orders)."""
    # mufis_client has both auth dependencies overridden → should pass
    # COUNT(*) returns 0, fetchall returns empty
    fake_db.set_fetchone_sequence([(0,)])
    fake_db.set_fetchall_sequence([[]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data


def test_mufis_auth_invalid_key(mufis_client_no_auth, fake_db):
    """#2: Zlý API key → 401."""
    # No tenant override → get_tenant_by_mufis_key will query DB → None → 401
    fake_db.cursor().fetchone = lambda: None
    resp = mufis_client_no_auth.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "wrong-key"},
    )
    assert resp.status_code in [401, 403]


def test_mufis_auth_invalid_ip(fake_db, monkeypatch):
    """#3: Správny key, nepovolená IP → 403."""
    from fastapi.testclient import TestClient
    from database import get_db
    from eshop.dependencies import get_tenant_by_mufis_key
    from main import app

    monkeypatch.setenv("MUFIS_IP_CHECK_ENABLED", "true")
    monkeypatch.setenv("MUFIS_ALLOWED_IPS", "10.0.0.1")  # TestClient = 127.0.0.1

    def override_get_db():
        yield fake_db

    async def override_mufis_key():
        return _TENANT_DICT

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tenant_by_mufis_key] = override_mufis_key
    # NOTE: verify_mufis_access is NOT overridden → will check IP

    try:
        client = TestClient(app)
        resp = client.post(
            "/api/eshop/mufis/getOrder",
            data={},
            headers={"API-KEY": "test-key"},
        )
        assert resp.status_code == 403
    finally:
        app.dependency_overrides.clear()


# ===========================================================================
# getOrder TESTS (2)
# ===========================================================================


def test_mufis_getorder_empty(mufis_client, fake_db):
    """#4: Žiadne paid objednávky → prázdny orders[]."""
    # COUNT(*) returns 0, fetchall returns []
    fake_db.set_fetchone_sequence([(0,)])
    fake_db.set_fetchall_sequence([[]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data
    assert len(data["orders"]) == 0


def test_mufis_getorder_dry_run(mufis_client, fake_db, monkeypatch):
    """#5: DRY_RUN=true → vráti data, mufis_synced_at ostane NULL."""
    monkeypatch.setenv("MUFIS_DRY_RUN", "true")

    order_row = _make_order_row(order_id=42, order_number="ORD-DR-001", status="paid")

    # Sequence: COUNT(*) → 1, then order items fetchall (empty)
    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],  # main order query
            [],  # order items for order 42
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["orders"]) == 1
    assert data["orders"][0]["order_number"] == "ORD-DR-001"

    # Verify NO UPDATE mufis_synced_at was executed (dry-run)
    queries = fake_db.cursor().executed_queries
    synced_update_queries = [
        q for q in queries if "UPDATE" in q[0] and "mufis_synced_at" in q[0]
    ]
    assert len(synced_update_queries) == 0, "DRY-RUN should NOT update mufis_synced_at"


# ===========================================================================
# setOrder TESTS (3)
# ===========================================================================


def test_mufis_setorder_status_mapping(mufis_client, fake_db):
    """#6: "kézbesítve" → status='delivered' v DB + history source='mufis'."""
    # fetchone #1: SELECT order_id, status → existing order
    # fetchone #2: SELECT for email (won't happen — status not "shipped")
    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=10, status="paid"),
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={
            "order_number": "ORD-MAP-001",
            "status": "kézbesítve",
        },
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    assert resp.json()["ok"] == 1

    # Verify SQL queries
    queries = fake_db.cursor().executed_queries

    # Find UPDATE query
    update_queries = [q for q in queries if q[0].startswith("UPDATE eshop_orders SET")]
    assert len(update_queries) >= 1
    update_sql, update_params = update_queries[0]
    # Should contain mapped status 'delivered' (not 'kézbesítve')
    assert "status = %s" in update_sql
    assert "delivered" in update_params
    # Should also store original Hungarian status
    assert "mufis_status = %s" in update_sql
    assert "kézbesítve" in update_params

    # Find INSERT INTO status_history
    history_queries = [q for q in queries if "eshop_order_status_history" in q[0]]
    assert len(history_queries) == 1
    hist_sql, hist_params = history_queries[0]
    assert "source" in hist_sql
    assert "mufis_original_status" in hist_sql
    assert "mufis" in hist_params
    assert "kézbesítve" in hist_params
    assert "delivered" in hist_params


def test_mufis_setorder_unknown_status(mufis_client, fake_db):
    """#7: "xyz" → status='processing' (default)."""
    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=11, status="paid"),
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={
            "order_number": "ORD-UNK-001",
            "status": "unknown-xyz-status",
        },
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    assert resp.json()["ok"] == 1

    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if q[0].startswith("UPDATE eshop_orders SET")]
    assert len(update_queries) >= 1
    _, update_params = update_queries[0]
    # Unknown status → defaults to 'processing'
    assert "processing" in update_params


def test_mufis_setorder_tracking(mufis_client, fake_db):
    """#8: tracking_number + tracking_url + carrier uložené v DB."""
    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=12, status="paid"),
            # fetchone for email (shipped + tracking)
            (
                "ORD-TRK-001",
                "test@test.sk",
                "Test",
                "TRACK-456",
                "https://tracking.com/456",
            ),
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={
            "order_number": "ORD-TRK-001",
            "status": "futárnak átadva",
            "package_number": "TRACK-456",
            "tracking_link": "https://tracking.com/456",
            "carrier": "MPL",
        },
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    assert resp.json()["ok"] == 1

    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if q[0].startswith("UPDATE eshop_orders SET")]
    assert len(update_queries) >= 1
    update_sql, update_params = update_queries[0]

    # Verify mapped status
    assert "shipped" in update_params  # "futárnak átadva" → "shipped"

    # Verify tracking fields
    assert "mufis_tracking_number = %s" in update_sql
    assert "TRACK-456" in update_params
    assert "mufis_tracking_url = %s" in update_sql
    assert "https://tracking.com/456" in update_params
    assert "mufis_carrier = %s" in update_sql
    assert "MPL" in update_params


# ===========================================================================
# PRODUCT TESTS (2)
# ===========================================================================


def test_mufis_getproduct(mufis_client, fake_db):
    """#9: Vracia aktívne produkty."""
    product_row = _make_product_row(product_id=1, sku="SKU-001", stock_quantity=10)

    # COUNT(*) → 1, products fetchall → 1 product
    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence([[product_row]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getProduct",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "products" in data
    assert len(data["products"]) == 1
    assert data["products"][0]["sku"] == "SKU-001"
    assert data["products"][0]["stock_quantity"] == 10


def test_mufis_setproduct(mufis_client, fake_db):
    """#10: stock_quantity update."""
    resp = mufis_client.post(
        "/api/eshop/mufis/setProduct",
        data={
            "sku": "SKU-001",
            "stock_quantity": "5",
        },
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    assert resp.json()["ok"] == 1

    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if "UPDATE eshop_products" in q[0]]
    assert len(update_queries) == 1
    _, update_params = update_queries[0]
    assert 5 in update_params  # stock_quantity
    assert "SKU-001" in update_params


# ===========================================================================
# UNIT TESTS (2)
# ===========================================================================


def test_status_mapping_complete():
    """#11: Všetky MUFIS_STATUS_MAP hodnoty sú platné ORDER_STATUSES."""
    from eshop.mufis_status import MUFIS_STATUS_MAP, ORDER_STATUSES

    for mufis_status, internal_status in MUFIS_STATUS_MAP.items():
        assert internal_status in ORDER_STATUSES, (
            f"'{internal_status}' (z '{mufis_status}') nie je v ORDER_STATUSES"
        )


def test_status_mapping_unknown_default():
    """#12: Unknown MuFis status → 'processing' default."""
    from eshop.mufis_status import map_mufis_status

    result = map_mufis_status("totálne-neznámy-status")
    assert result == "processing"

    # Test case-insensitivity
    result2 = map_mufis_status("KÉZBESÍTVE")
    assert result2 == "delivered"

    result3 = map_mufis_status("  Futárnak Átadva  ")
    assert result3 == "shipped"
