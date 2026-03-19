"""Unit testy pre ComgateClient — 7 testov.

Tests:
  1. test_comgate_client_init_production — production mode → base_url bez /test/
  2. test_comgate_client_init_test — test mode → base_url s /test/
  3. test_comgate_parse_response — parsing OK response
  4. test_comgate_parse_response_error — parsing error response
  5. test_comgate_verify_callback_valid — verify_callback s correct secret
  6. test_comgate_verify_callback_invalid — verify_callback s wrong secret
  7. test_comgate_create_payment_price_conversion — _convert_to_cents
"""

import os
import sys

# Set JWT_SECRET_KEY before any app imports (required by nex_config.security)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-comgate-tests")

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eshop.comgate import ComgateClient


# ---------------------------------------------------------------------------
# 1. Init — production mode
# ---------------------------------------------------------------------------


def test_comgate_client_init_production():
    """Test: production mode → base_url bez /test/."""
    client = ComgateClient(
        merchant_id="12345",
        secret="test_secret",
        test_mode=False,
    )
    assert client.base_url == "https://payments.comgate.cz/v1.0"
    assert client.merchant_id == "12345"
    assert client.secret == "test_secret"
    assert client.test_mode is False


# ---------------------------------------------------------------------------
# 2. Init — test mode
# ---------------------------------------------------------------------------


def test_comgate_client_init_test():
    """Test: test mode uses same base_url; test flag is sent as data param."""
    client = ComgateClient(
        merchant_id="12345",
        secret="test_secret",
        test_mode=True,
    )
    # Comgate does NOT use /test/ URL prefix; test mode is a request parameter
    assert client.base_url == "https://payments.comgate.cz/v1.0"
    assert client.test_mode is True


# ---------------------------------------------------------------------------
# 3. Parse response — OK
# ---------------------------------------------------------------------------


def test_comgate_parse_response():
    """Test: parsing Comgate response (OK)."""
    client = ComgateClient("12345", "secret")

    response_text = "code=0&message=OK&transId=ABC123&redirect=https://example.com"
    parsed = client._parse_response(response_text)

    assert parsed["code"] == "0"
    assert parsed["message"] == "OK"
    assert parsed["transId"] == "ABC123"
    assert parsed["redirect"] == "https://example.com"


# ---------------------------------------------------------------------------
# 4. Parse response — error
# ---------------------------------------------------------------------------


def test_comgate_parse_response_error():
    """Test: parsing Comgate error response."""
    client = ComgateClient("12345", "secret")

    response_text = "code=1100&message=unknown+error"
    parsed = client._parse_response(response_text)

    assert parsed["code"] == "1100"
    assert parsed["message"] == "unknown error"


# ---------------------------------------------------------------------------
# 5. Verify callback — valid secret
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_comgate_verify_callback_valid():
    """Test: verify_callback s správnym secretom."""
    client = ComgateClient("12345", "correct_secret")

    result = await client.verify_callback(
        merchant="12345",
        test="true",
        price="1000",
        curr="CZK",
        label="ORDER-001",
        refId="ORDER-001",
        transId="ABCD-1234",
        secret="correct_secret",
        email="test@test.sk",
        status="PAID",
    )

    assert result is True


# ---------------------------------------------------------------------------
# 6. Verify callback — invalid secret
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_comgate_verify_callback_invalid():
    """Test: verify_callback so zlým secretom."""
    client = ComgateClient("12345", "correct_secret")

    result = await client.verify_callback(
        merchant="12345",
        test="true",
        price="1000",
        curr="CZK",
        label="ORDER-001",
        refId="ORDER-001",
        transId="ABCD-1234",
        secret="wrong_secret",
        email="test@test.sk",
        status="PAID",
    )

    assert result is False


# ---------------------------------------------------------------------------
# 7. Price conversion — _convert_to_cents
# ---------------------------------------------------------------------------


def test_comgate_create_payment_price_conversion():
    """Test: konverzia EUR na haliere (cents)."""
    client = ComgateClient("12345", "secret")

    # 9.90 EUR → 990 halierov
    assert client._convert_to_cents(9.90) == 990

    # 19.80 EUR → 1980 halierov
    assert client._convert_to_cents(19.80) == 1980

    # 0.01 EUR → 1 halier
    assert client._convert_to_cents(0.01) == 1

    # 100.00 EUR → 10000 halierov
    assert client._convert_to_cents(100.00) == 10000

    # 39.90 EUR → 3990 halierov
    assert client._convert_to_cents(39.90) == 3990
