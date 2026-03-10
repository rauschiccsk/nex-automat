"""
Unit tests for NEX Manager API — ESHOP module.

Tests cover:
- Tenant resolution (X-Eshop-Token, MuFis API-KEY)
- Public product endpoints (list, detail, 404, tenant isolation, inactive filter)
- Public order endpoints (create, validation, pricing, status)
- Admin endpoints (orders CRUD, products CRUD, tenants, auth)
- MuFis endpoints (getOrder, setOrder, getProduct, setProduct)
- Comgate payment gateway (client, callback, return, order creation)

Total: ~61 tests
"""

import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

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
    "smtp_from": "noreply@emcenter.sk",
    "admin_email": "odbyt@em-1.sk",
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
    "smtp_from": "noreply@other.sk",
    "admin_email": "admin@other.sk",
}

NOW = datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

# product row: product_id, sku, name, short_description, description,
#              price, price_vat, vat_rate, stock_quantity, image_url, weight, is_active
PRODUCT_ROW_1 = (
    1,
    "EM-500",
    "OASIS EM-1 500ml",
    "Trial balenie",
    None,
    Decimal("8.25"),
    Decimal("9.90"),
    Decimal("20.00"),
    10,
    None,
    None,
    True,
)
PRODUCT_ROW_2 = (
    2,
    "EM-5L",
    "OASIS EM-1 5L",
    "Odporúčané balenie",
    None,
    Decimal("33.25"),
    Decimal("39.90"),
    Decimal("20.00"),
    5,
    None,
    None,
    True,
)
PRODUCT_ROW_INACTIVE = (
    3,
    "EM-OLD",
    "Starý produkt",
    "Neaktívny",
    None,
    Decimal("5.00"),
    Decimal("6.00"),
    Decimal("20.00"),
    0,
    None,
    None,
    False,
)

# product lookup row for order creation:
# product_id, sku, name, price, price_vat, vat_rate, is_active
PRODUCT_LOOKUP_1 = (
    1,
    "EM-500",
    "OASIS EM-1 500ml",
    Decimal("8.25"),
    Decimal("9.90"),
    Decimal("20.00"),
    True,
)
PRODUCT_LOOKUP_2 = (
    2,
    "EM-5L",
    "OASIS EM-1 5L",
    Decimal("33.25"),
    Decimal("39.90"),
    Decimal("20.00"),
    True,
)
PRODUCT_LOOKUP_INACTIVE = (
    3,
    "EM-OLD",
    "Starý produkt",
    Decimal("5.00"),
    Decimal("6.00"),
    Decimal("20.00"),
    False,
)

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
            "product_id",
            "sku",
            "name",
            "short_description",
            "description",
            "price",
            "price_vat",
            "vat_rate",
            "stock_quantity",
            "image_url",
            "weight",
            "is_active",
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
            None,  # advisory lock (no return)
            (None,),  # MAX order_number
            (42,),  # INSERT RETURNING order_id
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
            None,  # advisory lock
            (None,),  # no existing orders
            (1,),  # order_id
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
            None,  # advisory lock
            (None,),  # MAX
            (1,),  # order_id
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
            None,  # advisory lock
            (None,),  # MAX
            (1,),  # order_id
        ]
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(
                items=[
                    {"sku": "EM-500", "quantity": 1},
                    {"sku": "EM-5L", "quantity": 1},
                ]
            ),
        )
        assert resp.status_code == 200
        data = resp.json()
        # 9.90 + 39.90 = 49.80
        expected_total = float(Decimal("9.90") + Decimal("39.90"))
        assert float(data["total_amount_vat"]) == pytest.approx(
            expected_total, abs=0.01
        )

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
            "EM-2026-00001",
            "new",
            "pending",
            "",
            "",
            NOW,
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
            (
                1,
                "EM-2026-00001",
                "Test",
                "t@t.sk",
                Decimal("19.80"),
                "EUR",
                "new",
                "pending",
                NOW,
                NOW,
            ),
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
            1,
            "EM-2026-00001",
            1,
            "t@t.sk",
            "Test",
            "",
            "sk",
            "Test",
            "",
            "Testova 1",
            "BA",
            "81101",
            "SK",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            Decimal("16.50"),
            Decimal("19.80"),
            "EUR",
            "bank_transfer",
            "pending",
            None,
            "",
            Decimal("0"),
            "",
            "",
            "",
            "",
            False,
            "new",
            "",
            NOW,
            NOW,
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
            10,
            1,
            "NEW-SKU",
            None,
            "New Product",
            None,
            None,
            None,
            Decimal("10.00"),
            Decimal("12.00"),
            Decimal("20.00"),
            50,
            None,
            True,
            0,
            NOW,
            NOW,
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
            1,
            1,
            "EM-500",
            None,
            "Updated Name",
            None,
            None,
            None,
            Decimal("8.25"),
            Decimal("9.90"),
            Decimal("20.00"),
            10,
            None,
            True,
            0,
            NOW,
            NOW,
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
                (
                    1,
                    "EM-2026-00001",
                    1,
                    "t@t.sk",
                    "Test",
                    "",
                    "sk",
                    "Test",
                    "",
                    "Testova",
                    "BA",
                    "81101",
                    "SK",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    Decimal("16.50"),
                    Decimal("19.80"),
                    "EUR",
                    "bank_transfer",
                    "pending",
                    "",
                    Decimal("0"),
                    "",
                    "",
                    "",
                    "",
                    False,
                    "new",
                    "",
                    NOW,
                    NOW,
                ),
            ],
            [  # items for order 1
                (
                    "EM-500",
                    "OASIS EM-1 500ml",
                    2,
                    Decimal("8.25"),
                    Decimal("9.90"),
                    Decimal("20.00"),
                    "product",
                ),
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
            [
                (
                    1,
                    "EM-2026-00001",
                    1,
                    "t@t.sk",
                    "Test",
                    "",
                    "sk",
                    "Test",
                    "",
                    "Testova",
                    "BA",
                    "81101",
                    "SK",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    Decimal("16.50"),
                    Decimal("19.80"),
                    "EUR",
                    "bank_transfer",
                    "pending",
                    "",
                    Decimal("0"),
                    "",
                    "",
                    "",
                    "",
                    False,
                    "new",
                    "",
                    NOW,
                    NOW,
                )
            ],
            [
                (
                    "EM-500",
                    "OASIS",
                    2,
                    Decimal("8.25"),
                    Decimal("9.90"),
                    Decimal("20.00"),
                    "product",
                )
            ],
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
            [
                (
                    1,
                    "EM-2026-00001",
                    1,
                    "t@t.sk",
                    "Test",
                    "",
                    "sk",
                    "Test",
                    "",
                    "Testova",
                    "BA",
                    "81101",
                    "SK",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    Decimal("16.50"),
                    Decimal("19.80"),
                    "EUR",
                    "bank_transfer",
                    "pending",
                    "",
                    Decimal("0"),
                    "",
                    "",
                    "",
                    "",
                    False,
                    "new",
                    "",
                    NOW,
                    NOW,
                )
            ],
            [
                (
                    "EM-500",
                    "OASIS",
                    2,
                    Decimal("8.25"),
                    Decimal("9.90"),
                    Decimal("20.00"),
                    "product",
                )
            ],
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
            (
                "EM-2026-00001",
                "customer@test.sk",
                "Test",
                "Z1234567890",
                "",
            ),  # order for email (shipped)
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
            (1, "new"),  # order 1
            (
                "EM-2026-00001",
                "customer@test.sk",
                "Test",
                "PKG1",
                "",
            ),  # order for email (shipped)
            (2, "new"),  # order 2
        ]
        batch_data = json.dumps(
            [
                {
                    "order_number": "EM-2026-00001",
                    "status": "shipped",
                    "package_number": "PKG1",
                },
                {"order_number": "EM-2026-00002", "status": "processing"},
            ]
        )
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
            (
                1,
                "EM-500",
                None,
                "OASIS EM-1 500ml",
                "Trial",
                None,
                None,
                Decimal("8.25"),
                Decimal("9.90"),
                Decimal("20.00"),
                10,
                None,
                True,
                1,
            ),
            (
                2,
                "EM-5L",
                None,
                "OASIS EM-1 5L",
                "Odporúčané",
                None,
                None,
                Decimal("33.25"),
                Decimal("39.90"),
                Decimal("20.00"),
                5,
                None,
                True,
                2,
            ),
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
        batch_data = json.dumps(
            [
                {"sku": "EM-500", "stock_quantity": 100},
                {"sku": "EM-5L", "stock_quantity": 50},
            ]
        )
        resp = client_mufis.post(
            "/api/eshop/mufis/setProduct",
            data={"data": batch_data},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] == 1


