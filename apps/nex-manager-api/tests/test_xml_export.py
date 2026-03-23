"""Tests for XML export to SFTP directory — 4 testy.

Overuje, že save_xml_export() správne ukladá XML súbory do SFTP-accessible
adresára a že zlyhanie je non-blocking.

Tests:
  XML EXPORT (4):
    1. test_save_xml_export — basic save to tmpdir
    2. test_save_xml_export_creates_directory — auto-creates directory
    3. test_save_xml_export_failure_does_not_raise — error is logged, not raised
    4. test_callback_triggers_xml_export — PAID callback triggers XML export
"""

import os
import sys
import tempfile
from decimal import Decimal
from unittest.mock import AsyncMock, patch, MagicMock

import pytest

# Set JWT_SECRET_KEY before any app imports
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-xml-tests")

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ===========================================================================
# TEST 1 — Basic XML save
# ===========================================================================


def test_save_xml_export():
    """#1: save_xml_export writes XML file to the configured directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("eshop.router.XML_EXPORT_DIR", tmpdir):
            from eshop.router import save_xml_export

            save_xml_export("EM-2026-00001", "<order>test</order>")

            filepath = os.path.join(tmpdir, "objednavka_EM-2026-00001.xml")
            assert os.path.exists(filepath), f"Expected file at {filepath}"
            with open(filepath, "r", encoding="utf-8") as f:
                assert f.read() == "<order>test</order>"


# ===========================================================================
# TEST 2 — Auto-creates directory
# ===========================================================================


def test_save_xml_export_creates_directory():
    """#2: save_xml_export creates the export directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        nested = os.path.join(tmpdir, "sub", "dir")
        with patch("eshop.router.XML_EXPORT_DIR", nested):
            from eshop.router import save_xml_export

            save_xml_export("EM-2026-00002", "<order>nested</order>")

            filepath = os.path.join(nested, "objednavka_EM-2026-00002.xml")
            assert os.path.exists(filepath)


# ===========================================================================
# TEST 3 — Failure is non-blocking
# ===========================================================================


def test_save_xml_export_failure_does_not_raise():
    """#3: save_xml_export logs error but does NOT raise on failure."""
    with patch("eshop.router.XML_EXPORT_DIR", "/nonexistent/readonly/path"):
        with patch("eshop.router.os.makedirs", side_effect=PermissionError("denied")):
            from eshop.router import save_xml_export

            # Must NOT raise — non-blocking behavior
            save_xml_export("EM-2026-00003", "<order>fail</order>")


# ===========================================================================
# TEST 4 — PAID callback triggers XML export
# ===========================================================================


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


_CALLBACK_DATA = {
    "merchant": "12345",
    "test": "true",
    "price": "1200",
    "curr": "EUR",
    "label": "ORD-XML-001",
    "refId": "ORD-XML-001",
    "transId": "TRANS-XML-001",
    "secret": "test_secret",
    "status": "PAID",
    "email": "test@test.sk",
}


@patch("eshop.router.notify_mufis_order_change", new_callable=AsyncMock)
@patch(
    "eshop.email_service.EshopEmailService.send_order_confirmation",
    new_callable=AsyncMock,
)
@patch(
    "eshop.email_service.EshopEmailService.send_admin_new_order",
    new_callable=AsyncMock,
)
@patch(
    "eshop.email_service.EshopEmailService.send_payment_confirmation",
    new_callable=AsyncMock,
)
@patch("eshop.router.save_xml_export")
def test_callback_triggers_xml_export(
    mock_xml_export,
    mock_payment_conf,
    mock_admin_email,
    mock_order_conf,
    mock_mufis,
    payment_client,
    fake_db,
):
    """#4: PAID callback triggers save_xml_export with correct order_number."""
    # Setup DB sequence for successful PAID flow
    fake_db.set_fetchone_sequence(
        [
            # 1. Find order by refId
            (1, 1, Decimal("12.00"), "EUR", "pending", "new"),
            # 2. Load tenant to verify secrets
            (1, "12345", "test_secret"),
            # 3. Fetch tenant for email
            (
                "noreply@test.sk",
                "admin@test.sk",
                "TEST",
                "test.sk",
                "#2E7D32",
                "EUR",
                "admin@test.sk",
            ),
            # 4. Fetch order for email
            (
                "ORD-XML-001",  # order_number
                "c@test.sk",  # customer_email
                "Test Customer",  # customer_name
                Decimal("12.00"),  # total_amount_vat
                "EUR",  # currency
                "credit_card",  # payment_method
                "2026-03-21",  # created_at
                "0900111222",  # customer_phone
                "",  # company_name
                "Test Customer",  # billing_name
                "",  # billing_name2
                "Hlavná 1",  # billing_street
                "Bratislava",  # billing_city
                "81101",  # billing_zip
                "SK",  # billing_country
                "Test Customer",  # shipping_name
                "",  # shipping_name2
                "Hlavná 1",  # shipping_street
                "Bratislava",  # shipping_city
                "81101",  # shipping_zip
                "SK",  # shipping_country
                "courier",  # delivery_method
                Decimal("3.50"),  # shipping_price
                "standard",  # shipping_type
                "",  # packeta_point_id
                "",  # packeta_point_name
                "",  # note
                "",  # order_notes
                "",  # company_ico
                "",  # company_dic
                "",  # company_ic_dph
                None,  # customer_id (guest order)
            ),
        ]
    )
    fake_db.set_fetchall_sequence(
        [
            # items for email
            [("Test Product", 1, Decimal("12.00"), "SKU001", Decimal("20"), "product")],
        ]
    )

    mock_payment_conf.return_value = None
    mock_admin_email.return_value = None
    mock_order_conf.return_value = None
    mock_mufis.return_value = None

    resp = payment_client.post("/api/eshop/payment/callback", data=_CALLBACK_DATA)

    assert resp.status_code == 200
    assert resp.text == "code=0&message=OK"

    # XML export must have been called with the order number
    mock_xml_export.assert_called_once()
    call_args = mock_xml_export.call_args
    assert call_args[0][0] == "ORD-XML-001"  # order_number
    assert "<order>" in call_args[0][1] or "<?xml" in call_args[0][1]  # xml_content
