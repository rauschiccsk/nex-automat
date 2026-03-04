"""Unit tests for Migration (MIG) module — categories, batches, stats, mappings, run, reset, RBAC.

13+ test cases covering:
1. Get categories — 200, returns 9 categories
2. Get categories — dependency levels (PAB/GSC level=0, STK level=1)
3. Get category detail — 200, PAB has correct source_tables
4. Get category not found — 404
5. Get categories — can_run logic (PAB can_run=True, STK can_run=False)
6. Get category batches — 200, empty list
7. Get stats — 200, total_categories=9
8. Get mappings — 200, empty list
9. Run migration — 501 Not Implemented for PAB
10. Run migration — 400 for unknown category
11. Run migration — 400 for dependencies not met (STK)
12. Reset category — changes status to pending
13. Migration RBAC — 403 without permission
"""

import os
import sys
from datetime import datetime, timezone

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# 1. Get categories — 200, returns 9 categories
# ---------------------------------------------------------------------------
def test_get_categories(client, fake_db):
    """GET /api/migration/categories — 200, returns 9 categories."""
    # Each _build_category_response call queries migration_category_status
    # for the category itself + each of its dependencies.
    # 9 categories, each has varying number of deps.
    # We return pending status for all.
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        # All status queries return pending row
        return ("pending", 0, None, None, None)

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.get("/api/migration/categories")

    assert resp.status_code == 200
    data = resp.json()
    assert "categories" in data
    assert data["total"] == 9
    assert data["pending"] == 9
    assert data["completed"] == 0
    assert data["failed"] == 0
    assert len(data["categories"]) == 9


# ---------------------------------------------------------------------------
# 2. Get categories — dependency levels
# ---------------------------------------------------------------------------
def test_get_categories_dependency_levels(client, fake_db):
    """GET /api/migration/categories — PAB/GSC at level 0, STK at level 1."""
    fake_db.cursor().fetchone = lambda: ("pending", 0, None, None, None)

    resp = client.get("/api/migration/categories")

    assert resp.status_code == 200
    cats = {c["code"]: c for c in resp.json()["categories"]}

    # Level 0 — no dependencies
    assert cats["PAB"]["level"] == 0
    assert cats["GSC"]["level"] == 0

    # Level 1 — depends on level 0 categories
    assert cats["STK"]["level"] == 1
    assert cats["ICB"]["level"] == 1
    assert cats["ISB"]["level"] == 1
    assert cats["OBJ"]["level"] == 1
    assert cats["DOD"]["level"] == 1

    # Level 2 — TSH depends on PAB, GSC, STK
    assert cats["TSH"]["level"] == 2

    # Level 3 — PAYJRN depends on ICB, ISB
    assert cats["PAYJRN"]["level"] == 2


# ---------------------------------------------------------------------------
# 3. Get category detail — 200, PAB has correct source_tables
# ---------------------------------------------------------------------------
def test_get_category_detail(client, fake_db):
    """GET /api/migration/categories/PAB — 200 with correct data."""
    # PAB has no dependencies, so only 1 fetchone for PAB status
    fake_db.cursor().fetchone = lambda: ("pending", 0, None, None, None)

    resp = client.get("/api/migration/categories/PAB")

    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "PAB"
    assert data["name"] == "Katalóg partnerov"
    assert "PAB" in data["source_tables"]
    assert "PAYLST" in data["source_tables"]
    assert "partners" in data["target_tables"]
    assert data["dependency_codes"] == []
    assert data["level"] == 0


# ---------------------------------------------------------------------------
# 4. Get category not found — 404
# ---------------------------------------------------------------------------
def test_get_category_not_found(client, fake_db):
    """GET /api/migration/categories/UNKNOWN — 404."""
    resp = client.get("/api/migration/categories/UNKNOWN")

    assert resp.status_code == 404
    assert "neexistuje" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 5. Get categories — can_run logic
# ---------------------------------------------------------------------------
def test_get_categories_can_run(client, fake_db):
    """GET /api/migration/categories — PAB can_run=True, STK can_run=False."""
    # All categories return pending
    fake_db.cursor().fetchone = lambda: ("pending", 0, None, None, None)

    resp = client.get("/api/migration/categories")

    assert resp.status_code == 200
    cats = {c["code"]: c for c in resp.json()["categories"]}

    # PAB has no dependencies → can_run=True
    assert cats["PAB"]["can_run"] is True
    assert cats["PAB"]["blocked_by"] == []

    # STK depends on GSC (pending) → can_run=False
    assert cats["STK"]["can_run"] is False
    assert "GSC" in cats["STK"]["blocked_by"]


