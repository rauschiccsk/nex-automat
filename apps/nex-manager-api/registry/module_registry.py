"""
Module Registry — loads module definitions from module_registry.yaml.

The YAML file in the repository root is the single source of truth for all
NEX Manager business and system modules.

Usage:
    from registry.module_registry import get_registry

    registry = get_registry()
    active = registry.active_modules()
    planned = registry.planned_modules()
"""

from __future__ import annotations

import importlib
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class CategoryDef:
    """Category definition from YAML."""

    key: str
    name: str
    order: int


@dataclass
class ModuleDef:
    """Single module definition from YAML."""

    key: str
    name: str
    category: str
    icon: str
    order: int
    status: str
    backend_router: str
    frontend_module: str
    roles: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class ModuleRegistry:
    """In-memory registry of all modules loaded from YAML."""

    REQUIRED_MODULE_FIELDS = (
        "key",
        "name",
        "category",
        "icon",
        "order",
        "status",
        "backend_router",
        "frontend_module",
        "roles",
    )
    VALID_STATUSES = ("active", "planned")
    VALID_ROLES = ("ri", "ha", "shu")

    def __init__(self, yaml_path: str | Path) -> None:
        self.yaml_path = Path(yaml_path)
        self._categories: list[CategoryDef] = []
        self._modules: list[ModuleDef] = []
        self._raw: dict[str, Any] = {}
        self._load()

    # -- loading --------------------------------------------------------

    def _load(self) -> None:
        if not self.yaml_path.exists():
            raise FileNotFoundError(f"Module registry file not found: {self.yaml_path}")

        with open(self.yaml_path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        if not isinstance(data, dict):
            raise ValueError("module_registry.yaml must be a YAML mapping")

        self._raw = data

        # Categories
        for cat in data.get("categories", []):
            self._categories.append(
                CategoryDef(
                    key=cat["key"],
                    name=cat["name"],
                    order=cat["order"],
                )
            )

        # Modules
        category_keys = {c.key for c in self._categories}
        for mod in data.get("modules", []):
            # Validate required fields
            for fld in self.REQUIRED_MODULE_FIELDS:
                if fld not in mod:
                    raise ValueError(
                        f"Module '{mod.get('key', '???')}' missing field: {fld}"
                    )
            if mod["status"] not in self.VALID_STATUSES:
                raise ValueError(
                    f"Module '{mod['key']}' has invalid status: {mod['status']}"
                )
            if mod["category"] not in category_keys:
                raise ValueError(
                    f"Module '{mod['key']}' references unknown category: "
                    f"{mod['category']}"
                )
            for role in mod["roles"]:
                if role not in self.VALID_ROLES:
                    raise ValueError(f"Module '{mod['key']}' has invalid role: {role}")

            self._modules.append(
                ModuleDef(
                    key=mod["key"],
                    name=mod["name"],
                    category=mod["category"],
                    icon=mod["icon"],
                    order=mod["order"],
                    status=mod["status"],
                    backend_router=mod["backend_router"],
                    frontend_module=mod["frontend_module"],
                    roles=mod["roles"],
                )
            )

        logger.info(
            "Module registry loaded: %d categories, %d modules (%d active)",
            len(self._categories),
            len(self._modules),
            len(self.active_modules()),
        )

    # -- queries --------------------------------------------------------

    @property
    def version(self) -> str:
        return self._raw.get("version", "unknown")

    @property
    def categories(self) -> list[CategoryDef]:
        return list(self._categories)

    @property
    def modules(self) -> list[ModuleDef]:
        return list(self._modules)

    def active_modules(self) -> list[ModuleDef]:
        return [m for m in self._modules if m.status == "active"]

    def planned_modules(self) -> list[ModuleDef]:
        return [m for m in self._modules if m.status == "planned"]

    def get_module(self, key: str) -> ModuleDef | None:
        for m in self._modules:
            if m.key == key:
                return m
        return None

    def modules_by_category(self) -> dict[str, list[ModuleDef]]:
        """Return modules grouped by category, ordered by category order."""
        cat_order = {c.key: c.order for c in self._categories}
        groups: dict[str, list[ModuleDef]] = {}
        for m in self._modules:
            groups.setdefault(m.category, []).append(m)
        # Sort by category order
        return dict(sorted(groups.items(), key=lambda x: cat_order.get(x[0], 999)))

    def get_category(self, key: str) -> CategoryDef | None:
        for c in self._categories:
            if c.key == key:
                return c
        return None

    # -- router resolution ---------------------------------------------------

    def resolve_router_import(self, backend_router: str) -> tuple[str, str] | None:
        """Resolve backend_router value to (module_import_path, attribute).

        Handles both patterns found in the codebase:
        - Single-file module: "users" → import from "users.router" attr "router"
        - Directory module: "pab" → import from "pab.router" attr "router"

        Both patterns in nex-manager-api use the same convention:
          <module_name>/router.py  with ``router = APIRouter(...)``

        Returns None if the router file does not exist.
        """
        # The backend app root is the parent of *this* file's package
        app_root = Path(__file__).resolve().parent.parent

        # Pattern: <backend_router>/router.py (directory with router.py)
        router_dir = app_root / backend_router
        if router_dir.is_dir():
            router_file = router_dir / "router.py"
            if router_file.exists():
                return f"{backend_router}.router", "router"
            # Check __init__.py for router attribute
            init_file = router_dir / "__init__.py"
            if init_file.exists():
                return backend_router, "router"

        # Pattern: <backend_router>.py (single file — not currently used but
        # supported for future flexibility)
        single_file = app_root / f"{backend_router}.py"
        if single_file.exists():
            return backend_router, "router"

        return None

    def import_router(self, mod: ModuleDef) -> Any:
        """Import and return the FastAPI router object for a module.

        Raises ImportError if the module is active and router cannot be loaded.
        Logs a warning for planned modules.
        """
        resolved = self.resolve_router_import(mod.backend_router)
        if resolved is None:
            if mod.status == "active":
                raise ImportError(
                    f"Active module '{mod.key}' — router not found for "
                    f"backend_router='{mod.backend_router}'"
                )
            logger.warning(
                "Planned module '%s' — router not found for "
                "backend_router='%s', skipping",
                mod.key,
                mod.backend_router,
            )
            return None

        module_path, attr_name = resolved
        try:
            py_module = importlib.import_module(module_path)
            router_obj = getattr(py_module, attr_name)
            logger.debug(
                "Loaded router for module '%s' from %s.%s",
                mod.key,
                module_path,
                attr_name,
            )
            return router_obj
        except Exception:
            if mod.status == "active":
                raise
            logger.warning(
                "Planned module '%s' — failed to import %s.%s, skipping",
                mod.key,
                module_path,
                attr_name,
                exc_info=True,
            )
            return None


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_registry: ModuleRegistry | None = None


def _default_yaml_path() -> Path:
    """Resolve the YAML path.

    Priority:
    1. MODULE_REGISTRY_YAML env var
    2. /app/module_registry.yaml  (Docker: COPY to /app/)
    3. Repo root (5 levels up from this file for dev):
       registry/module_registry.py → nex-manager-api → apps → nex-automat-src
    """
    env_path = os.environ.get("MODULE_REGISTRY_YAML")
    if env_path:
        return Path(env_path)

    # Docker layout: /app/module_registry.yaml
    docker_path = Path("/app/module_registry.yaml")
    if docker_path.exists():
        return docker_path

    # Dev layout: walk up to repo root
    here = Path(__file__).resolve().parent  # registry/
    app_root = here.parent  # nex-manager-api/
    apps_dir = app_root.parent  # apps/
    repo_root = apps_dir.parent  # nex-automat-src/
    return repo_root / "module_registry.yaml"


def get_registry() -> ModuleRegistry:
    """Return the singleton ModuleRegistry, loading it on first call."""
    global _registry
    if _registry is None:
        yaml_path = _default_yaml_path()
        _registry = ModuleRegistry(yaml_path)
    return _registry


def reload_registry() -> ModuleRegistry:
    """Force-reload the registry from YAML (useful for tests)."""
    global _registry
    yaml_path = _default_yaml_path()
    _registry = ModuleRegistry(yaml_path)
    return _registry
