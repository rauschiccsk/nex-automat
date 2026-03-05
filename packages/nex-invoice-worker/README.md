# nex-invoice-worker

Shared multi-tenant invoice worker package for the NEX Automat platform.

## Overview

This package is the unified multi-tenant invoice worker (formerly `apps/supplier-invoice-worker/`
and `apps/andros-invoice-worker/`, now consolidated) with tenant-aware configuration.

## Usage

Set `WORKER_TENANT` environment variable to select the tenant mode:

```bash
# Supplier (ICC) mode - email/PDF + API pipeline
WORKER_TENANT=supplier python -m nex_invoice_worker.workers.main_worker

# Andros mode - API + PostgreSQL persistence
WORKER_TENANT=andros python -m nex_invoice_worker.workers.main_worker
```

## Docker

Single Dockerfile supports both tenants via environment variable:

```yaml
supplier-invoice-worker:
  build: ./packages/nex-invoice-worker
  environment:
    - WORKER_TENANT=supplier

andros-invoice-worker:
  build: ./packages/nex-invoice-worker
  environment:
    - WORKER_TENANT=andros
```

## Tenant Differences

| Feature | Supplier (ICC) | Andros |
|---------|---------------|--------|
| Task queue | supplier-invoice-queue | andros-invoice-queue |
| Customer code | ICC | ANDROS |
| MARSO IČO | 10428342 | 10428342215 |
| Email/PDF pipeline | Yes | No |
| PostgreSQL persistence | No | Yes |
| Invoice deduplication | No | Yes |
| Pipeline posting | Always | Optional (skip_pipeline) |
