# NEX Automat — Current Status
Last updated: 2026-02-24

## Current State
- **Backend (FastAPI):** Production on ANDROS Ubuntu (Docker), PostgreSQL with 5 tables
- **Temporal workflows:** Production — invoice processing
- **NEX Manager:** Electron app in `apps/frontend/nex-manager/` — Electron 35 + React 19 + TS 5.9 + Zustand 5 + Tailwind v4; **5 stores** + **9 components** wired into **App.tsx layout shell**; auth gate, dark mode sync, grid layout; auto-versioning active, TS 0 errors, build passing (renderer 714 kB + CSS 32 kB); **electron-builder configured** (`dist` script ready, NSIS installer); latest version **0.1.21** (commit `9a8e113`)
- **Tag v0.1.0:** Pushed to GitHub ✅
- **GitHub Actions runners:** 2 self-hosted runners on ANDROS Ubuntu — `nex-command` + `rockart-web`, both healthy via systemd
- **CI/CD:** 6 jobs operational — ci.yml: lint, test, security, build, **deploy-staging** (auto on develop); deploy.yml: manual dispatch to **4 targets** (icc, andros, mager, all)
- **CD Pipeline:** Staging auto-deploy (DEPTEST) on `develop` push; Production manual dispatch on `main` to ICC/ANDROS/MAGER
- **DEPTEST staging stack:** PostgreSQL + Temporal + Temporal UI (3 containers) — all healthy; CI uses `--env-file deployment/docker/.env.deptest`
- **RAG:** Qdrant + Ollama, 222 points, nomic-embed-text
- **SYSTEM DB (users, groups, permissions):** Not yet created
- **⚠️ No web frontend exists** — NEX Manager is the sole frontend app
- **Latest commit on `develop`:** `9a8e113`

## Recent Changes
- 2026-02-24: ✅ **NEX Manager shell verification** — diagnostika potvrdila: 9 komponentov + 5 stores existujú a sú commitnuté; App.tsx kompletný (auth gate, full shell layout, dark mode sync, Toast); `tsc --noEmit` 0 chýb; build OK (v0.1.21, renderer 714 kB + CSS 32 kB); commit `9a8e113` na `develop` — **žiadne zmeny potrebné** (⚠️ `gh` CLI nemá token — CI treba overiť manuálne)
- 2026-02-24: **DEPTEST env-file fix in CI** — `.env.deptest` rewritten with correct password (`chmod 600`); all 6 `docker compose` commands in `ci.yml` now pass `--env-file deployment/docker/.env.deptest`; DEPTEST stack restarted — all 3 containers healthy (commit `ced79c8`)
- 2026-02-24: **DEPTEST healthcheck bash fix** — replaced Python JSON parser with bash, sleep 10→15s, added diagnostic output on failure (commit `cb9a4fa`)
- 2026-02-24: **DEPTEST PostgreSQL fix** — created `.env.deptest` (gitignored), added `.env.deptest.example` template, gitignore for `deployment/docker/.env.*` — all 3 DEPTEST containers healthy (commit `ed9f7b8`)
- 2026-02-24: **Electron Builder setup** — `electron-builder.yml` created (appId: `sk.icc.nex-manager`, NSIS installer, x64); `dist` script added to package.json; `electron-builder@^26.8.1` in devDependencies; `npm run build` verified OK
- 2026-02-24: **CD pipeline setup** — ci.yml gains `deploy-staging` job (auto-deploy to DEPTEST on develop push); deploy.yml expanded from 2→4 targets (icc, andros, mager, all) with `main` branch guard
- 2026-02-24: **App.tsx layout shell created (128 lines)** — wires all 9 components + 4 stores into grid layout with auth gate, dark mode, dynamic breadcrumbs; committed 30 files / 5127 lines; TS 0 errors, build passing
- 2026-02-24: Created CommandLine.tsx (237), InfoPanel.tsx (160), LoginScreen.tsx (167) — 3 new components (564 lines total)
- 2026-02-24: Created Header.tsx, Sidebar.tsx, TabBar.tsx — 3 main layout components (418 lines total), plus `version.ts` and `lib/utils.ts`
- 2026-02-24: Added 3 Zustand stores — uiStore, authStore, moduleStore — now 5/5 stores complete

## Known Issues
- **`gh` CLI not authenticated on ANDROS Ubuntu** — `gh auth login` not run; CI results must be verified manually on GitHub
- **CI staging backend deploy fails** — Run #57 `deploy-staging-backend` exit code 1; needs log inspection (git creds / `.env` / permissions)
- **DEPTEST env-file fix pushed — awaiting CI result** — commit `ced79c8` needs CI verification
- **`resources/icon.ico` CHÝBA** — electron-builder zlyhá bez ikony; adresár `resources/` existuje ale je prázdny
- **ANDROS Windows SSH nedostupný** — `172.17.0.1` je Docker bridge (localhost), nie Windows VM; deploy workflow na ANDROS Windows nefunkčný
- **`actionlint` not installed** — recommended: `go install github.com/rhysd/actionlint/cmd/actionlint@latest` for YAML validation
- **Store API gaps for UI toggles:** `commandLineActive` and `infoPanelOpen` not in uiStore — currently local state
- **ICCDEV still lacks SSH key / HTTPS credentials** — cannot push to GitHub
- **SYSTEM DB missing:** Users, groups, permissions tables not yet created

## Next Steps
- **Authenticate `gh` CLI** on ANDROS Ubuntu (`gh auth login`) to enable CI monitoring
- **Verify CI workflow result** for commit `9a8e113` on `develop` branch
- Investigate CI Run #57 staging backend deploy failure (logs, git creds, `.env`)
- Dodať `resources/icon.ico` a otestovať `npm run dist` (Electron build → .exe)
- Vyriešiť SSH/RDP konektivitu na ANDROS Windows VM pre deploy workflow
- SYSTEM DB — users, groups, permissions
