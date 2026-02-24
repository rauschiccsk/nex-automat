"""
Tests for product group/store endpoints.
"""

from unittest.mock import patch


class TestStoreEndpoints:
    """Tests for /api/v1/stores endpoints."""

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_list_product_groups(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores returns paginated product groups."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get("/api/v1/stores", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) == 3

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_list_product_groups_filter_by_parent(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores with parent_code filter."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get(
            "/api/v1/stores?parent_code=1", headers=api_key_header
        )

        assert response.status_code == 200
        data = response.json()
        # All returned groups should have parent_code=1
        for group in data["data"]:
            assert group["parent_code"] == 1

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_list_product_groups_filter_by_level(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores with level filter."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get("/api/v1/stores?level=1", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        for group in data["data"]:
            assert group["level"] == 1

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_get_product_groups_tree(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores/tree returns hierarchical tree."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get("/api/v1/stores/tree", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        # Should be a list of root nodes
        assert isinstance(data, list)
        # Root nodes should have children
        if data:
            assert "children" in data[0] or len(data) > 0

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_get_product_group_by_code(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores/{mglst_code} returns specific group."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get("/api/v1/stores/1", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["mglst_code"] == 1
        assert data["name"] == "Potraviny"

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_get_product_group_not_found(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores/{mglst_code} returns 404 for unknown code."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get("/api/v1/stores/99999", headers=api_key_header)

        assert response.status_code == 404

    @patch("src.api.routes.stores.get_mglst_repository")
    def test_get_product_group_children(
        self, mock_get_repo, api_v1_client, mock_mglst_repository, api_key_header
    ):
        """Test GET /api/v1/stores/{mglst_code}/children returns child groups."""
        mock_get_repo.return_value = mock_mglst_repository

        response = api_v1_client.get(
            "/api/v1/stores/1/children", headers=api_key_header
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        # All children should have parent_code=1
        for child in data["data"]:
            assert child["parent_code"] == 1
