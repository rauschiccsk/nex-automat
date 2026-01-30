"""
Partner endpoints (PAB table).
"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.pab_repository import PABRepository

from src.api.schemas.common import PaginatedResponse, PaginationParams
from src.api.schemas.partners import Partner, PartnerList, PartnerSearch, PartnerType
from src.core.config import settings

from .dependencies import ApiKey, Pagination

router = APIRouter()


def get_pab_repository() -> PABRepository:
    """Get PAB repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return PABRepository(client)


@router.get("", response_model=PartnerList)
async def list_partners(
    pagination: Pagination,
    _api_key: ApiKey,
    partner_type: Annotated[PartnerType | None, Query(description="Filter by type")] = None,
    active: Annotated[bool | None, Query(description="Filter by active status")] = None,
):
    """
    List all partners with pagination.

    Returns paginated list of partners from PAB table.
    """
    repo = get_pab_repository()

    try:
        # Get all records
        all_records = repo.get_all(max_records=10000)

        # Apply filters
        filtered_records = all_records
        if partner_type is not None:
            filtered_records = [r for r in filtered_records if r.partner_type == partner_type.value]
        if active is not None:
            filtered_records = [r for r in filtered_records if r.active == active]

        # Apply pagination
        total_items = len(filtered_records)
        start_idx = pagination.offset
        end_idx = start_idx + pagination.page_size
        page_records = filtered_records[start_idx:end_idx]

        # Convert to schema
        partners = [Partner.from_pab_record(r) for r in page_records]

        return PaginatedResponse.create(
            data=partners,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
        )

    finally:
        repo.close()


@router.get("/search", response_model=PartnerList)
async def search_partners(
    q: Annotated[str, Query(min_length=2, description="Search query")],
    pagination: Pagination,
    _api_key: ApiKey,
):
    """
    Search partners by name, ICO, or other fields.

    Performs fulltext search on partner data.
    """
    repo = get_pab_repository()

    try:
        # Get all records and filter
        all_records = repo.get_all(max_records=10000)
        q_lower = q.lower()

        matching_records = [
            r
            for r in all_records
            if q_lower in r.name1.lower()
            or q_lower in r.name2.lower()
            or q_lower in r.short_name.lower()
            or q_lower in r.ico.lower()
            or q_lower in r.dic.lower()
            or q_lower in r.city.lower()
        ]

        # Apply pagination
        total_items = len(matching_records)
        start_idx = pagination.offset
        end_idx = start_idx + pagination.page_size
        page_records = matching_records[start_idx:end_idx]

        # Convert to schema
        partners = [Partner.from_pab_record(r) for r in page_records]

        return PaginatedResponse.create(
            data=partners,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
        )

    finally:
        repo.close()


@router.get("/{pab_code}", response_model=Partner)
async def get_partner(
    pab_code: int,
    _api_key: ApiKey,
):
    """
    Get partner by code.

    Args:
        pab_code: Partner code
    """
    repo = get_pab_repository()

    try:
        # Find partner by code
        record = repo.find_one(lambda r: r.pab_code == pab_code)

        if not record:
            raise HTTPException(status_code=404, detail=f"Partner {pab_code} not found")

        return Partner.from_pab_record(record)

    finally:
        repo.close()
