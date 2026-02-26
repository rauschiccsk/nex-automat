# NEX Automat — Current Status
Last updated: 2026-02-26

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL with **11 tables** (5 original + 6 system)
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container `nex-manager-api` on `nex-network`
- **RBAC middleware** operational: `require_permission(module_code, permission)` factory — whitelist-validated, group-aggregated permission checks with 403 responses
- **Module Registry API** live: 3 endpoints (`/api/modules`, `/api/modules/by-category`, `/api/modules/{code}`) — JWT-protected, pg8000-compatible
- JWT auth fully operational: login, me, refresh endpoints — access_token (30min) + refresh_token
- DB driver: pg8000 (pure Python), raw SQL with cursor.execute()
- System DB tables live: `users`, `groups`, `user_groups`, `modules`, `group_module_permissions`, `audit_log`
- Seed data: 1 admin, 5 groups, 24 modules (7 categories), admin→Administrátori with full permissions (24/24)
- Migration system created: `database/migrations/` (no Alembic — custom)
- Temporal workflows production — invoice processing
- NEX Manager Electron app: 5 stores + 9 components, App.tsx complete, TS 0 errors, build passing (v0.1.21, 714 kB + 32 kB CSS)
- **User property mapping fixed**: `AuthUser.name` maps `full_name` from API → Header displays initials from full name (e.g. "JN"), not login username
- All 9 components + 5 stores verified: git-tracked and locally present, no discrepancies
- Repository file paths cleaned — 0 backslash filenames remaining
- CI/CD: **7/8 jobs passing** ✅ — lint, security, unit tests, docker builds (brain + telegram), electron build, backend staging deploy; electron staging deploy failing (SCP infra issue)
- CI electron build: electron-vite build + portable unpacked (`--dir`), runs on `ANDROS-WIN` with `shell: pwsh`
- DEPTEST staging stack: PostgreSQL + Temporal + Temporal UI (3 containers) — all healthy
- gh CLI authenticated on ANDROS Ubuntu — `rauschiccsk`, HTTPS, v2.87.2, CI monitoring operational
- RAG: Qdrant + Ollama, 222 points

## Recent Changes
- **2026-02-26** — ✅ Fix user property mapping: `AuthUser` gets `name` field (`full_name || username`); Header.tsx uses `user.name` for initials & display — white screen after login resolved (commit `ddb5496`)
- **2026-02-26** — ✅ RBAC Middleware: `require_permission()` factory in `auth/dependencies.py` — whitelist validation, `bool_or` group aggregation, 403 responses
- **2026-02-26** — ✅ Module Registry API: 3 endpoints (`/api/modules`, `by-category`, `{code}`) — JWT-protected, category/mock filters, pg8000 `::text` casts
- **2026-02-26** — ✅ CI: 7/8 jobs passing (run #22452772637) — electron staging deploy SCP failure (infra, not code)
- **2026-02-26** — ✅ JWT Auth Endpoints: nex-manager-api microservice (FastAPI, port 9110) — login/me/refresh all tested, Docker container running
- **2026-02-26** — ✅ System DB: 6 tables created (users, groups, user_groups, modules, group_module_permissions, audit_log) + seed data + migration system
- **2026-02-26** — ✅ CI: all 8 jobs passing (including previously-failing build-electron + staging deploys)
- **2026-02-26** — ✅ CI diagnostics: retrieved full error log from run `22437723428` — root cause identified: `electron-builder` v26.8.1 rejects `--config.win.sign`
- **2026-02-24** — ✅ Added `npm run build` verification, NEX Manager shell verification — 9 components + 5 stores confirmed

## Known Issues
- **CI electron staging deploy failing** — SCP infra issue, not code (7/8 jobs passing)
- **`resources/icon.ico` CHÝBA** — electron-builder zlyhá bez ikony; adresár `resources/` existuje ale je prázdny
- **ANDROS Windows SSH nedostupný** — `172.17.0.1` je Docker bridge (localhost), nie Windows VM; deploy workflow na ANDROS Windows nefunkčný
- **Store API gaps for UI toggles:** `commandLineActive` and `infoPanelOpen` not in uiStore — currently local state

## Next Steps
- Investigate CI electron staging deploy SCP failure
- Dodať `resources/icon.ico` a otestovať `npm run dist` (Electron build → .exe)
- Vyriešiť SSH/RDP konektivitu na ANDROS Windows VM pre deploy workflow
- NEX Manager — connect module grid to live Module Registry API
- Implement audit_log writes for login/permission events
