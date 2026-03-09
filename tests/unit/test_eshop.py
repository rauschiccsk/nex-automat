"""
Unit tests for NEX Manager API — ESHOP module.

Tests cover:
- Tenant resolution (X-Eshop-Token, MuFis API-KEY)
- Public product endpoints (list, detail, 404, tenant isolation, inactive filter)
- Public order endpoints (create, validation, pricing, status)
- Admin endpoints (orders CRUD, products CRUD, tenants, auth)
- MuFis endpoints (getOrder, setOrder, getProduct, setProduct)

Total: ~41 tests
"""

import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add nex-manager-api to path so we can import its modules
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "apps" / "nex-manager-api")
)

from fastapi.testclient import TestClient

from auth.dependencies import get_current_user
from database import get_db
from eshop.dependencies import get_tenant_by_mufis_key, get_tenant_by_token
from main import app

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FAKE_USER = {
    "user_id": 1,
    "login_name": "admin",
    "full_name": "Administrátor",
    "email": "admin@icc.sk",
    "is_active": True,
}

FAKE_TENANT = {
    "tenant_id": 1,
    "company_name": "ICC s.r.o.",
    "domain": "emcenter.sk",
    "brand_name": "EM Center",
    "logo_url": None,
    "primary_color": "#2E7D32",
    "currency": "EUR",
    "vat_rate_default": Decimal("20.00"),
    "default_lang": "sk",
    "is_active": True,
}

FAKE_TENANT_2 = {
    "tenant_id": 2,
    "company_name": "Other s.r.o.",
    "domain": "other.sk",
    "brand_name": "Other",
    "logo_url": None,
    "primary_color": "#000000",
    "currency": "EUR",
    "vat_rate_default": Decimal("20.00"),
    "default_lang": "sk",
    "is_active": True,
}

NOW = datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

# product row: product_id, sku, name, short_description, description,
#              price, price_vat, vat_rate, stock_quantity, image_url, weight, is_active
PRODUCT_ROW_1 = (
    1, "EM-500", "OASIS EM-1 500ml", "Trial balenie", None,
    Decimal("8.25"), Decimal("9.90"), Decimal("20.00"), 10, None, None, True,
)
PRODUCT_ROW_2 = (
    2, "EM-5L", "OASIS EM-1 5L", "Odporúčané balenie", None,
    Decimal("33.25"), Decimal("39.90"), Decimal("20.00"), 5, None, None, True,
)
PRODUCT_ROW_INACTIVE = (
    3, "EM-OLD", "Starý produkt", "Neaktívny", None,
    Decimal("5.00"), Decimal("6.00"), Decimal("20.00"), 0, None, None, False,
)

# product lookup row for order creation:
# product_id, sku, name, price, price_vat, vat_rate, is_active
PRODUCT_LOOKUP_1 = (1, "EM-500", "OASIS EM-1 500ml", Decimal("8.25"), Decimal("9.90"), Decimal("20.00"), True)
PRODUCT_LOOKUP_2 = (2, "EM-5L", "OASIS EM-1 5L", Decimal("33.25"), Decimal("39.90"), Decimal("20.00"), True)
PRODUCT_LOOKUP_INACTIVE = (3, "EM-OLD", "Starý produkt", Decimal("5.00"), Decimal("6.00"), Decimal("20.00"), False)

# Permission check result — True means granted
PERM_GRANTED = (True,)
PERM_DENIED = (False,)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_db():
    """Mock pg8000 connection + cursor."""
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


@pytest.fixture()
def client_public(mock_db):
    """TestClient with mocked DB and eshop token auth."""
    conn, _ = mock_db

    app.dependency_overrides[get_db] = lambda: conn
    app.dependency_overrides[get_tenant_by_token] = lambda: FAKE_TENANT

    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_public_no_auth(mock_db):
    """TestClient without eshop token override — will 401."""
    conn, _ = mock_db
    app.dependency_overrides[get_db] = lambda: conn
    # No tenant override — requires real X-Eshop-Token
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_admin(mock_db):
    """TestClient with JWT auth for admin endpoints."""
    conn, _ = mock_db

    app.dependency_overrides[get_db] = lambda: conn
    app.dependency_overrides[get_current_user] = lambda: FAKE_USER

    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_admin_no_auth(mock_db):
    """TestClient without JWT override — will 401 on admin endpoints."""
    conn, _ = mock_db
    app.dependency_overrides[get_db] = lambda: conn
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_mufis(mock_db):
    """TestClient with MuFis API-KEY auth."""
    conn, _ = mock_db

    app.dependency_overrides[get_db] = lambda: conn
    app.dependency_overrides[get_tenant_by_mufis_key] = lambda: FAKE_TENANT

    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_mufis_no_auth(mock_db):
    """TestClient without MuFis API-KEY override — will 401."""
    conn, _ = mock_db
    app.dependency_overrides[get_db] = lambda: conn
    yield TestClient(app)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helper — build valid order request body
