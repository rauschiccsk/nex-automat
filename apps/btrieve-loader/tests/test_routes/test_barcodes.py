"""
Tests for barcode endpoints.
"""

from unittest.mock import patch

import pytest


class TestBarcodeEndpoints:
    """Tests for /api/v1/barcodes endpoints."""

    @patch("src.api.routes.barcodes.get_gscat_repository")
    @patch("src.api.routes.barcodes.get_barcode_repository")
    def test_lookup_barcode_gscat(
        self,
        mock_get_barcode_repo,
        mock_get_gscat_repo,
        api_v1_client,
        mock_gscat_repository,
        mock_barcode_repository,
        api_key_header,
    ):
        """Test GET /api/v1/barcodes/{ean} finds product in GSCAT."""
        mock_get_gscat_repo.return_value = mock_gscat_repository
        mock_get_barcode_repo.return_value = mock_barcode_repository

        response = api_v1_client.get("/api/v1/barcodes/8590001000010", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["gs_code"] == 1001
        assert data["bar_code"] == "8590001000010"
        assert "product_name" in data

    @patch("src.api.routes.barcodes.get_gscat_repository")
    @patch("src.api.routes.barcodes.get_barcode_repository")
    def test_lookup_barcode_secondary(
        self,
        mock_get_barcode_repo,
        mock_get_gscat_repo,
        api_v1_client,
        mock_gscat_repository,
        mock_barcode_repository,
        api_key_header,
        sample_products,
    ):
        """Test GET /api/v1/barcodes/{ean} finds product via BARCODE table."""
        # Primary lookup returns None
        mock_gscat_repository.find_by_barcode.return_value = None
        mock_gscat_repository.find_one.return_value = sample_products[0]
        mock_get_gscat_repo.return_value = mock_gscat_repository
        mock_get_barcode_repo.return_value = mock_barcode_repository

        response = api_v1_client.get("/api/v1/barcodes/8590001000099", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["gs_code"] == 1001

    @patch("src.api.routes.barcodes.get_gscat_repository")
    @patch("src.api.routes.barcodes.get_barcode_repository")
    def test_lookup_barcode_not_found(
        self,
        mock_get_barcode_repo,
        mock_get_gscat_repo,
        api_v1_client,
        mock_gscat_repository,
        mock_barcode_repository,
        api_key_header,
    ):
        """Test GET /api/v1/barcodes/{ean} returns 404 for unknown barcode."""
        mock_gscat_repository.find_by_barcode.return_value = None
        mock_barcode_repository.find_by_barcode.return_value = None
        mock_get_gscat_repo.return_value = mock_gscat_repository
        mock_get_barcode_repo.return_value = mock_barcode_repository

        response = api_v1_client.get("/api/v1/barcodes/0000000000000", headers=api_key_header)

        assert response.status_code == 404

    @patch("src.api.routes.barcodes.get_gscat_repository")
    @patch("src.api.routes.barcodes.get_barcode_repository")
    def test_lookup_barcode_normalizes_input(
        self,
        mock_get_barcode_repo,
        mock_get_gscat_repo,
        api_v1_client,
        mock_gscat_repository,
        mock_barcode_repository,
        api_key_header,
    ):
        """Test GET /api/v1/barcodes/{ean} normalizes EAN (strips spaces/dashes)."""
        mock_get_gscat_repo.return_value = mock_gscat_repository
        mock_get_barcode_repo.return_value = mock_barcode_repository

        response = api_v1_client.get("/api/v1/barcodes/859-0001-000010", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["gs_code"] == 1001

    @patch("src.api.routes.barcodes.get_gscat_repository")
    @patch("src.api.routes.barcodes.get_barcode_repository")
    def test_get_product_barcodes(
        self,
        mock_get_barcode_repo,
        mock_get_gscat_repo,
        api_v1_client,
        mock_gscat_repository,
        mock_barcode_repository,
        api_key_header,
    ):
        """Test GET /api/v1/barcodes/product/{product_code} returns all barcodes."""
        mock_get_gscat_repo.return_value = mock_gscat_repository
        mock_get_barcode_repo.return_value = mock_barcode_repository

        response = api_v1_client.get("/api/v1/barcodes/product/1001", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        # Should have primary + secondary barcodes
        assert len(data["data"]) >= 1

    @patch("src.api.routes.barcodes.get_gscat_repository")
    @patch("src.api.routes.barcodes.get_barcode_repository")
    def test_get_product_barcodes_not_found(
        self,
        mock_get_barcode_repo,
        mock_get_gscat_repo,
        api_v1_client,
        mock_gscat_repository,
        mock_barcode_repository,
        api_key_header,
    ):
        """Test GET /api/v1/barcodes/product/{product_code} returns 404."""
        mock_gscat_repository.find_one.return_value = None
        mock_barcode_repository.find.return_value = []
        mock_get_gscat_repo.return_value = mock_gscat_repository
        mock_get_barcode_repo.return_value = mock_barcode_repository

        response = api_v1_client.get("/api/v1/barcodes/product/99999", headers=api_key_header)

        assert response.status_code == 404
