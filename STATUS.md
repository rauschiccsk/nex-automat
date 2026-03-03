# NEX Automat — Current Status
Last updated: 2026-03-03

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL with **11 tables** (5 original + 6 system)
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container `nex-manager-api` on `nex-network`
- **RBAC middleware** operational: `require_permission(module_code, permission)` factory — whitelist-validated, group-aggregated permission checks with 403 responses
- **Module Registry API** live: 3 endpoints (`/api/modules`, `/api/modules/by-category`, `/api/modules/{code}`) — JWT-protected, pg8000-compatible
- **Module inventory verified**: **23 modules** (7 categories) — PAB="Katalóg partnerov", GSC="Katalóg produktov" (category=catalogs), VAH removed; all match INVENTORY.md across DB seed, live DB, backend, and frontend
- JWT auth fully operational: login, me, refresh endpoints — access_token (30min) + refresh_token
- DB driver: pg8000 (pure Python), raw SQL with cursor.execute()
- System DB tables live: `users`, `groups`, `user_groups`, `modules`, `group_module_permissions`, `audit_log`
- Seed data: 1 admin, 5 groups, **23 modules** (7 categories), admin→Administrátori with full permissions (23/23)
- Migration system created: `database/migrations/` (no Alembic — custom)
- Temporal workflows production — invoice processing
- NEX Manager Electron app: 5 stores + 9 components, App.tsx complete, TS 0 errors, build passing (**v0.1.38**, 714 kB + 32 kB CSS)
- **Frontend icon rendering**: `ICON_MAP` + `<IconComponent />` pattern across Sidebar, InfoPanel, CommandLine
- **Login→logout loop fixed**: race condition in App.tsx resolved — selective 401-only logout, concurrent loadModules guard, debug breadcrumbs
- All 9 components + 5 stores verified: git-tracked and locally present, no discrepancies
- Repository file paths cleaned — 0 backslash filenames remaining
- CI/CD: **7/8 jobs passing** ✅ — lint, security, unit tests, docker builds (brain + telegram), electron build, backend staging deploy; electron staging deploy failing (Windows `Access is denied` permission issue)
- CI electron build: electron-vite build + portable unpacked (`--dir`), runs on `ANDROS-WIN` with `shell: pwsh`
- **CI deploy strategy**: Staging deploys trigger on `develop` push only; production deploy on `main` via manual `workflow_dispatch` (`deploy.yml`)
- Both self-hosted runners ONLINE: `nex-automat` (Linux/ANDROS), `nex-automat-win` (Windows/ANDROS-WIN)
- DEPTEST staging stack: PostgreSQL + Temporal + Temporal UI (3 containers) — all healthy
- gh CLI authenticated on ANDROS Ubuntu — `rauschiccsk`, HTTPS, v2.87.2, CI monitoring operational
- RAG: Qdrant + Ollama, 222 points

## Recent Changes
- **2026-03-03** — ✅ Module cleanup: PAB renamed "Katalóg partnerov", GSC renamed "Katalóg produktov", category→catalogs, VAH removed → **23 modules**; INVENTORY.md updated
- **2026-03-03** — ✅ Frontend icon system: `ICON_MAP` + `<IconComponent />` rendering in Sidebar, InfoPanel, CommandLine
- **2026-03-03** — ✅ CI 7/8 passing: electron staging deploy fails on `Stop-Process "NEX Manager"` (Access is denied — Windows runner permission issue, not code)
- **2026-03-03** — ✅ Module inventory audit: verified all 23 modules across DB seed, live DB, backend schemas/router, and frontend match INVENTORY.md
- **2026-03-03** — ✅ CI deploy diagnostics: confirmed staging deploy jobs are `develop`-only by design; `main` uses manual `deploy.yml` (workflow_dispatch)
- **2026-02-26** — ✅ Fix login→logout loop: race condition in App.tsx — selective 401-only logout, concurrent loadModules guard
- **2026-02-26** — ✅ Fix user property mapping: `AuthUser` gets `name` field (`full_name || username`); Header.tsx uses `user.name` for initials & display
- **2026-02-26** — ✅ RBAC Middleware: `require_permission()` factory in `auth/dependencies.py` — whitelist validation, `bool_or` group aggregation, 403 responses
- **2026-02-26** — ✅ Module Registry API: 3 endpoints (`/api/modules`, `by-category`, `{code}`) — JWT-protected, category/mock filters, pg8000 `::text` casts
- **2026-02-26** — ✅ CI: 7/8 jobs passing (run #22452772637) — electron staging deploy SCP failure (infra, not code)

## Known Issues
- **CI electron staging deploy failing** — `Stop-Process "NEX Manager"` gets `Access is denied` on Windows runner (process runs under different user than runner); not code-related
- **`resources/icon.ico` CHÝBA** — electron-builder zlyhá bez ikony; adresár `resources/` existuje ale je prázdny
- **ANDROS Windows SSH nedostupný** — `172.17.0.1` je Docker bridge (localhost), nie Windows VM; deploy workflow na ANDROS Windows nefunkčný
- **Store API gaps for UI toggles:** `commandLineActive` and `infoPanelOpen` not in uiStore — currently local state

## Next Steps
- Fix CI electron staging deploy: resolve Windows runner permission issue (`Stop-Process` Access Denied)
- Dodať `resources/icon.ico` a otestovať `npm run dist` (Electron build → .exe)
- Vyriešiť SSH/RDP konektivitu na ANDROS Windows VM pre deploy workflow
- NEX Manager — connect module grid to live Module Registry API
- Implement audit_log writes for login/permission events
