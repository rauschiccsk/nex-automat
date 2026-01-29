"""
Tests for monitoring and metrics functionality
"""

import time

import pytest


def test_monitoring_module_imports():
    """Test that monitoring module can be imported"""
    try:
        from src.utils import monitoring

        assert monitoring is not None
    except ImportError as e:
        pytest.fail(f"Failed to from src.utils import monitoring: {e}")


def test_metrics_class_exists():
    """Test that Metrics class exists"""
    from src.utils.monitoring import Metrics

    assert Metrics is not None


def test_create_metrics():
    """Test creating Metrics instance"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    assert metrics.start_time > 0
    assert metrics.invoices_processed == 0
    assert metrics.invoices_failed == 0
    assert metrics.requests_total == 0


def test_increment_invoice_success():
    """Test incrementing successful invoice counter"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    initial = metrics.invoices_processed
    metrics.increment_invoice(success=True)

    assert metrics.invoices_processed == initial + 1
    assert metrics.invoices_failed == 0


def test_increment_invoice_failed():
    """Test incrementing failed invoice counter"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    initial = metrics.invoices_failed
    metrics.increment_invoice(success=False)

    assert metrics.invoices_failed == initial + 1
    assert metrics.invoices_processed == 0


def test_increment_request_success():
    """Test incrementing successful request counter"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    initial = metrics.requests_success
    metrics.increment_request(success=True)

    assert metrics.requests_success == initial + 1
    assert metrics.requests_total == 1


def test_increment_request_failed():
    """Test incrementing failed request counter"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    initial = metrics.requests_failed
    metrics.increment_request(success=False)

    assert metrics.requests_failed == initial + 1
    assert metrics.requests_total == 1


def test_uptime_calculation():
    """Test uptime calculation"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    # Wait a tiny bit
    time.sleep(0.1)

    uptime = metrics.get_uptime()
    assert uptime > 0
    assert uptime >= 0.1


def test_reset_metrics():
    """Test resetting metrics counters"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    # Increment some counters
    metrics.increment_invoice(success=True)
    metrics.increment_invoice(success=False)
    metrics.increment_request(success=True)

    # Verify they're not zero
    assert metrics.invoices_processed > 0
    assert metrics.invoices_failed > 0
    assert metrics.requests_total > 0

    # Reset
    metrics.reset()

    # Should be zero again
    assert metrics.invoices_processed == 0
    assert metrics.invoices_failed == 0
    assert metrics.requests_total == 0
    assert metrics.requests_success == 0
    assert metrics.requests_failed == 0


def test_get_stats():
    """Test get_stats() returns complete statistics dict"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()

    # Add some activity
    metrics.increment_invoice(success=True)
    metrics.increment_invoice(success=True)
    metrics.increment_invoice(success=False)
    metrics.increment_request(success=True)

    stats = metrics.get_stats()

    assert isinstance(stats, dict)
    assert "uptime_seconds" in stats
    assert "requests" in stats
    assert "invoices" in stats
    assert "system" in stats
    assert "psutil_available" in stats

    # Check nested structure
    assert stats["requests"]["total"] == 1
    assert stats["requests"]["success"] == 1
    assert stats["invoices"]["processed"] == 2
    assert stats["invoices"]["failed"] == 1