# ============================================================================
# COMGATE — Client Unit Tests (6 tests)
# ============================================================================

from eshop.comgate import ComgateClient, ComgateError, get_comgate_client


FAKE_TENANT_COMGATE = {
    **FAKE_TENANT,
    "comgate_merchant_id": "12345",
    "comgate_secret": "supersecretkey",
    "comgate_test_mode": True,
}

FAKE_TENANT_NO_COMGATE = {
    **FAKE_TENANT,
}


class TestComgateClient:
    """ComgateClient unit tests — mock HTTP calls, no real requests."""

    def test_create_payment_request_body(self):
        """create_payment constructs correct request body with all parameters."""
        client = ComgateClient(merchant_id="12345", secret="testsecret", test_mode=True)
        captured_data = {}

        def mock_post_sync(endpoint, data):
            captured_data.update(data)
            return {
                "code": "0",
                "message": "OK",
                "transId": "AB12-CD34-EF56",
                "redirect": "https://payments.comgate.cz/client/pay/AB12-CD34-EF56",
            }

        client._post_sync = mock_post_sync
        import asyncio

        asyncio.get_event_loop().run_until_complete(
            client.create_payment(
                price_cents=3990,
                currency="EUR",
                order_number="EM-2026-00001",
                customer_email="test@test.sk",
                label="EM Center",
                country="SK",
                lang="sk",
            )
        )
        assert captured_data["merchant"] == "12345"
        assert captured_data["test"] == "true"
        assert captured_data["price"] == 3990
        assert captured_data["curr"] == "EUR"
        assert captured_data["refId"] == "EM-2026-00001"
        assert captured_data["email"] == "test@test.sk"
        assert captured_data["method"] == "ALL"
        assert captured_data["prepareOnly"] == "true"
        assert captured_data["secret"] == "testsecret"
        assert captured_data["country"] == "SK"
        assert captured_data["lang"] == "sk"

    def test_create_payment_parses_success(self):
        """create_payment correctly parses successful response."""
        client = ComgateClient(merchant_id="12345", secret="testsecret", test_mode=True)

        def mock_post_sync(endpoint, data):
            return {
                "code": "0",
                "message": "OK",
                "transId": "AB12-CD34-EF56",
                "redirect": "https://payments.comgate.cz/client/pay/AB12-CD34-EF56",
            }

        client._post_sync = mock_post_sync
        import asyncio

        result = asyncio.get_event_loop().run_until_complete(
            client.create_payment(
                price_cents=3990,
                currency="EUR",
                order_number="EM-2026-00001",
                customer_email="test@test.sk",
                label="EM Center",
                country="SK",
                lang="sk",
            )
        )
        assert result["transId"] == "AB12-CD34-EF56"
        assert "redirect_url" in result
        assert "comgate.cz" in result["redirect_url"]

    def test_create_payment_handles_error(self):
        """create_payment raises ComgateError on error response."""
        client = ComgateClient(merchant_id="12345", secret="testsecret", test_mode=True)

        def mock_post_sync(endpoint, data):
            return {"code": "1101", "message": "invalid merchant"}

        client._post_sync = mock_post_sync
        import asyncio

        with pytest.raises(ComgateError) as exc_info:
            asyncio.get_event_loop().run_until_complete(
                client.create_payment(
                    price_cents=3990,
                    currency="EUR",
                    order_number="EM-2026-00001",
                    customer_email="test@test.sk",
                    label="EM Center",
                    country="SK",
                    lang="sk",
                )
            )
        assert exc_info.value.code == 1101
        assert "invalid merchant" in exc_info.value.message

    def test_verify_callback_valid_secret(self):
        """verify_callback returns True for matching secret."""
        client = ComgateClient(
            merchant_id="12345", secret="supersecretkey", test_mode=True
        )
        import asyncio

        result = asyncio.get_event_loop().run_until_complete(
            client.verify_callback(
                merchant="12345",
                test="true",
                price="3990",
                curr="EUR",
                label="EM Center",
                refId="EM-2026-00001",
                transId="AB12-CD34-EF56",
                secret="supersecretkey",
                email="test@test.sk",
                status="PAID",
            )
        )
        assert result is True

    def test_verify_callback_invalid_secret(self):
        """verify_callback returns False for wrong secret."""
        client = ComgateClient(
            merchant_id="12345", secret="supersecretkey", test_mode=True
        )
        import asyncio

        result = asyncio.get_event_loop().run_until_complete(
            client.verify_callback(
                merchant="12345",
                test="true",
                price="3990",
                curr="EUR",
                label="EM Center",
                refId="EM-2026-00001",
                transId="AB12-CD34-EF56",
                secret="wrongsecret",
                email="test@test.sk",
                status="PAID",
            )
        )
        assert result is False

    def test_price_conversion_cents(self):
        """EUR amounts convert to cents correctly using Decimal."""
        # 39.90 EUR → 3990 cents
        assert int(Decimal("39.90") * 100) == 3990
        # 9.90 EUR → 990 cents
        assert int(Decimal("9.90") * 100) == 990
        # 0.01 EUR → 1 cent
        assert int(Decimal("0.01") * 100) == 1
        # 100.00 EUR → 10000 cents
        assert int(Decimal("100.00") * 100) == 10000
        # Verify float would be wrong (classic floating-point issue)
        # Decimal handles this correctly
        assert int(Decimal("19.80") * 100) == 1980


