"""Tests for MuFis product mapping — 3PACK quantity multiplier + barcode resolution."""

import os
import sys

# Set JWT_SECRET_KEY before any app imports (required by nex_config.security)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-mufis-tests")

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eshop.router import MUFIS_PRODUCT_MAPPING


class TestMufisProductMapping:
    """Test MUFIS_PRODUCT_MAPPING dictionary."""

    def test_mapping_has_all_products(self):
        """All known products are in mapping."""
        assert "EM-500" in MUFIS_PRODUCT_MAPPING
        assert "EM-500-3PACK" in MUFIS_PRODUCT_MAPPING
        assert "EM-5L" in MUFIS_PRODUCT_MAPPING

    def test_3pack_quantity_multiplier(self):
        """EM-500-3PACK has quantity multiplier of 3."""
        mapping = MUFIS_PRODUCT_MAPPING["EM-500-3PACK"]
        assert mapping["mufis_quantity_multiplier"] == 3

    def test_3pack_barcode_maps_to_base_product(self):
        """EM-500-3PACK barcode should come from EM-500 (base product)."""
        mapping = MUFIS_PRODUCT_MAPPING["EM-500-3PACK"]
        assert mapping["mufis_barcode_sku"] == "EM-500"

    def test_single_bottle_multiplier(self):
        """EM-500 single bottle has multiplier of 1."""
        mapping = MUFIS_PRODUCT_MAPPING["EM-500"]
        assert mapping["mufis_quantity_multiplier"] == 1

    def test_5l_multiplier(self):
        """EM-5L has multiplier of 1."""
        mapping = MUFIS_PRODUCT_MAPPING["EM-5L"]
        assert mapping["mufis_quantity_multiplier"] == 1

    def test_unknown_sku_fallback(self):
        """Unknown SKU should use default mapping (multiplier=1, barcode_sku=self)."""
        unknown_sku = "UNKNOWN-PRODUCT"
        mapping = MUFIS_PRODUCT_MAPPING.get(
            unknown_sku,
            {"mufis_quantity_multiplier": 1, "mufis_barcode_sku": unknown_sku},
        )
        assert mapping["mufis_quantity_multiplier"] == 1
        assert mapping["mufis_barcode_sku"] == unknown_sku

    def test_3pack_quantity_calculation(self):
        """Simulate: order 2x EM-500-3PACK -> MuFis gets quantity 6."""
        order_quantity = 2
        mapping = MUFIS_PRODUCT_MAPPING["EM-500-3PACK"]
        mufis_quantity = order_quantity * mapping["mufis_quantity_multiplier"]
        assert mufis_quantity == 6

    def test_single_bottle_quantity_calculation(self):
        """Simulate: order 2x EM-500 -> MuFis gets quantity 2."""
        order_quantity = 2
        mapping = MUFIS_PRODUCT_MAPPING["EM-500"]
        mufis_quantity = order_quantity * mapping["mufis_quantity_multiplier"]
        assert mufis_quantity == 2
