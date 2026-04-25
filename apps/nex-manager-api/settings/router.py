"""Settings router — list / get / update runtime tunables.

All endpoints require USR.can_admin permission (only admins can see/edit
system settings). Updates write through DB; in Phase 2.2 there is no
process-local cache — every backfill call site re-reads on demand.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from auth.dependencies import require_permission
from database import get_db

from .schemas import (
    SettingListResponse,
    SettingResponse,
    SettingUpdateRequest,
)

router = APIRouter(prefix="/api/system/settings", tags=["settings"])


_SELECT = (
    "SELECT setting_key, value, scope, category, description, "
    "updated_by, updated_at, created_at FROM system_settings"
)


def _row_to_response(row) -> SettingResponse:
    return SettingResponse(
        setting_key=row[0],
        value=row[1],
        scope=row[2],
        category=row[3],
        description=row[4],
        updated_by=row[5],
        updated_at=row[6],
        created_at=row[7],
    )


@router.get("", response_model=SettingListResponse)
def list_settings(
    _current_user=Depends(require_permission("USR", "can_admin")),
    db=Depends(get_db),
):
    """List all settings, ordered by category then key."""
    cur = db.cursor()
    cur.execute(_SELECT + " ORDER BY category, setting_key")
    rows = cur.fetchall()
    settings = [_row_to_response(r) for r in rows]
    return SettingListResponse(settings=settings, total=len(settings))


@router.get("/public")
def list_public_settings(db=Depends(get_db)):
    """Return UI-category settings as a flat key->value dict.

    No authentication required — these are inherently public values
    (debounce delays, toast durations) shipped in the FE bundle anyway.
    Frontend boot-time config loader uses this endpoint to read live
    runtime values; falls back to compile-time defaults if unreachable.

    Scope: WHERE category = 'ui' (extend as more public categories arise).
    """
    cur = db.cursor()
    cur.execute("SELECT setting_key, value FROM system_settings WHERE category = 'ui'")
    rows = cur.fetchall()
    return {key: value for key, value in rows}


@router.get("/{setting_key}", response_model=SettingResponse)
def get_setting_endpoint(
    setting_key: str,
    _current_user=Depends(require_permission("USR", "can_admin")),
    db=Depends(get_db),
):
    """Get one setting by key."""
    cur = db.cursor()
    cur.execute(_SELECT + " WHERE setting_key = %s", (setting_key,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nastavenie '{setting_key}' nebolo nájdené",
        )
    return _row_to_response(row)


@router.put("/{setting_key}", response_model=SettingResponse)
def update_setting(
    setting_key: str,
    body: SettingUpdateRequest,
    current_user=Depends(require_permission("USR", "can_admin")),
    db=Depends(get_db),
):
    """Update a setting's value. Key cannot be changed (it's the PK)."""
    cur = db.cursor()
    cur.execute(
        "UPDATE system_settings SET value = %s::jsonb, updated_by = %s, "
        "updated_at = NOW() WHERE setting_key = %s",
        (
            __import__("json").dumps(body.value),
            current_user["login_name"],
            setting_key,
        ),
    )

    # Re-read to return the updated row.
    cur.execute(_SELECT + " WHERE setting_key = %s", (setting_key,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nastavenie '{setting_key}' nebolo nájdené",
        )
    db.commit()
    return _row_to_response(row)
