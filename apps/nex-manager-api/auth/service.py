"""Authentication business logic — JWT creation, password verification."""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError  # noqa: F401

from settings.service import get_setting

from .config import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE,
    REFRESH_TOKEN_EXPIRE,
)


def _access_token_expire() -> timedelta:
    """Read access token expiry from runtime settings, fallback to compile-time default."""
    seconds = get_setting(
        "auth.access_token_expiry_seconds",
        default=int(ACCESS_TOKEN_EXPIRE.total_seconds()),
    )
    return timedelta(seconds=int(seconds))


def _refresh_token_expire() -> timedelta:
    """Read refresh token expiry from runtime settings, fallback to compile-time default."""
    days = get_setting(
        "auth.refresh_token_expiry_days",
        default=REFRESH_TOKEN_EXPIRE.days,
    )
    return timedelta(days=int(days))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against bcrypt hash."""
    pw_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))


def hash_password(password: str) -> str:
    """Create bcrypt hash from plain password."""
    pw_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def create_access_token(
    user_id: int, login_name: str, session_id: int, token_version: int
) -> str:
    """Create a short-lived JWT access token with session anchor (sid+tv).

    The ``sid`` claim binds the token to a specific user_sessions row;
    ``tv`` is verified against ``user_sessions.token_version`` on every
    authenticated request — bumping tv (e.g. on logout) invalidates this
    token immediately.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": login_name,
        "sid": session_id,
        "tv": token_version,
        "type": "access",
        "iat": now,
        "exp": now + _access_token_expire(),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: int, session_id: int, token_version: int) -> str:
    """Create a long-lived JWT refresh token bound to the same session.

    Refresh issues a new access token without changing tv (per Q-A 2026-04-25
    decision: refresh = session extension, not rotation).
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "sid": session_id,
        "tv": token_version,
        "type": "refresh",
        "iat": now,
        "exp": now + _refresh_token_expire(),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
