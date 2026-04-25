"""Tests for sessions module (Phase 1.1) — list + termination endpoints.

Auth integration with sid+tv JWT claims is in Phase 1.2 (auth/*); these tests
exercise the session domain endpoints directly with mocked auth.
"""

from __future__ import annotations

from datetime import datetime, timezone


def test_list_all_sessions_empty(client, fake_db, fake_user):
    """GET /api/sessions returns empty list when no rows."""
    fake_db.set_fetchall_sequence([[]])  # SELECT returns no rows
    response = client.get("/api/sessions")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["sessions"] == []


def test_list_all_sessions_with_rows(client, fake_db, fake_user):
    """GET /api/sessions returns rows mapped to SessionResponse."""
    now = datetime(2026, 4, 25, 16, 0, 0, tzinfo=timezone.utc)
    fake_db.set_fetchall_sequence(
        [
            [
                (
                    1,
                    fake_user["user_id"],
                    "admin",
                    "Admin User",
                    "Mozilla/5.0",
                    "127.0.0.1",
                    now,
                    now,
                ),
            ],
        ]
    )
    response = client.get("/api/sessions")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["sessions"][0]["session_id"] == 1
    assert body["sessions"][0]["login_name"] == "admin"


def test_terminate_my_other_sessions_bumps_token_version(client, fake_db, fake_user):
    """DELETE /api/sessions/me/all bumps token_version for caller's other sessions."""
    response = client.delete("/api/sessions/me/all")
    assert response.status_code == 200
    body = response.json()
    assert "ukončené" in body["message"]
    # Verify UPDATE was executed with token_version + 1
    update_queries = [
        q for q, _ in fake_db._cursor.executed_queries if "UPDATE user_sessions" in q
    ]
    assert len(update_queries) == 1
    assert "token_version + 1" in update_queries[0]


def test_terminate_user_sessions_admin_bumps_all(client, fake_db, fake_user):
    """DELETE /api/sessions/user/{id}/all bumps token_version for that user."""
    response = client.delete("/api/sessions/user/42/all")
    assert response.status_code == 200
    body = response.json()
    assert "42" in body["message"]


def test_terminate_session_not_found(client, fake_db, fake_user):
    """DELETE /api/sessions/{id} returns 404 if session doesn't exist."""
    fake_db.set_fetchone_sequence([None])  # session lookup returns None
    response = client.delete("/api/sessions/999")
    assert response.status_code == 404
    assert "nebola nájdená" in response.json()["detail"]


def test_terminate_own_session_succeeds(client, fake_db, fake_user):
    """DELETE /api/sessions/{id} succeeds if session belongs to caller."""
    fake_db.set_fetchone_sequence(
        [
            (fake_user["user_id"],),  # session.user_id matches caller
        ]
    )
    response = client.delete("/api/sessions/5")
    assert response.status_code == 200
    assert "ukončená" in response.json()["message"]
