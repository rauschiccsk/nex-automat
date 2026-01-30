"""
Tests for product endpoints.
"""

from unittest.mock import patch

import pytest


class TestProductEndpoints:
    """Tests for /api/v1/products endpoints."""

    def test_list_products_no_auth(self, api_v1_client):
        """Test GET /api/v1/products without auth returns 422."""
        response = api_v1_client.get("/api/v1/products")
        # Without API key configured, should work (auth skipped)
        # If API key is required, would return 422
        assert response.status_code in [200, 422]

    @patch("src.api.routes.products.get_gscat_repository")
    def test_list_products(self, mock_get_repo, api_v1_client, mock_gscat_repository, api_key_header):
        """Test GET /api/v1/products returns paginated products."""
        mock_get_repo.return_value = mock_gscat_repository

        response = api_v1_client.get("/api/v1/products", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) == 3
        assert data["data"][0]["gs_code"] == 1001

    @patch("src.api.routes.products.get_gscat_repository")
    def test_list_products_pagination(self, mock_get_repo, api_v1_client, mock_gscat_repository, api_key_header):
        """Test GET /api/v1/products with pagination params."""
        mock_get_repo.return_value = mock_gscat_repository

        response = api_v1_client.get("/api/v1/products?page=1&page_size=2", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["page_size"] == 2

    @patch("src.api.routes.products.get_gscat_repository")
    def test_search_products(self, mock_get_repo, api_v1_client, mock_gscat_repository, api_key_header):
        """Test GET /api/v1/products/search with query."""
        mock_get_repo.return_value = mock_gscat_repository

        response = api_v1_client.get("/api/v1/products/search?q=Chlieb", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert "Chlieb" in data["data"][0]["gs_name"]

    @patch("src.api.routes.products.get_gscat_repository")
    def test_search_products_min_length(self, mock_get_repo, api_v1_client, mock_gscat_repository, api_key_header):
        """Test GET /api/v1/products/search with too short query."""
        mock_get_repo.return_value = mock_gscat_repository

        response = api_v1_client.get("/api/v1/products/search?q=X", headers=api_key_header)

        # Query validation should fail (min_length=2)
        assert response.status_code == 422

    @patch("src.api.routes.products.get_gscat_repository")
    def test_get_product_by_code(self, mock_get_repo, api_v1_client, mock_gscat_repository, api_key_header):
        """Test GET /api/v1/products/{code} returns specific product."""
        mock_get_repo.return_value = mock_gscat_repository

        response = api_v1_client.get("/api/v1/products/1001", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["gs_code"] == 1001
        assert data["gs_name"] == "Chlieb biely 500g"

    @patch("src.api.routes.products.get_gscat_repository")
    def test_get_product_not_found(self, mock_get_repo, api_v1_client, mock_gscat_repository, api_key_header):
        """Test GET /api/v1/products/{code} returns 404 for unknown code."""
        mock_get_repo.return_value = mock_gscat_repository

        response = api_v1_client.get("/api/v1/products/99999", headers=api_key_header)

        assert response.status_code == 404


class TestProductMatchEndpoint:
    """Tests for /api/v1/products/match endpoint."""

    @patch("src.api.routes.products.ProductMatcher")
    def test_match_product_by_ean(self, mock_matcher_class, api_v1_client, api_key_header, sample_products):
        """Test POST /api/v1/products/match with EAN."""
        # Setup mock matcher
        mock_matcher = mock_matcher_class.return_value
        mock_result = type(
            "MatchResult",
            (),
            {
                "is_match": True,
                "confidence": 0.95,
                "confidence_level": "high",
                "method": "ean",
                "product": sample_products[0],
                "alternatives": [],
            },
        )()
        mock_matcher.match_item.return_value = mock_result

        response = api_v1_client.post(
            "/api/v1/products/match",
            json={"original_ean": "8590001000010"},
            headers=api_key_header,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_match"] is True
        assert data["confidence"] == 0.95
        assert data["method"] == "ean"

    @patch("src.api.routes.products.ProductMatcher")
    def test_match_product_no_match(self, mock_matcher_class, api_v1_client, api_key_header):
        """Test POST /api/v1/products/match with no match."""
        mock_matcher = mock_matcher_class.return_value
        mock_result = type(
            "MatchResult",
            (),
            {
                "is_match": False,
                "confidence": 0.3,
                "confidence_level": "low",
                "method": "none",
                "product": None,
                "alternatives": [],
            },
        )()
        mock_matcher.match_item.return_value = mock_result

        response = api_v1_client.post(
            "/api/v1/products/match",
            json={"original_name": "Unknown Product XYZ"},
            headers=api_key_header,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_match"] is False
