"""Unit testy pre payment_callback guard logic.

Tests:
  1. test_cancelled_ignored_when_paid — CANCELLED callback ignored for paid order
  2. test_cancelled_ignored_when_shipped — CANCELLED callback ignored for shipped order
  3. test_cancelled_ignored_when_delivered — CANCELLED callback ignored for delivered order
  4. test_cancelled_processed_when_pending — CANCELLED callback processed for pending order
  5. test_stale_transid_ignored — stale transId ignored for non-PAID callback
  6. test_paid_callback_accepts_different_transid — PAID callback NOT blocked by stale transId check
"""

import asyncio
import hmac
import os
import sys
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

# Add app root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from eshop.router import payment_callback


class FakeCursor:
    """Minimal fake cursor for unit-testing payment_callback."""

    def __init__(self):
        self._fetchone_results: list = []
        self._fetchone_index = 0
        self.executed_queries: list[tuple] = []

    def execute(self, query: str, params=None):
        self.executed_queries.append((query, params or ()))

    def fetchone(self):
        if self._fetchone_index < len(self._fetchone_results):
            result = self._fetchone_results[self._fetchone_index]
            self._fetchone_index += 1
            return result
        return None


class FakeConn:
    """Minimal fake connection."""

    def __init__(self):
        self._cursor = FakeCursor()
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def set_fetchone_sequence(self, results: list):
        self._cursor._fetchone_results = results
        self._cursor._fetchone_index = 0


# Shared test constants
SECRET = "test-secret-123"
MERCHANT_ID = "12345"
ORDER_TOTAL = Decimal("19.90")
PRICE_CENTS = str(int(ORDER_TOTAL * 100))  # "1990"
CURRENCY = "EUR"
ORDER_NUMBER = "EM-2026-00099"
TRANS_ID = "ABC-CURRENT"
STALE_TRANS_ID = "XYZ-OLD-SESSION"


def _run(coro):
    """Run async coroutine in sync test."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


def _make_conn(
    payment_status="pending",
    order_status="new",
    stored_transaction_id=None,
):
    """Create FakeConn pre-loaded with order + tenant fetchone results."""
    conn = FakeConn()
    conn.set_fetchone_sequence(
        [
            # 1. Order lookup (SELECT order_id, tenant_id, total_amount_vat,
            #    currency, payment_status, status, comgate_transaction_id)
            (1, 1, ORDER_TOTAL, CURRENCY, payment_status, order_status, stored_transaction_id),
            # 2. Tenant lookup (SELECT tenant_id, comgate_merchant_id, comgate_secret)
            (1, MERCHANT_ID, SECRET),
        ]
    )
    return conn


def _call_callback(conn, status_val="CANCELLED", transId=TRANS_ID):
    """Call payment_callback with valid params."""
    return _run(
        payment_callback(
            merchant=MERCHANT_ID,
            test="true",
            price=PRICE_CENTS,
            curr=CURRENCY,
            label="Test order",
            refId=ORDER_NUMBER,
            transId=transId,
            secret=SECRET,
            email="test@test.com",
            status_val=status_val,
            db=conn,
        )
    )


# ---------------------------------------------------------------------------
# Test 1: CANCELLED ignored when order already paid
# ---------------------------------------------------------------------------


def test_cancelled_ignored_when_paid():
    """CANCELLED callback for paid order → return OK, no DB update."""
    conn = _make_conn(payment_status="paid", stored_transaction_id=TRANS_ID)
    response = _call_callback(conn, status_val="CANCELLED", transId=TRANS_ID)

    assert response.body == b"code=0&message=OK"
    assert not conn.committed
    # No UPDATE executed (only SELECT queries)
    updates = [q for q, _ in conn._cursor.executed_queries if "UPDATE" in q]
    assert len(updates) == 0


# ---------------------------------------------------------------------------
# Test 2: CANCELLED ignored when order shipped
# ---------------------------------------------------------------------------


def test_cancelled_ignored_when_shipped():
    """CANCELLED callback for shipped order → return OK, no DB update."""
    conn = _make_conn(payment_status="shipped", stored_transaction_id=TRANS_ID)
    response = _call_callback(conn, status_val="CANCELLED", transId=TRANS_ID)

    assert response.body == b"code=0&message=OK"
    assert not conn.committed
    updates = [q for q, _ in conn._cursor.executed_queries if "UPDATE" in q]
    assert len(updates) == 0


# ---------------------------------------------------------------------------
# Test 3: CANCELLED ignored when order delivered
# ---------------------------------------------------------------------------


def test_cancelled_ignored_when_delivered():
    """CANCELLED callback for delivered order → return OK, no DB update."""
    conn = _make_conn(payment_status="delivered", stored_transaction_id=TRANS_ID)
    response = _call_callback(conn, status_val="CANCELLED", transId=TRANS_ID)

    assert response.body == b"code=0&message=OK"
    assert not conn.committed
    updates = [q for q, _ in conn._cursor.executed_queries if "UPDATE" in q]
    assert len(updates) == 0


# ---------------------------------------------------------------------------
# Test 4: CANCELLED processed normally when payment is pending
# ---------------------------------------------------------------------------


def test_cancelled_processed_when_pending():
    """CANCELLED callback for pending order → should process (UPDATE executed)."""
    conn = _make_conn(payment_status="pending", order_status="new")
    response = _call_callback(conn, status_val="CANCELLED", transId=TRANS_ID)

    assert response.body == b"code=0&message=OK"
    assert conn.committed
    updates = [q for q, _ in conn._cursor.executed_queries if "UPDATE" in q]
    assert len(updates) >= 1, "CANCELLED for pending order should trigger UPDATE"


# ---------------------------------------------------------------------------
# Test 5: Stale transId ignored for CANCELLED
# ---------------------------------------------------------------------------


def test_stale_transid_ignored():
    """CANCELLED with stale transId (different from stored) → ignored."""
    conn = _make_conn(
        payment_status="pending",
        stored_transaction_id=TRANS_ID,
    )
    response = _call_callback(conn, status_val="CANCELLED", transId=STALE_TRANS_ID)

    assert response.body == b"code=0&message=OK"
    assert not conn.committed
    updates = [q for q, _ in conn._cursor.executed_queries if "UPDATE" in q]
    assert len(updates) == 0


# ---------------------------------------------------------------------------
# Test 6: PAID callback accepts different transId (allows new payment session)
# ---------------------------------------------------------------------------


def test_paid_callback_accepts_different_transid():
    """PAID with different transId → should process (new payment session)."""
    conn = _make_conn(
        payment_status="pending",
        order_status="new",
        stored_transaction_id=STALE_TRANS_ID,
    )
    response = _call_callback(conn, status_val="PAID", transId=TRANS_ID)

    assert response.body == b"code=0&message=OK"
    assert conn.committed
    updates = [q for q, _ in conn._cursor.executed_queries if "UPDATE" in q]
    assert len(updates) >= 1, "PAID callback should update even with different transId"
