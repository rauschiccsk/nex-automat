"""MuFis Integration Tests — 39 tests covering auth, getOrder, setOrder, product, status mapping.

Tests:
  AUTH (3):
    1. Valid API key + allowed IP → 200
    2. Invalid API key → 401
    3. Valid key, blocked IP → 401

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

  Audit Gap Fixes (5):
    13. A1: Invalid auth → 401 (nie 403)
    14. G2: getOrder has all required MuFis v1.2 fields
    15. G2: payment_type mapping (card → CARD)
    16. G2: Packeta delivery_point mapping
    17. G2: date_mod uses updated_at

  G1+G4 Request Params + Pagination (6):
    18. G1/G4: Default filter (paid + unsynced) + pagination fields
    19. G1: Filter by order_number → bypasses default filter
    20. G1: Filter by CSV status → IN clause
    21. G1: Filter by updated_at_min → bypasses default filter
    22. G1: Filter by date_from + date_to → created_at::date range
    23. G4: Pagination fields + page parameter forwarding

  S1+S2 setOrder Batch Mode + multiple_packages (5):
    24. S1: Batch mode s 2 objednávkami
    25. S1: Batch mode s invalid JSON
    26. S1: Batch partial success (1 ok, 1 not found)
    27. S2: multiple_packages=1 JSON array → comma-separated
    28. S1/S2: Single mode backward compatibility

  P1+P2+P3 getProduct Params + Stock/Barcode + Pagination (5):
    29. P1: Default all products + pagination fields
    30. P1: Filter by CSV SKU → IN clause
    31. P1: Filter by active=1 → is_active
    32. P2: stock_quantity + barcode from DB (not hardcoded)
    33. P3: Pagination total_pages + page

  SP1+SP3+W1 setProduct Batch Mode + Webhook (6):
    34. SP1: setProduct batch mode s data=[{sku, stock_quantity}]
    35. SP1: setProduct batch invalid JSON → error
    36. SP1: setProduct batch partial success (mix existujúcich/neexistujúcich)
    37. SP3: setProduct single mode stock_quantity update → DB
    38. W1: Webhook dry-run mode → GET sa nevolá
    39. W1: Webhook sends GET na MUFIS_WEBHOOK_URL
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
    "admin_notification_email": "admin@test.sk",
}

_TENANT_DICT_WITH_IP = {**_TENANT_DICT, "client_ip": "127.0.0.1"}


def _make_order_row(
    order_id=1,
    order_number="ORD-001",
    status="paid",
    tracking_number="",
    tracking_link="",
    payment_method="bank_transfer",
    delivery_method="courier",
    delivery_point_group="",
    delivery_point_id="",
    packeta_point_id="",
    packeta_point_name="",
    comgate_transaction_id="",
    company_ic_dph="",
    eu_vat_number="",
    updated_at=None,
    order_notes="",
):
    """Build a fake eshop_orders DB row matching getOrder SELECT columns.

    Columns (44 total):
      0:  order_id
      1:  order_number
      2:  tenant_id
      3:  customer_email
      4:  customer_name
      5:  customer_phone
      6:  lang
      7:  billing_name
      8:  billing_name2
      9:  billing_street
      10: billing_city
      11: billing_zip
      12: billing_country
      13: shipping_name
      14: shipping_name2
      15: shipping_street
      16: shipping_city
      17: shipping_zip
      18: shipping_country
      19: ico
      20: dic
      21: eu_vat_number
      22: total_amount
      23: total_amount_vat
      24: currency
      25: payment_method
      26: payment_status
      27: shipping_type
      28: shipping_price
      29: delivery_point_group
      30: delivery_point_id
      31: tracking_number
      32: tracking_link
      33: multiple_packages
      34: status
      35: note
      36: created_at
      37: updated_at
      38: comgate_transaction_id
      39: company_ic_dph
      40: delivery_method
      41: packeta_point_id
      42: packeta_point_name
      43: order_notes
    """
    now = datetime(2026, 3, 16, 12, 0, 0)
    return (
        order_id,  # 0: order_id
        order_number,  # 1: order_number
        1,  # 2: tenant_id
        "test@test.sk",  # 3: customer_email
        "Test Customer",  # 4: customer_name
        "+421900000000",  # 5: customer_phone
        "sk",  # 6: lang
        "Billing Name",  # 7: billing_name
        "",  # 8: billing_name2
        "Hlavná 1",  # 9: billing_street
        "Bratislava",  # 10: billing_city
        "81101",  # 11: billing_zip
        "SK",  # 12: billing_country
        "Ship Name",  # 13: shipping_name
        "",  # 14: shipping_name2
        "Nová 5",  # 15: shipping_street
        "Košice",  # 16: shipping_city
        "04001",  # 17: shipping_zip
        "SK",  # 18: shipping_country
        "",  # 19: ico
        "",  # 20: dic
        eu_vat_number,  # 21: eu_vat_number
        Decimal("100.00"),  # 22: total_amount
        Decimal("120.00"),  # 23: total_amount_vat
        "EUR",  # 24: currency
        payment_method,  # 25: payment_method
        "paid",  # 26: payment_status
        "courier",  # 27: shipping_type
        Decimal("5.00"),  # 28: shipping_price
        delivery_point_group,  # 29: delivery_point_group
        delivery_point_id,  # 30: delivery_point_id
        tracking_number,  # 31: tracking_number
        tracking_link,  # 32: tracking_link
        False,  # 33: multiple_packages
        status,  # 34: status
        "",  # 35: note
        now,  # 36: created_at
        updated_at or now,  # 37: updated_at
        comgate_transaction_id,  # 38: comgate_transaction_id
        company_ic_dph,  # 39: company_ic_dph
        delivery_method,  # 40: delivery_method
        packeta_point_id,  # 41: packeta_point_id
        packeta_point_name,  # 42: packeta_point_name
        order_notes,  # 43: order_notes
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
    assert resp.status_code == 401


def test_mufis_auth_invalid_ip(fake_db, monkeypatch):
    """#3: Správny key, nepovolená IP → 401."""
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
        assert resp.status_code == 401
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


