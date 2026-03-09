# NEX Automat — Current Status
Last updated: 2026-03-09 (v10)

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL 16.12 with **29 tables**, 2 enums, 6 functions, 11+ sequences, 5 triggers
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container on `nex-network`, `nex-config` package installed in image
- **Dynamic Module Registry** ✅ — `module_registry.yaml` (24 modules, 7 categories) as single source of truth; `GET /api/system/modules` endpoint (no auth); dynamic router registration in `main.py`; frontend `useModuleRegistry` hook + centralized `iconMap.ts`
- **ESHOP module** DONE ✅ — multi-tenant e-shop integration: 5 DB tables, 19 endpoints (4 public + 2 payment + 9 admin + 4 MuFis), 3 auth layers (`X-Eshop-Token`, JWT, `API-KEY`), tenant resolution, order lifecycle, stock sync, **Comgate payment gateway** integration
- **PAB module** DONE: endpoints, 77 backend tests, 20 frontend files, 9 tabs, versioning (modify_id + partner_catalog_history + triggers), partner_class (business/retail/guest), `partner_code` removed (redundant with `partner_id`)
- **USR module** DONE ✅ | **PAB module** DONE ✅ | **MIG module** full-stack ✅ | **ESHOP module** DONE ✅ | **GRP module** deferred | Remaining 19 modules — planned
- **PAB Migration** DONE ✅ — 164 partners re-migrated (+ extensions, addresses, contacts, bank_accounts, history), 0 errors, diacritics fixed, country_code mapping corrected, partner_code removed
- **T6 Worker deduplication** DONE ✅ — `packages/nex-invoice-worker/` (merged supplier + andros workers, -6679 lines)
- **R2 nex-config centralized config** ✅ | **R3 complete** ✅ (staging, shared, backend apps, workers, Windows apps — all wired)
- **RAG chunk size unified** ✅ — `RAG_CHUNK_SIZE = 1500` in nex-config, all consumers wired
- NEX Manager Electron app: **v0.2.0**, 5 stores + 9 components + USR + PAB + MIG modules
- **Frontend test infrastructure** ✅ — Vitest + React Testing Library + jsdom, **277 tests**, V8 coverage (80% thresholds); **PAB tabs coverage ~98% stmts / ~80% branches** (9 tabs, all ≥80%)
- **Playwright E2E tests** ✅ — 39 passed / 6 skipped / 0 failed, proper waits, **hard-delete teardown** (no soft-delete pollution), safety guards (partner_id ≥ 95000 only)
- **CI/CD: 10/10 jobs passing** ✅ — all green; E2E job #10 **conditional** (runs only with `[e2e]` commit tag)
- **Test suite: 178 backend + 277 frontend + 39 E2E = 494 total**, 1 pre-existing fail (DB connectivity)
- **TESTING.md** ✅ — Knowledge Base document defining 3-layer testing architecture (Vitest+RTL → Playwright → MAT)

## Recent Changes
- **2026-03-09** — 💳 F1.4: Comgate payment gateway integration — `ComgateClient` service (`comgate.py`), `POST /payment/callback` (Comgate notification), `GET /payment/return` (customer redirect), order creation with `payment_url`, 22 new tests (63 ESHOP total), idempotent callbacks, constant-time secret verification
- **2026-03-09** — 🛒 ESHOP module: full-stack backend — 5 DB tables (`eshop_tenants/products/orders/order_items/order_status_history`), 3 triggers, 17 endpoints (public 4 + admin 9 + MuFis 4), 3 auth layers, 41 backend tests; CI 10/10 GREEN
- **2026-03-07** — 🧪 F2.5: PAB tabs coverage boost — 99 new tests in PabTabs.test.tsx (27→126), all 9 tabs now ≥80% coverage; avg stmts 49%→98%, branches 47%→80%, funcs 27%→96%; 277 frontend tests total; CI green
- **2026-03-07** — 🧪 F5: MIG + USR frontend unit tests — 47 new tests (7 files): MIG (24) + USR (23); API paths corrected; all 127 frontend tests passing
- **2026-03-07** — ✅ F4c: E2E cleanup fix + CI split — hard-delete teardown, safety guards (partner_id ≥ 95000), E2E job conditional (`[e2e]` tag); CI 10/10 GREEN
- **2026-03-07** — ✅ F4b: E2E CI fix — replaced 28× `waitForTimeout` with proper Playwright waits; 39 passed / 6 skipped / 0 failed — **CI 10/10 GREEN**
- **2026-03-07** — ❌ F4: Playwright E2E infra + 22 scenarios + CI job #10 — FAILED (SSH timeout after 3600s on ubuntu-cc, no changes applied)
- **2026-03-07** — 📋 TESTING.md Knowledge Base: 3-layer testing architecture (Vitest+RTL → Playwright → MAT), module test status matrix, universal MAT checklist
- **2026-03-07** — 🧪 F2: PAB Frontend Tests — 74 new tests across 5 files; PAB coverage ~76% statements, 75% branches — CI 9/9 green
- **2026-03-07** — 🧪 Frontend Test Infra: Vitest + RTL + jsdom setup, 6 smoke tests, CI `frontend-tests` job #9 — CI 9/9 green
- **2026-03-06** — 🐛 PAB Migration Fix + Run: migrated **164 partners** (+ ext, addr, contacts, bank accts, history), 0 errors

## Known Issues
- 🟡 **Qdrant reindex partial failure** — Ollama embedding endpoint returns HTTP 500 from nex-brain (only 1/5 docs reindexed)
- 🟡 **No Alembic migrations** — schema managed via raw SQL; migration tooling not yet adopted
- 🟡 **1 pre-existing test failure** — DB connectivity test (not related to module registry)
- 🟡 **6 E2E tests skipped** — non-blocking, to be investigated

## Next Steps
- **ESHOP Comgate credentials** — Add `comgate_merchant_id`, `comgate_secret` to `eshop_tenants` table and configure per-tenant
- **ESHOP frontend** — Admin UI for orders/products/tenants management in NEX Manager
- **GRP module** — Group management (deferred, next priority)
- **Remaining 19 modules** — STK, GSC, FAK, etc. (planned, registry-ready via YAML)
- **M4 expand to other categories** — GSC, STK extractors following PAB pattern
- Fix Qdrant/Ollama reindex pipeline (HTTP 500 from nex-brain)
- Implement audit_log writes for login/permission events
