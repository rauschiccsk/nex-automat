# NEX Automat - Master TODO

**Lokácia:** docs/knowledge/TODO_MASTER.md
**Aktualizované:** 2025-12-27
**Zdroj:** RAG analýza strategických dokumentov

---

## 🔴 HIGH PRIORITY

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| ANDROS server hardware upgrade | deployment | SuperMicro dual Xeon, 128GB RAM |
| ANDROS deployment planning | supplier-invoice-loader | Nový zákazník Q1 2026 |
| Fáza 5: Btrieve Models TSH/TSI/PLS/RPC | nexdata | Základné pre fázy 6-8 |
| Web UI schvaľovací workflow | supplier-invoice-staging-web | Dialógy schváliť/zamietnuť |
| Web UI Docker deployment | supplier-invoice-staging-web | Nginx + Docker Compose |

---

## 🟡 MEDIUM PRIORITY

### NEX Automat Core (Fázy 6-8)

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Fáza 6: GSCAT WRITE + BARCODE WRITE | nexdata | Vytvorenie produktových kariet |
| Fáza 6: GUI výber tovarovej skupiny | supplier-invoice-staging | PySide6 |
| Fáza 7: TSH/TSI WRITE | nexdata | Zaevidovanie dodávateľského DL |
| Fáza 8: RPC WRITE | nexdata | Požiadavky na zmenu cien |
| Fáza 9: E2E testing + Production hardening | testing | Q2 2026 |

### NEX Brain

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| NEX Brain Fáza 2: Knowledge Base import | nex-brain | Dokumenty pre zákazníkov |
| NEX Brain Fáza 3: NEX Genesis Integration | nex-brain | Live ERP queries |

### Monitoring & Operations

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Prometheus metrics collection | monitoring | /metrics endpoint |
| Grafana dashboard | monitoring | Vizualizácia |
| Centralized logging (ELK/Loki) | monitoring | Log aggregation |
| Backup retention policy | operations | 30/90/365 days |

---

## 🟢 LOW PRIORITY / BACKLOG

### AI/ML Technologies

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Supplier classifier ML | supplier-invoice-loader | Auto-identifikácia dodávateľov |
| PaddleOCR evaluation | ai-service | Lepší OCR pre zlé skeny |
| Camelot table extraction | ai-service | 🔥 Vysoká priorita podľa AI_ML_TECHNOLOGIES.md |
| Claude API validation | ai-service | 99%+ presnosť |
| DuckDB analytics | analytics | 10-100x rýchlejšie SQL |

### GUI / Web Improvements

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Web UI hlavička faktúry - chýbajúce polia | supplier-invoice-staging-web | IČO, dátumy |
| Invoice editing capabilities | supplier-invoice-staging | Editovanie v GUI |
| Batch operations | supplier-invoice-staging | Hromadné spracovanie |
| Advanced filtering | supplier-invoice-staging | Pokročilé filtre |
| Statistics dashboard | supplier-invoice-staging | Štatistiky |
| Product matching improvement | supplier-invoice-staging | Vyššia úspešnosť |

### Code Quality

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Remove TODO comments from code | all | GitHub security warning |
| Code review - hardcoded values | all | Extract to config |
| Secrets scanning | all | Remove any exposed credentials |

### Future (Q3-Q4 2026)

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Mobile Application | mobile | React Native/Flutter |
| ICC Internal Deployment | deployment | Interný zákazník |
| Scale to 10+ customers | deployment | Q4 2026 |

### Testing & Quality

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| GUI application tests | testing | supplier-invoice-staging |
| E2E tests (full workflow) | testing | End-to-end |
| Performance/Load testing | testing | Benchmark |
| Code coverage 90%+ | testing | mypy, pylint |
| Security scanning | testing | Dependency vulnerabilities |

### Documentation

| Úloha | Modul | Poznámka |
|-------|-------|----------|
| Video tutorials | docs | Pre používateľov |
| Quick start guide (1-page) | docs | Onboarding |
| Contributing guide | docs | Pre developerov |
| API integration examples | docs | Externé integrácie |

---

## ✅ DONE (posledné)