# ===========================================================================
# NEW: MuFis Audit Gap Tests (5) — A1 + G2 fixes
# ===========================================================================


def test_mufis_auth_returns_401_for_invalid_key(mufis_client_no_auth, fake_db):
    """A1: MuFis auth neplatný API key → HTTP 401 (nie 403)."""
    fake_db.cursor().fetchone = lambda: None
    resp = mufis_client_no_auth.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "invalid_key_12345"},
    )
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    detail = resp.json().get("detail", "")
    assert "Neplatný" in detail or "Unauthorized" in detail


def test_mufis_getorder_response_has_all_required_fields(mufis_client, fake_db):
    """G2: getOrder response obsahuje VŠETKY povinné polia podľa MuFis API v1.2 spec."""
    order_row = _make_order_row(
        order_id=50,
        order_number="ORD-FIELDS-001",
        status="paid",
        comgate_transaction_id="CG-12345",
    )

    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],  # main order query
            [],  # order items for order 50
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

    order_data = data["orders"][0]

    # Required fields per MuFis API v1.2 spec
    required_fields = [
        "order_id",
        "order_number",
        "order_date",
        "status",
        "date_mod",
        "billing_name",
        "billing_name2",
        "billing_city",
        "billing_streetnum",
        "billing_zip",
        "billing_country",
        "shipping_name",
        "shipping_name2",
        "shipping_city",
        "shipping_streetnum",
        "shipping_zip",
        "shipping_country",
        "email",
        "phone",
        "eu_vat_number",
        "lang",
        "currency",
        "total_price",
        "payment_type",
        "shipping_type",
        "delivery_point_group",
        "delivery_point_id",
        "order_items",
        "meta_data",
    ]

    missing_fields = [f for f in required_fields if f not in order_data]
    assert not missing_fields, f"Missing required fields: {missing_fields}"

    # Verify date_mod format (Y-m-d H:M:S)
    try:
        datetime.strptime(order_data["date_mod"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail(f"date_mod has wrong format: {order_data['date_mod']}")

    # Verify order_date format (Y-m-d)
    try:
        datetime.strptime(order_data["order_date"], "%Y-%m-%d")
    except ValueError:
        pytest.fail(f"order_date has wrong format: {order_data['order_date']}")

    # Verify meta_data contains comgate_transaction_id
    meta_keys = [m["key"] for m in order_data["meta_data"]]
    assert "comgate_transaction_id" in meta_keys


def test_mufis_getorder_payment_type_mapping(mufis_client, fake_db):
    """G2: payment_method='card' → response payment_type='CARD'."""
    order_row = _make_order_row(
        order_id=51,
        order_number="ORD-PAY-001",
        status="paid",
        payment_method="card",
    )

    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],
            [],  # items
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    order_data = data["orders"][0]
    assert order_data["payment_type"] == "CARD", (
        f"Expected CARD, got {order_data['payment_type']}"
    )


def test_mufis_getorder_delivery_packeta(mufis_client, fake_db):
    """G2: packeta_point objednávka → delivery_point_group='packeta', delivery_point_id správne."""
    order_row = _make_order_row(
        order_id=52,
        order_number="ORD-PKT-001",
        status="paid",
        delivery_method="packeta_point",
        packeta_point_id="12345",
        packeta_point_name="Packeta Point Bratislava",
    )

    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],
            [],  # items
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    order_data = data["orders"][0]

    assert order_data["delivery_point_group"] == "packeta"
    assert order_data["delivery_point_id"] == "12345"

    # Check meta_data for packeta_point_name
    meta_keys = [m["key"] for m in order_data["meta_data"]]
    assert "packeta_point_name" in meta_keys
    packeta_meta = next(
        m for m in order_data["meta_data"] if m["key"] == "packeta_point_name"
    )
    assert packeta_meta["value"] == "Packeta Point Bratislava"


