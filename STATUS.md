# NEX Automat — Current Status
Last updated: 2026-03-04

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL with **15 tables** (5 original + 7 system + 3 migration tracking)
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container on `nex-network`
- **PAB module** full-stack live: 4 CRUD endpoints + pagination/sorting/search + RBAC + audit log + Electron frontend (**BaseGrid-powered** list view + 6-tab form dialog) + 10 seed partners + 12/12 E2E tests passing
- **USR module** live ✅ | **PAB module** live ✅
- **Grid infrastructure** ported ✅: `DataGrid` + `BaseGrid` + filters/formatters/types — TanStack React Table + Virtual, dark mode, server-side pagination, CSV/JSON export
- **PAB PartnerListView on BaseGrid** ✅: refactored from ~520 LOC to ~130 LOC, client-side loading (page_size: 10000), 30-column grid config with custom cell renderers (partner_type badges, is_active icons)
- **nex-migration ETL module** ✅ M1 (architecture): 18 files, 1217 LOC — extractors (Windows/Btrieve), transformers, loaders (PostgreSQL), 9 category dependency graph (PAB→GSC→STK→TSH→ICB→ISB→OBJ→DOD→PAYJRN), 3 tracking DB tables, PAB field mappings from real nexdata
- **RBAC middleware** operational: `require_permission(module_code, permission)` factory
- **Module Registry API** live: 3 endpoints, JWT-protected, pg8000-compatible
- **23 modules** (7 categories), seed data: 1 admin, 5 groups, full permissions
- JWT auth fully operational: login, me, refresh, change-password — access_token (30min) + refresh_token
- NEX Manager Electron app: **v0.2.0**, 5 stores + 9 components + USR module + PAB module, TS 0 errors
- **Dark mode fully operational**: Tailwind v4 `@custom-variant dark` enabled, 156+ dark: utilities active, system theme detection
- **Session persistence**: window bounds (electron-store), tabs + UI state (Zustand persist), logout cleanup, tab validation on module load
- **Login UX**: username auto-focused, Enter on username → focuses password, Enter on password → submits
- **CI/CD: 8/8 jobs passing** ✅ — all green including Electron staging deploy
- Both self-hosted runners ONLINE: `nex-automat` (Linux), `nex-automat-win` (Windows)

## Recent Changes
- **2026-03-04** — ✅ nex-migration M1 ETL architecture: 18 files (1217 LOC), 3 DB tracking tables (batches/id_map/category_status), 9 category dependency graph, PAB field mappings from real nexdata, abstract extractors/transformers/loaders, 12 transform functions, CLI runners (Windows extract + Ubuntu load) — CI 8/8 green (3 commits)
- **2026-03-03** — ✅ PAB PartnerListView refactored to BaseGrid: ~520→~130 LOC, `partnersGridConfig.tsx` (30 columns, custom cell renderers — partner_type color badges, is_active icons), client-side loading (page_size: 10000), toolbar with RBAC "Nový partner" button, row double-click edit — CI 8/8 green
- **2026-03-03** — ✅ Grid infrastructure port: 6 new files in `components/grids/` — DataGrid (~700 LOC), BaseGrid, gridTypes, gridFilters, gridFormatters, index — TanStack React Table + Virtual, dark mode, server-side pagination, native dialog, Tailwind v4 compatible, TS 0 errors
- **2026-03-03** — ✅ PAB module seed + E2E: 10 sample partners (SK/CZ/HU/AT, various types/payment methods), 12 E2E tests PASS
- **2026-03-03** — ✅ PAB module frontend: `PartnerListView` + `PartnerFormDialog` (6-tab form), API service, TS types, module registration — CI 8/8 green
- **2026-03-03** — ✅ PAB module backend: `partners` table (UUID, RAG-compatible schema), 4 CRUD endpoints, pagination + sorting + search, RBAC, audit log, 16 unit tests — CI 8/8 green
- **2026-03-03** — ✅ Dark mode fix: Tailwind v4 `@custom-variant dark` in `index.css`, system theme detection — CI 8/8 green
- **2026-03-03** — ✅ Session persistence: window bounds (electron-store), tab persistence (Zustand persist), logout cleanup, tab validation
- **2026-03-03** — ✅ Login Enter-key UX + autoFocus on username input
- **2026-03-03** — ✅ App versioning pipeline: version bump to **v0.2.0** — CI 8/8 green
- **2026-03-03** — ✅ USR module backend: 5 CRUD endpoints + password management, RBAC, audit log, 22 unit tests

## Known Issues
- **`resources/icon.ico` CHÝBA** — electron-builder zlyhá bez ikony; adresár `resources/` existuje ale je prázdny
- **ANDROS Windows SSH nedostupný** — `172.17.0.1` je Docker bridge (localhost), nie Windows VM; deploy workflow na ANDROS Windows nefunkčný
- **Store API gaps for UI toggles:** `commandLineActive` and `infoPanelOpen` not in uiStore — currently local state
- **Mypy + unit test annotations**: pre-existing CI warnings (non-blocking, same as previous green runs)

## Next Steps
- **nex-migration M2**: Implement PAB concrete extractor + transformer + loader (first working category end-to-end)
- Migrate remaining module list views to BaseGrid (GSC and others as modules are built)
- Dodať `resources/icon.ico` a otestovať `npm run dist` (Electron build → .exe)
- Vyriešiť SSH/RDP konektivitu na ANDROS Windows VM pre deploy workflow
- NEX Manager — connect module grid to live Module Registry API
- Implement audit_log writes for login/permission events (users CRUD already audit-logged)
- NEX Manager frontend — USR module UI (user list, create/edit forms, password management)
