"""
Unit tests for NEX Manager API — Users module and auth change-password.

Tests cover:
- GET /api/users (list, filters, search)
- GET /api/users/{id} (detail, not found)
- POST /api/users (create, duplicate, validation)
- PUT /api/users/{id} (update, not found, group update)
- PUT /api/users/{id}/password (admin password change)
- PUT /api/auth/change-password (self password change)
- RBAC permission checks
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add nex-manager-api to path so we can import its modules
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "apps" / "nex-manager-api")
)

from fastapi.testclient import TestClient

from auth.dependencies import get_current_user
from database import get_db
from main import app

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FAKE_USER = {
    "user_id": 1,
    "login_name": "admin",
    "full_name": "Administr\u00e1tor",
    "email": "admin@icc.sk",
    "is_active": True,
}

FAKE_USER_ROW = (
    1,
    "admin",
    "Administr\u00e1tor",
    "admin@icc.sk",
    True,
    datetime(2024, 1, 1, tzinfo=timezone.utc),
    datetime(2024, 1, 1, tzinfo=timezone.utc),
    datetime(2024, 1, 1, tzinfo=timezone.utc),
)

FAKE_GROUP_ROWS = [(1, "Administr\u00e1tori")]

BCRYPT_HASH = "$2b$12$x5AGAyWA/Td4/EGpv3PGUOSGpz1vl3aimwMgoqh6Z21iUngaqJVD."

# Permission check result — True means granted
PERM_GRANTED = (True,)
PERM_DENIED = (False,)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_db():
    """Mock pg8000 connection + cursor."""
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


@pytest.fixture()
def client(mock_db):
    """TestClient with mocked DB and auth — permission always GRANTED.

    The require_permission dependency does:
    1. get_current_user (overridden to return FAKE_USER)
    2. cursor.execute + cursor.fetchone for permission check

    We override get_current_user and get_db.  The cursor.fetchone
    side_effect list must start with PERM_GRANTED for the RBAC check,
    followed by endpoint-specific values.
    """
    conn, _ = mock_db

    app.dependency_overrides[get_db] = lambda: conn
    app.dependency_overrides[get_current_user] = lambda: FAKE_USER

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture()
def client_no_auth(mock_db):
    """TestClient with NO auth override — Bearer token required, will 401."""
    conn, _ = mock_db
    app.dependency_overrides[get_db] = lambda: conn
    # Do NOT override get_current_user -> requires real Bearer token
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_no_permission(mock_db):
    """TestClient where RBAC always denies.

    get_current_user is overridden, but the permission query returns False.
    """
    conn, cursor = mock_db
    cursor.fetchone.return_value = PERM_DENIED

    app.dependency_overrides[get_db] = lambda: conn
    app.dependency_overrides[get_current_user] = lambda: FAKE_USER

    yield TestClient(app)

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _set_cursor_sequence(cursor, values: list):
    """Set fetchone side_effect.  First value is always PERM_GRANTED."""
    cursor.fetchone.side_effect = [PERM_GRANTED] + values
    # fetchall: we build a parallel list
    fetchall_values = []
    for v in values:
        if isinstance(v, list):
            fetchall_values.append(v)
        elif v is None:
            fetchall_values.append([])
        else:
            fetchall_values.append([v])
    cursor.fetchall.side_effect = fetchall_values


# ============================================================================
# TEST: List users
# ============================================================================


class TestListUsers:
    """GET /api/users tests."""

    def test_list_users_success(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        cursor.fetchall.side_effect = [
            [FAKE_USER_ROW],  # main query
            FAKE_GROUP_ROWS,  # groups for user 1
        ]
        resp = client.get("/api/users")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["users"][0]["login_name"] == "admin"
        assert "password_hash" not in json.dumps(data)

    def test_list_users_with_group_filter(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        cursor.fetchall.side_effect = [
            [FAKE_USER_ROW],
            FAKE_GROUP_ROWS,
        ]
        resp = client.get("/api/users?group_id=1")
        assert resp.status_code == 200

    def test_list_users_with_is_active_filter(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        cursor.fetchall.side_effect = [[]]  # no users
        resp = client.get("/api/users?is_active=false")
        assert resp.status_code == 200
        assert resp.json()["total"] == 0

    def test_list_users_with_search(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        cursor.fetchall.side_effect = [
            [FAKE_USER_ROW],
            FAKE_GROUP_ROWS,
        ]
        resp = client.get("/api/users?search=admin")
        assert resp.status_code == 200
        assert resp.json()["total"] == 1


# ============================================================================
# TEST: Get user detail
# ============================================================================


class TestGetUser:
    """GET /api/users/{user_id} tests."""

    def test_get_user_success(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, FAKE_USER_ROW]
        cursor.fetchall.side_effect = [FAKE_GROUP_ROWS]
        resp = client.get("/api/users/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == 1
        assert data["login_name"] == "admin"
        assert data["updated_at"] is not None

    def test_get_user_not_found(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, None]
        resp = client.get("/api/users/999")
        assert resp.status_code == 404
        assert "nebol n\u00e1jden" in resp.json()["detail"]


# ============================================================================
# TEST: Create user
# ============================================================================


class TestCreateUser:
    """POST /api/users tests."""

    def test_create_user_success(self, client, mock_db):
        _, cursor = mock_db
        new_row = (
            2,
            "newuser",
            "New User",
            "new@icc.sk",
            True,
            None,
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        # PERM_GRANTED, uniqueness check (None=not found), INSERT RETURNING
        cursor.fetchone.side_effect = [PERM_GRANTED, None, new_row]
        resp = client.post(
            "/api/users",
            json={
                "username": "newuser",
                "full_name": "New User",
                "email": "new@icc.sk",
                "password": "secret123",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["login_name"] == "newuser"
        assert "password_hash" not in json.dumps(data)

    def test_create_user_duplicate_username(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, (1,)]  # username exists
        resp = client.post(
            "/api/users",
            json={
                "username": "admin",
                "full_name": "Dup",
                "email": "dup@icc.sk",
                "password": "secret123",
            },
        )
        assert resp.status_code == 409
        assert "u\u017e existuje" in resp.json()["detail"]

    def test_create_user_short_password(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        resp = client.post(
            "/api/users",
            json={
                "username": "short",
                "full_name": "Short Pw",
                "email": "short@icc.sk",
                "password": "abc",
            },
        )
        assert resp.status_code == 422

    def test_create_user_invalid_email(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        resp = client.post(
            "/api/users",
            json={
                "username": "bademail",
                "full_name": "Bad Email",
                "email": "notanemail",
                "password": "secret123",
            },
        )
        assert resp.status_code == 422

    def test_create_user_with_group_ids(self, client, mock_db):
        _, cursor = mock_db
        new_row = (
            3,
            "grouped",
            "Grouped User",
            "g@icc.sk",
            True,
            None,
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        cursor.fetchone.side_effect = [PERM_GRANTED, None, new_row]
        cursor.fetchall.side_effect = [FAKE_GROUP_ROWS]  # get groups after insert
        resp = client.post(
            "/api/users",
            json={
                "username": "grouped",
                "full_name": "Grouped User",
                "email": "g@icc.sk",
                "password": "secret123",
                "group_ids": [1, 2],
            },
        )
        assert resp.status_code == 201


# ============================================================================
# TEST: Update user
# ============================================================================


class TestUpdateUser:
    """PUT /api/users/{user_id} tests."""

    def test_update_user_success(self, client, mock_db):
        _, cursor = mock_db
        updated_row = (
            1,
            "admin",
            "Updated Name",
            "upd@icc.sk",
            True,
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 2, 1, tzinfo=timezone.utc),
        )
        # PERM, check exists, UPDATE(no fetch), audit(no fetch), fetch updated
        cursor.fetchone.side_effect = [
            PERM_GRANTED,
            ("admin",),
            updated_row,
        ]
        cursor.fetchall.side_effect = [FAKE_GROUP_ROWS]
        resp = client.put(
            "/api/users/1",
            json={"full_name": "Updated Name", "email": "upd@icc.sk"},
        )
        assert resp.status_code == 200
        assert resp.json()["full_name"] == "Updated Name"

    def test_update_user_not_found(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, None]
        resp = client.put("/api/users/999", json={"full_name": "X"})
        assert resp.status_code == 404

    def test_update_user_with_group_ids(self, client, mock_db):
        _, cursor = mock_db
        updated_row = (
            1,
            "admin",
            "Admin",
            "admin@icc.sk",
            True,
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 2, 1, tzinfo=timezone.utc),
        )
        cursor.fetchone.side_effect = [
            PERM_GRANTED,
            ("admin",),
            updated_row,
        ]
        cursor.fetchall.side_effect = [FAKE_GROUP_ROWS]
        resp = client.put("/api/users/1", json={"group_ids": [1]})
        assert resp.status_code == 200


# ============================================================================
# TEST: Admin password change
# ============================================================================


class TestAdminPasswordChange:
    """PUT /api/users/{user_id}/password tests."""

    def test_admin_change_password_success(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, ("admin",)]
        resp = client.put(
            "/api/users/1/password",
            json={"new_password": "newsecret123"},
        )
        assert resp.status_code == 200
        assert "zmenen" in resp.json()["message"]

    def test_admin_change_password_not_found(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED, None]
        resp = client.put(
            "/api/users/999/password",
            json={"new_password": "newsecret123"},
        )
        assert resp.status_code == 404

    def test_admin_change_password_short(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [PERM_GRANTED]
        resp = client.put(
            "/api/users/1/password",
            json={"new_password": "abc"},
        )
        assert resp.status_code == 422


# ============================================================================
# TEST: Self password change
# ============================================================================


class TestSelfPasswordChange:
    """PUT /api/auth/change-password tests."""

    def test_self_change_password_success(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(BCRYPT_HASH,)]
        with (
            patch("auth.router.verify_password", return_value=True),
            patch("auth.router.hash_password", return_value=BCRYPT_HASH),
        ):
            resp = client.put(
                "/api/auth/change-password",
                json={
                    "current_password": "admin",
                    "new_password": "newsecret123",
                },
            )
        assert resp.status_code == 200
        assert "zmenen" in resp.json()["message"]

    def test_self_change_wrong_current_password(self, client, mock_db):
        _, cursor = mock_db
        cursor.fetchone.side_effect = [(BCRYPT_HASH,)]
        with patch("auth.router.verify_password", return_value=False):
            resp = client.put(
                "/api/auth/change-password",
                json={
                    "current_password": "wrongpassword",
                    "new_password": "newsecret123",
                },
            )
        assert resp.status_code == 401
        assert "aktu\u00e1lne heslo" in resp.json()["detail"]

    def test_self_change_short_new_password(self, client, mock_db):
        resp = client.put(
            "/api/auth/change-password",
            json={
                "current_password": "admin",
                "new_password": "ab",
            },
        )
        assert resp.status_code == 422


# ============================================================================
# TEST: RBAC — permission denied
# ============================================================================


class TestRBAC:
    """RBAC permission denied tests."""

    def test_list_users_no_permission(self, client_no_permission, mock_db):
        resp = client_no_permission.get("/api/users")
        assert resp.status_code == 403

    def test_create_user_no_permission(self, client_no_permission, mock_db):
        resp = client_no_permission.post(
            "/api/users",
            json={
                "username": "noperm",
                "full_name": "No Perm",
                "email": "no@icc.sk",
                "password": "secret123",
            },
        )
        assert resp.status_code == 403