# ============================================================================
# COMGATE — Helper Function Tests (2 tests)
# ============================================================================


class TestComgateHelper:
    """get_comgate_client helper tests."""

    def test_get_client_configured(self):
        """Returns ComgateClient when credentials configured."""
        client = get_comgate_client(FAKE_TENANT_COMGATE)
        assert client is not None
        assert client.merchant_id == "12345"
        assert client.secret == "supersecretkey"
        assert client.test_mode is True

    def test_get_client_not_configured(self):
        """Returns None when Comgate not configured."""
        client = get_comgate_client(FAKE_TENANT_NO_COMGATE)
        assert client is None


# ============================================================================
# COMGATE — Payment Callback Integration Tests (8 tests)
# ============================================================================


@pytest.fixture()
def client_no_auth(mock_db):
    """TestClient with mocked DB but NO auth — for payment endpoints."""
    conn, _ = mock_db
    app.dependency_overrides[get_db] = lambda: conn
    yield TestClient(app)
    app.dependency_overrides.clear()


def _callback_data(**overrides):
    """Create valid Comgate callback POST data."""
    base = {
        "merchant": "12345",
        "test": "true",
        "price": "1980",
        "curr": "EUR",
        "label": "EM Center",
        "refId": "EM-2026-00001",
        "transId": "AB12-CD34-EF56",
        "secret": "supersecretkey",
        "email": "test@test.sk",
        "status": "PAID",
    }
    base.update(overrides)
    return base


