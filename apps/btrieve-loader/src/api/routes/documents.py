"""
Document endpoints (TSH/TSI tables).
"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.tsh_repository import TSHRepository
from nexdata.repositories.tsi_repository import TSIRepository

from src.api.schemas.common import PaginatedResponse
from src.api.schemas.documents import (
    DocumentHeader,
    DocumentHeaderList,
    DocumentItem,
    DocumentItemList,
    DocumentStatus,
    DocumentType,
    DocumentWithItems,
)
from src.core.config import settings

from .dependencies import ApiKey, Pagination

router = APIRouter()


def get_tsh_repository(book_id: str = "001") -> TSHRepository:
    """Get TSH repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return TSHRepository(client, book_id=book_id)


def get_tsi_repository(book_id: str = "001") -> TSIRepository:
    """Get TSI repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return TSIRepository(client, book_id=book_id)


@router.get("", response_model=DocumentHeaderList)
async def list_documents(
    pagination: Pagination,
    _api_key: ApiKey,
    book_id: Annotated[str, Query(description="Book ID (e.g., 001)")] = "001",
    doc_type: Annotated[
        DocumentType | None, Query(description="Filter by type")
    ] = None,
    status: Annotated[
        DocumentStatus | None, Query(description="Filter by status")
    ] = None,
    pab_code: Annotated[int | None, Query(description="Filter by partner")] = None,
    date_from: Annotated[date | None, Query(description="Filter from date")] = None,
    date_to: Annotated[date | None, Query(description="Filter to date")] = None,
):
    """
    List document headers with filtering and pagination.

    Returns documents from TSH table.
    """
    repo = get_tsh_repository(book_id)

    try:
        # Get all records
        all_records = repo.get_all(max_records=10000)

        # Apply filters
        filtered_records = all_records

        if doc_type is not None:
            filtered_records = [
                r for r in filtered_records if r.doc_type == doc_type.value
            ]

        if status is not None and hasattr(
            filtered_records[0] if filtered_records else None, "status"
        ):
            filtered_records = [
                r
                for r in filtered_records
                if getattr(r, "status", None) == status.value
            ]

        if pab_code is not None:
            filtered_records = [r for r in filtered_records if r.pab_code == pab_code]

        if date_from is not None:
            filtered_records = [
                r for r in filtered_records if r.doc_date and r.doc_date >= date_from
            ]

        if date_to is not None:
            filtered_records = [
                r for r in filtered_records if r.doc_date and r.doc_date <= date_to
            ]

        # Sort by date descending
        filtered_records.sort(
            key=lambda r: r.doc_date if r.doc_date else date.min, reverse=True
        )

        # Apply pagination
        total_items = len(filtered_records)
        start_idx = pagination.offset
        end_idx = start_idx + pagination.page_size
        page_records = filtered_records[start_idx:end_idx]

        # Convert to schema
        documents = [DocumentHeader.from_tsh_record(r) for r in page_records]

        return PaginatedResponse.create(
            data=documents,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
        )

    finally:
        repo.close()


@router.get("/{doc_number}", response_model=DocumentWithItems)
async def get_document(
    doc_number: str,
    _api_key: ApiKey,
    book_id: Annotated[str, Query(description="Book ID")] = "001",
):
    """
    Get document header with all items.

    Args:
        doc_number: Document number
        book_id: Book ID (e.g., 001)
    """
    tsh_repo = get_tsh_repository(book_id)
    tsi_repo = get_tsi_repository(book_id)

    try:
        # Find header
        header_record = tsh_repo.find_one(
            lambda r: r.doc_number.strip() == doc_number.strip()
        )

        if not header_record:
            raise HTTPException(
                status_code=404, detail=f"Document {doc_number} not found"
            )

        # Find items
        item_records = tsi_repo.find(
            lambda r: r.doc_number.strip() == doc_number.strip(), max_results=1000
        )

        # Sort items by line number
        item_records.sort(key=lambda r: r.line_number)

        # Convert to schema
        header = DocumentHeader.from_tsh_record(header_record)
        items = [DocumentItem.from_tsi_record(r) for r in item_records]

        return DocumentWithItems(header=header, items=items)

    finally:
        tsh_repo.close()
        tsi_repo.close()


@router.get("/{doc_number}/items", response_model=DocumentItemList)
async def get_document_items(
    doc_number: str,
    _api_key: ApiKey,
    book_id: Annotated[str, Query(description="Book ID")] = "001",
):
    """
    Get document items only.

    Args:
        doc_number: Document number
        book_id: Book ID (e.g., 001)
    """
    tsi_repo = get_tsi_repository(book_id)

    try:
        # Find items
        item_records = tsi_repo.find(
            lambda r: r.doc_number.strip() == doc_number.strip(), max_results=1000
        )

        if not item_records:
            raise HTTPException(
                status_code=404, detail=f"No items found for document {doc_number}"
            )

        # Sort by line number
        item_records.sort(key=lambda r: r.line_number)

        # Convert to schema
        items = [DocumentItem.from_tsi_record(r) for r in item_records]

        return PaginatedResponse.create(
            data=items,
            page=1,
            page_size=len(items),
            total_items=len(items),
        )

    finally:
        tsi_repo.close()
