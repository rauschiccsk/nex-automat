"""Sessions router — list active sessions, force logout (Track 1 Phase 1.1).

Endpoints:
- GET /api/sessions          — list all active sessions (admin)
- GET /api/sessions/me       — list caller's own sessions
- DELETE /api/sessions/{id}  — terminate one session (admin or owner)
- DELETE /api/sessions/me/all — terminate all caller's sessions except current
- DELETE /api/sessions/user/{user_id}/all — terminate all sessions of given user (admin)

Auth integration with sid+tv JWT claims is added in Phase 1.2 (auth/*).
For Phase 1.1, endpoints rely on existing get_current_user / require_permission.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from auth.dependencies import get_current_user, require_permission
from database import get_db

from .schemas import MessageResponse, SessionListResponse, SessionResponse

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

# By convention: token_version=0 means "active" (JWT carrying tv=0 still valid).
# Any tv>0 means the session was terminated (logout, force-logout). Terminated
# rows stay in DB for audit but are hidden from UI listings.
_ACTIVE_FILTER = "s.token_version = 0"

_SESSION_SELECT = (
    "SELECT s.session_id, s.user_id, u.login_name, u.full_name, "
    "s.user_agent, s.ip_address, s.last_seen_at, s.created_at "
    "FROM user_sessions s "
    "JOIN users u ON u.user_id = s.user_id"
)


def _row_to_response(row, current_session_id: int | None) -> SessionResponse:
    return SessionResponse(
        session_id=row[0],
        user_id=row[1],
        login_name=row[2],
        full_name=row[3],
        user_agent=row[4],
        ip_address=row[5],
        last_seen_at=row[6],
        created_at=row[7],
        is_self=(current_session_id is not None and row[0] == current_session_id),
    )


def _current_session_id(current_user: dict) -> int | None:
    """Extract sid from current_user dict (set by Phase 1.2 get_current_user)."""
    return current_user.get("session_id")


# ─────────────────────────────────────────────────────────────────────
# List endpoints
# ─────────────────────────────────────────────────────────────────────


@router.get("", response_model=SessionListResponse)
def list_all_sessions(
    current_user=Depends(require_permission("USR", "can_admin")),
    db=Depends(get_db),
):
    """List all active sessions across all users (admin only).

    Filters out terminated sessions (token_version > 0) — those rows stay
    in DB for audit but never appear in UI.
    """
    cur = db.cursor()
    cur.execute(
        _SESSION_SELECT + f" WHERE {_ACTIVE_FILTER} ORDER BY s.last_seen_at DESC"
    )
    rows = cur.fetchall()
    cur_sid = _current_session_id(current_user)
    sessions = [_row_to_response(r, cur_sid) for r in rows]
    return SessionListResponse(sessions=sessions, total=len(sessions))


@router.get("/me", response_model=SessionListResponse)
def list_my_sessions(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """List caller's own active sessions (filters terminated rows)."""
    cur = db.cursor()
    cur.execute(
        _SESSION_SELECT
        + f" WHERE s.user_id = %s AND {_ACTIVE_FILTER} ORDER BY s.last_seen_at DESC",
        (current_user["user_id"],),
    )
    rows = cur.fetchall()
    cur_sid = _current_session_id(current_user)
    sessions = [_row_to_response(r, cur_sid) for r in rows]
    return SessionListResponse(sessions=sessions, total=len(sessions))


# ─────────────────────────────────────────────────────────────────────
# Termination endpoints
# ─────────────────────────────────────────────────────────────────────


@router.delete("/me/all", response_model=MessageResponse)
def terminate_my_other_sessions(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Bump token_version on all caller's sessions EXCEPT the current one.

    Effect: every other device of this user is logged out at the next
    authenticated request (tv claim mismatch → 401).
    """
    cur_sid = _current_session_id(current_user)
    cur = db.cursor()
    if cur_sid is None:
        # Phase 1.1 fallback (no sid yet): bump everything for this user.
        cur.execute(
            "UPDATE user_sessions SET token_version = token_version + 1, "
            "updated_at = NOW() WHERE user_id = %s",
            (current_user["user_id"],),
        )
    else:
        cur.execute(
            "UPDATE user_sessions SET token_version = token_version + 1, "
            "updated_at = NOW() WHERE user_id = %s AND session_id != %s",
            (current_user["user_id"], cur_sid),
        )
    db.commit()
    return MessageResponse(message="Ostatné sessions boli ukončené")


@router.delete("/user/{user_id}/all", response_model=MessageResponse)
def terminate_user_sessions(
    user_id: int,
    current_user=Depends(require_permission("USR", "can_admin")),
    db=Depends(get_db),
):
    """Bump token_version on all sessions of given user (admin force-logout)."""
    cur = db.cursor()
    cur.execute(
        "UPDATE user_sessions SET token_version = token_version + 1, "
        "updated_at = NOW() WHERE user_id = %s",
        (user_id,),
    )
    db.commit()
    return MessageResponse(
        message=f"Všetky sessions používateľa {user_id} boli ukončené"
    )


@router.delete("/{session_id}", response_model=MessageResponse)
def terminate_session(
    session_id: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Terminate one session by id. Owner or admin only.

    Bumps token_version → JWT carrying old tv becomes invalid at next request.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT user_id FROM user_sessions WHERE session_id = %s",
        (session_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session nebola nájdená",
        )
    owner_id = row[0]

    # Authorization: owner OR admin (USR.can_admin permission)
    is_owner = owner_id == current_user["user_id"]
    if not is_owner:
        # Need admin perm — re-check explicitly (this endpoint accepts get_current_user
        # to allow self-termination without admin perm).
        cur.execute(
            "SELECT bool_or(gmp.can_admin) "
            "FROM user_groups ug "
            "JOIN group_module_permissions gmp ON ug.group_id = gmp.group_id "
            "JOIN modules m ON gmp.module_id = m.module_id "
            "WHERE ug.user_id = %s AND m.module_code = 'USR' AND m.is_active = true",
            (current_user["user_id"],),
        )
        perm_row = cur.fetchone()
        if not (perm_row and perm_row[0] is True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie ukončiť cudziu session",
            )

    cur.execute(
        "UPDATE user_sessions SET token_version = token_version + 1, "
        "updated_at = NOW() WHERE session_id = %s",
        (session_id,),
    )
    db.commit()
    return MessageResponse(message="Session bola ukončená")
