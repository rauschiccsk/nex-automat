"""Unit testy pre eshop/utils.py — generate_order_number().

Tests:
  1. test_order_number_first_in_year — first order → seq 00001
  2. test_order_number_increments — existing max → next seq
  3. test_order_number_global_sequence — two tenants, same prefix → sequential (no dups)
  4. test_order_number_different_prefix — different prefixes → independent sequences
  5. test_query_is_global — verify SQL has no tenant_id filter
"""

import os
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

# Add app root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from eshop.utils import generate_order_number


class FakeCursor:
    """Minimal fake cursor for unit-testing generate_order_number."""

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

    def cursor(self):
        return self._cursor

    def set_fetchone_sequence(self, results: list):
        self._cursor._fetchone_results = results
        self._cursor._fetchone_index = 0


# ---------------------------------------------------------------------------
# Test 1: First order in year → 00001
# ---------------------------------------------------------------------------


def test_order_number_first_in_year():
    """First order with prefix EM in year → EM-YYYY-00001."""
    conn = FakeConn()
    # Only 1 fetchone call — for SELECT MAX (advisory lock has no fetchone)
    conn.set_fetchone_sequence(
        [
            (None,),  # SELECT MAX → no existing orders
        ]
    )

    result = generate_order_number(tenant_id=1, brand_name="EMCenter", conn=conn)

    year = datetime.now().year
    assert result == f"EM-{year}-00001"


# ---------------------------------------------------------------------------
# Test 2: Increments from existing max
# ---------------------------------------------------------------------------


def test_order_number_increments():
    """Existing max EM-YYYY-00042 → next is EM-YYYY-00043."""
    year = datetime.now().year
    conn = FakeConn()
    conn.set_fetchone_sequence(
        [
            (f"EM-{year}-00042",),  # SELECT MAX → existing max
        ]
    )

    result = generate_order_number(tenant_id=1, brand_name="EMCenter", conn=conn)

    assert result == f"EM-{year}-00043"


# ---------------------------------------------------------------------------
# Test 3: Global sequence — two tenants, same prefix → no duplicate
# ---------------------------------------------------------------------------


def test_order_number_global_sequence():
    """Tenant 1 prefix EM → 00001, Tenant 2 prefix EM → 00002 (global seq)."""
    year = datetime.now().year

    # Tenant 1: no existing orders
    conn1 = FakeConn()
    conn1.set_fetchone_sequence(
        [
            (None,),  # SELECT MAX → nothing
        ]
    )
    order_num_1 = generate_order_number(tenant_id=1, brand_name="EMCenter", conn=conn1)
    assert order_num_1 == f"EM-{year}-00001"

    # Tenant 2: MAX query now sees tenant 1's order globally
    conn2 = FakeConn()
    conn2.set_fetchone_sequence(
        [
            (f"EM-{year}-00001",),  # SELECT MAX → tenant 1's order visible globally
        ]
    )
    order_num_2 = generate_order_number(tenant_id=2, brand_name="EMCenter", conn=conn2)
    assert order_num_2 == f"EM-{year}-00002"


# ---------------------------------------------------------------------------
# Test 4: Different prefixes → independent sequences
# ---------------------------------------------------------------------------


def test_order_number_different_prefix():
    """Prefix EM at 00005, prefix NO starts at 00001 — independent."""
    year = datetime.now().year

    conn = FakeConn()
    conn.set_fetchone_sequence(
        [
            (None,),  # SELECT MAX for NO- → nothing
        ]
    )
    result = generate_order_number(tenant_id=2, brand_name="NOComgate", conn=conn)
    assert result == f"NO-{year}-00001"


# ---------------------------------------------------------------------------
# Test 5: Verify the SQL query does NOT contain tenant_id filter
# ---------------------------------------------------------------------------


def test_query_is_global():
    """The MAX query must NOT filter by tenant_id — it must be global."""
    conn = FakeConn()
    conn.set_fetchone_sequence(
        [
            (None,),  # SELECT MAX
        ]
    )

    generate_order_number(tenant_id=1, brand_name="EMCenter", conn=conn)

    # Find the SELECT MAX query
    queries = conn._cursor.executed_queries
    max_query = next(
        (q for q in queries if "SELECT MAX" in q[0]),
        None,
    )
    assert max_query is not None, "SELECT MAX query must be executed"

    sql = max_query[0]
    params = max_query[1]

    # Must NOT have tenant_id in WHERE clause
    assert "tenant_id" not in sql, (
        f"MAX query must be global (no tenant_id filter), got: {sql}"
    )

    # Must have LIKE pattern only
    assert "LIKE" in sql, f"MAX query must filter by LIKE pattern, got: {sql}"

    # Params should be a single-element tuple (pattern only, no tenant_id)
    assert len(params) == 1, f"Expected 1 param (pattern), got {len(params)}: {params}"
