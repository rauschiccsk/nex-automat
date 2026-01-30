"""
Common schemas for API responses and pagination.
"""

from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseStatus(str, Enum):
    """API response status."""

    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=50, ge=1, le=1000, description="Items per page")
    sort_by: str | None = Field(default=None, description="Field to sort by")
    sort_desc: bool = Field(default=False, description="Sort descending")

    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    status: ResponseStatus = ResponseStatus.SUCCESS
    data: list[T] = Field(default_factory=list)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    has_next: bool = False
    has_prev: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)

    @classmethod
    def create(
        cls,
        data: list[T],
        page: int,
        page_size: int,
        total_items: int,
    ) -> "PaginatedResponse[T]":
        """Create paginated response with calculated fields."""
        total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            data=data,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )


class ErrorResponse(BaseModel):
    """Error response schema."""

    status: ResponseStatus = ResponseStatus.ERROR
    error_code: str
    message: str
    details: dict | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class SingleResponse(BaseModel, Generic[T]):
    """Single item response wrapper."""

    status: ResponseStatus = ResponseStatus.SUCCESS
    data: T
    timestamp: datetime = Field(default_factory=datetime.now)


class MessageResponse(BaseModel):
    """Simple message response."""

    status: ResponseStatus = ResponseStatus.SUCCESS
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
