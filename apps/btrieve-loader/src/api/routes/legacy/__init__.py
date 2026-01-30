"""Legacy routes for backward compatibility."""

from .invoice import router as invoice_router

__all__ = ["invoice_router"]