def test_mufis_getorder_date_mod_uses_updated_at(mufis_client, fake_db):
    """G2: date_mod reflektuje updated_at, nie created_at."""
    # Create order with different created_at and updated_at
    updated = datetime(2026, 3, 17, 15, 30, 0)
    order_row = _make_order_row(
        order_id=53,
        order_number="ORD-DMOD-001",
        status="paid",
        updated_at=updated,
    )

    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],
            [],  # items
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    order_data = data["orders"][0]

    # date_mod should reflect updated_at (2026-03-17 15:30:00)
    assert order_data["date_mod"] == "2026-03-17 15:30:00"
    # order_date should reflect created_at (2026-03-16)
    assert order_data["order_date"] == "2026-03-16"


# ===========================================================================
# NEW: MuFis Audit Gap Tests G1+G4 — Request Params + Pagination (6)
# ===========================================================================


def test_mufis_getorder_default_filter(mufis_client, fake_db):
    """G1/G4: getOrder bez parametrov → paid + unsynced + pagination fields."""
    fake_db.set_fetchone_sequence([(0,)])
    fake_db.set_fetchall_sequence([[]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    # Pagination fields
    assert "total_pages" in data
    assert "page" in data
    assert "orders" in data
    assert data["page"] == 1
    assert isinstance(data["total_pages"], int)
    assert data["total_pages"] >= 1

    # Verify default filter SQL contains paid + mufis_synced_at IS NULL
    queries = fake_db.cursor().executed_queries
    count_query = queries[0][0]
    assert "status = %s" in count_query
    assert "mufis_synced_at IS NULL" in count_query
    assert queries[0][1][1] == "paid"


def test_mufis_getorder_by_order_number(mufis_client, fake_db):
    """G1: getOrder s order_number filtrom → vracia konkrétnu objednávku."""
    order_row = _make_order_row(order_id=60, order_number="ORD-FILT-001", status="new")
    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],  # main order query
            [],  # order items
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={"order_number": "ORD-FILT-001"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert len(data["orders"]) == 1
    assert data["orders"][0]["order_number"] == "ORD-FILT-001"

    # Verify SQL: order_number filter present, default filter NOT present
    queries = fake_db.cursor().executed_queries
    count_query = queries[0][0]
    assert "order_number = %s" in count_query
    assert "mufis_synced_at IS NULL" not in count_query


def test_mufis_getorder_by_status_csv(mufis_client, fake_db):
    """G1: getOrder s comma-separated status filtrom → IN klauzula."""
    order_row_1 = _make_order_row(order_id=61, order_number="ORD-CSV-001", status="new")
    order_row_2 = _make_order_row(
        order_id=62, order_number="ORD-CSV-002", status="processing"
    )
    fake_db.set_fetchone_sequence([(2,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row_1, order_row_2],  # main order query
            [],  # items for order 61
            [],  # items for order 62
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={"status": "new,processing"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert len(data["orders"]) == 2

    # Verify SQL: IN clause with 2 statuses
    queries = fake_db.cursor().executed_queries
    count_query_sql = queries[0][0]
    count_query_params = queries[0][1]
    assert "status IN (%s, %s)" in count_query_sql
    assert "new" in count_query_params
    assert "processing" in count_query_params
    # Default filter should NOT be present
    assert "mufis_synced_at IS NULL" not in count_query_sql


def test_mufis_getorder_by_updated_at_min(mufis_client, fake_db):
    """G1: getOrder s updated_at_min filtrom → WHERE updated_at >= %s."""
    order_row = _make_order_row(
        order_id=63,
        order_number="ORD-UPD-001",
        status="paid",
        updated_at=datetime(2026, 3, 17, 10, 0, 0),
    )
    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],
            [],  # items
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={"updated_at_min": "2026-03-17 00:00:00"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["orders"]) == 1

    # Verify SQL: updated_at filter present, default filter NOT present
    queries = fake_db.cursor().executed_queries
    count_query_sql = queries[0][0]
    count_query_params = queries[0][1]
    assert "updated_at >= %s" in count_query_sql
    assert "2026-03-17 00:00:00" in count_query_params
    assert "mufis_synced_at IS NULL" not in count_query_sql


def test_mufis_getorder_by_date_range(mufis_client, fake_db):
    """G1: getOrder s date_from + date_to → WHERE created_at::date >= / <=."""
    order_row = _make_order_row(order_id=64, order_number="ORD-DATE-001", status="paid")
    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [
            [order_row],
            [],  # items
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={"date_from": "2026-03-01", "date_to": "2026-03-31"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["orders"]) == 1

    # Verify SQL: date range filters present
    queries = fake_db.cursor().executed_queries
    count_query_sql = queries[0][0]
    count_query_params = queries[0][1]
    assert "created_at::date >= %s" in count_query_sql
    assert "created_at::date <= %s" in count_query_sql
    assert "2026-03-01" in count_query_params
    assert "2026-03-31" in count_query_params
    # Default filter should NOT be present
    assert "mufis_synced_at IS NULL" not in count_query_sql


def test_mufis_getorder_pagination_fields(mufis_client, fake_db):
    """G4: getOrder response obsahuje pagination polia s page param."""
    fake_db.set_fetchone_sequence([(0,)])
    fake_db.set_fetchall_sequence([[]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={"page": "2"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    # Required pagination fields
    assert "total_pages" in data
    assert "page" in data
    assert isinstance(data["total_pages"], int)
    assert isinstance(data["page"], int)
    assert data["page"] == 2

    # Verify LIMIT/OFFSET in SELECT query
    queries = fake_db.cursor().executed_queries
    select_query = queries[1][0]  # second query is the SELECT
    assert "LIMIT %s OFFSET %s" in select_query


# ===========================================================================
# NEW: MuFis Audit Gap Tests S1+S2 — setOrder Batch Mode + multiple_packages (5)
# ===========================================================================


def test_mufis_setorder_batch_mode(mufis_client, fake_db):
    """S1: setOrder batch mode s data=[...] JSON array — 2 objednávky."""
    import json as _json

    # fetchone sequence: order1 lookup, order2 lookup
    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=20, status="paid"),
            _make_order_status_row(order_id=21, status="paid"),
        ]
    )

    batch_data = [
        {
            "order_number": "ORD-B-001",
            "status": "összeszedve",
            "package_number": "PKG001",
            "tracking_link": "https://track1.com",
        },
        {
            "order_number": "ORD-B-002",
            "status": "futárnak átadva",
            "package_number": "PKG002",
        },
    ]

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={"data": _json.dumps(batch_data)},
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    # Verify batch response format
    assert "orders" in data
    assert len(data["orders"]) == 2

    # Verify each result
    for i, result in enumerate(data["orders"]):
        assert "order_number" in result
        assert result["order_number"] == batch_data[i]["order_number"]
        assert result["ok"] == 1
        assert result["error"] == ""

    # Verify DB updates — 2 UPDATE queries
    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if q[0].startswith("UPDATE eshop_orders SET")]
    assert len(update_queries) == 2

    # First order: "összeszedve" → "processing"
    assert "processing" in update_queries[0][1]
    assert "PKG001" in update_queries[0][1]

    # Second order: "futárnak átadva" → "shipped"
    assert "shipped" in update_queries[1][1]
    assert "PKG002" in update_queries[1][1]


def test_mufis_setorder_batch_invalid_json(mufis_client):
    """S1: setOrder batch mode s invalid JSON vracia error."""
    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={"data": "not-valid-json{"},
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    assert "orders" in data
    assert len(data["orders"]) == 1
    assert data["orders"][0]["ok"] == 0
    assert "Invalid JSON" in data["orders"][0]["error"]


def test_mufis_setorder_batch_partial_success(mufis_client, fake_db):
    """S1: setOrder batch s mixed ok/error (1 existuje, 1 neexistuje)."""
    import json as _json

    # fetchone: first order found, second order NOT found (None)
    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=30, status="paid"),
            None,  # NONEXISTENT-ORDER
        ]
    )

    batch_data = [
        {"order_number": "ORD-PS-001", "status": "összeszedve"},
        {"order_number": "NONEXISTENT-ORDER", "status": "futárnak átadva"},
    ]

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={"data": _json.dumps(batch_data)},
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    assert len(data["orders"]) == 2
    assert data["orders"][0]["ok"] == 1
    assert data["orders"][1]["ok"] == 0
    assert "not found" in data["orders"][1]["error"].lower()


def test_mufis_setorder_multiple_packages(mufis_client, fake_db):
    """S2: setOrder s multiple_packages=1 a JSON array tracking info."""
    import json as _json

    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=40, status="paid"),
        ]
    )

    package_numbers = ["PKG001", "PKG002", "PKG003"]
    tracking_links = ["https://track1.com", "https://track2.com", "https://track3.com"]

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={
            "order_number": "ORD-MP-001",
            "status": "futárnak átadva",
            "multiple_packages": "1",
            "package_number": _json.dumps(package_numbers),
            "tracking_link": _json.dumps(tracking_links),
        },
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] == 1
    assert data["error"] == ""

    # Verify DB has comma-separated tracking numbers
    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if q[0].startswith("UPDATE eshop_orders SET")]
    assert len(update_queries) == 1

    update_sql, update_params = update_queries[0]

    # Check comma-separated values stored
    assert "mufis_tracking_number = %s" in update_sql
    assert "PKG001,PKG002,PKG003" in update_params

    assert "mufis_tracking_url = %s" in update_sql
    assert "https://track1.com,https://track2.com,https://track3.com" in update_params


