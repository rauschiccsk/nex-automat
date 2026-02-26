"""Pydantic models for module registry endpoints."""

from datetime import datetime

from pydantic import BaseModel


class ModuleResponse(BaseModel):
    """Single module detail."""

    module_id: int
    module_code: str
    module_name: str
    category: str
    icon: str
    module_type: str
    is_mock: bool
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ModuleListResponse(BaseModel):
    """List of modules with total count."""

    modules: list[ModuleResponse]
    total: int


class ModuleCategoryGroup(BaseModel):
    """Modules grouped under a single category."""

    category: str
    modules: list[ModuleResponse]


class ModulesByCategoryResponse(BaseModel):
    """All modules grouped by category."""

    categories: list[ModuleCategoryGroup]
    total: int