# ---------------------------------------------------------------------------
# 6. Get category batches — 200, empty list
# ---------------------------------------------------------------------------
def test_get_category_batches_empty(client, fake_db):
    """GET /api/migration/categories/PAB/batches — 200, empty list."""
    fake_db.cursor().fetchall = lambda: []

    resp = client.get("/api/migration/categories/PAB/batches")

    assert resp.status_code == 200
    data = resp.json()
    assert data["batches"] == []
    assert data["total"] == 0


# ---------------------------------------------------------------------------
# 7. Get stats — 200, total_categories=9
# ---------------------------------------------------------------------------
def test_get_stats(client, fake_db):
    """GET /api/migration/stats — 200 with correct totals."""
    call_count = 0

    def mock_fetchall():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # status GROUP BY query
            return [("pending", 9)]
        return []

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            # SUM(record_count)
            return (0,)
        if call_count == 3:
            # COUNT batches
            return (0,)
        if call_count == 4:
            # MAX(last_migrated_at)
            return (None,)
        return None

    fake_db.cursor().fetchall = mock_fetchall
    fake_db.cursor().fetchone = mock_fetchone

    resp = client.get("/api/migration/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data["total_categories"] == 9
    assert data["pending_categories"] == 9
    assert data["completed_categories"] == 0
    assert data["total_records_migrated"] == 0
    assert data["total_batches"] == 0


# ---------------------------------------------------------------------------
# 8. Get mappings — 200, empty list
# ---------------------------------------------------------------------------
def test_get_mappings_empty(client, fake_db):
    """GET /api/migration/mappings/PAB — 200, empty list."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        return (0,)  # count = 0

    fake_db.cursor().fetchone = mock_fetchone
    fake_db.cursor().fetchall = lambda: []

    resp = client.get("/api/migration/mappings/PAB")

    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1


# ---------------------------------------------------------------------------
# 9. Run migration — 501 Not Implemented for PAB
# ---------------------------------------------------------------------------
def test_run_migration_not_implemented(client, fake_db):
    """POST /api/migration/run — 501 for PAB (no deps to check)."""
    call_count = 0

    def mock_fetchone():
        nonlocal call_count
        call_count += 1
        # No running batch check → None
        return None

    fake_db.cursor().fetchone = mock_fetchone

    resp = client.post(
        "/api/migration/run",
        json={"category": "PAB", "dry_run": False},
    )

    assert resp.status_code == 501
    assert "not yet implemented" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 10. Run migration — 400 for unknown category
# ---------------------------------------------------------------------------
def test_run_migration_unknown_category(client, fake_db):
    """POST /api/migration/run — 400 for non-existent category."""
    resp = client.post(
        "/api/migration/run",
        json={"category": "NOPE"},
    )

    assert resp.status_code == 400
    assert "Neznáma" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 11. Run migration — 400 for dependencies not met (STK)
# ---------------------------------------------------------------------------
def test_run_migration_dependencies_not_met(client, fake_db):
    """POST /api/migration/run — 400 for STK when GSC is pending."""
    # STK depends on GSC — _get_category_status returns pending for GSC
    fake_db.cursor().fetchone = lambda: ("pending", 0, None, None, None)

    resp = client.post(
        "/api/migration/run",
        json={"category": "STK"},
    )

    assert resp.status_code == 400
    assert (
        "závislosti" in resp.json()["detail"].lower() or "GSC" in resp.json()["detail"]
    )


# ---------------------------------------------------------------------------
# 12. Reset category — changes status to pending
# ---------------------------------------------------------------------------
def test_reset_category(client, fake_db):
    """POST /api/migration/categories/PAB/reset — 200, resets to pending."""
    resp = client.post("/api/migration/categories/PAB/reset")

    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "PAB"
    assert "pending" in data["message"]

    # Verify UPDATE was executed
    queries = fake_db.cursor().executed_queries
    update_queries = [q for q, _ in queries if "UPDATE migration_category_status" in q]
    assert len(update_queries) >= 1


# ---------------------------------------------------------------------------
# 13. Migration RBAC — 403 without permission
# ---------------------------------------------------------------------------
def test_migration_rbac(client_no_auth):
    """GET /api/migration/categories — without auth token returns 401/403."""
    resp = client_no_auth.get("/api/migration/categories")

    # Without auth header, HTTPBearer raises 403
    assert resp.status_code in (401, 403)
