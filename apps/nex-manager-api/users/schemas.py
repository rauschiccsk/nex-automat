"""Pydantic models for user management endpoints."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class GroupInfo(BaseModel):
    """Group membership info."""

    group_id: int
    group_name: str


class UserResponse(BaseModel):
    """User information returned from API."""

    user_id: int
    login_name: str
    full_name: str
    email: str | None = None
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None
    groups: list[GroupInfo] = []


class UserListResponse(BaseModel):
    """List of users with total count."""

    users: list[UserResponse]
    total: int


class CreateUserRequest(BaseModel):
    """Request body for creating a new user."""

    username: str
    full_name: str
    email: str
    password: str
    is_active: bool = True
    group_ids: Optional[list[int]] = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Heslo mus\u00ed ma\u0165 minim\u00e1lne 6 znakov")
        return v

    @field_validator("email")
    @classmethod
    def email_format(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("Neplatn\u00fd form\u00e1t emailu")
        return v


class UpdateUserRequest(BaseModel):
    """Request body for updating a user. Username is NOT editable."""

    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    group_ids: Optional[list[int]] = None

    @field_validator("email")
    @classmethod
    def email_format(cls, v: str | None) -> str | None:
        if v is not None and ("@" not in v or "." not in v):
            raise ValueError("Neplatn\u00fd form\u00e1t emailu")
        return v


class ChangePasswordRequest(BaseModel):
    """Request body for admin password change."""

    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Heslo mus\u00ed ma\u0165 minim\u00e1lne 6 znakov")
        return v


class SelfChangePasswordRequest(BaseModel):
    """Request body for self password change."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Heslo mus\u00ed ma\u0165 minim\u00e1lne 6 znakov")
        return v
