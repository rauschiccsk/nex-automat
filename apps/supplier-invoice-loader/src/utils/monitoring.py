# -*- coding: utf-8 -*-
"""
Supplier Invoice Loader - Monitoring & Metrics
Tracks application health, uptime, and processing statistics
"""

import time

# Optional psutil dependency
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class Metrics:
    """Application metrics tracker"""

    def __init__(self):
        self.start_time = time.time()
        self.requests_total = 0
        self.requests_success = 0
        self.requests_failed = 0
        self.invoices_processed = 0
        self.invoices_failed = 0

        # Backward compatibility alias
        self.api_requests = 0

    def get_uptime(self) -> float:
        """Get application uptime in seconds"""
        return time.time() - self.start_time

    def get_system_metrics(self) -> dict:
        """Get system metrics (CPU, memory) if psutil available"""
        if PSUTIL_AVAILABLE:
            try:
                return {
                    "cpu_percent": psutil.cpu_percent(interval=0.1),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage("/").percent,
                }
            except Exception:
                pass

        # Fallback without psutil
        return {
            "cpu_percent": None,
            "memory_percent": None,
            "disk_percent": None,
        }

    def increment_request(self, success: bool = True):
        """Increment request counter"""
        self.requests_total += 1
        self.api_requests += 1  # Backward compatibility
        if success:
            self.requests_success += 1
        else:
            self.requests_failed += 1

    def increment_invoice(self, success: bool = True):
        """Increment invoice processing counter"""
        if success:
            self.invoices_processed += 1
        else:
            self.invoices_failed += 1

    def get_stats(self) -> dict:
        """Get all statistics"""
        return {
            "uptime_seconds": self.get_uptime(),
            "requests": {
                "total": self.requests_total,
                "success": self.requests_success,
                "failed": self.requests_failed,
            },
            "invoices": {
                "processed": self.invoices_processed,
                "failed": self.invoices_failed,
            },
            "system": self.get_system_metrics(),
            "psutil_available": PSUTIL_AVAILABLE,
        }

    def reset(self):
        """Reset all counters (for testing)"""
        self.requests_total = 0
        self.requests_success = 0
        self.requests_failed = 0
        self.invoices_processed = 0
        self.invoices_failed = 0
        self.api_requests = 0  # Backward compatibility


# Global metrics instance
_metrics = Metrics()


def get_metrics() -> Metrics:
    """Get global metrics instance"""
    return _metrics


def reset_metrics():
    """Reset global metrics (for testing)"""
    _metrics.reset()


def check_storage_health() -> dict:
    """
    Check storage directories health

    Returns:
        dict with storage health status
    """
    try:
        from src.utils import config

        pdf_dir_exists = config.PDF_DIR.exists()
        xml_dir_exists = config.XML_DIR.exists()

        # Create directories if they don't exist
        if not pdf_dir_exists:
            config.PDF_DIR.mkdir(parents=True, exist_ok=True)
            pdf_dir_exists = True

        if not xml_dir_exists:
            config.XML_DIR.mkdir(parents=True, exist_ok=True)
            xml_dir_exists = True

        storage_healthy = pdf_dir_exists and xml_dir_exists

        return {
            "pdf_dir_exists": pdf_dir_exists,
            "xml_dir_exists": xml_dir_exists,
            "storage_healthy": storage_healthy,
        }

    except Exception as e:
        return {
            "pdf_dir_exists": False,
            "xml_dir_exists": False,
            "storage_healthy": False,
            "error": str(e),
        }
