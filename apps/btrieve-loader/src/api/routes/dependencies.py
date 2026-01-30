"""
Common dependencies for API routes.
"""

from fastapi import Depends, Header, HTTPException, Query

from src.api.schemas.common import PaginationParams
from src.core.btrieve import get_btrieve_manager
from src.core.config import settings


async def verify_api_key(x_api_key: str | None = Header(None)) -> str:
    """
    Verify API key from X-API-Key header.

    Args:
        x_api_key: API key from header

    Raises:
        HTTPException: If API key is invalid or missing

    Returns:
        Valid API key
    """
    if not settings.api_key:
        # No API key configured, skip auth
        return ""

    if not x_api_key:
        raise HTTPException(status_code=422, detail="Missing X-API-Key header")

    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return x_api_key


def get_pagination(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=50, ge=1, le=1000, description="Items per page"),
    sort_by: str | None = Query(default=None, description="Field to sort by"),
    sort_desc: bool = Query(default=False, description="Sort descending"),
) -> PaginationParams:
    """Get pagination parameters from query string."""
    return PaginationParams(
        page=page,
        page_size=min(page_size, settings.max_page_size),
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


def get_btrieve():
    """Dependency to get BtrieveClientManager."""
    return get_btrieve_manager()
