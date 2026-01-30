"""API Routes for Btrieve-Loader REST API."""

from fastapi import APIRouter

from .barcodes import router as barcodes_router
from .documents import router as documents_router
from .health import router as health_router
from .legacy import invoice_router
from .partners import router as partners_router
from .products import router as products_router
from .stores import router as stores_router

# Main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(partners_router, prefix="/partners", tags=["Partners"])
api_router.include_router(barcodes_router, prefix="/barcodes", tags=["Barcodes"])
api_router.include_router(stores_router, prefix="/stores", tags=["Stores"])
api_router.include_router(documents_router, prefix="/documents", tags=["Documents"])

__all__ = ["api_router", "invoice_router"]
