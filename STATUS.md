# NEX Automat — Current Status
Last updated: 2026-03-06

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL 16.12 with **24 tables**, 2 enums, 5 functions, 11+ sequences
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container on `nex-network`, `nex-config` package installed in image
- **Dynamic Module Registry** ✅ — `module_registry.yaml` (24 modules, 7 categories) as single source of truth; `GET /api/system/modules` endpoint (no auth); dynamic router registration in `main.py`; frontend `useModuleRegistry` hook + centralized `iconMap.ts`
- **PAB module** DONE: 30 endpoints, 77 tests, 20 frontend files (~3196 lines), 9 tabs, versioning (modify_id + partner_catalog_history + triggers), partner_class (business/retail/guest)
- **USR module** DONE ✅ | **PAB module** DONE ✅ | **MIG module** full-stack ✅ (backend API + frontend dashboard + run button + PAB migration working) | **GRP module** deferred | Remaining 20 modules — planned
- **PAB Migration** DONE ✅ — 164 partners migrated (+ extensions, addresses, contacts, bank_accounts, history), 0 errors
- **T6 Worker deduplication** DONE ✅ — `packages/nex-invoice-worker/` (merged supplier + andros workers, -6679 lines)
- **R2 nex-config centralized config** ✅ | **R3 complete** ✅ (staging, shared, backend apps, workers, Windows apps — all wired)
- **RAG chunk size unified** ✅ — `RAG_CHUNK_SIZE = 1500` in nex-config, all consumers wired
- NEX Manager Electron app: **v0.2.0**, 5 stores + 9 components + USR + PAB + MIG modules
- **CI/CD: 8/8 jobs passing** ✅ — all green
- **Test suite: 115 passing** (10 new registry + 105 existing), 1 pre-existing fail (DB connectivity)

## Recent Changes
- **2026-03-06** — 🐛 PAB Migration Fix + Run: fixed Dockerfile (missing COPY transform/load/data), `contact_type` constraint (`"main"→"person"`), `target_id` type (`UUID→VARCHAR(255)`); migrated **164 partners** (+ 164 ext, 163 addr, 18 contacts, 13 bank accts, 164 history), 0 errors
- **2026-03-06** — ▶️ MIG Run Button: category cards now show ▶ Spustiť / ↻ Re-run / spinner / 🔒 lock based on state, confirmation dialog, error display (+210 lines in MigrationDashboard.tsx)
- **2026-03-06** — 🔄 PAB ETL Rewrite (Session 14): rewritten for normalized `partner_catalog*` schema (6 tables, INTEGER PK), reset migration tracking, cleaned obsolete `partners` data. Ready for manual execution from MIG module.
- **2026-03-06** — 🔌 Dynamic Module Registry: `module_registry.yaml` (24 modules, 7 categories), `GET /api/system/modules`, dynamic router registration, frontend `useModuleRegistry` hook + `iconMap.ts`, 10 new tests (115 total), CI 8/8 green
- **2026-03-06** — 📚 Knowledge Base update: 5 files rewritten (PARTNERS_REFERENCE v2.0, DATABASE_SCHEMAS, STATUS, HISTORY, ARCHITECTURE), Qdrant 646→647
- **2026-03-06** — 🏗️ PAB Module Phase 2: Frontend UI — 20 files, 3196 lines, 9 tabs (BaseGrid + tabbed detail + History tab), CI 8/8 green
- **2026-03-06** — 🔄 PAB Versioning: modify_id + partner_class + partner_catalog_history + INSERT/UPDATE triggers + 20 new tests (77 total), CI 8/8 green
- **2026-03-06** — 📦 PAB Module Phase 1: 8-table DB migration + 28 backend API endpoints + 57 tests, CI 8/8 green
- **2026-03-06** — 🧹 T6 Worker Deduplication: merged supplier + andros workers → packages/nex-invoice-worker/, -6679 lines
- **2026-03-06** — 🔧 NEX Command Tech Debt Cleanup: fix 30 skipped tests, env var naming, build-windows fix — ZERO tech debt


## Known Issues
- 🟡 **Qdrant reindex partial failure** — Ollama embedding endpoint returns HTTP 500 from nex-brain (only 1/5 docs reindexed)
- 🟡 **No Alembic migrations** — schema managed via raw SQL; migration tooling not yet adopted
- 🟡 **1 pre-existing test failure** — DB connectivity test (not related to module registry)

## Next Steps
- **GRP module** — Group management (deferred, next priority)
- **Remaining 20 modules** — STK, GSC, FAK, etc. (planned, registry-ready via YAML)
- **M4 expand to other categories** — GSC, STK extractors following PAB pattern
- Fix Qdrant/Ollama reindex pipeline (HTTP 500 from nex-brain)
- Implement audit_log writes for login/permission events
