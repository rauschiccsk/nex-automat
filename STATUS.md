# NEX Automat — Current Status
Last updated: 2026-03-11 (v29)

## Current State
- Backend (FastAPI) production on ANDROS Ubuntu (Docker), PostgreSQL 16.12 with **31 tables**, 2 enums, 6 functions, 11+ sequences, 6 triggers
- **nex-manager-api** microservice live: FastAPI on port 9110, Docker container on `nex-network`, `nex-config` package installed in image
- **Dynamic Module Registry** ✅ — `module_registry.yaml` (24 modules, 7 categories) as single source of truth; `GET /api/system/modules` endpoint (no auth); dynamic router registration in `main.py`; frontend `useModuleRegistry` hook + centralized `iconMap.ts`
- **ESHOP module** DONE ✅ — multi-tenant e-shop integration: **7 DB tables** (incl. `eshop_customers`), **25 endpoints** (4 public + 2 lead + 2 payment + 9 admin + 4 MuFis + **4 customer**), 3 auth layers (`X-Eshop-Token`, JWT, `API-KEY`), tenant resolution, order lifecycle, stock sync, **Comgate payment gateway**, **email notifications** (5 templates), **lead capture system** (discount codes, GDPR validation), **customer registration/login** (JWT tokens, order history)
- **emcenter.sk** ✅ — **prod/staging split**: production (port 9162) = "Coming Soon" placeholder, staging (port 9163, emcenter.isnex.eu) = full e-shop (real em-1.sk content, lead capture, checkout, **UX polished**: Alfa Slab One brand font, sticky fixed header with cart badge, nav-clean layout, no-cache headers, **timestamp cache-busting** on static assets, funnel-clean); **checkout upgrade** (company fields, account creation, VOP consent); **3 legal pages** (VOP, Privacy Policy, Withdrawal); **Nginx API proxy** fixed (3 location blocks: `/api/products`, `/api/orders`, `/api/contact` → container 9163); **CSS safety net** (`data-sku` guard on promo badges); **env vars unified** (`ESHOP_API_URL`/`ESHOP_API_TOKEN` chain in `main.py`); **Git branching**: `main` = Coming Soon, `develop` = full features; Nginx reverse proxy, SSL, CI 3/3 GREEN (main)
- **PAB module** DONE: endpoints, 77 backend tests, 20 frontend files, 9 tabs, versioning (modify_id + partner_catalog_history + triggers), partner_class (business/retail/guest), `partner_code` removed (redundant with `partner_id`)
- **USR module** DONE ✅ | **PAB module** DONE ✅ | **MIG module** full-stack ✅ | **ESHOP module** DONE ✅ | **GRP module** deferred | Remaining 19 modules — planned
- **PAB Migration** DONE ✅ — 164 partners re-migrated (+ extensions, addresses, contacts, bank_accounts, history), 0 errors, diacritics fixed, country_code mapping corrected, partner_code removed
- **T6 Worker deduplication** DONE ✅ — `packages/nex-invoice-worker/` (merged supplier + andros workers, -6679 lines)
- **R2 nex-config centralized config** ✅ | **R3 complete** ✅ (staging, shared, backend apps, workers, Windows apps — all wired)
- **RAG chunk size unified** ✅ — `RAG_CHUNK_SIZE = 1500` in nex-config, all consumers wired
- NEX Manager Electron app: **v0.2.0**, 6 stores + 9 components + USR + PAB + MIG + **ESHOP** modules
- **ESHOP Admin Panel** ✅ — NEX Manager frontend module: 3-tab view (Orders/Products/Tenants), order detail with status/payment badges + history, product CRUD with auto-VAT, tenant list; 15 new files, Zustand store, 8 API endpoints in `api.ts`
- **Frontend test infrastructure** ✅ — Vitest + React Testing Library + jsdom, **304 tests**, V8 coverage (80% thresholds); **PAB tabs coverage ~98% stmts / ~80% branches** (9 tabs, all ≥80%)
- **Playwright E2E tests** ✅ — 39 passed / 6 skipped / 0 failed, proper waits, **hard-delete teardown** (no soft-delete pollution), safety guards (partner_id ≥ 95000 only)
- **CI/CD: 10/10 jobs passing** ✅ — all green; E2E job #10 **conditional** (runs only with `[e2e]` commit tag)
- **Test suite: 212 backend + 304 frontend + 39 E2E = 555 total** + **48 emcenter-web tests + 17 emcenter E2E**, 1 pre-existing fail (DB connectivity)
- **Nginx ESHOP routing** ✅ — 6 location blocks (4 proxy + 2 block), 3 rate limiting zones (`eshop_payment`, `eshop_mufis`, `eshop_public`), 4 security headers, admin endpoints blocked at Nginx level
- **DNS (emcenter.sk)** ✅ — SPF + DKIM (RSA 2048) + DMARC (quarantine) all configured
- **Umami Analytics** ✅ — self-hosted web analytics on `analytics.isnex.eu`; Docker container port 9164; dedicated PostgreSQL DB (14 tables); Nginx reverse proxy + Cloudflare DNS; wildcard `*.isnex.eu` SSL cert; **HTTPS 200 OK** ✅; **emcenter-web staging integrated** — tracking script + 4 custom events (`add-to-cart`, `lead-registered`, `checkout-step`, `order-submitted`)
- **Monitoring** ✅ — Prometheus + Grafana running; nex-manager-api `/health` endpoint scraped; port 9110 scrape target pending
- **TESTING.md** ✅ — Knowledge Base document defining 3-layer testing architecture (Vitest+RTL → Playwright → MAT)

