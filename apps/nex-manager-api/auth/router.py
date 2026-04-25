"""Authentication API endpoints — login, refresh, logout, me, change-password."""

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError

from database import get_db

from settings.service import get_setting

from .config import ACCESS_TOKEN_EXPIRE
from .dependencies import get_current_user
from .schemas import (
    LoginRequest,
    MeResponse,
    RefreshRequest,
    SelfChangePasswordRequest,
    TokenResponse,
    UserPermissions,
    UserResponse,
)
from .service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _client_ip(http_req: Request) -> str | None:
    """Extract client IP, honouring X-Forwarded-For (reverse proxy)."""
    forwarded = http_req.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return http_req.client.host if http_req.client else None


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, http_req: Request, db=Depends(get_db)):
    """Authenticate user, create new session row, return JWT access + refresh tokens.

    Each login creates a fresh user_sessions row (multi-device support).
    JWT carries sid+tv claims that bind tokens to that session.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT user_id, login_name, password_hash, is_active "
        "FROM users WHERE login_name = %s",
        (body.username,),
    )
    user = cur.fetchone()

    if not user or not verify_password(body.password, user[2]):
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

    # Create a new session row (multi-device — one per login).
    user_agent = http_req.headers.get("user-agent")
    if user_agent and len(user_agent) > 500:
        user_agent = user_agent[:500]
    ip_address = _client_ip(http_req)

    cur.execute(
        "INSERT INTO user_sessions (user_id, user_agent, ip_address) "
        "VALUES (%s, %s, %s) "
        "RETURNING session_id, token_version",
        (user[0], user_agent, ip_address),
    )
    session_row = cur.fetchone()
    session_id = session_row[0]
    token_version = session_row[1]
    db.commit()

    access_token = create_access_token(user[0], user[1], session_id, token_version)
    refresh_token = create_refresh_token(user[0], session_id, token_version)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(
            get_setting(
                "auth.access_token_expiry_seconds",
                default=int(ACCESS_TOKEN_EXPIRE.total_seconds()),
            )
        ),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db=Depends(get_db)):
    """Refresh access token using a valid refresh token.

    Validates session anchor (sid+tv must still match user_sessions row) —
    rejects tokens issued before the session was logged out (tv bumped) or
    deleted. Per Q-A 2026-04-25: refresh preserves tv (no rotation).
    """
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Neplatný typ tokenu")
        user_id = int(payload["sub"])
        session_id = int(payload["sid"])
        token_version = int(payload["tv"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Neplatný refresh token")

    cur = db.cursor()
    cur.execute(
        "SELECT u.user_id, u.login_name, u.is_active, s.token_version "
        "FROM users u "
        "JOIN user_sessions s ON s.user_id = u.user_id "
        "WHERE u.user_id = %s AND s.session_id = %s",
        (user_id, session_id),
    )
    row = cur.fetchone()

    if not row or not row[2]:  # is_active
        raise HTTPException(
            status_code=401,
            detail="Session nenájdená alebo používateľ je neaktívny",
        )

    if row[3] != token_version:
        raise HTTPException(
            status_code=401,
            detail="Session bola ukončená — prihláste sa znova",
        )

    access_token = create_access_token(row[0], row[1], session_id, token_version)
    refresh_token = create_refresh_token(row[0], session_id, token_version)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(
            get_setting(
                "auth.access_token_expiry_seconds",
                default=int(ACCESS_TOKEN_EXPIRE.total_seconds()),
            )
        ),
    )


@router.post("/logout")
def logout(current_user=Depends(get_current_user), db=Depends(get_db)):
    """Bump token_version on caller's current session — invalidates this JWT.

    Subsequent requests with the same access/refresh token return 401.
    Other devices of the same user are unaffected (separate session rows).
    """
    session_id = current_user.get("session_id")
    if session_id is None:
        # Token without sid (legacy or malformed) — no-op success.
        return {"message": "Odhlásený"}

    cur = db.cursor()
    cur.execute(
        "UPDATE user_sessions SET token_version = token_version + 1, "
        "updated_at = NOW() WHERE session_id = %s",
        (session_id,),
    )
    db.commit()
    return {"message": "Odhlásený"}


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


@router.put("/change-password")
def change_own_password(
    body: SelfChangePasswordRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Change own password. Requires current password verification."""
    user_id = current_user["user_id"]
    cur = db.cursor()

    # Fetch current password hash
    cur.execute(
        "SELECT password_hash FROM users WHERE user_id = %s",
        (user_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pou\u017e\u00edvate\u013e nebol n\u00e1jden\u00fd",
        )

    # Verify current password
    if not verify_password(body.current_password, row[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nespr\u00e1vne aktu\u00e1lne heslo",
        )

    # Hash and update new password
    pw_hash = hash_password(body.new_password)
    cur.execute(
        "UPDATE users SET password_hash = %s, updated_by = %s WHERE user_id = %s",
        (pw_hash, current_user["login_name"], user_id),
    )

    # Audit log
    cur.execute(
        "INSERT INTO audit_log (user_id, action, entity_type, entity_id, details) "
        "VALUES (%s, %s, %s, %s, %s)",
        (
            user_id,
            "password_change",
            "AUTH",
            user_id,
            json.dumps({"message": "User changed own password"}),
        ),
    )

    db.commit()
    return {"message": "Heslo bolo \u00faspe\u0161ne zmenen\u00e9"}
