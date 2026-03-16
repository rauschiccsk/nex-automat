"""MuFis API authentication — IP whitelist + API-KEY dependency.

Doplnkový bezpečnostný layer k existujúcemu get_tenant_by_mufis_key().
Použitie:  tenant = Depends(verify_mufis_access)  na MuFis endpointoch.

Env vars:
    MUFIS_ALLOWED_IPS  — comma-separated whitelist (e.g. "1.2.3.4,5.6.7.8")
    MUFIS_IP_CHECK_ENABLED — "true" to enforce, "false" to skip (default: true)
"""

import logging
import os
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from database import get_db

from .dependencies import get_tenant_by_mufis_key

logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    """Extract real client IP from nginx reverse proxy.

    Priority: X-Forwarded-For (first IP) > X-Real-IP > request.client.host
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For: client, proxy1, proxy2
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "unknown"


def _is_ip_check_enabled() -> bool:
    """Check if IP whitelist enforcement is enabled."""
    return os.environ.get("MUFIS_IP_CHECK_ENABLED", "true").lower() == "true"


def _get_allowed_ips() -> list[str]:
    """Get allowed IP list from env var."""
    raw = os.environ.get("MUFIS_ALLOWED_IPS", "")
    return [ip.strip() for ip in raw.split(",") if ip.strip()]


async def verify_mufis_ip(request: Request) -> str:
    """Verify client IP is whitelisted for MuFis endpoints.

    Returns:
        Client IP on success

    Raises:
        HTTPException 403 if IP not whitelisted and check is enabled
    """
    client_ip = get_client_ip(request)
    endpoint = request.url.path

    if not _is_ip_check_enabled():
        logger.debug("MuFis IP check DISABLED: ip=%s, endpoint=%s", client_ip, endpoint)
        return client_ip

    allowed_ips = _get_allowed_ips()

    if not allowed_ips:
        # No whitelist configured — allow all with warning
        logger.warning("MuFis IP check: MUFIS_ALLOWED_IPS is empty — allowing all IPs")
        return client_ip

    if client_ip not in allowed_ips:
        logger.warning(
            "MuFis auth FAIL: ip=%s, endpoint=%s, reason='ip_not_whitelisted'",
            client_ip,
            endpoint,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: IP not whitelisted",
        )

    logger.info("MuFis IP check OK: ip=%s, endpoint=%s", client_ip, endpoint)
    return client_ip


async def verify_mufis_access(
    request: Request,
    tenant: dict = Depends(get_tenant_by_mufis_key),
    db=Depends(get_db),
) -> dict:
    """Combined MuFis auth: IP whitelist + API-KEY tenant resolution.

    Use this as a drop-in replacement for get_tenant_by_mufis_key
    when IP whitelisting is needed.

    Returns:
        Tenant dict (same as get_tenant_by_mufis_key) enriched with client_ip
    """
    client_ip = await verify_mufis_ip(request)
    tenant["client_ip"] = client_ip
    return tenant


# Type annotations for FastAPI Depends
MufisIp = Annotated[str, Depends(verify_mufis_ip)]
MufisAccess = Annotated[dict, Depends(verify_mufis_access)]
