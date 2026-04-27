"""
NEX Manager API — FastAPI Backend
==================================

REST API backend for the NEX Manager Electron desktop application.
Provides JWT authentication, user management, module permissions,
and dynamic module registration from module_registry.yaml.

Infrastructure routers (always loaded):
- /api/auth/*              — JWT authentication
- /api/modules/*           — module DB registry (existing)
- /api/partners/*          — legacy partner endpoints
- /api/system/modules      — YAML-based module registry endpoint
- /health                  — health check

Business-module routers (loaded dynamically from module_registry.yaml):
- Active modules  → router MUST exist (hard error if missing)
- Planned modules → router may not exist yet (warning logged, skipped)
"""

import logging
import os
import subprocess
import sys
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# ---------------------------------------------------------------------------
# Logging — ensure all application loggers emit to stdout at INFO level.
# Without this, only uvicorn's own access-log appears; our logger.info()
# calls in eshop.router / eshop.mufis_webhook stay silent (root=WARNING).
# ---------------------------------------------------------------------------
_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

# Infrastructure routers — always loaded, not managed by YAML registry
from auth.router import router as auth_router
from modules.router import router as modules_router
from partners.router import router as partners_router
from registry.module_registry import get_registry
from system.router import router as system_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="NEX Manager API",
    description="Backend API for NEX Manager — authentication, users, permissions",
    version="0.2.0",
)

# ---------------------------------------------------------------------------
# CORS — allow all origins for Electron desktop client
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip — large list responses (e.g. /api/pab/partners with 255k rows = ~80MB
# uncompressed JSON) compress to ~8-10MB before leaving the backend, cutting
# customer perceived load time from ~25s to ~5s on remote browsers.
# minimum_size=1024 skips compression for tiny payloads (no benefit).
app.add_middleware(GZipMiddleware, minimum_size=1024)

# ---------------------------------------------------------------------------
# INFRASTRUCTURE ROUTERS (hardcoded — not business modules)
# ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(modules_router)
app.include_router(partners_router)
app.include_router(system_router)

# ---------------------------------------------------------------------------
# DYNAMIC BUSINESS-MODULE ROUTERS (from module_registry.yaml)
# ---------------------------------------------------------------------------
_registry = get_registry()
_loaded_routers: list[str] = []

for mod in _registry.modules:
    router_obj = _registry.import_router(mod)
    if router_obj is not None:
        app.include_router(router_obj)
        _loaded_routers.append(mod.key)
        logger.info("Registered router for module '%s' (%s)", mod.key, mod.status)

logger.info(
    "Dynamic router registration complete: %d/%d loaded (%s)",
    len(_loaded_routers),
    len(_registry.modules),
    ", ".join(_loaded_routers),
)


# ---------------------------------------------------------------------------
# HEALTH / ROOT
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    """Service information."""
    registry = get_registry()
    return {
        "service": "NEX Manager API",
        "version": "0.2.0",
        "status": "running",
        "registry_version": registry.version,
        "modules_loaded": len(_loaded_routers),
        "modules_total": len(registry.modules),
        "endpoints": {
            "auth_login": "/api/auth/login",
            "auth_refresh": "/api/auth/refresh",
            "auth_me": "/api/auth/me",
            "auth_change_password": "/api/auth/change-password",
            "users_list": "/api/users",
            "users_detail": "/api/users/{id}",
            "users_create": "/api/users",
            "users_update": "/api/users/{id}",
            "users_password": "/api/users/{id}/password",
            "partners_list": "/api/partners",
            "partners_detail": "/api/partners/{id}",
            "partners_create": "/api/partners",
            "partners_update": "/api/partners/{id}",
            "pab_catalog_list": "/api/pab/partners",
            "pab_catalog_detail": "/api/pab/partners/{id}",
            "pab_catalog_create": "/api/pab/partners",
            "pab_catalog_update": "/api/pab/partners/{id}",
            "pab_catalog_delete": "/api/pab/partners/{id}",
            "migration_categories": "/api/migration/categories",
            "migration_run": "/api/migration/run",
            "migration_stats": "/api/migration/stats",
            "modules_list": "/api/modules",
            "modules_by_category": "/api/modules/by-category",
            "modules_detail": "/api/modules/{code}",
            "system_modules": "/api/system/modules",
            "eshop_products": "/api/eshop/products",
            "eshop_orders": "/api/eshop/orders",
            "eshop_admin_orders": "/api/eshop/admin/orders",
            "eshop_admin_products": "/api/eshop/admin/products",
            "eshop_admin_tenants": "/api/eshop/admin/tenants",
            "eshop_mufis": "/api/eshop/mufis/*",
            "docs": "/docs",
            "health": "/health",
        },
    }


@app.get("/health")
def health():
    """Health check for monitoring systems."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


def _get_git_version() -> str:
    """Get application version from ENV or git describe."""
    # Primary: read from ENV (set by Docker build args)
    env_version = os.environ.get("APP_VERSION")
    if env_version and env_version != "dev":
        return env_version

    # Fallback: git describe (local dev only)
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0.2.0"


def _get_git_commit() -> str:
    """Get git commit hash from ENV or git rev-parse."""
    # Primary: read from ENV
    env_commit = os.environ.get("APP_COMMIT")
    if env_commit and env_commit != "unknown":
        return env_commit

    # Fallback: git rev-parse (local dev only)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


@app.get("/api/version")
def get_version():
    """Return current version from git tag + commit hash."""
    return {"version": _get_git_version(), "commit": _get_git_commit()}


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    from nex_config.services import NEX_MANAGER_API_PORT

    print("=" * 60)
    print("  NEX Manager API v0.2.0")
    print(f"  Docs: http://localhost:{NEX_MANAGER_API_PORT}/docs")
    print(f"  Modules: {len(_loaded_routers)}/{len(_registry.modules)} loaded")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=NEX_MANAGER_API_PORT, log_level="info")
