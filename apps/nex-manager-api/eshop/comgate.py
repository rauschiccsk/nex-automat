"""Comgate payment gateway client.

Comgate API docs: https://help.comgate.cz/docs/api-protocol
All requests use application/x-www-form-urlencoded for both request and response.
"""

import asyncio
import hmac
import logging
import urllib.parse
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)


class ComgateError(Exception):
    """Comgate API error with code and message."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Comgate error {code}: {message}")


class ComgateClient:
    """Comgate payment gateway client.

    Uses stdlib urllib since httpx/aiohttp are not available.
    Async methods use asyncio.to_thread for non-blocking I/O.
    """

    BASE_URL = "https://payments.comgate.cz/v1.0"

    def __init__(self, merchant_id: str, secret: str, test_mode: bool = True):
        self.merchant_id = merchant_id
        self.secret = secret
        self.test_mode = test_mode

    def _parse_response(self, body: str) -> dict:
        """Parse Comgate URL-encoded response into dict.

        Comgate returns key=value pairs separated by &.
        Example: code=0&message=OK&transId=AB12-CD34-EF56&redirect=https://...
        """
        parsed = urllib.parse.parse_qs(body, keep_blank_values=True)
        # parse_qs returns lists; flatten to single values
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    def _post_sync(self, endpoint: str, data: dict) -> dict:
        """Synchronous POST to Comgate API."""
        url = f"{self.BASE_URL}/{endpoint}"
        encoded = urllib.parse.urlencode(data).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")

        return self._parse_response(body)

    async def create_payment(
        self,
        price_cents: int,
        currency: str,
        order_number: str,
        customer_email: str,
        label: str,
        country: str,
        lang: str,
    ) -> dict:
        """Create payment via Comgate API.

        Args:
            price_cents: Price in cents (integer). E.g. 3990 for 39.90 EUR.
            currency: ISO 4217 currency code (EUR, CZK, HUF).
            order_number: Internal order reference (refId).
            customer_email: Customer email for payment notification.
            label: Payment label (max 16 characters).
            country: Customer country code (SK, CZ, HU).
            lang: UI language (sk, cs, hu, en).

        Returns:
            dict with keys: transId, redirect_url

        Raises:
            ComgateError: If Comgate returns error code != 0.
        """
        data = {
            "merchant": self.merchant_id,
            "test": "true" if self.test_mode else "false",
            "country": country,
            "price": price_cents,
            "curr": currency,
            "label": label[:16],
            "refId": order_number,
            "email": customer_email,
            "lang": lang,
            "method": "ALL",
            "prepareOnly": "true",
            "secret": self.secret,
        }

        result = await asyncio.to_thread(self._post_sync, "create", data)

        code = int(result.get("code", -1))
        if code != 0:
            message = result.get("message", "Unknown error")
            raise ComgateError(code, message)

        return {
            "transId": result["transId"],
            "redirect_url": result["redirect"],
        }

    async def verify_callback(
        self,
        merchant: str,
        test: str,
        price: str,
        curr: str,
        label: str,
        refId: str,
        transId: str,
        secret: str,
        email: str,
        status: str,
    ) -> bool:
        """Verify callback authenticity via constant-time secret comparison.

        Args:
            All parameters as received from Comgate callback POST.

        Returns:
            True if secret matches, False otherwise.
        """
        return hmac.compare_digest(secret, self.secret)

    async def check_status(self, trans_id: str) -> dict:
        """Check payment status via Comgate API.

        Args:
            trans_id: Comgate transaction ID.

        Returns:
            dict with payment status fields.

        Raises:
            ComgateError: If Comgate returns error code != 0.
        """
        data = {
            "merchant": self.merchant_id,
            "transId": trans_id,
            "secret": self.secret,
        }

        result = await asyncio.to_thread(self._post_sync, "status", data)

        code = int(result.get("code", -1))
        if code != 0:
            message = result.get("message", "Unknown error")
            raise ComgateError(code, message)

        return result


def get_comgate_client(tenant: dict) -> Optional[ComgateClient]:
    """Create ComgateClient from tenant configuration.

    Returns None if Comgate is not configured for the tenant.
    Does NOT raise HTTPException — caller decides what to do.

    Args:
        tenant: Tenant dict with optional comgate_* keys.

    Returns:
        ComgateClient instance or None.
    """
    if not tenant.get("comgate_merchant_id") or not tenant.get("comgate_secret"):
        return None
    return ComgateClient(
        merchant_id=tenant["comgate_merchant_id"],
        secret=tenant["comgate_secret"],
        test_mode=tenant.get("comgate_test_mode", True),
    )
