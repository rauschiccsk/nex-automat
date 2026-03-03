"""Shared test fixtures for NEX Manager API tests."""

import os
import sys

import pytest

# Add the app root to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class FakeCursor:
    """Fake database cursor that returns configurable results.

    By default, permission queries (bool_or) return True so RBAC passes.
    Tests can override fetchone/fetchall via the connection object.
    """

    def __init__(self):
        self.executed_queries: list[tuple] = []
        self._fetchone_results: list = []
        self._fetchall_results: list = []
        self._fetchone_index = 0
        self._fetchall_index = 0

    def execute(self, query: str, params=None):
        self.executed_queries.append((query, params or ()))

    def fetchone(self):
        if self._fetchone_index < len(self._fetchone_results):
            result = self._fetchone_results[self._fetchone_index]
            self._fetchone_index += 1
            return result
        return None

    def fetchall(self):
        if self._fetchall_index < len(self._fetchall_results):
            result = self._fetchall_results[self._fetchall_index]
            self._fetchall_index += 1
            return result
        return []


class FakeConnection:
    """Fake database connection with a shared cursor."""

    def __init__(self):
        self._cursor = FakeCursor()
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

    def set_fetchone_sequence(self, results: list):
        """Set a sequence of fetchone results.

        Each call to cursor().fetchone() returns the next item.
        """
        self._cursor._fetchone_results = results
        self._cursor._fetchone_index = 0

    def set_fetchall_sequence(self, results: list):
        """Set a sequence of fetchall results."""
        self._cursor._fetchall_results = results
        self._cursor._fetchall_index = 0

    def reset_cursor(self):
        """Reset cursor state for new test flow."""
        self._cursor.executed_queries.clear()
        self._cursor._fetchone_index = 0
        self._cursor._fetchall_index = 0


@pytest.fixture
def fake_db():
    """Provide a fake database connection."""
    return FakeConnection()


@pytest.fixture
def fake_user():
    """Provide a fake authenticated user dict."""
    return {
        "user_id": 1,
        "login_name": "admin",
        "full_name": "Admin User",
        "email": "admin@test.sk",
        "is_active": True,
    }


@pytest.fixture
def client(fake_db, fake_user):
    """Test client with mocked DB and auth (all permissions granted).

    The RBAC check in ``_check_permission`` calls ``get_current_user``
    (overridden) then queries ``group_module_permissions`` via ``get_db``.
    We must ensure the permission query returns ``(True,)`` so endpoints
    don't return 403.

    Strategy: override ``get_current_user`` to skip JWT and override
    the actual ``_check_permission`` closures by overriding each one
    registered on the routes.  A simpler approach: monkeypatch
    ``require_permission`` at import time.

    Simplest approach that works: override ``get_current_user`` so it
    returns fake_user, AND ensure ``get_db`` yields a fake_db whose
    permission query returns True.  BUT we can't intercept which
    fetchone belongs to which query inside the same cursor.

    Best approach: override each ``_check_permission`` dependency that
    was registered on the app.  We find them by scanning app.routes.
    """
    from fastapi.testclient import TestClient
    from database import get_db
    from auth.dependencies import get_current_user, require_permission
    from main import app

    def override_get_db():
        yield fake_db

    async def override_current_user():
        return fake_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    # Override every _check_permission closure that was created by
    # require_permission().  They are registered as Depends() on routes.
    # We find them by looking at sub-dependencies that reference
    # get_current_user.
    # Scan all routes and override permission dependencies.
    _permission_deps = set()
    for route in getattr(app, "routes", []):
        if hasattr(route, "dependant") and hasattr(route.dependant, "dependencies"):
            for dep in route.dependant.dependencies:
                call = getattr(dep, "call", None)
                if call and getattr(call, "__name__", "") == "_check_permission":
                    _permission_deps.add(call)

    async def _mock_check_permission(
        current_user=None,
        db=None,
    ):
        return fake_user

    for dep_fn in _permission_deps:
        app.dependency_overrides[dep_fn] = _mock_check_permission

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def client_no_auth(fake_db):
    """Test client with mocked DB but NO auth override (for RBAC tests)."""
    from fastapi.testclient import TestClient
    from database import get_db
    from main import app

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
