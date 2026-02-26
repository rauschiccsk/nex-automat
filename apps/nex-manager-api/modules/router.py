"""Module registry API endpoints."""

from collections import OrderedDict

from fastapi import APIRouter, Depends, HTTPException, Query

from auth.dependencies import get_current_user
from database import get_db

from .schemas import (
    ModuleCategoryGroup,
    ModuleListResponse,
    ModuleResponse,
    ModulesByCategoryResponse,
)

router = APIRouter(prefix="/api/modules", tags=["modules"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MODULE_COLUMNS = (
    "module_id, module_code, module_name, "
    "category::text, icon, module_type::text, "
    "is_mock, sort_order, is_active, created_at, updated_at"
)


def _row_to_module(row: tuple) -> ModuleResponse:
    """Map a database row to a ModuleResponse."""
    return ModuleResponse(
        module_id=row[0],
        module_code=row[1],
        module_name=row[2],
        category=row[3],
        icon=row[4],
        module_type=row[5],
        is_mock=row[6],
        sort_order=row[7],
        is_active=row[8],
        created_at=row[9],
        updated_at=row[10],
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=ModuleListResponse)
def list_modules(
    category: str | None = Query(
        None, description="Filter by category (e.g. sales, stock)"
    ),
    include_mock: bool | None = Query(None, description="Filter by is_mock flag"),
    _current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """List all active modules with optional category and mock filters."""
    query = f"SELECT {_MODULE_COLUMNS} FROM modules WHERE is_active = true"
    params: list = []

    if category is not None:
        query += " AND category::text = %s"
        params.append(category)

    if include_mock is not None:
        query += " AND is_mock = %s"
        params.append(include_mock)

    query += " ORDER BY sort_order"

    cur = db.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    modules = [_row_to_module(r) for r in rows]
    return ModuleListResponse(modules=modules, total=len(modules))


@router.get("/by-category", response_model=ModulesByCategoryResponse)
def modules_by_category(
    _current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """List all active modules grouped by category, ordered by sort_order."""
    cur = db.cursor()
    cur.execute(
        f"SELECT {_MODULE_COLUMNS} FROM modules "
        "WHERE is_active = true ORDER BY sort_order"
    )
    rows = cur.fetchall()

    # Group into ordered dict to preserve sort_order within each category
    grouped: OrderedDict[str, list[ModuleResponse]] = OrderedDict()
    for row in rows:
        mod = _row_to_module(row)
        grouped.setdefault(mod.category, []).append(mod)

    categories = [
        ModuleCategoryGroup(category=cat, modules=mods) for cat, mods in grouped.items()
    ]

    total = sum(len(g.modules) for g in categories)
    return ModulesByCategoryResponse(categories=categories, total=total)


@router.get("/{module_code}", response_model=ModuleResponse)
def get_module(
    module_code: str,
    _current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Get a single module by its code."""
    cur = db.cursor()
    cur.execute(
        f"SELECT {_MODULE_COLUMNS} FROM modules "
        "WHERE module_code = %s AND is_active = true",
        (module_code,),
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"Modul '{module_code}' nebol nájdený",
        )

    return _row_to_module(row)
