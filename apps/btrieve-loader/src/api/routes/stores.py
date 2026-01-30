"""
Product group/store endpoints (MGLST table).
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.mglst_repository import MGLSTRepository

from src.api.schemas.common import PaginatedResponse, PaginationParams
from src.api.schemas.stores import ProductGroup, ProductGroupList, ProductGroupTree
from src.core.config import settings

from .dependencies import get_pagination, verify_api_key

router = APIRouter()


def get_mglst_repository() -> MGLSTRepository:
    """Get MGLST repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return MGLSTRepository(client)


@router.get("", response_model=ProductGroupList)
async def list_product_groups(
    parent_code: int | None = Query(default=None, description="Filter by parent"),
    active: bool | None = Query(default=None, description="Filter by active status"),
    level: int | None = Query(default=None, description="Filter by level"),
    pagination: PaginationParams = Depends(get_pagination),
    _api_key: str = Depends(verify_api_key),
):
    """
    List product groups with pagination.

    Returns flat list of product groups from MGLST table.
    """
    repo = get_mglst_repository()

    try:
        # Get all records
        all_records = repo.get_all(max_records=10000)

        # Apply filters
        filtered_records = all_records
        if parent_code is not None:
            filtered_records = [r for r in filtered_records if r.parent_code == parent_code]
        if active is not None:
            filtered_records = [r for r in filtered_records if r.active == active]
        if level is not None:
            filtered_records = [r for r in filtered_records if r.level == level]

        # Sort by sort_order
        filtered_records.sort(key=lambda r: r.sort_order)

        # Apply pagination
        total_items = len(filtered_records)
        start_idx = pagination.offset
        end_idx = start_idx + pagination.page_size
        page_records = filtered_records[start_idx:end_idx]

        # Convert to schema
        groups = [ProductGroup.from_mglst_record(r) for r in page_records]

        return PaginatedResponse.create(
            data=groups,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
        )

    finally:
        repo.close()


@router.get("/tree", response_model=list[ProductGroupTree])
async def get_product_groups_tree(
    _api_key: str = Depends(verify_api_key),
):
    """
    Get product groups as hierarchical tree.

    Returns nested tree structure of product groups.
    Uses ProductGroupTree.build_tree() for hierarchy.
    """
    repo = get_mglst_repository()

    try:
        # Get all records
        all_records = repo.get_all(max_records=10000)

        # Convert to ProductGroup schema
        groups = [ProductGroup.from_mglst_record(r) for r in all_records]

        # Build tree
        tree = ProductGroupTree.build_tree(groups)

        return tree

    finally:
        repo.close()


@router.get("/{mglst_code}", response_model=ProductGroup)
async def get_product_group(
    mglst_code: int,
    _api_key: str = Depends(verify_api_key),
):
    """
    Get product group by code.

    Args:
        mglst_code: Product group code
    """
    repo = get_mglst_repository()

    try:
        # Find group by code
        record = repo.find_one(lambda r: r.mglst_code == mglst_code)

        if not record:
            raise HTTPException(status_code=404, detail=f"Product group {mglst_code} not found")

        return ProductGroup.from_mglst_record(record)

    finally:
        repo.close()


@router.get("/{mglst_code}/children", response_model=ProductGroupList)
async def get_product_group_children(
    mglst_code: int,
    _api_key: str = Depends(verify_api_key),
):
    """
    Get child groups for a product group.

    Args:
        mglst_code: Parent group code
    """
    repo = get_mglst_repository()

    try:
        # Find children
        children = repo.find(lambda r: r.parent_code == mglst_code, max_results=1000)

        # Sort by sort_order
        children.sort(key=lambda r: r.sort_order)

        # Convert to schema
        groups = [ProductGroup.from_mglst_record(r) for r in children]

        return PaginatedResponse.create(
            data=groups,
            page=1,
            page_size=len(groups),
            total_items=len(groups),
        )

    finally:
        repo.close()
