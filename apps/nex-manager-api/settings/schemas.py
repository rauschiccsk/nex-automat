"""Pydantic schemas for Settings API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class SettingResponse(BaseModel):
    """One row from system_settings."""

    setting_key: str
    value: Any  # JSONB — int / string / bool / array
    scope: str
    category: str
    description: Optional[str] = None
    updated_by: Optional[str] = None
    updated_at: datetime
    created_at: datetime


class SettingListResponse(BaseModel):
    """List wrapper, optionally grouped by category."""

    settings: list[SettingResponse]
    total: int


class SettingUpdateRequest(BaseModel):
    """PUT body — only the value can be updated."""

    value: Any


class MessageResponse(BaseModel):
    message: str
