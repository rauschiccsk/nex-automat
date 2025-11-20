"""
Health monitoring system for supplier-invoice-loader
Provides system metrics, database status, and application health checks
"""

import platform
import psutil
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import asyncpg
from pydantic import BaseModel, ConfigDict


@dataclass
class SystemMetrics:
    """System resource metrics"""
    cpu_percent: float
    memory_total_gb: float
    memory_used_gb: float
    memory_percent: float
    disk_total_gb: float
    disk_used_gb: float
    disk_percent: float
    disk_free_gb: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class DatabaseStatus:
    """Database connection status"""
    connected: bool
    host: str
    database: str
    connection_time_ms: Optional[float] = None
    error: Optional[str] = None
    last_check: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = asdict(self)
        if data['last_check']:
            data['last_check'] = data['last_check'].isoformat()
        return data


@dataclass
class InvoiceStats:
    """Invoice processing statistics"""
    last_processed_at: Optional[datetime]
    last_invoice_id: Optional[int]
    total_processed: int
    total_failed: int
    success_rate: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = asdict(self)
        if data['last_processed_at']:
            data['last_processed_at'] = data['last_processed_at'].isoformat()
        return data


class HealthStatus(BaseModel):
    """Overall health status"""
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    uptime_seconds: int
    system_metrics: Dict
    database_status: Dict
    invoice_stats: Dict
    errors: List[str]
    warnings: List[str]
    
    def model_dump(self, **kwargs):
        """Override model_dump to handle datetime serialization"""
        data = super().model_dump(**kwargs)
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        return data


