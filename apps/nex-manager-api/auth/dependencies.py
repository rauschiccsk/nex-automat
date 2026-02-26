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

    Returns dict with user_id, login_name, full_name, email, is_active.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Neplatný typ tokenu")
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný alebo expirovaný token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cur = db.cursor()
    cur.execute(
        "SELECT user_id, login_name, full_name, email, is_active "
        "FROM users WHERE user_id = %s",
        (user_id,),
    )
    user = cur.fetchone()

    if not user or not user[4]:  # is_active
        raise HTTPException(
            status_code=401, detail="Používateľ nebol nájdený alebo je neaktívny"
        )

    return {
        "user_id": user[0],
        "login_name": user[1],
        "full_name": user[2],
        "email": user[3],
        "is_active": user[4],
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
