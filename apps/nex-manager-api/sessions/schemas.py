"""Pydantic schemas for Sessions module."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionResponse(BaseModel):
    """One row from user_sessions joined with user info for UI list."""

    session_id: int
    user_id: int
    login_name: str
    full_name: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    last_seen_at: datetime
    created_at: datetime
    is_self: bool  # True if this row is the caller's own current session


class SessionListResponse(BaseModel):
    """List wrapper."""

    sessions: list[SessionResponse]
    total: int


class MessageResponse(BaseModel):
    """Generic confirmation."""

    message: str
