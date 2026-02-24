"""
Tests for partner endpoints.
"""

from unittest.mock import patch


class TestPartnerEndpoints:
    """Tests for /api/v1/partners endpoints."""

    @patch("src.api.routes.partners.get_pab_repository")
    def test_list_partners(
        self, mock_get_repo, api_v1_client, mock_pab_repository, api_key_header
    ):
        """Test GET /api/v1/partners returns paginated partners."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get("/api/v1/partners", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) == 3

    @patch("src.api.routes.partners.get_pab_repository")
    def test_list_partners_filter_by_type(
        self, mock_get_repo, api_v1_client, mock_pab_repository, api_key_header
    ):
        """Test GET /api/v1/partners with partner_type filter."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get(
            "/api/v1/partners?partner_type=1", headers=api_key_header
        )

        assert response.status_code == 200
        data = response.json()
        # Should filter to only suppliers (partner_type=1)
        for partner in data["data"]:
            assert partner["partner_type"] == 1

    @patch("src.api.routes.partners.get_pab_repository")
    def test_list_partners_filter_by_active(
        self, mock_get_repo, api_v1_client, mock_pab_repository, api_key_header
    ):
        """Test GET /api/v1/partners with active filter."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get(
            "/api/v1/partners?active=true", headers=api_key_header
        )

        assert response.status_code == 200
        data = response.json()
        for partner in data["data"]:
            assert partner["active"] is True

    @patch("src.api.routes.partners.get_pab_repository")
    def test_search_partners(
        self,
        mock_get_repo,
        api_v1_client,
        mock_pab_repository,
        api_key_header,
        sample_partners,
    ):
        """Test GET /api/v1/partners/search with query."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get(
            "/api/v1/partners/search?q=Bratislava", headers=api_key_header
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1

    @patch("src.api.routes.partners.get_pab_repository")
    def test_search_partners_by_ico(
        self, mock_get_repo, api_v1_client, mock_pab_repository, api_key_header
    ):
        """Test GET /api/v1/partners/search by ICO."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get(
            "/api/v1/partners/search?q=12345678", headers=api_key_header
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert data["data"][0]["ico"] == "12345678"

    @patch("src.api.routes.partners.get_pab_repository")
    def test_get_partner_by_code(
        self, mock_get_repo, api_v1_client, mock_pab_repository, api_key_header
    ):
        """Test GET /api/v1/partners/{pab_code} returns specific partner."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get("/api/v1/partners/101", headers=api_key_header)

        assert response.status_code == 200
        data = response.json()
        assert data["pab_code"] == 101
        assert data["name1"] == "L & Š, s.r.o."

    @patch("src.api.routes.partners.get_pab_repository")
    def test_get_partner_not_found(
        self, mock_get_repo, api_v1_client, mock_pab_repository, api_key_header
    ):
        """Test GET /api/v1/partners/{pab_code} returns 404 for unknown code."""
        mock_get_repo.return_value = mock_pab_repository

        response = api_v1_client.get("/api/v1/partners/99999", headers=api_key_header)

        assert response.status_code == 404
