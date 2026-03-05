"""Tenant configuration for multi-tenant invoice worker.

The WORKER_TENANT environment variable determines the worker mode:
  - "supplier": ICC supplier invoice processing
  - "andros": ANDROS invoice processing
"""

import os
from enum import Enum


class WorkerTenant(str, Enum):
    """Supported worker tenants."""

    SUPPLIER = "supplier"
    ANDROS = "andros"


def get_tenant() -> WorkerTenant:
    """Get current tenant from WORKER_TENANT environment variable.

    Returns:
        WorkerTenant enum value (defaults to SUPPLIER if not set)
    """
    tenant = os.getenv("WORKER_TENANT", "supplier")
    return WorkerTenant(tenant)