## Recent Changes
- **2026-03-11** — 📊 Umami Analytics integration (emcenter-web staging) — tracking script (conditional `{% if umami_website_id %}`), `trackEvent()` helper, 4 custom events (`add-to-cart`, `lead-registered`, `checkout-step`, `order-submitted`); env vars `UMAMI_WEBSITE_ID` + `UMAMI_SCRIPT_URL`; 31 pytest + 10 E2E all passing; commit `80006a2` on develop
- **2026-03-11** — 🌐 Umami domain migration — `analytics.icc.sk` → `analytics.isnex.eu`; new Nginx config with wildcard `*.isnex.eu` SSL cert (Cloudflare origin); HTTP + HTTPS server blocks; all 3 tests passing (localhost:9164, HTTPS local, HTTPS via Cloudflare = **200 OK**); KB UMAMI.md updated
- **2026-03-11** — 🐛 F4.11: Definitívny env vars fix (staging) — root cause: `main.py` čítal `NEX_API_BASE`/`ESHOP_TOKEN` ale kontajner mal `ESHOP_API_URL`/`ESHOP_API_TOKEN` → API proxy vždy 502 → JS fallback; fix: env var chain (`ESHOP_API_URL` → `NEX_API_BASE` → default), debug log removed, cache-bust `v=1773225371`; API proxy teraz vracia reálne produkty; commit `78aaeab` on develop
- **2026-03-11** — 🐛 F4.10: Definitívny AKCIA badge fix (staging) — triple root cause: (1) Nginx `/api/` catch-all → 403, (2) stale browser cache, (3) sites-enabled copy not symlink; fix: 3 Nginx location blocks for API proxy, CSS safety net (`data-sku` guard), null-safe JS, timestamp cache-busting; commit on develop
- **2026-03-11** — 🐛 F4.9: Cache-busting fix (staging) — `?v=51d24a9` on static assets, Docker `--no-cache` rebuild, Cloudflare BYPASS confirmed; commit `9ead0b1` on develop
- **2026-03-10** — 🔧 F4.8: emcenter.sk staging 3 UX fixes — nav menu removed, sticky header fixed (`position: fixed`), Alfa Slab One brand font enforced; commit `3aee287` on develop
- **2026-03-10** — 🎨 F4.7: emcenter.sk staging UX polish — Nginx no-cache headers, Alfa Slab One brand font (10 elements), sticky header with cart badge (live count), external links removed (funnel-clean), lead capture e-Book text, discount field removed from checkout; commit `ecb3ec0` on develop
- **2026-03-10** — 📋 F4.4b: Kompletná analýza obsahu em-1.sk pre emcenter.sk — analytický report pôvodného webového obsahu (čisto research, žiadne zmeny v kóde)
- **2026-03-10** — ❌ F4.4a: Analýza pôvodného webového obsahu pre emcenter.sk — FAILED (invalid API key on windows-cc agent)
- **2026-03-09** — 🔒 F4.5: Nginx ESHOP API routing — 6 location blocks (4 proxy, 2 block), 3 rate limiting zones, 4 security headers, admin endpoints blocked at Nginx; DNS verified (SPF+DKIM+DMARC); Prometheus+Grafana confirmed running
- **2026-03-09** — 🖥️ F3.1: ESHOP Admin Panel (NEX Manager) — 3-tab view (Orders/Products/Tenants), order detail (status+payment badges, history, tracking), product CRUD with auto-VAT, tenant list; Zustand eshopStore, 8 admin API endpoints; 15 new + 3 modified files, **27 new tests** (304 frontend total); CI ALL GREEN
- **2026-03-09** — 🛒 F2.2: emcenter.sk API integration — proxy layer (5 endpoints → nex-manager-api), dynamic products from ESHOP API, full checkout flow (billing/shipping/company/payment), order success/failed pages, httpx async, `ESHOP_TOKEN` auth; 9 files (3 new); CI 3/3 GREEN

## Known Issues
- 🟡 **Qdrant reindex partial failure** — Ollama embedding endpoint returns HTTP 500 from nex-brain (only 1/5 docs reindexed)
- 🟡 **No Alembic migrations** — schema managed via raw SQL; migration tooling not yet adopted
- 🟡 **1 pre-existing test failure** — DB connectivity test (not related to module registry)
- 🟡 **6 E2E tests skipped** — non-blocking, to be investigated
- 🟡 **Prometheus scrape target for port 9110** — nex-manager-api not yet added to Prometheus config
- 🟡 **Nginx external verification pending** — curl tests done via `--resolve` (NAT hairpin issue); needs verification from external host

## Next Steps
- **Prometheus scrape target** — Add nex-manager-api (port 9110) to Prometheus config
- **emcenter.sk external verification** — Verify Nginx routing from external host (NAT hairpin workaround)
- **emcenter.sk F2.3** — Production Comgate credentials, end-to-end payment testing, go-live readiness
- **ESHOP Comgate credentials** — Add `comgate_merchant_id`, `comgate_secret` to `eshop_tenants` table and configure per-tenant
- **GRP module** — Group management (deferred, next priority)
- **Remaining 19 modules** — STK, GSC, FAK, etc. (planned, registry-ready via YAML)
- **M4 expand to other categories** — GSC, STK extractors following PAB pattern
- Fix Qdrant/Ollama reindex pipeline (HTTP 500 from nex-brain)
- Implement audit_log writes for login/permission events