class TestPaymentCallback:
    """POST /api/eshop/payment/callback tests."""

    def test_paid_callback_updates_order(self, client_no_auth, mock_db):
        """Valid PAID callback updates order payment_status to paid."""
        _, cursor = mock_db
        # 1. Find order by refId
        # 2. Find tenant by tenant_id
        cursor.fetchone.side_effect = [
            # order: order_id, tenant_id, total_amount_vat, currency, payment_status, status
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            # tenant: tenant_id, comgate_merchant_id, comgate_secret
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(),
        )
        assert resp.status_code == 200
        assert resp.text == "code=0&message=OK"
        # Verify UPDATE was called with payment_status = 'paid'
        calls = [str(c) for c in cursor.execute.call_args_list]
        paid_calls = [c for c in calls if "payment_status = 'paid'" in c]
        assert len(paid_calls) >= 1

    def test_paid_callback_saves_transaction_id(self, client_no_auth, mock_db):
        """Valid PAID callback stores comgate_transaction_id."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(),
        )
        assert resp.status_code == 200
        calls = [str(c) for c in cursor.execute.call_args_list]
        trans_calls = [c for c in calls if "comgate_transaction_id" in c]
        assert len(trans_calls) >= 1

    def test_paid_callback_creates_status_history(self, client_no_auth, mock_db):
        """PAID callback creates status history entry."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(),
        )
        assert resp.status_code == 200
        calls = [str(c) for c in cursor.execute.call_args_list]
        history_calls = [c for c in calls if "eshop_order_status_history" in c]
        assert len(history_calls) >= 1

    def test_cancelled_callback_updates_payment_status(self, client_no_auth, mock_db):
        """CANCELLED callback updates payment_status to failed."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(status="CANCELLED"),
        )
        assert resp.status_code == 200
        assert resp.text == "code=0&message=OK"
        calls = [str(c) for c in cursor.execute.call_args_list]
        failed_calls = [c for c in calls if "payment_status = 'failed'" in c]
        assert len(failed_calls) >= 1

    def test_invalid_secret_rejected(self, client_no_auth, mock_db):
        """Invalid secret is rejected (logged) but still returns 200."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(secret="wrongsecret"),
        )
        assert resp.status_code == 200
        assert resp.text == "code=0&message=OK"
        # No UPDATE should have been called for payment_status
        calls = [str(c) for c in cursor.execute.call_args_list]
        paid_calls = [c for c in calls if "payment_status = 'paid'" in c]
        assert len(paid_calls) == 0

    def test_price_mismatch_rejected(self, client_no_auth, mock_db):
        """Price mismatch is rejected but returns 200."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(price="9999"),  # Wrong price
        )
        assert resp.status_code == 200
        assert resp.text == "code=0&message=OK"
        calls = [str(c) for c in cursor.execute.call_args_list]
        paid_calls = [c for c in calls if "payment_status = 'paid'" in c]
        assert len(paid_calls) == 0

    def test_nonexistent_order_returns_200(self, client_no_auth, mock_db):
        """Non-existent refId still returns 200 (Comgate requirement)."""
        _, cursor = mock_db
        cursor.fetchone.return_value = None  # order not found
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(refId="NONEXISTENT"),
        )
        assert resp.status_code == 200
        assert resp.text == "code=0&message=OK"

    def test_duplicate_paid_callback_idempotent(self, client_no_auth, mock_db):
        """Already-paid order stays paid on duplicate callback."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            # Order already has payment_status='paid'
            (1, 1, Decimal("19.80"), "EUR", "paid", "paid"),
            (1, "12345", "supersecretkey"),
        ]
        resp = client_no_auth.post(
            "/api/eshop/payment/callback",
            data=_callback_data(),
        )
        assert resp.status_code == 200
        assert resp.text == "code=0&message=OK"
        # No UPDATE should have been called — idempotent
        calls = [str(c) for c in cursor.execute.call_args_list]
        update_calls = [c for c in calls if "UPDATE" in c]
        assert len(update_calls) == 0


# ============================================================================
# COMGATE — Payment Return Tests (3 tests)
# ============================================================================


class TestPaymentReturn:
    """GET /api/eshop/payment/return tests."""

    def test_valid_transaction_returns_status(self, client_no_auth, mock_db):
        """Valid transId returns order status."""
        _, cursor = mock_db
        cursor.fetchone.return_value = ("EM-2026-00001", "paid", "paid")
        resp = client_no_auth.get("/api/eshop/payment/return?id=AB12-CD34-EF56")
        assert resp.status_code == 200
        data = resp.json()
        assert data["order_number"] == "EM-2026-00001"
        assert data["status"] == "paid"
        assert data["payment_status"] == "paid"

    def test_nonexistent_transaction_returns_404(self, client_no_auth, mock_db):
        """Non-existent transId returns 404."""
        _, cursor = mock_db
        cursor.fetchone.return_value = None
        resp = client_no_auth.get("/api/eshop/payment/return?id=NONEXISTENT")
        assert resp.status_code == 404

    def test_response_format(self, client_no_auth, mock_db):
        """Response contains required fields."""
        _, cursor = mock_db
        cursor.fetchone.return_value = ("EM-2026-00001", "new", "pending")
        resp = client_no_auth.get("/api/eshop/payment/return?id=AB12-CD34-EF56")
        assert resp.status_code == 200
        data = resp.json()
        assert "order_number" in data
        assert "status" in data
        assert "payment_status" in data


# ============================================================================
# COMGATE — Order Creation with Payment Tests (3 tests)
# ============================================================================