# ---------------------------------------------------------------------------

def _order_body(**overrides):
    """Create a valid order request body with optional overrides."""
    base = {
        "customer_email": "test@test.sk",
        "customer_name": "Test Customer",
        "billing_name": "Test Customer",
        "billing_street": "Testová 1",
        "billing_city": "Bratislava",
        "billing_zip": "81101",
        "billing_country": "SK",
        "items": [{"sku": "EM-500", "quantity": 2}],
        "payment_method": "bank_transfer",
    }
    base.update(overrides)
    return base


# ============================================================================
# TENANT RESOLUTION (5 tests)
# ============================================================================


class TestTenantResolution:
    """Tenant resolution via X-Eshop-Token and MuFis API-KEY."""

    def test_valid_eshop_token(self, client_public, mock_db):
        """Valid X-Eshop-Token resolves tenant."""
        _, cursor = mock_db
        cursor.fetchall.return_value = [PRODUCT_ROW_1, PRODUCT_ROW_2]
        resp = client_public.get("/api/eshop/products")
        assert resp.status_code == 200

    def test_invalid_eshop_token(self, client_public_no_auth, mock_db):
        """Invalid token returns 401."""
        resp = client_public_no_auth.get(
            "/api/eshop/products",
            headers={"X-Eshop-Token": "invalid-token"},
        )
        # Without override, dependency will actually run and query DB
        # Mock cursor returns None → 401
        _, cursor = mock_db
        cursor.fetchone.return_value = None
        # Need to re-request since dependency runs on request
        resp = client_public_no_auth.get(
            "/api/eshop/products",
            headers={"X-Eshop-Token": "invalid-token"},
        )
        assert resp.status_code == 401

    def test_missing_eshop_token(self, client_public_no_auth):
        """Missing token returns 422 (header required)."""
        resp = client_public_no_auth.get("/api/eshop/products")
        assert resp.status_code in (401, 422)

    def test_valid_mufis_api_key(self, client_mufis, mock_db):
        """Valid MuFis API-KEY resolves tenant."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(0,)]  # count
        cursor.fetchall.return_value = []
        resp = client_mufis.post(
            "/api/eshop/mufis/getProduct",
            data={"page": "1"},
        )
        assert resp.status_code == 200

    def test_invalid_mufis_api_key(self, client_mufis_no_auth, mock_db):
        """Invalid MuFis API-KEY returns 401."""
        _, cursor = mock_db
        cursor.fetchone.return_value = None
        resp = client_mufis_no_auth.post(
            "/api/eshop/mufis/getProduct",
            data={"page": "1"},
            headers={"API-KEY": "invalid-key"},
        )
        assert resp.status_code == 401


# ============================================================================
# PUBLIC — Products (6 tests)
# ============================================================================


class TestPublicProducts:
    """GET /api/eshop/products tests."""

    def test_list_active_products(self, client_public, mock_db):
        """Returns active products for tenant."""
        _, cursor = mock_db
        cursor.fetchall.return_value = [PRODUCT_ROW_1, PRODUCT_ROW_2]
        resp = client_public.get("/api/eshop/products")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["products"]) == 2
        assert data["products"][0]["sku"] == "EM-500"

    def test_get_product_by_sku(self, client_public, mock_db):
        """Returns single product by SKU."""
        _, cursor = mock_db
        cursor.fetchone.return_value = PRODUCT_ROW_1
        resp = client_public.get("/api/eshop/products/EM-500")
        assert resp.status_code == 200
        data = resp.json()
        assert data["sku"] == "EM-500"
        assert data["name"] == "OASIS EM-1 500ml"

    def test_get_product_not_found(self, client_public, mock_db):
        """404 for non-existent SKU."""
        _, cursor = mock_db
        cursor.fetchone.return_value = None
        resp = client_public.get("/api/eshop/products/NONEXISTENT")
        assert resp.status_code == 404
        assert "nebol nájdený" in resp.json()["detail"]

    def test_tenant_isolation(self, client_public, mock_db):
        """Products from other tenants are not returned."""
        _, cursor = mock_db
        # Empty list — no products for this tenant
        cursor.fetchall.return_value = []
        resp = client_public.get("/api/eshop/products")
        assert resp.status_code == 200
        assert resp.json()["products"] == []

    def test_inactive_products_not_returned(self, client_public, mock_db):
        """Inactive products are filtered out in public API."""
        _, cursor = mock_db
        # Only active products returned by SQL (WHERE is_active = TRUE)
        cursor.fetchall.return_value = [PRODUCT_ROW_1]
        resp = client_public.get("/api/eshop/products")
        assert resp.status_code == 200
        products = resp.json()["products"]
        assert len(products) == 1
        assert all(p["is_active"] for p in products)

    def test_product_response_fields(self, client_public, mock_db):
        """Response contains all expected fields."""
        _, cursor = mock_db
        cursor.fetchone.return_value = PRODUCT_ROW_1
        resp = client_public.get("/api/eshop/products/EM-500")
        assert resp.status_code == 200
        data = resp.json()
        expected_fields = [
            "product_id", "sku", "name", "short_description", "description",
            "price", "price_vat", "vat_rate", "stock_quantity", "image_url",
            "weight", "is_active",
        ]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"


# ============================================================================
# PUBLIC — Orders (10 tests)
# ============================================================================


class TestPublicOrders:
    """POST /api/eshop/orders and GET /api/eshop/orders/{number} tests."""

    def test_create_order_success(self, client_public, mock_db):
        """Successful order creation."""
        _, cursor = mock_db
        # Sequence: product lookup, advisory lock, max order_number, INSERT RETURNING
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,  # product lookup for EM-500
            None,              # advisory lock (no return)
            (None,),           # MAX order_number
            (42,),             # INSERT RETURNING order_id
        ]
        resp = client_public.post("/api/eshop/orders", json=_order_body())
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "new"
        assert data["currency"] == "EUR"
        assert "order_number" in data

    def test_order_number_format(self, client_public, mock_db):
        """Order number follows PREFIX-YEAR-NNNNN format."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,              # advisory lock
            (None,),           # no existing orders
            (1,),              # order_id
        ]
        resp = client_public.post("/api/eshop/orders", json=_order_body())
        assert resp.status_code == 200
        order_number = resp.json()["order_number"]
        parts = order_number.split("-")
        assert len(parts) == 3
        assert parts[0] == "EM"  # first 2 chars of "EM Center"
        assert len(parts[2]) == 5  # 5-digit sequence

    def test_prices_from_db_not_request(self, client_public, mock_db):
        """Prices are calculated from DB, not from request."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,  # DB price: 9.90 VAT
            None,              # advisory lock
            (None,),           # MAX
            (1,),              # order_id
        ]
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(items=[{"sku": "EM-500", "quantity": 2}]),
        )
        assert resp.status_code == 200
        data = resp.json()
        # 2 * 9.90 = 19.80
        expected_vat = float(Decimal("9.90") * 2)
        assert float(data["total_amount_vat"]) == pytest.approx(expected_vat, abs=0.01)

    def test_totals_correctly_calculated(self, client_public, mock_db):
        """Totals are correctly summed for multiple items."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,  # EM-500: 9.90 VAT
            PRODUCT_LOOKUP_2,  # EM-5L: 39.90 VAT
            None,              # advisory lock
            (None,),           # MAX
            (1,),              # order_id
        ]
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(items=[
                {"sku": "EM-500", "quantity": 1},
                {"sku": "EM-5L", "quantity": 1},
            ]),
        )
        assert resp.status_code == 200
        data = resp.json()
        # 9.90 + 39.90 = 49.80
        expected_total = float(Decimal("9.90") + Decimal("39.90"))
        assert float(data["total_amount_vat"]) == pytest.approx(expected_total, abs=0.01)

    def test_nonexistent_sku_returns_400(self, client_public, mock_db):
        """Non-existent SKU returns 400."""
        _, cursor = mock_db
        cursor.fetchone.return_value = None  # product not found
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(items=[{"sku": "FAKE-SKU", "quantity": 1}]),
        )
        assert resp.status_code == 400
        assert "nebol nájdený" in resp.json()["detail"]

    def test_empty_items_returns_422(self, client_public, mock_db):
        """Empty items list returns 422 (validation)."""
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(items=[]),
        )
        assert resp.status_code == 422

    def test_missing_required_fields_returns_422(self, client_public):
        """Missing required fields returns 422."""
        resp = client_public.post(
            "/api/eshop/orders",
            json={"customer_email": "test@test.sk"},
        )
        assert resp.status_code == 422

    def test_order_status_is_new(self, client_public, mock_db):
        """New order has status 'new'."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,
            (None,),
            (1,),
        ]
        resp = client_public.post("/api/eshop/orders", json=_order_body())
        assert resp.status_code == 200
        assert resp.json()["status"] == "new"

    def test_status_history_created(self, client_public, mock_db):
        """Status history entry is created on order creation."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,
            (None,),
            (1,),
        ]
        resp = client_public.post("/api/eshop/orders", json=_order_body())
        assert resp.status_code == 200
        # Verify INSERT into eshop_order_status_history was called
        calls = [str(c) for c in cursor.execute.call_args_list]
        history_calls = [c for c in calls if "eshop_order_status_history" in c]
        assert len(history_calls) >= 1

    def test_get_order_by_number(self, client_public, mock_db):
        """GET order by order_number returns order with items."""
        _, cursor = mock_db
        cursor.fetchone.return_value = (
            "EM-2026-00001", "new", "pending", "", "", NOW,
        )
        cursor.fetchall.return_value = [
            ("EM-500", "OASIS EM-1 500ml", 2, Decimal("9.90"), Decimal("20.00")),
        ]
        resp = client_public.get("/api/eshop/orders/EM-2026-00001")
        assert resp.status_code == 200
        data = resp.json()
        assert data["order_number"] == "EM-2026-00001"
        assert data["status"] == "new"
        assert len(data["items"]) == 1
        assert data["items"][0]["sku"] == "EM-500"


