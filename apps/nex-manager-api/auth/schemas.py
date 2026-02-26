"""Pydantic models for authentication endpoints."""

from datetime import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Login request with username and password."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response after successful authentication."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class UserResponse(BaseModel):
    """User information response."""

    user_id: int
    login_name: str
    full_name: str
    email: str | None = None
    is_active: bool
    last_login_at: datetime | None = None
    groups: list[str] = []


class UserPermissions(BaseModel):
    """Module-level permissions for a user (aggregated across groups)."""

    module_code: str
    module_name: str
    can_view: bool = False
    can_create: bool = False
    can_edit: bool = False
    can_delete: bool = False
    can_print: bool = False
    can_export: bool = False
    can_admin: bool = False


class MeResponse(BaseModel):
    """Full user info with groups and permissions."""

    user: UserResponse
    permissions: list[UserPermissions] = []
