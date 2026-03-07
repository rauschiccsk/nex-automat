# NEX Automat — Current Status
Last updated: 2026-03-07 (v6)

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL 16.12 with **24 tables**, 2 enums, 5 functions, 11+ sequences
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container on `nex-network`, `nex-config` package installed in image
- **Dynamic Module Registry** ✅ — `module_registry.yaml` (24 modules, 7 categories) as single source of truth; `GET /api/system/modules` endpoint (no auth); dynamic router registration in `main.py`; frontend `useModuleRegistry` hook + centralized `iconMap.ts`
- **PAB module** DONE: endpoints, 77 backend tests, 20 frontend files, 9 tabs, versioning (modify_id + partner_catalog_history + triggers), partner_class (business/retail/guest), `partner_code` removed (redundant with `partner_id`)
- **USR module** DONE ✅ | **PAB module** DONE ✅ | **MIG module** full-stack ✅ (backend API + frontend dashboard + run button + PAB migration working) | **GRP module** deferred | Remaining 20 modules — planned
- **PAB Migration** DONE ✅ — 164 partners re-migrated (+ extensions, addresses, contacts, bank_accounts, history), 0 errors, diacritics fixed, country_code mapping corrected, partner_code removed
- **T6 Worker deduplication** DONE ✅ — `packages/nex-invoice-worker/` (merged supplier + andros workers, -6679 lines)
- **R2 nex-config centralized config** ✅ | **R3 complete** ✅ (staging, shared, backend apps, workers, Windows apps — all wired)
- **RAG chunk size unified** ✅ — `RAG_CHUNK_SIZE = 1500` in nex-config, all consumers wired
- NEX Manager Electron app: **v0.2.0**, 5 stores + 9 components + USR + PAB + MIG modules
- **Frontend test infrastructure** ✅ — Vitest + React Testing Library + jsdom, **80 tests** (6 smoke + 17 DataGrid + 57 PAB), V8 coverage (80% thresholds)
- **Playwright E2E tests** ✅ — 39 passed / 6 skipped / 0 failed, all `waitForTimeout` replaced with proper waits (28 occurrences in 6 files)
- **CI/CD: 10/10 jobs passing** ✅ — all green (includes `frontend-tests` #9 + `e2e-tests` #10)
- **Test suite: 115 backend + 80 frontend + 39 E2E = 234 total**, 1 pre-existing fail (DB connectivity)
- **TESTING.md** ✅ — Knowledge Base document defining 3-layer testing architecture (Vitest+RTL → Playwright → MAT)

## Recent Changes
- **2026-03-07** — ✅ F4b: E2E CI fix — replaced 28× `waitForTimeout` with proper Playwright waits (`waitForResponse`, `waitFor`, `toBeVisible`) in 6 files; CI timeout 15→30min; `playwright.config.ts` timeouts (test: 20s, expect: 3s); 39 passed / 6 skipped / 0 failed; commit `e939434` — **CI 10/10 GREEN**
- **2026-03-07** — ❌ F4: Playwright E2E infra + 22 scenarios + CI job #10 — FAILED (SSH timeout after 3600s on ubuntu-cc, no changes applied)
- **2026-03-07** — 📋 TESTING.md Knowledge Base: 3-layer testing architecture (Vitest+RTL → Playwright → MAT), module test status matrix (USR/PAB/MIG), universal MAT checklist (7 sections, ~50 items), module-specific MAT sections (PAB 5 sections, MIG 4, USR 4), new module onboarding guide — 210 lines
- **2026-03-07** — 🧪 F2: PAB Frontend Tests — 74 new tests across 5 files: DataGrid (17), PabPartnerList (11), PabCreateDialog (10), PabPartnerDetail (9), PabTabs (27); key adaptations: `@tanstack/react-virtual` mock, `vi.hoisted()` for API mocks, `blurFilters()` helper; PAB coverage ~76% statements, 75% branches — CI 9/9 green
- **2026-03-07** — 🧪 Frontend Test Infra: Vitest + RTL + jsdom setup, `vitest.config.ts`, `setup.ts` (window.electron/api mocks, matchMedia polyfill), 6 smoke tests, CI `frontend-tests` job #9 — CI 9/9 green
- **2026-03-06** — 🐛 PAB Migration Fix + Run: fixed Dockerfile (missing COPY transform/load/data), `contact_type` constraint (`"main"→"person"`), `target_id` type (`UUID→VARCHAR(255)`); migrated **164 partners** (+ 164 ext, 163 addr, 18 contacts, 13 bank accts, 164 history), 0 errors
- **2026-03-06** — ▶️ MIG Run Button: category cards now show ▶ Spustiť / ↻ Re-run / spinner / 🔒 lock based on state, confirmation dialog, error display
- **2026-03-06** — 🔄 PAB ETL Rewrite (Session 14): rewritten for normalized `partner_catalog*` schema (6 tables, INTEGER PK), reset migration tracking, cleaned obsolete `partners` data
- **2026-03-06** — 🔌 Dynamic Module Registry: `module_registry.yaml` (24 modules, 7 categories), `GET /api/system/modules`, dynamic router registration, frontend `useModuleRegistry` hook + `iconMap.ts`, 10 new tests (115 total), CI 8/8 green
- **2026-03-06** — 📚 Knowledge Base update: 5 files rewritten (PARTNERS_REFERENCE v2.0, DATABASE_SCHEMAS, STATUS, HISTORY, ARCHITECTURE), Qdrant 646→647
- **2026-03-06** — 🏗️ PAB Module Phase 2: Frontend UI — 20 files, 3196 lines, 9 tabs (BaseGrid + tabbed detail + History tab), CI 8/8 green

## Known Issues
- 🟡 **Qdrant reindex partial failure** — Ollama embedding endpoint returns HTTP 500 from nex-brain (only 1/5 docs reindexed)
- 🟡 **No Alembic migrations** — schema managed via raw SQL; migration tooling not yet adopted
- 🟡 **1 pre-existing test failure** — DB connectivity test (not related to module registry)
- 🟡 **6 E2E tests skipped** — non-blocking, to be investigated

## Next Steps
- **GRP module** — Group management (deferred, next priority)
- **Remaining 20 modules** — STK, GSC, FAK, etc. (planned, registry-ready via YAML)
- **M4 expand to other categories** — GSC, STK extractors following PAB pattern
- Fix Qdrant/Ollama reindex pipeline (HTTP 500 from nex-brain)
- Implement audit_log writes for login/permission events
