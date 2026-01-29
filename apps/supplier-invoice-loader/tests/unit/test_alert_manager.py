"""Tests for alert manager system"""

import pytest
from datetime import datetime, timedelta
from src.monitoring import AlertManager, AlertLevel, AlertType, AlertConfig


@pytest.fixture
def alert_config():
    """Create test alert configuration"""
    return AlertConfig(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="test@example.com",
        smtp_password="password",
        from_email="test@example.com",
        to_emails=["recipient@example.com"],
        use_tls=True,
    )


@pytest.fixture
def alert_manager(alert_config):
    """Create alert manager instance"""
    return AlertManager(alert_config)


def test_alert_manager_initialization(alert_manager):
    """Test alert manager initializes correctly"""
    assert alert_manager.config is not None
    assert len(alert_manager._alert_history) == 0


def test_critical_alert_creation(alert_manager):
    """Test creating critical alert"""
    # Don't actually send email in tests
    alert_manager._send_email = lambda **kwargs: True

    result = alert_manager.send_critical_alert(
        title="Test Critical", message="This is a test", alert_type=AlertType.SYSTEM
    )

    assert result is True
    assert len(alert_manager._alert_history) == 1
    alert = alert_manager._alert_history[0]
    assert alert.level == AlertLevel.CRITICAL
    assert alert.title == "Test Critical"


def test_warning_alert_creation(alert_manager):
    """Test creating warning alert"""
    alert_manager._send_email = lambda **kwargs: True

    result = alert_manager.send_warning(
        title="Test Warning", message="This is a warning", alert_type=AlertType.PERFORMANCE
    )

    assert result is True
    assert len(alert_manager._alert_history) == 1
    alert = alert_manager._alert_history[0]
    assert alert.level == AlertLevel.WARNING


def test_alert_history_filtering(alert_manager):
    """Test filtering alert history"""
    alert_manager._send_email = lambda **kwargs: True

    # Add multiple alerts
    alert_manager.send_critical_alert("Critical 1", "msg", AlertType.SYSTEM)
    alert_manager.send_warning("Warning 1", "msg", AlertType.DATABASE)
    alert_manager.send_critical_alert("Critical 2", "msg", AlertType.DISK_SPACE)

    # Filter by level
    critical_alerts = alert_manager.get_alert_history(level=AlertLevel.CRITICAL)
    assert len(critical_alerts) == 2

    # Filter by type
    system_alerts = alert_manager.get_alert_history(alert_type=AlertType.SYSTEM)
    assert len(system_alerts) == 1

    # Filter by time
    recent = alert_manager.get_alert_history(since=datetime.now() - timedelta(minutes=1))
    assert len(recent) == 3


def test_check_health_high_cpu(alert_manager):
    """Test health check triggers CPU alert"""
    alert_manager._send_email = lambda **kwargs: True

    health_status = {
        "system_metrics": {"cpu_percent": 95.0, "memory_percent": 50.0, "disk_percent": 50.0},
        "database_status": {"connected": True},
    }

    alerts = alert_manager.check_health_and_alert(health_status)
    assert len(alerts) == 1
    assert alerts[0].alert_type == AlertType.SYSTEM
    assert "CPU" in alerts[0].title


def test_check_health_database_down(alert_manager):
    """Test health check triggers database alert"""
    alert_manager._send_email = lambda **kwargs: True

    health_status = {
        "system_metrics": {"cpu_percent": 50.0, "memory_percent": 50.0, "disk_percent": 50.0},
        "database_status": {"connected": False, "error": "Connection refused"},
    }

    alerts = alert_manager.check_health_and_alert(health_status)
    assert len(alerts) == 1
    assert alerts[0].alert_type == AlertType.DATABASE
    assert alerts[0].level == AlertLevel.CRITICAL


def test_daily_summary_format(alert_manager):
    """Test daily summary formatting"""
    invoice_stats = {"total_processed": 100, "total_failed": 5, "success_rate": 95.0}
    system_stats = {"cpu_percent": 45.0, "memory_percent": 60.0, "disk_percent": 70.0}
    errors = ["Error 1", "Error 2"]

    html = alert_manager._format_daily_summary(invoice_stats, system_stats, errors)

    assert "Daily Summary" in html
    assert "100" in html  # processed count
    assert "95.0%" in html  # success rate
    assert "Error 1" in html


def test_alert_level_enum():
    """Test AlertLevel enum"""
    assert AlertLevel.INFO.value == "info"
    assert AlertLevel.WARNING.value == "warning"
    assert AlertLevel.ERROR.value == "error"
    assert AlertLevel.CRITICAL.value == "critical"


def test_alert_type_enum():
    """Test AlertType enum"""
    assert AlertType.SYSTEM.value == "system"
    assert AlertType.DATABASE.value == "database"
    assert AlertType.INVOICE.value == "invoice"
