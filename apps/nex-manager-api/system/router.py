"""System router — YAML-based module registry endpoint.

This endpoint does NOT require JWT authentication so the frontend can
fetch the module list before login (e.g. for splash screen or diagnostics).
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from registry.module_registry import get_registry

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/modules")
def list_system_modules(
    status: str | None = Query(
        None,
        description=("Filter by status: 'active', 'planned', or omit for all"),
    ),
):
    """Return modules and categories from the YAML registry.

    No authentication required — this is infrastructure metadata.

    Query params:
        status: "active" | "planned" | None (all)

    Response:
        {
            "version": "1.0",
            "categories": [...],
            "modules": [...],
            "total": 24
        }
    """
    registry = get_registry()

    # Categories
    categories = [
        {
            "key": c.key,
            "name": c.name,
            "order": c.order,
        }
        for c in registry.categories
    ]

    # Modules — optionally filtered by status
    if status == "active":
        modules = registry.active_modules()
    elif status == "planned":
        modules = registry.planned_modules()
    else:
        modules = registry.modules

    module_list = [
        {
            "key": m.key,
            "name": m.name,
            "category": m.category,
            "icon": m.icon,
            "order": m.order,
            "status": m.status,
            "backend_router": m.backend_router,
            "frontend_module": m.frontend_module,
            "roles": m.roles,
        }
        for m in modules
    ]

    return {
        "version": registry.version,
        "categories": categories,
        "modules": module_list,
        "total": len(module_list),
    }