class TestOrderCreationWithPayment:
    """POST /api/eshop/orders — Comgate integration tests."""

    def test_order_with_payment_url(self, mock_db):
        """Order creation returns payment_url when Comgate configured."""
        conn, cursor = mock_db

        # Override tenant to include Comgate credentials
        app.dependency_overrides[get_db] = lambda: conn
        app.dependency_overrides[get_tenant_by_token] = lambda: FAKE_TENANT_COMGATE

        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,  # product lookup
            None,  # advisory lock
            (None,),  # MAX order_number
            (42,),  # INSERT RETURNING order_id
        ]

        with patch("eshop.comgate.ComgateClient.create_payment") as mock_payment:
            mock_payment.return_value = {
                "transId": "AB12-CD34-EF56",
                "redirect_url": "https://payments.comgate.cz/client/pay/AB12",
            }
            client = TestClient(app)
            resp = client.post("/api/eshop/orders", json=_order_body())

        assert resp.status_code == 200
        data = resp.json()
        assert data["payment_url"] == ("https://payments.comgate.cz/client/pay/AB12")
        assert data["order_number"] is not None

        app.dependency_overrides.clear()

    def test_order_without_comgate(self, client_public, mock_db):
        """Order creation works without payment_url when Comgate not configured."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,  # advisory lock
            (None,),  # MAX order_number
            (42,),  # INSERT RETURNING order_id
        ]
        resp = client_public.post("/api/eshop/orders", json=_order_body())
        assert resp.status_code == 200
        data = resp.json()
        assert data["payment_url"] is None
        assert data["status"] == "new"

    def test_comgate_transaction_id_stored(self, mock_db):
        """Comgate transaction ID is stored in order."""
        conn, cursor = mock_db

        app.dependency_overrides[get_db] = lambda: conn
        app.dependency_overrides[get_tenant_by_token] = lambda: FAKE_TENANT_COMGATE

        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,  # advisory lock
            (None,),  # MAX order_number
            (42,),  # INSERT RETURNING order_id
        ]

        with patch("eshop.comgate.ComgateClient.create_payment") as mock_payment:
            mock_payment.return_value = {
                "transId": "AB12-CD34-EF56",
                "redirect_url": "https://payments.comgate.cz/client/pay/AB12",
            }
            client = TestClient(app)
            resp = client.post("/api/eshop/orders", json=_order_body())

        assert resp.status_code == 200
        # Verify UPDATE with comgate_transaction_id was called
        calls = [str(c) for c in cursor.execute.call_args_list]
        trans_calls = [c for c in calls if "comgate_transaction_id" in c]
        assert len(trans_calls) >= 1

        app.dependency_overrides.clear()


# ============================================================================
# EMAIL SERVICE — Unit Tests (10 tests)
# ============================================================================

import asyncio

from eshop.email_service import EshopEmailService

FAKE_TENANT_EMAIL = {
    "smtp_from": "noreply@emcenter.sk",
    "admin_email": "odbyt@em-1.sk",
    "brand_name": "EM Center",
    "domain": "emcenter.sk",
    "primary_color": "#2E7D32",
}

FAKE_TENANT_NO_SMTP = {
    "smtp_from": "",
    "admin_email": "admin@test.sk",
    "brand_name": "Test",
    "domain": "test.sk",
    "primary_color": "#000000",
}

SAMPLE_ORDER = {
    "order_number": "EM-2026-00001",
    "customer_email": "customer@test.sk",
    "customer_name": "Ján Tester",
    "customer_phone": "+421900000000",
    "billing_name": "Ján Tester",
    "billing_street": "Testová 1",
    "billing_city": "Bratislava",
    "billing_zip": "81101",
    "billing_country": "SK",
    "shipping_name": "Ján Tester",
    "shipping_street": "Testová 1",
    "shipping_city": "Bratislava",
    "shipping_zip": "81101",
    "shipping_country": "SK",
    "total_amount_vat": 19.80,
    "currency": "EUR",
    "payment_method": "bank_transfer",
    "note": "",
    "tracking_number": "Z1234567890",
    "tracking_link": "https://track.example.com/Z1234567890",
    "comgate_transaction_id": "AB12-CD34-EF56",
}

SAMPLE_ITEMS = [
    {"name": "OASIS EM-1 500ml", "quantity": 2, "unit_price_vat": 9.90},
    {"name": "OASIS EM-1 5L", "quantity": 1, "unit_price_vat": 39.90},
]


class TestEshopEmailService:
    """EshopEmailService unit tests — SMTP is always mocked."""

    def test_email_order_confirmation_html(self):
        """Order confirmation HTML contains order_number, customer_name, items."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["to"] = to
            captured["subject"] = subject
            captured["html"] = html_body

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_order_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert "EM-2026-00001" in captured["html"]
        assert "Tester" in captured["html"]
        assert "OASIS EM-1 500ml" in captured["html"]
        assert captured["to"] == "customer@test.sk"

    def test_email_payment_confirmation_html(self):
        """Payment confirmation HTML contains order_number and total."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["html"] = html_body

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_payment_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert "EM-2026-00001" in captured["html"]
        assert "19.80" in captured["html"]

    def test_email_shipping_notification_html(self):
        """Shipping notification HTML contains tracking_link."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["html"] = html_body

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_shipping_notification(SAMPLE_ORDER)
        )
        assert "https://track.example.com/Z1234567890" in captured["html"]
        assert "Z1234567890" in captured["html"]

    def test_email_admin_new_order_sent_to_admin(self):
        """Admin new order email is sent to admin_email."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["to"] = to

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_admin_new_order(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert captured["to"] == "odbyt@em-1.sk"

    def test_email_admin_payment_failed_sent_to_admin(self):
        """Admin payment failed email is sent to admin_email."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["to"] = to

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_admin_payment_failed(SAMPLE_ORDER)
        )
        assert captured["to"] == "odbyt@em-1.sk"

    def test_email_subject_contains_order_number(self):
        """Email subjects contain order_number."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["subject"] = subject

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_order_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert "EM-2026-00001" in captured["subject"]

    def test_email_from_contains_brand_and_sender(self):
        """From header contains brand_name and smtp_from."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def capture_send(to, subject, html_body):
            # Build msg to check From header
            from email.mime.multipart import MIMEMultipart as MM

            msg = MM("alternative")
            msg["From"] = f"{svc.brand_name} <{svc.sender}>"
            captured["from"] = msg["From"]

        svc._send_email = capture_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_order_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert "EM Center" in captured["from"]
        assert "noreply@emcenter.sk" in captured["from"]

    def test_email_html_contains_all_items(self):
        """All order items appear in HTML."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)
        captured = {}

        async def mock_send(to, subject, html_body):
            captured["html"] = html_body

        svc._send_email = mock_send
        asyncio.get_event_loop().run_until_complete(
            svc.send_order_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert "OASIS EM-1 500ml" in captured["html"]
        assert "OASIS EM-1 5L" in captured["html"]

    def test_email_smtp_failure_logged_not_raised(self):
        """SMTP exception is logged, not raised."""
        svc = EshopEmailService(FAKE_TENANT_EMAIL)

        with patch("eshop.email_service.smtplib.SMTP") as mock_smtp:
            mock_smtp.return_value.__enter__ = MagicMock()
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
            mock_smtp.return_value.__enter__.return_value.send_message.side_effect = (
                ConnectionRefusedError("Connection refused")
            )
            # Should NOT raise
            asyncio.get_event_loop().run_until_complete(
                svc.send_order_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
            )

    def test_email_skip_when_no_sender(self):
        """Email is skipped when smtp_from is empty."""
        svc = EshopEmailService(FAKE_TENANT_NO_SMTP)
        send_called = {"called": False}

        def spy_send_sync(msg, to):
            send_called["called"] = True

        svc._send_sync = spy_send_sync
        asyncio.get_event_loop().run_until_complete(
            svc.send_order_confirmation(SAMPLE_ORDER, SAMPLE_ITEMS)
        )
        assert send_called["called"] is False


# ============================================================================
# EMAIL — Integration Tests (4 tests)
# ============================================================================


class TestEmailIntegration:
    """Integration tests — verify email service is called from endpoints."""

    def test_order_creation_triggers_two_emails(self, client_public, mock_db):
        """Order creation calls send_order_confirmation + send_admin_new_order."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,  # advisory lock
            (None,),  # MAX order_number
            (42,),  # INSERT RETURNING order_id
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_order_confirmation = AsyncMock()
            instance.send_admin_new_order = AsyncMock()
            resp = client_public.post("/api/eshop/orders", json=_order_body())

        assert resp.status_code == 200
        instance.send_order_confirmation.assert_called_once()
        instance.send_admin_new_order.assert_called_once()

    def test_payment_callback_paid_triggers_email(self, client_no_auth, mock_db):
        """PAID callback calls send_payment_confirmation."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            # order lookup
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            # tenant for secret verification
            (1, "12345", "supersecretkey"),
            # tenant for email
            (
                "noreply@emcenter.sk",
                "odbyt@em-1.sk",
                "EM Center",
                "emcenter.sk",
                "#2E7D32",
                "EUR",
            ),
            # order for email
            (
                "EM-2026-00001",
                "customer@test.sk",
                "Test",
                Decimal("19.80"),
                "EUR",
                "bank_transfer",
            ),
        ]
        cursor.fetchall.return_value = [
            ("OASIS EM-1 500ml", 2, Decimal("9.90")),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_payment_confirmation = AsyncMock()
            resp = client_no_auth.post(
                "/api/eshop/payment/callback",
                data=_callback_data(),
            )

        assert resp.status_code == 200
        instance.send_payment_confirmation.assert_called_once()

    def test_payment_callback_cancelled_triggers_admin_email(
        self, client_no_auth, mock_db
    ):
        """CANCELLED callback calls send_admin_payment_failed."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, 1, Decimal("19.80"), "EUR", "pending", "new"),
            (1, "12345", "supersecretkey"),
            # tenant for email
            (
                "noreply@emcenter.sk",
                "odbyt@em-1.sk",
                "EM Center",
                "emcenter.sk",
                "#2E7D32",
                "EUR",
            ),
            # order for email
            (
                "EM-2026-00001",
                "customer@test.sk",
                "Test",
                Decimal("19.80"),
                "EUR",
                "bank_transfer",
                "AB12-CD34-EF56",
            ),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_admin_payment_failed = AsyncMock()
            resp = client_no_auth.post(
                "/api/eshop/payment/callback",
                data=_callback_data(status="CANCELLED"),
            )

        assert resp.status_code == 200
        instance.send_admin_payment_failed.assert_called_once()

    def test_mufis_setorder_shipped_triggers_email(self, client_mufis, mock_db):
        """MuFis setOrder with status=shipped triggers send_shipping_notification."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1, "new"),  # order exists
            # order for email
            (
                "EM-2026-00001",
                "customer@test.sk",
                "Test",
                "Z123",
                "https://track.example.com/Z123",
            ),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_shipping_notification = AsyncMock()
            resp = client_mufis.post(
                "/api/eshop/mufis/setOrder",
                data={
                    "order_number": "EM-2026-00001",
                    "status": "shipped",
                    "package_number": "Z123",
                    "tracking_link": "https://track.example.com/Z123",
                },
            )

        assert resp.status_code == 200
        instance.send_shipping_notification.assert_called_once()


# ============================================================================
# LEAD CAPTURE — Registration Tests (8 tests)
# ============================================================================


LEAD_BODY = {
    "email": "lead@test.sk",
    "first_name": "Ján",
    "last_name": "Testovič",
    "phone": "+421900111222",
    "gdpr_consent": True,
}

# lead insert returning: lead_id, expires_at
LEAD_INSERT_RETURN = (
    1,
    datetime(2026, 4, 15, 10, 0, 0, tzinfo=timezone.utc),
)


class TestLeadRegistration:
    """POST /api/eshop/leads tests."""

    def test_register_lead_success(self, client_public, mock_db):
        """Successful lead registration returns 201 with discount code."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            None,  # duplicate check — no existing lead
            None,  # discount code uniqueness check
            LEAD_INSERT_RETURN,  # INSERT RETURNING
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_lead_welcome_email = AsyncMock()
            resp = client_public.post("/api/eshop/leads", json=LEAD_BODY)

        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "lead@test.sk"
        assert data["discount_code"].startswith("OASIS-")
        assert len(data["discount_code"]) == 14  # OASIS- + 8 hex chars
        assert data["discount_percentage"] == 50.0
        assert data["lead_id"] == 1

    def test_register_lead_duplicate_email_409(self, client_public, mock_db):
        """Duplicate email for same tenant returns 409."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            (1,),  # duplicate check — existing lead found
        ]
        resp = client_public.post("/api/eshop/leads", json=LEAD_BODY)
        assert resp.status_code == 409
        assert "zaregistrovaný" in resp.json()["detail"]

    def test_register_lead_same_email_different_tenant_ok(self, mock_db):
        """Same email for different tenant returns 201."""
        conn, cursor = mock_db

        app.dependency_overrides[get_db] = lambda: conn
        app.dependency_overrides[get_tenant_by_token] = lambda: FAKE_TENANT_2

        cursor.fetchone.side_effect = [
            None,  # duplicate check — no existing lead for tenant 2
            None,  # discount code uniqueness check
            LEAD_INSERT_RETURN,  # INSERT RETURNING
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_lead_welcome_email = AsyncMock()
            client = TestClient(app)
            resp = client.post("/api/eshop/leads", json=LEAD_BODY)

        assert resp.status_code == 201
        app.dependency_overrides.clear()

    def test_register_lead_without_gdpr_400(self, client_public, mock_db):
        """GDPR consent false returns 400."""
        resp = client_public.post(
            "/api/eshop/leads",
            json={**LEAD_BODY, "gdpr_consent": False},
        )
        assert resp.status_code == 400
        assert "GDPR" in resp.json()["detail"]

    def test_register_lead_invalid_email_422(self, client_public, mock_db):
        """Invalid email format returns 422."""
        resp = client_public.post(
            "/api/eshop/leads",
            json={**LEAD_BODY, "email": "not-an-email"},
        )
        assert resp.status_code == 422

    def test_register_lead_empty_email_422(self, client_public, mock_db):
        """Empty email returns 422."""
        resp = client_public.post(
            "/api/eshop/leads",
            json={**LEAD_BODY, "email": ""},
        )
        assert resp.status_code == 422

    def test_two_registrations_different_codes(self, client_public, mock_db):
        """Two registrations generate different discount codes."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            None, None, LEAD_INSERT_RETURN,  # first registration
            None, None, (2, datetime(2026, 4, 15, 10, 0, 0, tzinfo=timezone.utc)),
        ]

        codes = []
        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_lead_welcome_email = AsyncMock()
            for email in ["lead1@test.sk", "lead2@test.sk"]:
                resp = client_public.post(
                    "/api/eshop/leads",
                    json={**LEAD_BODY, "email": email},
                )
                assert resp.status_code == 201
                codes.append(resp.json()["discount_code"])

        assert codes[0] != codes[1]

    def test_welcome_email_called(self, client_public, mock_db):
        """Welcome email is sent on successful registration."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            None,  # duplicate check
            None,  # code uniqueness check
            LEAD_INSERT_RETURN,  # INSERT RETURNING
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_lead_welcome_email = AsyncMock()
            resp = client_public.post("/api/eshop/leads", json=LEAD_BODY)

        assert resp.status_code == 201
        instance.send_lead_welcome_email.assert_called_once()


# ============================================================================
# LEAD CAPTURE — Discount Validation Tests (5 tests)
# ============================================================================


class TestDiscountValidation:
    """GET /api/eshop/leads/validate/{code} tests."""

    def test_valid_code(self, client_public, mock_db):
        """Valid active code returns valid=true with 50% discount."""
        _, cursor = mock_db
        cursor.fetchone.return_value = (
            Decimal("50.00"),  # discount_percentage
            datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),  # expires_at (future)
            True,  # is_active
            None,  # first_order_id (not used yet)
        )
        resp = client_public.get("/api/eshop/leads/validate/OASIS-ABCD1234")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is True
        assert data["discount_percentage"] == 50.0
        assert data["message"] == "Kód je platný"

    def test_nonexistent_code(self, client_public, mock_db):
        """Non-existent code returns valid=false."""
        _, cursor = mock_db
        cursor.fetchone.return_value = None
        resp = client_public.get("/api/eshop/leads/validate/FAKE-CODE-1234")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is False
        assert "Neplatný" in data["message"]

    def test_expired_code(self, client_public, mock_db):
        """Expired code returns valid=false with expiration message."""
        _, cursor = mock_db
        cursor.fetchone.return_value = (
            Decimal("50.00"),
            datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # past date
            True,
            None,
        )
        resp = client_public.get("/api/eshop/leads/validate/OASIS-EXPIRED1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is False
        assert "expiroval" in data["message"]

    def test_already_used_code(self, client_public, mock_db):
        """Already-used code (first_order_id set) returns valid=false."""
        _, cursor = mock_db
        cursor.fetchone.return_value = (
            Decimal("50.00"),
            datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),
            True,
            42,  # first_order_id — already used
        )
        resp = client_public.get("/api/eshop/leads/validate/OASIS-USED1234")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is False
        assert "použitý" in data["message"]

    def test_deactivated_code(self, client_public, mock_db):
        """Deactivated lead (is_active=false) returns valid=false."""
        _, cursor = mock_db
        cursor.fetchone.return_value = (
            Decimal("50.00"),
            datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),
            False,  # is_active = false
            None,
        )
        resp = client_public.get("/api/eshop/leads/validate/OASIS-DEAD1234")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is False
        assert "aktívny" in data["message"]


# ============================================================================
# LEAD CAPTURE — Discount in Order Tests (6 tests)
# ============================================================================


class TestDiscountInOrder:
    """POST /api/eshop/orders with discount_code tests."""

    def test_order_with_valid_discount_reduces_price(self, client_public, mock_db):
        """Order with valid discount code reduces total by 50%."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,  # product lookup EM-500
            None,  # MAX order_number (row=None → seq=1)
            (42,),  # INSERT RETURNING order_id
            # discount code validation — lead row
            (
                1,  # lead_id
                Decimal("50.00"),  # discount_percentage
                datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),  # expires_at
                True,  # is_active
                None,  # first_order_id
            ),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_order_confirmation = AsyncMock()
            instance.send_admin_new_order = AsyncMock()
            resp = client_public.post(
                "/api/eshop/orders",
                json=_order_body(discount_code="OASIS-ABCD1234"),
            )

        assert resp.status_code == 200
        data = resp.json()
        # Original: 2 * 9.90 = 19.80, discount 50% = 9.90, total = 9.90
        assert float(data["total_amount_vat"]) == pytest.approx(9.90, abs=0.01)

    def test_order_with_invalid_discount_400(self, client_public, mock_db):
        """Order with non-existent discount code returns 400."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,  # product lookup
            None,  # MAX order_number
            (42,),  # INSERT RETURNING order_id
            None,  # discount code lookup — not found
        ]
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(discount_code="FAKE-CODE-1234"),
        )
        assert resp.status_code == 400
        assert "Neplatný" in resp.json()["detail"]

    def test_order_with_expired_discount_400(self, client_public, mock_db):
        """Order with expired discount code returns 400."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,  # MAX order_number
            (42,),  # INSERT RETURNING order_id
            (
                1,
                Decimal("50.00"),
                datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # expired
                True,
                None,
            ),
        ]
        resp = client_public.post(
            "/api/eshop/orders",
            json=_order_body(discount_code="OASIS-EXPIRED1"),
        )
        assert resp.status_code == 400
        assert "expiroval" in resp.json()["detail"]

    def test_order_without_discount_full_price(self, client_public, mock_db):
        """Order without discount code pays full price (backward compatible)."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,
            (None,),
            (42,),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_order_confirmation = AsyncMock()
            instance.send_admin_new_order = AsyncMock()
            resp = client_public.post("/api/eshop/orders", json=_order_body())

        assert resp.status_code == 200
        data = resp.json()
        # 2 * 9.90 = 19.80, no discount
        assert float(data["total_amount_vat"]) == pytest.approx(19.80, abs=0.01)

    def test_discount_item_in_order_items(self, client_public, mock_db):
        """Discount creates order item with negative price and item_type='discount'."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,  # MAX order_number
            (42,),  # INSERT RETURNING order_id
            (
                1,
                Decimal("50.00"),
                datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),
                True,
                None,
            ),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_order_confirmation = AsyncMock()
            instance.send_admin_new_order = AsyncMock()
            resp = client_public.post(
                "/api/eshop/orders",
                json=_order_body(discount_code="OASIS-ABCD1234"),
            )

        assert resp.status_code == 200
        # Find the discount item insert call
        calls = [str(c) for c in cursor.execute.call_args_list]
        discount_calls = [c for c in calls if "'discount'" in c]
        assert len(discount_calls) >= 1
        # Verify negative price in call args
        negative_price_calls = [c for c in calls if "-9.9" in c]
        assert len(negative_price_calls) >= 1

    def test_lead_first_order_id_set_after_order(self, client_public, mock_db):
        """Lead.first_order_id is updated after successful order."""
        _, cursor = mock_db
        cursor.fetchone.side_effect = [
            PRODUCT_LOOKUP_1,
            None,  # MAX order_number
            (42,),  # INSERT RETURNING order_id = 42
            (
                1,
                Decimal("50.00"),
                datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),
                True,
                None,
            ),
        ]

        with patch("eshop.router.EshopEmailService") as MockEmailSvc:
            instance = MockEmailSvc.return_value
            instance.send_order_confirmation = AsyncMock()
            instance.send_admin_new_order = AsyncMock()
            resp = client_public.post(
                "/api/eshop/orders",
                json=_order_body(discount_code="OASIS-ABCD1234"),
            )

        assert resp.status_code == 200
        # Verify UPDATE eshop_leads SET first_order_id was called
        calls = [str(c) for c in cursor.execute.call_args_list]
        lead_update_calls = [
            c for c in calls if "eshop_leads" in c and "first_order_id" in c
        ]
        assert len(lead_update_calls) >= 1
