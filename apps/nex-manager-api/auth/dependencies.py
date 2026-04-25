"""FastAPI dependencies for authentication — JWT bearer token extraction & RBAC."""

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from database import get_db
from .service import decode_token

security = HTTPBearer()

# Whitelist of valid permission column names in group_module_permissions
_VALID_PERMISSIONS = frozenset(
    {
        "can_view",
        "can_create",
        "can_edit",
        "can_delete",
        "can_print",
        "can_export",
        "can_admin",
    }
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    """Extract and validate user from JWT Bearer token.

    Validates session anchor (sid+tv must match user_sessions row).
    Refreshes last_seen_at, throttled to 1 update per minute per session
    (per Q-B 2026-04-25 decision).

    Returns dict with user_id, login_name, full_name, email, is_active,
    session_id.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Neplatný typ tokenu")
        user_id = int(payload["sub"])
        session_id = int(payload["sid"])
        token_version = int(payload["tv"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný alebo expirovaný token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cur = db.cursor()
    cur.execute(
        "SELECT u.user_id, u.login_name, u.full_name, u.email, u.is_active, "
        "s.token_version "
        "FROM users u "
        "JOIN user_sessions s ON s.user_id = u.user_id "
        "WHERE u.user_id = %s AND s.session_id = %s",
        (user_id, session_id),
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(
            status_code=401, detail="Session nenájdená alebo používateľ neexistuje"
        )

    if not row[4]:  # is_active
        raise HTTPException(status_code=401, detail="Používateľ je neaktívny")

    if row[5] != token_version:
        raise HTTPException(
            status_code=401, detail="Session bola ukončená — prihláste sa znova"
        )

    # Throttled last_seen_at update — only if older than 1 minute.
    cur.execute(
        "UPDATE user_sessions SET last_seen_at = NOW(), updated_at = NOW() "
        "WHERE session_id = %s AND last_seen_at < NOW() - INTERVAL '1 minute'",
        (session_id,),
    )
    db.commit()

    return {
        "user_id": row[0],
        "login_name": row[1],
        "full_name": row[2],
        "email": row[3],
        "is_active": row[4],
        "session_id": session_id,
    }


def require_permission(module_code: str, permission: str) -> Callable:
    """Factory that returns a FastAPI dependency checking a specific module permission.

    Usage in an endpoint::

        @router.get("/items")
        def list_items(user=Depends(require_permission("GSC", "can_view"))):
            ...

    The returned dependency:
    1. Authenticates the user via ``get_current_user``.
    2. Validates *permission* against a whitelist (prevents SQL injection).
    3. Queries ``group_module_permissions`` aggregated via ``bool_or`` across
       all groups the user belongs to.
    4. Raises **403** if the permission is not granted.
    5. Returns the ``current_user`` dict on success.
    """
    if permission not in _VALID_PERMISSIONS:
        raise ValueError(
            f"Neplatné oprávnenie '{permission}'. "
            f"Povolené: {', '.join(sorted(_VALID_PERMISSIONS))}"
        )

    async def _check_permission(
        current_user=Depends(get_current_user),
        db=Depends(get_db),
    ):
        user_id = current_user["user_id"]
        cur = db.cursor()

        # permission column name is validated above — safe to interpolate
        cur.execute(
            f"SELECT bool_or(gmp.{permission}) "
            "FROM user_groups ug "
            "JOIN group_module_permissions gmp ON ug.group_id = gmp.group_id "
            "JOIN modules m ON gmp.module_id = m.module_id "
            "WHERE ug.user_id = %s AND m.module_code = %s AND m.is_active = true",
            (user_id, module_code),
        )
        row = cur.fetchone()
        has_permission = row and row[0] is True

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Nemáte oprávnenie '{permission}' pre modul '{module_code}'",
            )

        return current_user

    return _check_permission
