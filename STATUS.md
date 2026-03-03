# NEX Automat — Current Status
Last updated: 2026-03-03

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL with **11 tables** (5 original + 6 system)
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container `nex-manager-api` on `nex-network`
- **RBAC middleware** operational: `require_permission(module_code, permission)` factory — whitelist-validated, group-aggregated permission checks with 403 responses
- **Module Registry API** live: 3 endpoints (`/api/modules`, `/api/modules/by-category`, `/api/modules/{code}`) — JWT-protected, pg8000-compatible
- **Module inventory verified**: **23 modules** (7 categories) — PAB="Katalóg partnerov", GSC="Katalóg produktov" (category=catalogs), VAH removed; all match INVENTORY.md across DB seed, live DB, backend, and frontend
- **Users CRUD API** live: 6 endpoints (`/api/users` CRUD + `/api/users/{id}/password` + `/api/auth/change-password`) — RBAC-protected (USR module), audit-logged, 22 unit tests passing
- JWT auth fully operational: login, me, refresh, change-password endpoints — access_token (30min) + refresh_token
- DB driver: pg8000 (pure Python), raw SQL with cursor.execute()
- System DB tables live: `users`, `groups`, `user_groups`, `modules`, `group_module_permissions`, `audit_log`
- Seed data: 1 admin, 5 groups, **23 modules** (7 categories), admin→Administrátori with full permissions (23/23)
- Migration system created: `database/migrations/` (no Alembic — custom)
- Temporal workflows production — invoice processing
- NEX Manager Electron app: 5 stores + 9 components, App.tsx complete, TS 0 errors, build passing (**v0.2.0**, 714 kB + 32 kB CSS)
- **Dark mode fully operational**: Tailwind v4 `@custom-variant dark` enabled, 156 dark: utilities active, system theme detection with `prefers-color-scheme` listener
- **App versioning pipeline**: `scripts/version.js` generates `version.ts` from git tags → Sidebar displays dynamically; CI has `fetch-depth: 0` for full tag history
- **Frontend icon rendering**: `ICON_MAP` + `<IconComponent />` pattern across Sidebar, InfoPanel, CommandLine
- **Login→logout loop fixed**: race condition in App.tsx resolved — selective 401-only logout, concurrent loadModules guard, debug breadcrumbs
- All 9 components + 5 stores verified: git-tracked and locally present, no discrepancies
- Repository file paths cleaned — 0 backslash filenames remaining
- CI/CD: **8/8 jobs passing** ✅ — lint, security, unit tests, docker builds (brain + telegram), electron build, backend staging deploy, electron staging deploy
- CI electron build: electron-vite build + portable unpacked (`--dir`), runs on `ANDROS-WIN` with `shell: pwsh`
- **CI deploy strategy**: Staging deploys trigger on `develop` push only; production deploy on `main` via manual `workflow_dispatch` (`deploy.yml`)
- Both self-hosted runners ONLINE: `nex-automat` (Linux/ANDROS), `nex-automat-win` (Windows/ANDROS-WIN)
- DEPTEST staging stack: PostgreSQL + Temporal + Temporal UI (3 containers) — all healthy
- gh CLI authenticated on ANDROS Ubuntu — `rauschiccsk`, HTTPS, v2.87.2, CI monitoring operational
- RAG: Qdrant + Ollama, 222 points

## Recent Changes
- **2026-03-03** — ✅ Dark mode fix: Tailwind v4 `@custom-variant dark` in `index.css` (root cause), `App.tsx` system theme detection with `prefers-color-scheme` listener, `Toast.tsx` dark variants — CI 8/8 green
- **2026-03-03** — ✅ Session persistence: window bounds (electron-store), tab persistence (Zustand persist), UI/sidebar persistence, logout cleanup, tab validation
- **2026-03-03** — ✅ Login Enter-key UX: `useRef` + `onKeyDown` on username input → Enter focuses password field
- **2026-03-03** — ✅ Login autoFocus on username input
- **2026-03-03** — ✅ App versioning pipeline: `fetch-depth: 0` in CI build-electron for git tag access, version bump to **v0.2.0**, `package.json` updated, git tag pushed — CI 8/8 green
- **2026-03-03** — ✅ Fix reserved `$pid` variable in Electron deploy job: renamed `$pid` → `$procPid` at 3 locations in ci.yml — CI 8/8 green
- **2026-03-03** — ✅ CI Job 8 fix: cross-session process kill for Electron deploy — `taskkill /F /PID` via CIM + robocopy /MIR fallback + pwsh scope qualifier fix
- **2026-03-03** — ✅ CI 8/8 passing: fixed electron staging deploy
- **2026-03-03** — ✅ USR module backend: `apps/nex-manager-api/users/` — 5 CRUD endpoints + admin password reset + self change-password; Pydantic schemas, RBAC, audit log, 22 unit tests
- **2026-03-03** — ✅ Module cleanup: PAB renamed "Katalóg partnerov", GSC renamed "Katalóg produktov", category→catalogs, VAH removed → **23 modules**; INVENTORY.md updated

## Known Issues
- **`resources/icon.ico` CHÝBA** — electron-builder zlyhá bez ikony; adresár `resources/` existuje ale je prázdny
- **ANDROS Windows SSH nedostupný** — `172.17.0.1` je Docker bridge (localhost), nie Windows VM; deploy workflow na ANDROS Windows nefunkčný
- **Store API gaps for UI toggles:** `commandLineActive` and `infoPanelOpen` not in uiStore — currently local state

## Next Steps
- Dodať `resources/icon.ico` a otestovať `npm run dist` (Electron build → .exe)
- Vyriešiť SSH/RDP konektivitu na ANDROS Windows VM pre deploy workflow
- NEX Manager — connect module grid to live Module Registry API
- Implement audit_log writes for login/permission events (users CRUD already audit-logged)
- NEX Manager frontend — USR module UI (user list, create/edit forms, password management)
