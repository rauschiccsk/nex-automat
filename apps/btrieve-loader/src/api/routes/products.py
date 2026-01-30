"""
Product endpoints (GSCAT table).
"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.gscat_repository import GSCATRepository
from pydantic import BaseModel

from src.api.schemas.common import PaginatedResponse, PaginationParams
from src.api.schemas.products import Product, ProductList, ProductSearch
from src.business.product_matcher import MatchResult, ProductMatcher
from src.core.config import settings

from .dependencies import ApiKey, Pagination

router = APIRouter()


def get_gscat_repository() -> GSCATRepository:
    """Get GSCAT repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return GSCATRepository(client)


# Pydantic models for match endpoint
class MatchRequest(BaseModel):
    """Product match request."""

    original_name: str | None = None
    edited_name: str | None = None
    original_ean: str | None = None
    edited_ean: str | None = None
    min_confidence: float = 0.6


class MatchAlternative(BaseModel):
    """Alternative match result."""

    gs_code: int
    gs_name: str
    confidence: float


class MatchResponse(BaseModel):
    """Product match response."""

    is_match: bool
    confidence: float
    confidence_level: str
    method: str
    product: Product | None = None
    alternatives: list[MatchAlternative] = []


@router.get("", response_model=ProductList)
async def list_products(
    pagination: Pagination,
    _api_key: ApiKey,
):
    """
    List all products with pagination.

    Returns paginated list of products from GSCAT table.
    """
    repo = get_gscat_repository()

    try:
        # Get all records (with limit)
        all_records = repo.get_all(max_records=10000)

        # Apply pagination
        total_items = len(all_records)
        start_idx = pagination.offset
        end_idx = start_idx + pagination.page_size
        page_records = all_records[start_idx:end_idx]

        # Convert to schema
        products = [Product.from_gscat_record(r) for r in page_records]

        return PaginatedResponse.create(
            data=products,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
        )

    finally:
        repo.close()


@router.get("/search", response_model=ProductList)
async def search_products(
    q: Annotated[str, Query(min_length=2, description="Search query")],
    pagination: Pagination,
    _api_key: ApiKey,
):
    """
    Search products by name or barcode.

    Performs fulltext search on product names.
    """
    repo = get_gscat_repository()

    try:
        # Search by name
        matching_records = repo.search_by_name(q, limit=pagination.page_size * 10)

        # Also search by barcode if query looks like one
        if q.isdigit() and len(q) >= 8:
            barcode_match = repo.find_by_barcode(q)
            if barcode_match and barcode_match not in matching_records:
                matching_records.insert(0, barcode_match)

        # Apply pagination
        total_items = len(matching_records)
        start_idx = pagination.offset
        end_idx = start_idx + pagination.page_size
        page_records = matching_records[start_idx:end_idx]

        # Convert to schema
        products = [Product.from_gscat_record(r) for r in page_records]

        return PaginatedResponse.create(
            data=products,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
        )

    finally:
        repo.close()


@router.get("/{code}", response_model=Product)
async def get_product(
    code: int,
    _api_key: ApiKey,
):
    """
    Get product by code.

    Args:
        code: Product code (GsCode/PLU)
    """
    repo = get_gscat_repository()

    try:
        # Find product by code
        record = repo.find_one(lambda r: r.GsCode == code)

        if not record:
            raise HTTPException(status_code=404, detail=f"Product {code} not found")

        return Product.from_gscat_record(record)

    finally:
        repo.close()


@router.post("/match", response_model=MatchResponse)
async def match_product(
    request: MatchRequest,
    _api_key: ApiKey,
):
    """
    Match invoice item to NEX Genesis product.

    Uses EAN matching first, then fuzzy name matching.
    Returns best match with confidence score and alternatives.
    """
    matcher = ProductMatcher(str(settings.btrieve_path))

    # Build item_data dict for matcher
    item_data = {
        "original_name": request.original_name or "",
        "edited_name": request.edited_name or "",
        "original_ean": request.original_ean or "",
        "edited_ean": request.edited_ean or "",
    }

    # Perform matching
    result: MatchResult = matcher.match_item(
        item_data,
        min_confidence=request.min_confidence,
    )

    # Build response
    response = MatchResponse(
        is_match=result.is_match,
        confidence=result.confidence,
        confidence_level=result.confidence_level,
        method=result.method,
    )

    if result.product:
        response.product = Product.from_gscat_record(result.product)

    if result.alternatives:
        response.alternatives = [
            MatchAlternative(
                gs_code=alt[0].GsCode,
                gs_name=alt[0].GsName,
                confidence=alt[1],
            )
            for alt in result.alternatives
        ]

    return response