def test_get_system_metrics():
    """Test system metrics collection"""
    from src.utils.monitoring import Metrics

    metrics = Metrics()
    system = metrics.get_system_metrics()

    assert isinstance(system, dict)
    assert "cpu_percent" in system
    assert "memory_percent" in system
    assert "disk_percent" in system

    # Values might be None if psutil not available
    if system["cpu_percent"] is not None:
        assert isinstance(system["cpu_percent"], (int, float))


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_check_storage_health():
    """Test storage health check"""
    from src.utils import monitoring

    result = monitoring.check_storage_health()

    assert isinstance(result, dict)
    assert "pdf_dir_exists" in result
    assert "xml_dir_exists" in result
    assert "storage_healthy" in result

    # Should be boolean values
    assert isinstance(result["storage_healthy"], bool)


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_check_database_health():
    """Test database health check"""
    from src.utils import monitoring

    result = monitoring.check_database_health()

    assert isinstance(result, dict)
    assert "db_exists" in result
    assert "db_accessible" in result
    assert "database_healthy" in result


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_check_smtp_config():
    """Test SMTP configuration check"""
    from src.utils import monitoring

    result = monitoring.check_smtp_config()

    assert isinstance(result, dict)
    assert "smtp_configured" in result
    assert "alert_email" in result
    assert "daily_summary_enabled" in result


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_get_system_info():
    """Test system information retrieval"""
    from src.utils import monitoring

    result = monitoring.get_system_info()

    assert isinstance(result, dict)

    # Should have CPU and memory info
    # Values might be None if psutil fails
    assert "cpu_percent" in result
    assert "memory_percent" in result


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_get_health_status():
    """Test health status endpoint data"""
    from src.utils import monitoring

    result = monitoring.get_health_status()

    assert isinstance(result, dict)
    assert "status" in result
    assert "timestamp" in result
    assert "uptime" in result
    assert "storage_ok" in result
    assert "database_ok" in result

    # Status should be one of expected values
    assert result["status"] in ["healthy", "degraded", "unhealthy"]


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_get_detailed_status():
    """Test detailed status endpoint data"""
    from src.utils import monitoring

    result = monitoring.get_detailed_status()

    assert isinstance(result, dict)
    assert "status" in result
    assert "timestamp" in result
    assert "customer" in result
    assert "uptime" in result
    assert "components" in result
    assert "statistics" in result

    # Check nested structure
    assert "storage" in result["components"]
    assert "database" in result["components"]
    assert "smtp" in result["components"]


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_get_metrics_prometheus():
    """Test Prometheus format metrics"""
    from src.utils import monitoring

    result = monitoring.get_metrics_prometheus()

    assert isinstance(result, str)

    # Should contain Prometheus format elements
    assert "# HELP" in result
    assert "# TYPE" in result
    assert "app_uptime_seconds" in result


def test_global_metrics_instance():
    """Test that global metrics instance exists"""
    from src.utils import monitoring

    # Should have get_metrics() function
    metrics = monitoring.get_metrics()
    assert metrics is not None
    assert isinstance(metrics, monitoring.Metrics)


def test_metrics_persistence():
    """Test that metrics persist across function calls"""
    from src.utils import monitoring

    # Reset first
    monitoring.reset_metrics()

    # Increment
    monitoring.get_metrics().increment_invoice(success=True)

    # Should persist
    assert monitoring.get_metrics().invoices_processed == 1

    # Get stats - should still have same value
    stats = monitoring.get_metrics().get_stats()
    assert stats["invoices"]["processed"] == 1


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_health_status_values():
    """Test that health status returns correct values"""
    from src.utils import monitoring

    status = monitoring.get_health_status()

    # If storage and DB are healthy, overall should be healthy
    if status["storage_ok"] and status["database_ok"]:
        assert status["status"] == "healthy"

    # If neither is healthy, should be unhealthy
    if not status["storage_ok"] and not status["database_ok"]:
        assert status["status"] == "unhealthy"


@pytest.mark.skip(reason="Function removed from monitoring.py")
def test_system_info_types():
    """Test that system info returns correct types"""
    from src.utils import monitoring

    info = monitoring.get_system_info()

    # CPU and memory should be numbers or None
    if info["cpu_percent"] is not None:
        assert isinstance(info["cpu_percent"], (int, float))
        assert 0 <= info["cpu_percent"] <= 100

    if info["memory_percent"] is not None:
        assert isinstance(info["memory_percent"], (int, float))
        assert 0 <= info["memory_percent"] <= 100


@pytest.mark.integration
def test_end_to_end_monitoring():
    """Integration test for full monitoring workflow"""
    from src.utils import monitoring

    # Reset first
    monitoring.reset_metrics()

    # Simulate some activity
    monitoring.get_metrics().increment_invoice(success=True)
    monitoring.get_metrics().increment_invoice(success=True)
    monitoring.get_metrics().increment_invoice(success=False)
    monitoring.get_metrics().increment_request(success=True)

    # Get stats
    stats = monitoring.get_metrics().get_stats()

    # Should reflect our activity
    assert stats["invoices"]["processed"] == 2
    assert stats["invoices"]["failed"] == 1
    assert stats["requests"]["total"] == 1
    assert stats["requests"]["success"] == 1
