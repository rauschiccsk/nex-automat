"""MuFis webhook — fire-and-forget GET notification on order changes.

When a new order is created or an existing order status changes,
we notify MuFis via HTTP GET so it can call our getOrder endpoint
immediately instead of waiting for its hourly poll cycle.

Configuration (env vars):
    MUFIS_WEBHOOK_URL — Full URL provided by MuFis (GET)
    MUFIS_DRY_RUN    — "true" to skip actual HTTP call (default: true)
"""

import logging
import os

import httpx

logger = logging.getLogger(__name__)

MUFIS_WEBHOOK_URL = os.getenv("MUFIS_WEBHOOK_URL", "")
MUFIS_DRY_RUN = os.getenv("MUFIS_DRY_RUN", "true").lower() == "true"


async def notify_mufis_order_change():
    """Send GET request to MuFis webhook URL to notify about order changes.

    This is fire-and-forget — failures are logged as warnings but never
    block the caller or raise exceptions.
    """
    if not MUFIS_WEBHOOK_URL:
        logger.debug("MUFIS_WEBHOOK_URL not configured, skipping webhook")
        return

    if MUFIS_DRY_RUN:
        logger.info("DRY-RUN: Would notify MuFis webhook at %s", MUFIS_WEBHOOK_URL)
        return

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(MUFIS_WEBHOOK_URL)
            logger.info("MuFis webhook notified: %s", response.status_code)
    except Exception as e:
        logger.warning("MuFis webhook failed (non-blocking): %s", e)