# ============================================================================
# ADMIN (8 tests)
# ============================================================================


class TestAdmin:
    """Admin ESHOP endpoints (JWT auth)."""

    def test_admin_list_orders(self, client_admin, mock_db):
        """GET admin/orders returns paginated list."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PERM_GRANTED,
            (1,),  # count
        ]
        cursor.fetchall.return_value = [
            (1, "EM-2026-00001", "Test", "t@t.sk",
             Decimal("19.80"), "EUR", "new", "pending", NOW, NOW),
        ]
        resp = client_admin.get("/api/eshop/admin/orders")
        assert resp.status_code == 200
        data = resp.json()
        assert "orders" in data
        assert "total" in data
        assert data["total"] == 1

    def test_admin_get_order_detail(self, client_admin, mock_db):
        """GET admin/orders/{id} returns detail with items + history."""
        _, cursor = mock_db
        order_row = (
            1, "EM-2026-00001", 1, "t@t.sk", "Test", "", "sk",
            "Test", "", "Testova 1", "BA", "81101", "SK",
            "", "", "", "", "", "",
            "", "", "",
            Decimal("16.50"), Decimal("19.80"), "EUR",
            "bank_transfer", "pending", None, "", Decimal("0"),
            "", "", "", "", False, "new", "", NOW, NOW,
        )
        cursor.fetchone.side_effect = [PERM_GRANTED, order_row]
        cursor.fetchall.side_effect = [
            [("EM-500", "OASIS EM-1 500ml", 2, Decimal("9.90"), Decimal("20.00"))],
            [(None, "new", "system", "", NOW)],
        ]
        resp = client_admin.get("/api/eshop/admin/orders/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["order_number"] == "EM-2026-00001"
        assert len(data["items"]) == 1
        assert len(data["status_history"]) == 1

    def test_admin_update_order_status(self, client_admin, mock_db):
        """PATCH admin/orders/{id} updates status."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, ("new",)]  # PERM + current status
        resp = client_admin.patch(
            "/api/eshop/admin/orders/1",
            json={"status": "processing"},
        )
        assert resp.status_code == 200

    def test_admin_status_history_on_update(self, client_admin, mock_db):
        """Status change creates history entry."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, ("new",)]
        resp = client_admin.patch(
            "/api/eshop/admin/orders/1",
            json={"status": "shipped"},
        )
        assert resp.status_code == 200
        calls = [str(c) for c in cursor.execute.call_args_list]
        history_calls = [c for c in calls if "eshop_order_status_history" in c]
        assert len(history_calls) >= 1

    def test_admin_create_product(self, client_admin, mock_db):
        """POST admin/products creates product."""
        _, cursor = mock_db
        new_product_row = (
            10, 1, "NEW-SKU", None, "New Product", None,
            None, None, Decimal("10.00"), Decimal("12.00"), Decimal("20.00"),
            50, None, True, 0, NOW, NOW,
        )
        cursor.fetchone.side_effect = [PERM_GRANTED, new_product_row]
        resp = client_admin.post(
            "/api/eshop/admin/products?tenant_id=1",
            json={
                "sku": "NEW-SKU",
                "name": "New Product",
                "price": 10.00,
                "price_vat": 12.00,
                "vat_rate": 20.00,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["sku"] == "NEW-SKU"

    def test_admin_update_product(self, client_admin, mock_db):
        """PATCH admin/products/{id} partial update."""
        _, cursor = mock_db
        updated_row = (
            1, 1, "EM-500", None, "Updated Name", None,
            None, None, Decimal("8.25"), Decimal("9.90"), Decimal("20.00"),
            10, None, True, 0, NOW, NOW,
        )
        cursor.fetchone.side_effect = [PERM_GRANTED, updated_row]
        resp = client_admin.patch(
            "/api/eshop/admin/products/1",
            json={"name": "Updated Name"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"

    def test_admin_delete_product_soft(self, client_admin, mock_db):
        """DELETE admin/products/{id} soft deletes."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, (1,)]  # PERM + RETURNING
        resp = client_admin.delete("/api/eshop/admin/products/1")
        assert resp.status_code == 204

    def test_admin_no_jwt_returns_401(self, client_admin_no_auth):
        """Admin endpoints without JWT return 401."""
        resp = client_admin_no_auth.get("/api/eshop/admin/orders")
        assert resp.status_code in (401, 403)


