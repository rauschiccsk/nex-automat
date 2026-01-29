"""
Staging API Routes - REST endpoints for supplier-invoice-staging-web
====================================================================
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from nex_staging import DatabaseConnection, InvoiceRepository
from nex_staging.models import FileStatus
from pydantic import BaseModel

from src.utils import config

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/staging", tags=["staging"])


# ============================================================================
# PYDANTIC MODELS FOR API
# ============================================================================


class UpdateItemPriceRequest(BaseModel):
    """Request to update item price."""

    selling_price_excl_vat: float


class UpdateItemsBatchRequest(BaseModel):
    """Request to update multiple items."""

    items: list[dict]


class ApproveInvoiceRequest(BaseModel):
    """Request to approve invoice."""

    status: str = "approved"


# ============================================================================
# DEPENDENCY - Database Connection
# ============================================================================


def get_repository() -> InvoiceRepository:
    """Get invoice repository with database connection."""
    import os

    db = DatabaseConnection(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DATABASE,
        user=config.POSTGRES_USER,
        password=os.environ.get("POSTGRES_PASSWORD", config.POSTGRES_PASSWORD or ""),
    )
    return InvoiceRepository(db)


# ============================================================================
# ENDPOINTS
# ============================================================================


@router.get("/config")
async def get_staging_config():
    """
    Get staging web UI configuration.

    Returns customer-specific settings for the staging web UI,
    controlling which features are available (price edit, margin edit, etc.)

    Returns:
        StagingWebConfig dict with allow_* flags
    """
    return config.STAGING_WEB_CONFIG


@router.get("/invoices")
async def get_invoices(file_status: str | None = None, limit: int = 100):
    """
    Get list of staging invoices.

    Args:
        file_status: Filter by status (received/staged/archived)
        limit: Maximum number of invoices

    Returns:
        List of invoice heads
    """
    try:
        repo = get_repository()

        status_filter = None
        if file_status:
            status_filter = FileStatus(file_status)

        heads = repo.get_invoice_heads(file_status=status_filter, limit=limit)

        result = []
        for h in heads:
            result.append(
                {
                    "id": h.id,
                    "xml_invoice_number": h.xml_invoice_number,
                    "xml_issue_date": str(h.xml_issue_date) if h.xml_issue_date else None,
                    "xml_due_date": str(h.xml_due_date) if h.xml_due_date else None,
                    "xml_supplier_ico": h.xml_supplier_ico,
                    "xml_supplier_name": h.xml_supplier_name,
                    "xml_total_without_vat": float(h.xml_total_without_vat)
                    if h.xml_total_without_vat
                    else None,
                    "xml_total_vat": float(h.xml_total_vat) if h.xml_total_vat else None,
                    "xml_total_with_vat": float(h.xml_total_with_vat)
                    if h.xml_total_with_vat
                    else None,
                    "xml_currency": h.xml_currency,
                    "file_status": h.file_status.value if h.file_status else None,
                    "item_count": h.item_count,
                    "items_matched": h.items_matched,
                    "match_percent": float(h.match_percent) if h.match_percent else None,
                    "created_at": str(h.created_at) if h.created_at else None,
                }
            )

        return {"count": len(result), "invoices": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/invoices/{invoice_id}")
async def get_invoice_detail(invoice_id: int):
    """
    Get invoice with items.

    Args:
        invoice_id: Invoice head ID

    Returns:
        Invoice head with items
    """
    try:
        repo = get_repository()

        # Get all heads and find the one we need
        heads = repo.get_invoice_heads()
        head = next((h for h in heads if h.id == invoice_id), None)

        if not head:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Get items
        items = repo.get_invoice_items(invoice_id)

        return {
            "invoice": {
                "id": head.id,
                "xml_invoice_number": head.xml_invoice_number,
                "xml_issue_date": str(head.xml_issue_date) if head.xml_issue_date else None,
                "xml_due_date": str(head.xml_due_date) if head.xml_due_date else None,
                "xml_supplier_ico": head.xml_supplier_ico,
                "xml_supplier_name": head.xml_supplier_name,
                "xml_total_without_vat": float(head.xml_total_without_vat)
                if head.xml_total_without_vat
                else None,
                "xml_total_vat": float(head.xml_total_vat) if head.xml_total_vat else None,
                "xml_total_with_vat": float(head.xml_total_with_vat)
                if head.xml_total_with_vat
                else None,
                "xml_currency": head.xml_currency,
                "file_status": head.file_status.value if head.file_status else None,
                "item_count": head.item_count,
                "items_matched": head.items_matched,
            },
            "items": [
                {
                    "id": item.id,
                    "invoice_head_id": item.invoice_head_id,
                    "xml_line_number": item.xml_line_number,
                    "xml_seller_code": item.xml_seller_code,
                    "xml_ean": item.xml_ean,
                    "xml_product_name": item.xml_product_name,
                    "xml_quantity": float(item.xml_quantity) if item.xml_quantity else None,
                    "xml_unit": item.xml_unit,
                    "xml_unit_price": float(item.xml_unit_price) if item.xml_unit_price else None,
                    "xml_unit_price_vat": float(item.xml_unit_price_vat)
                    if item.xml_unit_price_vat
                    else None,
                    "xml_total_price": float(item.xml_total_price)
                    if item.xml_total_price
                    else None,
                    "xml_vat_rate": float(item.xml_vat_rate) if item.xml_vat_rate else None,
                    "nex_product_id": item.nex_product_id,
                    "nex_product_name": item.nex_product_name,
                    "nex_ean": item.nex_ean,
                    "matched": item.matched,
                    "matched_by": item.matched_by,
                    "edited_unit_price": float(item.edited_unit_price)
                    if item.edited_unit_price
                    else None,
                }
                for item in items
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}")
async def update_item_price(item_id: int, request: UpdateItemPriceRequest):
    """
    Update single item price.

    Args:
        item_id: Item ID
        request: New price data

    Returns:
        Success status
    """
    try:
        repo = get_repository()
        success = repo.update_item_pricing(item_id, request.selling_price_excl_vat)

        if not success:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"success": True, "item_id": item_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/batch")
async def update_items_batch(request: UpdateItemsBatchRequest):
    """
    Update multiple items at once.

    Args:
        request: List of items with prices

    Returns:
        Count of updated items
    """
    try:
        repo = get_repository()
        updated = repo.save_items_batch(request.items)

        return {"success": True, "updated_count": updated}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/invoices/{invoice_id}/approve")
async def approve_invoice(invoice_id: int, request: ApproveInvoiceRequest):
    """
    Approve invoice and change status.

    Args:
        invoice_id: Invoice head ID
        request: Approval data

    Returns:
        Success status
    """
    try:
        repo = get_repository()

        # Update file_status to archived (approved)
        success = repo.update_file_status(invoice_id, FileStatus.ARCHIVED)

        if not success:
            raise HTTPException(status_code=404, detail="Invoice not found")

        return {"success": True, "invoice_id": invoice_id, "status": "archived"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
