"""Tests for the YAML-based module registry.

Covers:
1.  YAML loads without errors
2.  USR and PAB (and MIG) are active
3.  Remaining modules are planned
4.  Every module has all required fields
5.  Every module references a valid category
6.  No duplicate order numbers within a category
7.  Active modules have an existing router file
8.  Roles contain only valid values (ri, ha, shu)
9.  GET /api/system/modules returns correct data
10. Registry contains exactly 24 modules (per INVENTORY.md)
"""

import os
import sys
from pathlib import Path

import pytest

# Ensure app root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Set JWT_SECRET_KEY before any app imports (required by nex_config.security)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-registry-tests")

# Point MODULE_REGISTRY_YAML to the repo-root file so tests work
# regardless of working directory.
_REPO_ROOT = (
    Path(__file__).resolve().parents[3]
)  # tests → nex-manager-api → apps → nex-automat-src
_YAML_PATH = _REPO_ROOT / "module_registry.yaml"
os.environ["MODULE_REGISTRY_YAML"] = str(_YAML_PATH)

from registry.module_registry import ModuleRegistry, reload_registry  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def registry() -> ModuleRegistry:
    """Load the module registry once for the whole test module."""
    return reload_registry()


# ---------------------------------------------------------------------------
# 1. YAML loads without errors
# ---------------------------------------------------------------------------


def test_load_registry(registry: ModuleRegistry):
    """YAML file loads successfully and registry is populated."""
    assert registry is not None
    assert len(registry.modules) > 0
    assert len(registry.categories) > 0
    assert registry.version == "1.0"


# ---------------------------------------------------------------------------
# 2. USR, PAB, MIG are active
# ---------------------------------------------------------------------------


def test_active_modules(registry: ModuleRegistry):
    """USR, PAB and MIG must be marked as active."""
    active_keys = {m.key for m in registry.active_modules()}
    assert "USR" in active_keys, "USR should be active"
    assert "PAB" in active_keys, "PAB should be active"
    assert "MIG" in active_keys, "MIG should be active"


# ---------------------------------------------------------------------------
# 3. Remaining modules are planned
# ---------------------------------------------------------------------------


def test_planned_modules(registry: ModuleRegistry):
    """All non-active modules should be 'planned'."""
    active_keys = {m.key for m in registry.active_modules()}
    for mod in registry.modules:
        if mod.key not in active_keys:
            assert mod.status == "planned", (
                f"Module '{mod.key}' should be 'planned', got '{mod.status}'"
            )


# ---------------------------------------------------------------------------
# 4. All required fields present
# ---------------------------------------------------------------------------


def test_module_info_fields(registry: ModuleRegistry):
    """Every module must have all required fields with non-empty values."""
    required_fields = [
        "key",
        "name",
        "category",
        "icon",
        "order",
        "status",
        "backend_router",
        "frontend_module",
        "roles",
    ]
    for mod in registry.modules:
        for field_name in required_fields:
            value = getattr(mod, field_name, None)
            assert value is not None, f"Module '{mod.key}' missing field '{field_name}'"
            if isinstance(value, str):
                assert len(value) > 0, f"Module '{mod.key}' has empty '{field_name}'"
            elif isinstance(value, list):
                assert len(value) > 0, (
                    f"Module '{mod.key}' has empty '{field_name}' list"
                )


# ---------------------------------------------------------------------------
# 5. Every module references a valid category
# ---------------------------------------------------------------------------


def test_categories_defined(registry: ModuleRegistry):
    """Every module's category must exist in the categories list."""
    category_keys = {c.key for c in registry.categories}
    for mod in registry.modules:
        assert mod.category in category_keys, (
            f"Module '{mod.key}' references unknown category '{mod.category}'. "
            f"Known: {category_keys}"
        )


# ---------------------------------------------------------------------------
# 6. No duplicate order within a category
# ---------------------------------------------------------------------------


def test_unique_orders(registry: ModuleRegistry):
    """Within each category, order numbers must be unique."""
    by_category: dict[str, list[int]] = {}
    for mod in registry.modules:
        by_category.setdefault(mod.category, []).append(mod.order)

    for cat, orders in by_category.items():
        assert len(orders) == len(set(orders)), (
            f"Duplicate order numbers in category '{cat}': {orders}"
        )


# ---------------------------------------------------------------------------
# 7. Active modules have an existing router file
# ---------------------------------------------------------------------------


def test_active_module_has_router(registry: ModuleRegistry):
    """Active modules must have a resolvable router file on disk."""
    for mod in registry.active_modules():
        resolved = registry.resolve_router_import(mod.backend_router)
        assert resolved is not None, (
            f"Active module '{mod.key}' — router not found for "
            f"backend_router='{mod.backend_router}'"
        )


# ---------------------------------------------------------------------------
# 8. Roles are valid
# ---------------------------------------------------------------------------


def test_roles_valid(registry: ModuleRegistry):
    """Every role must be one of: ri, ha, shu."""
    valid_roles = {"ri", "ha", "shu"}
    for mod in registry.modules:
        for role in mod.roles:
            assert role in valid_roles, (
                f"Module '{mod.key}' has invalid role '{role}'. Valid: {valid_roles}"
            )


# ---------------------------------------------------------------------------
# 9. GET /api/system/modules endpoint
# ---------------------------------------------------------------------------


def test_api_modules_endpoint():
    """GET /api/system/modules returns correct structure."""
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)
    response = client.get("/api/system/modules")
    assert response.status_code == 200

    data = response.json()
    assert "version" in data
    assert "categories" in data
    assert "modules" in data
    assert "total" in data
    assert data["total"] == len(data["modules"])
    assert data["total"] >= 24

    # Test status filter
    active_response = client.get("/api/system/modules?status=active")
    assert active_response.status_code == 200
    active_data = active_response.json()
    for mod in active_data["modules"]:
        assert mod["status"] == "active"

    planned_response = client.get("/api/system/modules?status=planned")
    assert planned_response.status_code == 200
    planned_data = planned_response.json()
    for mod in planned_data["modules"]:
        assert mod["status"] == "planned"


# ---------------------------------------------------------------------------
# 10. Registry contains exactly 24 modules (per INVENTORY.md)
# ---------------------------------------------------------------------------


def test_all_24_modules_in_registry(registry: ModuleRegistry):
    """Registry must contain exactly 24 modules as defined in INVENTORY.md."""
    expected_keys = {
        "USR",
        "MIG",
        "GRP",
        "SET",
        "AUD",
        "PAB",
        "GSC",
        "STK",
        "IMB",
        "OMB",
        "PMB",
        "INV",
        "ICB",
        "PON",
        "ODB",
        "DOD",
        "ISB",
        "OBJ",
        "JRN",
        "ACT",
        "VTR",
        "UCT",
        "POK",
        "UZV",
    }
    actual_keys = {m.key for m in registry.modules}

    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys

    assert len(missing) == 0, f"Missing modules: {missing}"
    assert len(extra) == 0, f"Extra modules: {extra}"
    assert len(registry.modules) == 24
