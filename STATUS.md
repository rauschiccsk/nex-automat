# NEX Automat — Current Status
Last updated: 2026-03-04

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL with **15 tables** (5 original + 7 system + 3 migration tracking)
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container on `nex-network`
- **PAB module** full-stack live: 4 CRUD endpoints + pagination/sorting/search + RBAC + audit log + Electron frontend (**BaseGrid-powered** list view + 6-tab form dialog) + 10 seed partners + 12/12 E2E tests passing
- **USR module** live ✅ | **PAB module** live ✅ | **MIG module** full-stack ✅ (backend API + frontend dashboard)
- **nex-migration M4 PABExtractor** ✅: 164 PAB records extracted from Btrieve (0 failures), cp852 encoding fix, BtrieveClient+PABRepository wiring
- **Grid infrastructure** ported ✅: `DataGrid` + `BaseGrid` + filters/formatters/types — TanStack React Table + Virtual, dark mode, server-side pagination, CSV/JSON export
- **PAB PartnerListView on BaseGrid** ✅: refactored from ~520 LOC to ~130 LOC, client-side loading (page_size: 10000), 30-column grid config with custom cell renderers (partner_type badges, is_active icons)
- **nex-migration M1–M3** ✅: M1 ETL architecture (18 files, 1217 LOC) + M2 Backend API (7 RBAC endpoints, 10 Pydantic schemas, 13 unit tests) + M3 Frontend (MigrationDashboard + CategoryDetail + RunWizard + grid configs, 9 files, 1364 LOC)
- **RBAC middleware** operational: `require_permission(module_code, permission)` factory
- **Module Registry API** live: 3 endpoints, JWT-protected, pg8000-compatible
- **24 modules** (7 categories + MIG), seed data: 1 admin, 5 groups, full permissions
- JWT auth fully operational: login, me, refresh, change-password — access_token (30min) + refresh_token
- NEX Manager Electron app: **v0.2.0**, 5 stores + 9 components + USR module + PAB module + MIG module, TS 0 errors
- **Dark mode fully operational**: Tailwind v4 `@custom-variant dark` enabled, 156+ dark: utilities active, system theme detection
- **Session persistence**: window bounds (electron-store), tabs + UI state (Zustand persist), logout cleanup, tab validation on module load
- **Login UX**: username auto-focused, Enter on username → focuses password, Enter on password → submits
- **R2 nex-config centralized config** ✅: `packages/nex-config/` — 7 modules (database, services, timeouts, limits, paths, rag, security), env-var driven, security guard
- **CI/CD: 8/8 jobs passing** ✅ — all green including Electron staging deploy
- Both self-hosted runners ONLINE: `nex-automat` (Linux), `nex-automat-win` (Windows)

## Recent Changes
- **2026-03-04** — 📦 R2 nex-config centralized config package: `packages/nex-config/` — 7 modules (database, services, timeouts, limits, paths, rag, security), env-var driven, security guard (RuntimeError if JWT_SECRET_KEY missing), smoke-tested, ruff-formatted — CI 8/8 green
- **2026-03-04** — 🔒 R1 Critical Security Fixes: removed hardcoded password from `test_pg8000_direct.py`, JWT secret now mandatory (RuntimeError if missing), DB name unified to `supplier_invoice_staging` across 11 files — CI 8/8 green
- **2026-03-04** — 🔍 Clean Code Audit (read-only): 3 critical findings — hardcoded DB password, JWT secret weak fallback, DB name inconsistency; 5 centralization items
- **2026-03-04** — ✅ Qdrant KB reindex: 259→289 points, DATABASE_SCHEMAS.md (22 chunks) + SCHEMA_GOVERNANCE.md (8 chunks) ingested via custom batch script
- **2026-03-04** — ✅ M4 PABExtractor WORKING: 164 PAB records extracted (0 failures), cp852 encoding fix
- **2026-03-04** — ✅ nex-migration M5 PAB Transform+Load: PABTransformer + PABLoader, 24 new tests, 102/102 total
- **2026-03-04** — ✅ nex-migration M3 Frontend: MigrationDashboard + CategoryDetail + RunWizard + migrationGridConfigs, 9 files (1364 LOC) — CI 8/8 green
- **2026-03-04** — ✅ nex-migration M2 Backend API: 7 RBAC endpoints, 10 Pydantic schemas, 13 unit tests — CI 8/8 green
- **2026-03-04** — ✅ nex-migration M1 ETL architecture: 18 files (1217 LOC), 3 DB tracking tables, 9 category dependency graph
- **2026-03-03** — ✅ PAB PartnerListView refactored to BaseGrid: ~520→~130 LOC, client-side loading (page_size: 10000) — CI 8/8 green

## Known Issues
- **M4 PABExtractor extraction done** — 164 records OK, but M4→M5 pipeline not yet wired into `/api/migration/run`
- 🟡 **R2 nex-config created but not yet consumed** — config package exists, R3–R5 needed to wire existing code to use it (replace hardcoded localhost:5432, magic values, Windows paths)
- **`resources/icon.ico` CHÝBA** — electron-builder zlyhá bez ikony; adresár `resources/` existuje ale je prázdny
- **ANDROS Windows SSH nedostupný** — `172.17.0.1` je Docker bridge (localhost), nie Windows VM; deploy workflow na ANDROS Windows nefunkčný
- **Store API gaps for UI toggles:** `commandLineActive` and `infoPanelOpen` not in uiStore — currently local state
- **MIG run endpoint returns 501** — placeholder until M4→M5 pipeline is wired into run endpoint
- 🟡 **No Alembic migrations** — schema managed via raw SQL; migration tooling not yet adopted

## Next Steps
- **Wire M4+M5 into `/api/migration/run`** — PABExtractor (164 records) + PABTransformer + PABLoader ready, need run endpoint integration
- **M4 expand to other categories** — GSC, STK extractors following PAB pattern
- Migrate remaining module list views to BaseGrid (GSC and others as modules are built)
- Dodať `resources/icon.ico` a otestovať `npm run dist` (Electron build → .exe)
- Vyriešiť SSH/RDP konektivitu na ANDROS Windows VM pre deploy workflow
- NEX Manager — connect module grid to live Module Registry API
- Implement audit_log writes for login/permission events (users CRUD already audit-logged)
- NEX Manager frontend — USR module UI (user list, create/edit forms, password management)