def test_mufis_setorder_single_mode_unchanged(mufis_client, fake_db):
    """S1/S2: Existujúce single mód správanie neporušené (backward compat)."""
    fake_db.set_fetchone_sequence(
        [
            _make_order_status_row(order_id=50, status="paid"),
        ]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/setOrder",
        data={
            "order_number": "ORD-SINGLE-001",
            "status": "összeszedve",
            "package_number": "PKG-SINGLE",
            "tracking_link": "https://track-single.com",
        },
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    # Single mode response format — flat dict, NOT nested in "orders"
    assert "ok" in data
    assert data["ok"] == 1
    assert data["error"] == ""
    assert "orders" not in data

    # Verify DB update
    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if q[0].startswith("UPDATE eshop_orders SET")]
    assert len(update_queries) == 1
    update_sql, update_params = update_queries[0]

    assert "processing" in update_params  # "összeszedve" → "processing"
    assert "PKG-SINGLE" in update_params
    assert "https://track-single.com" in update_params


# ===========================================================================
# NEW: MuFis getProduct Gap Tests P1+P2+P3 (5)
# ===========================================================================


def test_mufis_getproduct_default_all(mufis_client, fake_db):
    """P1: getProduct bez parametrov vracia všetky produkty s pagination poliami."""
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

    # Response must contain pagination fields
    assert "total_pages" in data
    assert "page" in data
    assert "products" in data
    assert data["page"] == 1
    assert isinstance(data["total_pages"], int)
    assert data["total_pages"] >= 1

    # Products list not empty
    assert len(data["products"]) == 1

    # Verify SQL: only tenant_id filter, no other conditions
    queries = fake_db.cursor().executed_queries
    count_query = queries[0][0]
    assert "tenant_id = %s" in count_query
    assert "product_id = %s" not in count_query
    assert "sku" not in count_query
    assert "is_active" not in count_query


