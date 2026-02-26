"""Authentication API endpoints — login, refresh, me."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError

from database import get_db

from .config import ACCESS_TOKEN_EXPIRE
from .dependencies import get_current_user
from .schemas import (
    LoginRequest,
    MeResponse,
    RefreshRequest,
    TokenResponse,
    UserPermissions,
    UserResponse,
)
from .service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db=Depends(get_db)):
    """Authenticate user and return JWT access + refresh tokens."""
    cur = db.cursor()
    cur.execute(
        "SELECT user_id, login_name, password_hash, is_active "
        "FROM users WHERE login_name = %s",
        (request.username,),
    )
    user = cur.fetchone()

    if not user or not verify_password(request.password, user[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nesprávne prihlasovacie údaje",
        )

    if not user[3]:  # is_active
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Účet je deaktivovaný",
        )

    # Update last_login_at
    cur.execute(
        "UPDATE users SET last_login_at = %s WHERE user_id = %s",
        (datetime.now(timezone.utc), user[0]),
    )

    access_token = create_access_token(user[0], user[1])
    refresh_token = create_refresh_token(user[0])

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(ACCESS_TOKEN_EXPIRE.total_seconds()),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db=Depends(get_db)):
    """Refresh access token using a valid refresh token."""
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Neplatný typ tokenu")
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Neplatný refresh token")

    cur = db.cursor()
    cur.execute(
        "SELECT user_id, login_name, is_active FROM users WHERE user_id = %s",
        (user_id,),
    )
    user = cur.fetchone()

    if not user or not user[2]:  # is_active
        raise HTTPException(
            status_code=401,
            detail="Používateľ nebol nájdený alebo je neaktívny",
        )

    access_token = create_access_token(user[0], user[1])
    refresh_token = create_refresh_token(user[0])

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(ACCESS_TOKEN_EXPIRE.total_seconds()),
    )


@router.get("/me", response_model=MeResponse)
def get_me(current_user=Depends(get_current_user), db=Depends(get_db)):
    """Get current user info with group memberships and module permissions."""
    user_id = current_user["user_id"]
    cur = db.cursor()

    # Get groups
    cur.execute(
        "SELECT g.group_name "
        "FROM user_groups ug "
        "JOIN groups g ON ug.group_id = g.group_id "
        "WHERE ug.user_id = %s AND g.is_active = true",
        (user_id,),
    )
    groups = [r[0] for r in cur.fetchall()]

    # Get aggregated permissions across all user's groups
    cur.execute(
        "SELECT m.module_code, m.module_name, "
        "bool_or(gmp.can_view) AS can_view, "
        "bool_or(gmp.can_create) AS can_create, "
        "bool_or(gmp.can_edit) AS can_edit, "
        "bool_or(gmp.can_delete) AS can_delete, "
        "bool_or(gmp.can_print) AS can_print, "
        "bool_or(gmp.can_export) AS can_export, "
        "bool_or(gmp.can_admin) AS can_admin "
        "FROM user_groups ug "
        "JOIN group_module_permissions gmp ON ug.group_id = gmp.group_id "
        "JOIN modules m ON gmp.module_id = m.module_id "
        "WHERE ug.user_id = %s AND m.is_active = true "
        "GROUP BY m.module_code, m.module_name "
        "ORDER BY m.module_code",
        (user_id,),
    )
    permissions = [
        UserPermissions(
            module_code=r[0],
            module_name=r[1],
            can_view=r[2],
            can_create=r[3],
            can_edit=r[4],
            can_delete=r[5],
            can_print=r[6],
            can_export=r[7],
            can_admin=r[8],
        )
        for r in cur.fetchall()
    ]

    user_response = UserResponse(
        user_id=current_user["user_id"],
        login_name=current_user["login_name"],
        full_name=current_user["full_name"],
        email=current_user["email"],
        is_active=current_user["is_active"],
        groups=groups,
    )

    return MeResponse(user=user_response, permissions=permissions)
