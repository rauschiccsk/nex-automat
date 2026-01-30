"""
Tests for document endpoints.
"""

from unittest.mock import patch

import pytest


class TestDocumentEndpoints:
    """Tests for /api/v1/documents endpoints."""

    @patch("src.api.routes.documents.get_tsh_repository")
    def test_list_documents(self, mock_get_repo, api_v1_client, mock_tsh_repository, api_key_header):
        """Test GET /api/v1/documents returns paginated documents."""
        mock_get_repo.return_value = mock_tsh_repository

        response = api_v1_client.get("/api/v1/documents", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) == 2

    @patch("src.api.routes.documents.get_tsh_repository")
    def test_list_documents_with_book_id(self, mock_get_repo, api_v1_client, mock_tsh_repository, api_key_header):
        """Test GET /api/v1/documents with book_id param."""
        mock_get_repo.return_value = mock_tsh_repository

        response = api_v1_client.get("/api/v1/documents?book_id=001", headers=api_key_header)

        assert response.status_code == 200
        mock_get_repo.assert_called_with("001")

    @patch("src.api.routes.documents.get_tsh_repository")
    def test_list_documents_filter_by_type(self, mock_get_repo, api_v1_client, mock_tsh_repository, api_key_header):
        """Test GET /api/v1/documents with doc_type filter."""
        mock_get_repo.return_value = mock_tsh_repository

        response = api_v1_client.get("/api/v1/documents?doc_type=1", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        for doc in data["data"]:
            assert doc["doc_type"] == 1

    @patch("src.api.routes.documents.get_tsh_repository")
    def test_list_documents_filter_by_partner(self, mock_get_repo, api_v1_client, mock_tsh_repository, api_key_header):
        """Test GET /api/v1/documents with pab_code filter."""
        mock_get_repo.return_value = mock_tsh_repository

        response = api_v1_client.get("/api/v1/documents?pab_code=101", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        for doc in data["data"]:
            assert doc["pab_code"] == 101

    @patch("src.api.routes.documents.get_tsh_repository")
    def test_list_documents_filter_by_date(self, mock_get_repo, api_v1_client, mock_tsh_repository, api_key_header):
        """Test GET /api/v1/documents with date range filter."""
        mock_get_repo.return_value = mock_tsh_repository

        response = api_v1_client.get(
            "/api/v1/documents?date_from=2025-01-01&date_to=2025-01-31", headers=api_key_header
        )

        assert response.status_code == 200

    @patch("src.api.routes.documents.get_tsi_repository")
    @patch("src.api.routes.documents.get_tsh_repository")
    def test_get_document_with_items(
        self,
        mock_get_tsh_repo,
        mock_get_tsi_repo,
        api_v1_client,
        mock_tsh_repository,
        mock_tsi_repository,
        api_key_header,
    ):
        """Test GET /api/v1/documents/{doc_number} returns header with items."""
        mock_get_tsh_repo.return_value = mock_tsh_repository
        mock_get_tsi_repo.return_value = mock_tsi_repository

        response = api_v1_client.get("/api/v1/documents/2025001", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "header" in data
        assert "items" in data
        assert data["header"]["doc_number"] == "2025001"
        assert len(data["items"]) == 2

    @patch("src.api.routes.documents.get_tsi_repository")
    @patch("src.api.routes.documents.get_tsh_repository")
    def test_get_document_not_found(
        self,
        mock_get_tsh_repo,
        mock_get_tsi_repo,
        api_v1_client,
        mock_tsh_repository,
        mock_tsi_repository,
        api_key_header,
    ):
        """Test GET /api/v1/documents/{doc_number} returns 404."""
        mock_tsh_repository.find_one.return_value = None
        mock_get_tsh_repo.return_value = mock_tsh_repository
        mock_get_tsi_repo.return_value = mock_tsi_repository

        response = api_v1_client.get("/api/v1/documents/UNKNOWN123", headers=api_key_header)

        assert response.status_code == 404

    @patch("src.api.routes.documents.get_tsi_repository")
    def test_get_document_items_only(self, mock_get_repo, api_v1_client, mock_tsi_repository, api_key_header):
        """Test GET /api/v1/documents/{doc_number}/items returns only items."""
        mock_get_repo.return_value = mock_tsi_repository

        response = api_v1_client.get("/api/v1/documents/2025001/items", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 2
        # Items should be sorted by line_number
        assert data["data"][0]["line_number"] == 1
        assert data["data"][1]["line_number"] == 2

    @patch("src.api.routes.documents.get_tsi_repository")
    def test_get_document_items_not_found(self, mock_get_repo, api_v1_client, mock_tsi_repository, api_key_header):
        """Test GET /api/v1/documents/{doc_number}/items returns 404."""
        mock_tsi_repository.find.return_value = []
        mock_get_repo.return_value = mock_tsi_repository

        response = api_v1_client.get("/api/v1/documents/UNKNOWN123/items", headers=api_key_header)

        assert response.status_code == 404
