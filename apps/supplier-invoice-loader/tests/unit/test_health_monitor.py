"""Tests for health monitoring system"""

import pytest
from datetime import datetime, timedelta
from src.monitoring import HealthMonitor, SystemMetrics, HealthStatus


def test_system_metrics():
    """Test system metrics collection"""
    monitor = HealthMonitor()
    metrics = monitor.get_system_metrics()
    
    assert isinstance(metrics, SystemMetrics)
    assert 0 <= metrics.cpu_percent <= 100
    assert metrics.memory_total_gb > 0
    assert metrics.disk_total_gb > 0
    assert 0 <= metrics.memory_percent <= 100
    assert 0 <= metrics.disk_percent <= 100


def test_uptime_tracking():
    """Test uptime tracking"""
    monitor = HealthMonitor()
    
    uptime = monitor.get_uptime_seconds()
    assert uptime >= 0
    
    formatted = monitor.get_uptime_formatted()
    assert 's' in formatted  # Should contain seconds


def test_quick_status():
    """Test quick status endpoint"""
    monitor = HealthMonitor()
    status = monitor.get_quick_status()
    
    assert status['status'] == 'online'
    assert 'timestamp' in status
    assert 'uptime' in status
    assert 'system' in status
    assert isinstance(status['uptime_seconds'], int)


@pytest.mark.asyncio
async def test_database_status_without_pool():
    """Test database status without pool"""
    monitor = HealthMonitor(db_pool=None)
    status = await monitor.check_database_status()
    
    assert status.connected is False
    assert status.error == "Database pool not initialized"


@pytest.mark.asyncio
async def test_invoice_stats_without_pool():
    """Test invoice stats without pool"""
    monitor = HealthMonitor(db_pool=None)
    stats = await monitor.get_invoice_stats()
    
    assert stats.total_processed == 0
    assert stats.total_failed == 0
    assert stats.success_rate == 0.0


@pytest.mark.asyncio
async def test_health_status_structure():
    """Test health status structure"""
    monitor = HealthMonitor(db_pool=None)
    health = await monitor.get_health_status()
    
    assert isinstance(health, HealthStatus)
    assert health.status in ['healthy', 'degraded', 'unhealthy']
    assert isinstance(health.timestamp, datetime)
    assert health.uptime_seconds >= 0
    assert 'cpu_percent' in health.system_metrics
    assert 'connected' in health.database_status


def test_metrics_serialization():
    """Test metrics can be serialized to dict"""
    monitor = HealthMonitor()
    metrics = monitor.get_system_metrics()
    
    data = metrics.to_dict()
    assert isinstance(data, dict)
    assert 'cpu_percent' in data
    assert 'memory_total_gb' in data
    assert 'disk_percent' in data