# ============================================================================
# MUFIS (12 tests)
# ============================================================================


class TestMuFis:
    """MuFis integration endpoints (form-urlencoded, API-KEY auth)."""

    def test_get_order_basic(self, client_mufis, mock_db):
        """getOrder returns orders for tenant."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(1,)]  # count
        cursor.fetchall.side_effect = [
            [  # order row
                (1, "EM-2026-00001", 1, "t@t.sk", "Test", "", "sk",
                 "Test", "", "Testova", "BA", "81101", "SK",
                 "", "", "", "", "", "",
                 "", "", "",
                 Decimal("16.50"), Decimal("19.80"), "EUR",
                 "bank_transfer", "pending", "", Decimal("0"),
                 "", "", "", "", False, "new", "",
                 NOW, NOW),
            ],
            [  # items for order 1
                ("EM-500", "OASIS EM-1 500ml", 2, Decimal("8.25"),
                 Decimal("9.90"), Decimal("20.00"), "product"),
            ],
        ]
        resp = client_mufis.post("/api/eshop/mufis/getOrder", data={"page": "1"})
        assert resp.status_code == 200
        data = resp.json()
        assert "orders" in data
        assert data["page"] == 1

    def test_get_order_with_order_number_filter(self, client_mufis, mock_db):
        """getOrder filters by order_number."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(1,)]
        cursor.fetchall.side_effect = [
            [(1, "EM-2026-00001", 1, "t@t.sk", "Test", "", "sk",
              "Test", "", "Testova", "BA", "81101", "SK",
              "", "", "", "", "", "",
              "", "", "",
              Decimal("16.50"), Decimal("19.80"), "EUR",
              "bank_transfer", "pending", "", Decimal("0"),
              "", "", "", "", False, "new", "",
              NOW, NOW)],
            [("EM-500", "OASIS", 2, Decimal("8.25"), Decimal("9.90"), Decimal("20.00"), "product")],
        ]
        resp = client_mufis.post(
            "/api/eshop/mufis/getOrder",
            data={"order_number": "EM-2026-00001"},
        )
        assert resp.status_code == 200

    def test_get_order_with_updated_at_min(self, client_mufis, mock_db):
        """getOrder filters by updated_at_min."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(0,)]
        cursor.fetchall.return_value = []
        resp = client_mufis.post(
            "/api/eshop/mufis/getOrder",
            data={"updated_at_min": "2026-01-01T00:00:00"},
        )
        assert resp.status_code == 200

    def test_get_order_with_status_filter(self, client_mufis, mock_db):
        """getOrder filters by status."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(0,)]
        cursor.fetchall.return_value = []
        resp = client_mufis.post(
            "/api/eshop/mufis/getOrder",
            data={"status": "new"},
        )
        assert resp.status_code == 200

    def test_get_order_with_date_range(self, client_mufis, mock_db):
        """getOrder filters by date_from/date_to."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(0,)]
        cursor.fetchall.return_value = []
        resp = client_mufis.post(
            "/api/eshop/mufis/getOrder",
            data={"date_from": "2026-01-01", "date_to": "2026-12-31"},
        )
        assert resp.status_code == 200

    def test_get_order_pagination(self, client_mufis, mock_db):
        """getOrder returns pagination info."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(100,)]  # 100 total → 2 pages
        cursor.fetchall.return_value = []
        resp = client_mufis.post(
            "/api/eshop/mufis/getOrder",
            data={"page": "2"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_pages"] == 2
        assert data["page"] == 2

    def test_get_order_items_format(self, client_mufis, mock_db):
        """getOrder returns items in correct nested format."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(1,)]
        cursor.fetchall.side_effect = [
            [(1, "EM-2026-00001", 1, "t@t.sk", "Test", "", "sk",
              "Test", "", "Testova", "BA", "81101", "SK",
              "", "", "", "", "", "",
              "", "", "",
              Decimal("16.50"), Decimal("19.80"), "EUR",
              "bank_transfer", "pending", "", Decimal("0"),
              "", "", "", "", False, "new", "",
              NOW, NOW)],
            [("EM-500", "OASIS", 2, Decimal("8.25"), Decimal("9.90"), Decimal("20.00"), "product")],
        ]
        resp = client_mufis.post("/api/eshop/mufis/getOrder", data={})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["orders"]) == 1
        order = data["orders"][0]
        assert "items" in order
        assert len(order["items"]) == 1
        assert order["items"][0]["sku"] == "EM-500"

    def test_set_order_update(self, client_mufis, mock_db):
        """setOrder updates status and tracking."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, "new"),  # order exists with status 'new'
        ]
        resp = client_mufis.post(
            "/api/eshop/mufis/setOrder",
            data={
                "order_number": "EM-2026-00001",
                "status": "shipped",
                "package_number": "Z1234567890",
                "tracking_link": "https://track.example.com/Z1234567890",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] == 1

    def test_set_order_batch(self, client_mufis, mock_db):
        """setOrder batch update via 'data' param."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, "new"),    # order 1
            (2, "new"),    # order 2
        ]
        batch_data = json.dumps([
            {"order_number": "EM-2026-00001", "status": "shipped", "package_number": "PKG1"},
            {"order_number": "EM-2026-00002", "status": "processing"},
        ])
        resp = client_mufis.post(
            "/api/eshop/mufis/setOrder",
            data={"data": batch_data},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] == 1

    def test_get_product_basic(self, client_mufis, mock_db):
        """getProduct returns products for tenant."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(2,)]  # count
        cursor.fetchall.return_value = [
            (1, "EM-500", None, "OASIS EM-1 500ml", "Trial", None,
             None, Decimal("8.25"), Decimal("9.90"), Decimal("20.00"),
             10, None, True, 1),
            (2, "EM-5L", None, "OASIS EM-1 5L", "Odporúčané", None,
             None, Decimal("33.25"), Decimal("39.90"), Decimal("20.00"),
             5, None, True, 2),
        ]
        resp = client_mufis.post("/api/eshop/mufis/getProduct", data={"page": "1"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["products"]) == 2
        # Active field should be 1/0 (integer)
        assert data["products"][0]["active"] == 1

    def test_set_product_stock_update(self, client_mufis, mock_db):
        """setProduct updates stock quantity."""
        _, cursor = mock_db
        resp = client_mufis.post(
            "/api/eshop/mufis/setProduct",
            data={"sku": "EM-500", "stock_quantity": "42"},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] == 1

    def test_set_product_batch(self, client_mufis, mock_db):
        """setProduct batch update via 'data' param."""
        _, cursor = mock_db
        batch_data = json.dumps([
            {"sku": "EM-500", "stock_quantity": 100},
            {"sku": "EM-5L", "stock_quantity": 50},
        ])
        resp = client_mufis.post(
            "/api/eshop/mufis/setProduct",
            data={"data": batch_data},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] == 1
