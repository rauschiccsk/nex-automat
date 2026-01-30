"""
Health check and metrics endpoints.
"""

import time
from datetime import datetime

from fastapi import APIRouter, Response

from src.core.config import settings

router = APIRouter()

# Start time for uptime calculation
START_TIME = time.time()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns service status for monitoring systems.
    """
    uptime_seconds = int(time.time() - START_TIME)

    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version,
        "uptime_seconds": uptime_seconds,
        "timestamp": datetime.now().isoformat(),
        "btrieve_path": str(settings.btrieve_path),
    }


@router.get("/metrics")
async def prometheus_metrics():
    """
    Prometheus metrics endpoint.

    Returns metrics in Prometheus format.
    """
    uptime_seconds = int(time.time() - START_TIME)

    metrics = []

    # Service info
    metrics.append(f"# HELP btrieve_loader_info Service information")
    metrics.append(f"# TYPE btrieve_loader_info gauge")
    metrics.append(f'btrieve_loader_info{{version="{settings.api_version}"}} 1')

    # Uptime
    metrics.append(f"# HELP btrieve_loader_uptime_seconds Service uptime in seconds")
    metrics.append(f"# TYPE btrieve_loader_uptime_seconds counter")
    metrics.append(f"btrieve_loader_uptime_seconds {uptime_seconds}")

    return Response(content="\n".join(metrics), media_type="text/plain")


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.

    Checks if service is ready to accept requests.
    """
    # TODO: Add Btrieve connection check
    return {
        "ready": True,
        "timestamp": datetime.now().isoformat(),
    }
