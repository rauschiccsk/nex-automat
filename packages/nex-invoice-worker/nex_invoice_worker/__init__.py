"""
NEX Invoice Worker - Shared multi-tenant invoice processing package.

Supports WORKER_TENANT environment variable for tenant-specific behavior:
  - "supplier" (default): ICC supplier invoice processing (email/PDF + API pipeline)
  - "andros": ANDROS invoice processing (API + PostgreSQL persistence)

Usage:
    from nex_invoice_worker.config import get_tenant, WorkerTenant
    from nex_invoice_worker.config.settings import get_settings
"""
