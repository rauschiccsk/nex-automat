"""Unit testy pre shipping order item creation + XML export.

Tests:
  1. test_xml_no_duplicate_shipping — shipping item not duplicated in XML
  2. test_xml_shipping_correct_plu_courier — courier PLU = 304
  3. test_xml_shipping_correct_plu_packeta — packeta PLU = 303
  4. test_xml_no_shipping_when_price_zero — no shipping in XML when price = 0
  5. test_xml_shipping_skips_shipping_sku_in_items — SHIPPING SKU items skipped in loop
"""

import os
import sys
from xml.etree.ElementTree import fromstring

# Add app root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from eshop.email_service import EshopEmailService


def _make_service():
    """Create EshopEmailService with minimal tenant config."""
    tenant = {
        "admin_notification_email": "admin@test.com",
        "smtp_host": "localhost",
        "smtp_port": 587,
        "smtp_user": "test",
        "smtp_password": "test",
        "smtp_from": "test@test.com",
        "brand_name": "TestBrand",
    }
    return EshopEmailService(tenant)


def _make_order(**overrides):
    """Create minimal order dict for XML generation."""
    base = {
        "order_number": "EM-2026-99999",
        "customer_name": "Test Customer",
        "customer_email": "test@test.com",
        "customer_phone": "+421900000000",
        "billing_name": "Test",
        "billing_street": "Test 1",
        "billing_city": "Bratislava",
        "billing_zip": "81101",
        "billing_country": "SK",
        "shipping_name": "",
        "shipping_name2": "",
        "shipping_street": "",
        "shipping_city": "",
        "shipping_zip": "",
        "shipping_country": "",
        "payment_method": "CARD",
        "total_amount_vat": 13.40,
        "shipping_price": 3.50,
        "delivery_method": "courier",
        "packeta_point_id": "",
        "packeta_point_name": "",
        "delivery_point_group": "",
        "delivery_point_id": "",
        "created_at": "2026-03-20 12:00:00",
    }
    base.update(overrides)
    return base


def _make_items():
    """Create product items (no shipping item)."""
    return [
        {
            "sku": "EM-500",
            "name": "Oasis EM-1 - 500ml",
            "quantity": 1,
            "unit_price_vat": 9.90,
            "vat_rate": 23,
        }
    ]


# ---------------------------------------------------------------------------
# Test 1: No duplicate shipping items in XML
# ---------------------------------------------------------------------------


def test_xml_no_duplicate_shipping():
    """Shipping item must appear exactly once in XML (not duplicated)."""
    svc = _make_service()
    order = _make_order(shipping_price=3.50, delivery_method="courier")
    items = _make_items()

    xml_str = svc._generate_order_xml(order, items)
    root = fromstring(xml_str)

    shipping_items = [
        i for i in root.findall(".//item") if i.findtext("sku") == "SHIPPING"
    ]
    assert len(shipping_items) == 1, (
        f"Expected exactly 1 SHIPPING item in XML, found {len(shipping_items)}"
    )


# ---------------------------------------------------------------------------
# Test 2: Courier shipping has PLU 304
# ---------------------------------------------------------------------------


def test_xml_shipping_correct_plu_courier():
    """Courier shipping must have PLU 304."""
    svc = _make_service()
    order = _make_order(
        shipping_price=3.50,
        delivery_method="courier",
        packeta_point_id="",
    )
    items = _make_items()

    xml_str = svc._generate_order_xml(order, items)
    root = fromstring(xml_str)

    shipping_items = [
        i for i in root.findall(".//item") if i.findtext("sku") == "SHIPPING"
    ]
    assert len(shipping_items) == 1
    assert shipping_items[0].findtext("plu") == "304"


# ---------------------------------------------------------------------------
# Test 3: Packeta shipping has PLU 303
# ---------------------------------------------------------------------------


def test_xml_shipping_correct_plu_packeta():
    """Packeta shipping must have PLU 303."""
    svc = _make_service()
    order = _make_order(
        shipping_price=2.50,
        delivery_method="packeta_point",
        packeta_point_id="12345",
    )
    items = _make_items()

    xml_str = svc._generate_order_xml(order, items)
    root = fromstring(xml_str)

    shipping_items = [
        i for i in root.findall(".//item") if i.findtext("sku") == "SHIPPING"
    ]
    assert len(shipping_items) == 1
    assert shipping_items[0].findtext("plu") == "303"


# ---------------------------------------------------------------------------
# Test 4: No shipping in XML when price = 0
# ---------------------------------------------------------------------------


def test_xml_no_shipping_when_price_zero():
    """No shipping item in XML when shipping_price = 0."""
    svc = _make_service()
    order = _make_order(shipping_price=0)
    items = _make_items()

    xml_str = svc._generate_order_xml(order, items)
    root = fromstring(xml_str)

    shipping_items = [
        i for i in root.findall(".//item") if i.findtext("sku") == "SHIPPING"
    ]
    assert len(shipping_items) == 0, "No SHIPPING item expected when shipping_price = 0"


# ---------------------------------------------------------------------------
# Test 5: SHIPPING SKU items in items list are skipped (defensive)
# ---------------------------------------------------------------------------


def test_xml_shipping_skips_shipping_sku_in_items():
    """Even if items list contains SHIPPING SKU, it should be skipped
    (defensive — items query should already exclude it)."""
    svc = _make_service()
    order = _make_order(shipping_price=3.50, delivery_method="courier")
    items = _make_items() + [
        {
            "sku": "SHIPPING",
            "name": "Kurier na adresu",
            "quantity": 1,
            "unit_price_vat": 3.50,
            "vat_rate": 20,
        }
    ]

    xml_str = svc._generate_order_xml(order, items)
    root = fromstring(xml_str)

    shipping_items = [
        i for i in root.findall(".//item") if i.findtext("sku") == "SHIPPING"
    ]
    # Must be exactly 1 (the one from _generate_order_xml shipping logic)
    # not 2 (from items list + shipping logic)
    assert len(shipping_items) == 1, (
        f"Expected 1 SHIPPING item (defensive skip), found {len(shipping_items)}"
    )
    assert shipping_items[0].findtext("plu") == "304"