class HealthMonitor:
    """Health monitoring system"""
    
    def __init__(self, db_pool: Optional[asyncpg.Pool] = None):
        """
        Initialize health monitor
        
        Args:
            db_pool: Database connection pool
        """
        self.db_pool = db_pool
        self.start_time = datetime.now()
        self._last_db_check: Optional[DatabaseStatus] = None
        self._last_invoice_stats: Optional[InvoiceStats] = None
    
    def get_uptime_seconds(self) -> int:
        """Get application uptime in seconds"""
        return int((datetime.now() - self.start_time).total_seconds())
    
    def get_uptime_formatted(self) -> str:
        """Get formatted uptime string"""
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_total_gb = memory.total / (1024 ** 3)
        memory_used_gb = memory.used / (1024 ** 3)
        memory_percent = memory.percent
        
        # Disk usage (current drive)
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        disk_free_gb = disk.free / (1024 ** 3)
        disk_percent = disk.percent
        
        return SystemMetrics(
            cpu_percent=round(cpu_percent, 2),
            memory_total_gb=round(memory_total_gb, 2),
            memory_used_gb=round(memory_used_gb, 2),
            memory_percent=round(memory_percent, 2),
            disk_total_gb=round(disk_total_gb, 2),
            disk_used_gb=round(disk_used_gb, 2),
            disk_free_gb=round(disk_free_gb, 2),
            disk_percent=round(disk_percent, 2)
        )
    
    async def check_database_status(self) -> DatabaseStatus:
        """Check database connection status"""
        if not self.db_pool:
            return DatabaseStatus(
                connected=False,
                host="not_configured",
                database="not_configured",
                error="Database pool not initialized",
                last_check=datetime.now()
            )
        
        start_time = datetime.now()
        
        try:
            async with self.db_pool.acquire() as conn:
                # Simple query to check connection
                await conn.fetchval("SELECT 1")
                
                # Get database info
                db_name = await conn.fetchval("SELECT current_database()")
                
                connection_time = (datetime.now() - start_time).total_seconds() * 1000
                
                status = DatabaseStatus(
                    connected=True,
                    host=str(self.db_pool._connect_args[0].get('host', 'unknown')),
                    database=db_name,
                    connection_time_ms=round(connection_time, 2),
                    last_check=datetime.now()
                )
                
                self._last_db_check = status
                return status
                
        except Exception as e:
            status = DatabaseStatus(
                connected=False,
                host=str(self.db_pool._connect_args[0].get('host', 'unknown')),
                database="unknown",
                error=str(e),
                last_check=datetime.now()
            )
            self._last_db_check = status
            return status
    
    async def get_invoice_stats(self) -> InvoiceStats:
        """Get invoice processing statistics"""
        if not self.db_pool:
            return InvoiceStats(
                last_processed_at=None,
                last_invoice_id=None,
                total_processed=0,
                total_failed=0,
                success_rate=0.0
            )
        
        try:
            async with self.db_pool.acquire() as conn:
                # Get last processed invoice
                last_invoice = await conn.fetchrow("""
                    SELECT id, created_at 
                    FROM invoices_pending 
                    ORDER BY created_at DESC 
                    LIMIT 1
                """)
                
                # Get statistics
                stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
                        SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected
                    FROM invoices_pending
                """)
                
                total = stats['total'] or 0
                approved = stats['approved'] or 0
                rejected = stats['rejected'] or 0
                
                success_rate = (approved / total * 100) if total > 0 else 0.0
                
                invoice_stats = InvoiceStats(
                    last_processed_at=last_invoice['created_at'] if last_invoice else None,
                    last_invoice_id=last_invoice['id'] if last_invoice else None,
                    total_processed=approved,
                    total_failed=rejected,
                    success_rate=round(success_rate, 2)
                )
                
                self._last_invoice_stats = invoice_stats
                return invoice_stats
                
        except Exception as e:
            # Return cached stats if available
            if self._last_invoice_stats:
                return self._last_invoice_stats
            
            return InvoiceStats(
                last_processed_at=None,
                last_invoice_id=None,
                total_processed=0,
                total_failed=0,
                success_rate=0.0
            )
    
    async def get_health_status(self) -> HealthStatus:
        """Get overall health status"""
        errors = []
        warnings = []
        
        # Get metrics
        system_metrics = self.get_system_metrics()
        db_status = await self.check_database_status()
        invoice_stats = await self.get_invoice_stats()
        
        # Check for issues
        if system_metrics.cpu_percent > 90:
            warnings.append(f"High CPU usage: {system_metrics.cpu_percent}%")
        
        if system_metrics.memory_percent > 90:
            warnings.append(f"High memory usage: {system_metrics.memory_percent}%")
        
        if system_metrics.disk_percent > 90:
            errors.append(f"Critical disk space: {system_metrics.disk_percent}% used")
        elif system_metrics.disk_percent > 80:
            warnings.append(f"High disk usage: {system_metrics.disk_percent}%")
        
        if not db_status.connected:
            errors.append(f"Database not connected: {db_status.error}")
        elif db_status.connection_time_ms and db_status.connection_time_ms > 1000:
            warnings.append(f"Slow database connection: {db_status.connection_time_ms}ms")
        
        # Check last invoice processing
        if invoice_stats.last_processed_at:
            time_since_last = datetime.now() - invoice_stats.last_processed_at
            if time_since_last > timedelta(hours=24):
                warnings.append(f"No invoices processed in last 24 hours")
        
        # Determine overall status
        if errors:
            status = "unhealthy"
        elif warnings:
            status = "degraded"
        else:
            status = "healthy"
        
        return HealthStatus(
            status=status,
            timestamp=datetime.now(),
            uptime_seconds=self.get_uptime_seconds(),
            system_metrics=system_metrics.to_dict(),
            database_status=db_status.to_dict(),
            invoice_stats=invoice_stats.to_dict(),
            errors=errors,
            warnings=warnings
        )
    
    def get_quick_status(self) -> Dict:
        """Get quick status without async operations"""
        return {
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "uptime": self.get_uptime_formatted(),
            "uptime_seconds": self.get_uptime_seconds(),
            "system": self.get_system_metrics().to_dict()
        }
