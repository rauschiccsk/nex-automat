"""
Tests for health check endpoints.
"""


class TestHealthEndpoints:
    """Tests for /api/v1/health, /api/v1/metrics, /api/v1/ready endpoints."""

    def test_health_endpoint(self, api_v1_client):
        """Test GET /api/v1/health returns healthy status."""
        response = api_v1_client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime_seconds" in data

    def test_metrics_endpoint(self, api_v1_client):
        """Test GET /api/v1/metrics returns metrics data."""
        response = api_v1_client.get("/api/v1/metrics")

        assert response.status_code == 200
        content = response.text
        # Prometheus format
        assert "btrieve_loader_info" in content
        assert "btrieve_loader_uptime_seconds" in content

    def test_ready_endpoint(self, api_v1_client):
        """Test GET /api/v1/ready returns readiness status."""
        response = api_v1_client.get("/api/v1/ready")

        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True
        assert "timestamp" in data


class TestRootEndpoints:
    """Tests for root-level endpoints (backward compatibility)."""

    def test_root_endpoint(self, api_v1_client):
        """Test GET / returns service info."""
        response = api_v1_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert data["status"] == "running"

    def test_root_health_endpoint(self, api_v1_client):
        """Test GET /health returns healthy status."""
        response = api_v1_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_metrics_endpoint(self, api_v1_client):
        """Test GET /metrics returns metrics in JSON."""
        response = api_v1_client.get("/metrics")

        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "app_info" in data