def test_mufis_getproduct_by_sku_csv(mufis_client, fake_db):
    """P1: getProduct s sku=EM-500,EM-500-3PACK filtruje správne cez IN klauzulu."""
    product_row_1 = _make_product_row(product_id=1, sku="EM-500", stock_quantity=10)
    product_row_2 = _make_product_row(
        product_id=2, sku="EM-500-3PACK", stock_quantity=5
    )

    # COUNT(*) → 2, products fetchall → 2 products
    fake_db.set_fetchone_sequence([(2,)])
    fake_db.set_fetchall_sequence([[product_row_1, product_row_2]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getProduct",
        data={"sku": "EM-500,EM-500-3PACK"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert len(data["products"]) == 2

    # Verify SQL: IN clause with 2 SKUs
    queries = fake_db.cursor().executed_queries
    count_query_sql = queries[0][0]
    count_query_params = queries[0][1]
    assert "sku IN (%s, %s)" in count_query_sql
    assert "EM-500" in count_query_params
    assert "EM-500-3PACK" in count_query_params


def test_mufis_getproduct_by_active(mufis_client, fake_db):
    """P1: getProduct s active=1 vracia len aktívne produkty."""
    product_row = _make_product_row(product_id=1, sku="SKU-ACTIVE", stock_quantity=10)

    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence([[product_row]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getProduct",
        data={"active": "1"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert len(data["products"]) == 1

    # Verify SQL: is_active filter
    queries = fake_db.cursor().executed_queries
    count_query_sql = queries[0][0]
    count_query_params = queries[0][1]
    assert "is_active = %s" in count_query_sql
    # active=1 → True
    assert True in count_query_params


def test_mufis_getproduct_stock_barcode(mufis_client, fake_db):
    """P2: getProduct response obsahuje stock_quantity a barcode z DB."""
    product_row = (
        1,  # product_id
        "SKU-BC",  # sku
        "8592000001234",  # barcode
        "Product with Barcode",  # name
        "Short",  # short_description
        "Full",  # description
        "",  # image_url
        Decimal("10.00"),  # price
        Decimal("12.00"),  # price_vat
        Decimal("20.00"),  # vat_rate
        42,  # stock_quantity
        Decimal("0.5"),  # weight
        True,  # is_active
        0,  # sort_order
    )

    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence([[product_row]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getProduct",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert len(data["products"]) == 1
    product = data["products"][0]

    # stock_quantity from DB (not hardcoded 0)
    assert product["stock_quantity"] == 42
    # barcode from DB (not empty string)
    assert product["barcode"] == "8592000001234"


def test_mufis_getproduct_pagination(mufis_client, fake_db):
    """P3: getProduct response obsahuje total_pages a page z pagination."""
    # COUNT(*) → 0 (empty), products fetchall → []
    fake_db.set_fetchone_sequence([(0,)])
    fake_db.set_fetchall_sequence([[]])

    resp = mufis_client.post(
        "/api/eshop/mufis/getProduct",
        data={"page": "2"},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()

    # Required pagination fields
    assert "total_pages" in data
    assert "page" in data
    assert isinstance(data["total_pages"], int)
    assert isinstance(data["page"], int)
    assert data["page"] == 2

    # Verify LIMIT/OFFSET in SELECT query
    queries = fake_db.cursor().executed_queries
    select_query = queries[1][0]  # second query is the SELECT
    assert "LIMIT %s OFFSET %s" in select_query


# ===========================================================================
# NEW: MuFis Audit Gap Tests SP1+SP3+W1 — setProduct Batch + Webhook (6)
# ===========================================================================


def test_mufis_setproduct_batch_mode(mufis_client, fake_db):
    """SP1: setProduct batch mode s data=[{sku, stock_quantity}] → {"products": [...]}."""
    import json as _json

    batch_data = [
        {"sku": "SKU-B-001", "stock_quantity": 10},
        {"sku": "SKU-B-002", "stock_quantity": 25},
    ]

    resp = mufis_client.post(
        "/api/eshop/mufis/setProduct",
        data={"data": _json.dumps(batch_data)},
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    # Verify batch response format
    assert "products" in data
    assert len(data["products"]) == 2

    # Verify each result
    for i, result in enumerate(data["products"]):
        assert "sku" in result
        assert result["sku"] == batch_data[i]["sku"]
        assert result["ok"] == 1
        assert result["error"] == ""

    # Verify DB updates — 2 UPDATE queries
    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if "UPDATE eshop_products" in q[0]]
    assert len(update_queries) == 2
    assert 10 in update_queries[0][1]
    assert "SKU-B-001" in update_queries[0][1]
    assert 25 in update_queries[1][1]
    assert "SKU-B-002" in update_queries[1][1]


def test_mufis_setproduct_batch_invalid_json(mufis_client):
    """SP1: setProduct batch mode s neplatným JSON → error."""
    resp = mufis_client.post(
        "/api/eshop/mufis/setProduct",
        data={"data": "not-valid-json{"},
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    assert "products" in data
    assert len(data["products"]) == 1
    assert data["products"][0]["ok"] == 0
    assert "Invalid JSON" in data["products"][0]["error"]


def test_mufis_setproduct_batch_partial_success(mufis_client, fake_db):
    """SP1: setProduct batch s mix platných a neplatných položiek."""
    import json as _json

    batch_data = [
        {"sku": "SKU-OK", "stock_quantity": 15},
        {"sku": "", "stock_quantity": 5},  # empty SKU → error
        {"sku": "SKU-NOQTY"},  # missing stock_quantity → error
    ]

    resp = mufis_client.post(
        "/api/eshop/mufis/setProduct",
        data={"data": _json.dumps(batch_data)},
        headers={"API-KEY": "test-key"},
    )

    assert resp.status_code == 200
    data = resp.json()

    assert "products" in data
    assert len(data["products"]) == 3

    # First: OK
    assert data["products"][0]["ok"] == 1
    assert data["products"][0]["sku"] == "SKU-OK"
    assert data["products"][0]["error"] == ""

    # Second: error (empty sku)
    assert data["products"][1]["ok"] == 0
    assert "sku" in data["products"][1]["error"].lower()

    # Third: error (missing stock_quantity)
    assert data["products"][2]["ok"] == 0
    assert "stock_quantity" in data["products"][2]["error"].lower()


def test_mufis_setproduct_stock_update(mufis_client, fake_db):
    """SP3: setProduct single mode skutočne uloží stock_quantity do DB s updated_at."""
    resp = mufis_client.post(
        "/api/eshop/mufis/setProduct",
        data={
            "sku": "SKU-STOCK-001",
            "stock_quantity": "42",
        },
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] == 1
    assert data["error"] == ""

    # Single mode response — flat dict, NOT nested in "products"
    assert "products" not in data

    queries = fake_db.cursor().executed_queries
    update_queries = [q for q in queries if "UPDATE eshop_products" in q[0]]
    assert len(update_queries) == 1

    update_sql, update_params = update_queries[0]
    # Verify stock_quantity and updated_at in SQL
    assert "stock_quantity = %s" in update_sql
    assert "updated_at = CURRENT_TIMESTAMP" in update_sql
    assert 42 in update_params
    assert "SKU-STOCK-001" in update_params


def test_mufis_webhook_dry_run(monkeypatch):
    """W1: V dry-run režime sa HTTP GET nevolá."""
    import asyncio

    from eshop import mufis_webhook

    monkeypatch.setattr(
        mufis_webhook, "MUFIS_WEBHOOK_URL", "https://mufis.example.com/webhook"
    )
    monkeypatch.setattr(mufis_webhook, "MUFIS_DRY_RUN", True)

    with patch("eshop.mufis_webhook.httpx.AsyncClient") as mock_client_cls:
        asyncio.get_event_loop().run_until_complete(
            mufis_webhook.notify_mufis_order_change()
        )
        # In dry-run mode, AsyncClient should NOT be called
        mock_client_cls.assert_not_called()


def test_mufis_webhook_sends_get(monkeypatch):
    """W1: Webhook posiela GET request na MUFIS_WEBHOOK_URL."""
    import asyncio

    from eshop import mufis_webhook

    monkeypatch.setattr(
        mufis_webhook, "MUFIS_WEBHOOK_URL", "https://mufis.example.com/webhook"
    )
    monkeypatch.setattr(mufis_webhook, "MUFIS_DRY_RUN", False)

    mock_response = AsyncMock()
    mock_response.status_code = 200

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("eshop.mufis_webhook.httpx.AsyncClient", return_value=mock_client):
        asyncio.get_event_loop().run_until_complete(
            mufis_webhook.notify_mufis_order_change()
        )

        # Verify GET was called with the webhook URL
        mock_client.get.assert_called_once_with("https://mufis.example.com/webhook")


# ===========================================================================
# ORDER NOTES + EMAIL NOTIFICATION TESTS (5)
# ===========================================================================


def test_mufis_getorder_order_notes_in_meta_data(mufis_client, fake_db, monkeypatch):
    """#40: order_notes sa objaví v meta_data[] v getOrder response."""
    monkeypatch.setenv("MUFIS_DRY_RUN", "true")
    order_row = _make_order_row(
        order_notes="TESTOVACIA OBJEDNAVKA – staging",
    )
    fake_db.set_fetchone_sequence([(1,)])  # count
    fake_db.set_fetchall_sequence(
        [[order_row], [("EM-500", "Product", 2, Decimal("8.25"), Decimal("9.90"), Decimal("20.00"), "product")]]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["orders"]) == 1
    order = data["orders"][0]
    meta_keys = [m["key"] for m in order["meta_data"]]
    assert "order_notes" in meta_keys
    notes_entry = next(m for m in order["meta_data"] if m["key"] == "order_notes")
    assert "TESTOVACIA" in notes_entry["value"]


def test_mufis_getorder_no_order_notes_when_empty(mufis_client, fake_db, monkeypatch):
    """#41: Prázdne order_notes sa neobjavujú v meta_data[]."""
    monkeypatch.setenv("MUFIS_DRY_RUN", "true")
    order_row = _make_order_row(order_notes="")
    fake_db.set_fetchone_sequence([(1,)])
    fake_db.set_fetchall_sequence(
        [[order_row], [("EM-500", "Product", 2, Decimal("8.25"), Decimal("9.90"), Decimal("20.00"), "product")]]
    )

    resp = mufis_client.post(
        "/api/eshop/mufis/getOrder",
        data={},
        headers={"API-KEY": "test-key"},
    )
    assert resp.status_code == 200
    order = resp.json()["orders"][0]
    meta_keys = [m["key"] for m in order["meta_data"]]
    assert "order_notes" not in meta_keys


def test_email_service_admin_notification_email_fallback():
    """#42: EshopEmailService uses admin_notification_email over admin_email."""
    from eshop.email_service import EshopEmailService

    # admin_notification_email has priority
    svc = EshopEmailService({
        "admin_notification_email": "notif@test.sk",
        "admin_email": "admin@test.sk",
        "smtp_from": "noreply@test.sk",
        "brand_name": "Test",
        "domain": "test.sk",
        "primary_color": "#2E7D32",
    })
    assert svc.admin_email == "notif@test.sk"

    # Falls back to admin_email when admin_notification_email is None
    svc2 = EshopEmailService({
        "admin_notification_email": None,
        "admin_email": "admin@test.sk",
        "smtp_from": "noreply@test.sk",
        "brand_name": "Test",
        "domain": "test.sk",
        "primary_color": "#2E7D32",
    })
    assert svc2.admin_email == "admin@test.sk"


def test_email_service_order_notes_in_admin_email():
    """#43: Admin email obsahuje order_notes ak sú prítomné."""
    from eshop.email_service import EshopEmailService

    svc = EshopEmailService({
        "admin_email": "admin@test.sk",
        "smtp_from": "noreply@test.sk",
        "brand_name": "Test",
        "domain": "test.sk",
        "primary_color": "#2E7D32",
    })

    import asyncio
    from unittest.mock import AsyncMock, patch

    order = {
        "order_number": "ORD-TEST-001",
        "customer_name": "Test Zákazník",
        "customer_email": "test@test.sk",
        "customer_phone": "+421900000000",
        "total_amount_vat": 120.00,
        "currency": "EUR",
        "payment_method": "bank_transfer",
        "note": "",
        "order_notes": "TESTOVACIA OBJEDNAVKA – staging",
    }
    items = [{"name": "EM-1", "quantity": 1, "unit_price_vat": 9.90}]

    with patch.object(svc, "_send_email", new_callable=AsyncMock) as mock_send:
        asyncio.get_event_loop().run_until_complete(
            svc.send_admin_new_order(order, items)
        )
        assert mock_send.called
        html_body = mock_send.call_args[0][2]
        assert "TESTOVACIA" in html_body


def test_email_service_send_does_not_block():
    """#44: Email send failure nesmie blokovať — error je len zalogovaný."""
    from eshop.email_service import EshopEmailService

    svc = EshopEmailService({
        "admin_email": "admin@test.sk",
        "smtp_from": "noreply@test.sk",
        "brand_name": "Test",
        "domain": "test.sk",
        "primary_color": "#2E7D32",
    })

    import asyncio
    from unittest.mock import patch

    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.side_effect = ConnectionRefusedError("SMTP down")
        # Should NOT raise — errors are caught internally
        asyncio.get_event_loop().run_until_complete(
            svc.send_admin_new_order(
                {"order_number": "ORD-001", "customer_name": "Test",
                 "customer_email": "t@t.sk", "customer_phone": "",
                 "total_amount_vat": 10, "currency": "EUR",
                 "payment_method": "bank", "note": "", "order_notes": ""},
                [{"name": "P", "quantity": 1, "unit_price_vat": 10}],
            )
        )