| Úloha | Modul | Dátum |
|-------|-------|-------|
| Mágerstav v3.2 deployment | supplier-invoice-loader | 2025-12-27 |
| Web UI frontend deploy na /app | supplier-invoice-staging-web | 2025-12-27 |
| Static files serving cez FastAPI | supplier-invoice-loader | 2025-12-27 |
| STATUS_CONFIG fix - 'staged' status | supplier-invoice-staging-web | 2025-12-27 |
| match_percent null fallback fix | supplier-invoice-staging-web | 2025-12-27 |
| Windows služba NEX-SupplierInvoiceLoader | deployment | 2025-12-27 |
| NSSM konfigurácia s POSTGRES_PASSWORD | deployment | 2025-12-27 |
| Vite base="/app/" konfigurácia | supplier-invoice-staging-web | 2025-12-27 |
| React Router basename="/app" | supplier-invoice-staging-web | 2025-12-27 |
| Web UI pripojenie na reálny backend | supplier-invoice-staging-web | 2025-12-26 |
| staging_routes.py FastAPI endpointy | supplier-invoice-loader | 2025-12-26 |
| pg8000 named parameters fix | nex-staging | 2025-12-26 |
| NEX Brain port presun 8001→8003 | nex-brain | 2025-12-26 |
| BaseGrid reusable system | supplier-invoice-staging-web | 2025-12-26 |
| Editovateľné bunky (marža, predajná cena) | supplier-invoice-staging-web | 2025-12-26 |
| Prepočty marža ↔ predajná cena | supplier-invoice-staging-web | 2025-12-26 |
| Export CSV funkcionalita | supplier-invoice-staging-web | 2025-12-26 |
| InvoiceHeadsGrid + InvoiceItemsGrid configs | supplier-invoice-staging-web | 2025-12-26 |
| supplier-invoice-staging-web Fáza 1-4 | web | 2025-12-26 |
| Web UI DataGrid s column filters | web | 2025-12-26 |
| Web UI keyboard navigation (NEX Genesis štýl) | web | 2025-12-26 |
| Web UI column configuration (⚙️) | web | 2025-12-26 |
| NEX Brain Telegram vylepšenia | nex-brain | 2025-12-24 |
| NEX Brain RAG multi-tenant | nex-brain | 2025-12-24 |
| n8n → Temporal migration | workflow | 2025-12-21 |
| Mágerstav v3.1 deployment | supplier-invoice-loader | 2025-12-24 |
| Daily Summary Reports modul | supplier-invoice-loader | 2025-12-24 |
| Windows Task Scheduler (18:00 Po-Pi) | supplier-invoice-loader | 2025-12-24 |
| Telegram tokeny revoke | nex-brain | 2025-12-24 |
| SMTP SSL konfigurácia | supplier-invoice-loader | 2025-12-24 |
| Security fix - tokeny z Git | nex-automat | 2025-12-24 |
| docs/knowledge/ removed from Git | nex-automat | 2025-12-24 |
| PostgreSQL migration pg8000 | supplier-invoice-loader | 2025-12-23 |
| PyQt5 → PySide6 migration | supplier-invoice-staging | 2025-12-20 |
| NEX Brain Fáza 1 Foundation | nex-brain | 2025-12-19 |
| RAG System MVP | rag-api | 2025-12-16 |

---

## 📋 Fázy z PROJECT_ROADMAP.md

| Fáza | Názov | Status |
|------|-------|--------|
| 1 | Email → Staging → GUI | ✅ COMPLETE |
| 2 | GO-LIVE Preview/Demo | ✅ COMPLETE |
| 3 | Dokumentácia a Refaktoring | ✅ COMPLETE |
| 4 | supplier-invoice-staging (PySide6) | ✅ COMPLETE |
| 4.5 | supplier-invoice-staging-web (React) | ✅ COMPLETE |
| 5 | Btrieve Models (TSH, TSI, PLS, RPC) | ⚪ TODO Q1 2026 |
| 6 | Vytvorenie produktových kariet | ⚪ TODO Q1 2026 |
| 7 | Zaevidovanie dodávateľského DL | ⚪ TODO Q1 2026 |
| 8 | Požiadavky na zmenu cien | ⚪ TODO Q2 2026 |
| 9 | Testing + Production Hardening | ⚪ TODO Q2 2026 |
| 10 | Ďalší zákazníci + Rozšírenia | ⚪ FUTURE Q3 2026+ |

---

## 📋 Konfigurácia portov (Dev PC)

| Služba | Port |
|--------|------|
| RAG API | 8765 |
| Temporal Server | 7233 |
| Temporal UI | 8233 |
| NEX Brain API | 8003 |
| supplier-invoice-loader | 8001 |
| supplier-invoice-staging-web | 5173 (dev) / 8001/app (prod) |
| PostgreSQL | 5432 |

---

## 📋 Pravidlá

1. Aktualizovať na konci každého chatu
2. Presúvať dokončené do DONE sekcie
3. Uložiť do `docs/knowledge/TODO_MASTER.md`
4. RAG update: `python tools/rag/rag_update.py --new`