"""
Save complete Temporal Migration Document
Uloží kompletný migračný dokument do knowledge base
"""
from pathlib import Path

DOC_PATH = Path("docs/knowledge/strategic/N8N_TO_TEMPORAL_MIGRATION.md")

CONTENT = '''# Migrácia n8n → Temporal (Natívne Windows)

**Projekt:** NEX Automat  
**Status:** 📋 Planned  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-20  
**Autor:** Zoltán Rausch, Claude

---

## 1. EXECUTIVE SUMMARY

### Prečo migrujeme?

| Problém s n8n | Riešenie Temporal |
|---------------|-------------------|
| n8n beží na ICC serveri | Temporal beží u zákazníka |
| Závislosť na Cloudflare Tunnel | Všetko lokálne, žiadny tunel |
| Single point of failure | Samostatný systém pre každého zákazníka |
| Limitované error handling | Natívne retry, timeout, compensation |
| Ťažký debugging | Temporal UI, detailné logy |

### Kľúčové rozhodnutie

**BEZ DOCKERU** - natívna inštalácia na Windows Server (kvôli kompatibilite so staršími servermi ako Windows Server 2012)

---

## 2. AKTUÁLNY STAV (n8n)

### 2.1 Workflow: n8n-SupplierInvoiceEmailLoader

**ID:** `yBsDIpw6oMs96hi6`  
**Status:** ✅ ACTIVE (produkcia)

```
┌─────────────────────────────────────────────────────────────┐
│                      ICC SERVER                              │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │  Gmail IMAP     │───→│  n8n Workflow   │                 │
│  │  (trigger)      │    │  (processing)   │                 │
│  └─────────────────┘    └────────┬────────┘                 │
└──────────────────────────────────┼──────────────────────────┘
                                   │ HTTPS (Cloudflare Tunnel)
                                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   ZÁKAZNÍK SERVER (Mágerstav)               │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │  FastAPI        │───→│  PostgreSQL     │                 │
│  │  /invoice       │    │  (staging)      │                 │
│  └─────────────────┘    └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 IMAP Konfigurácia

| Parameter | Hodnota |
|-----------|---------|
| Email | `magerstavinvoice@gmail.com` |
| Host | `imap.gmail.com` |
| Port | `993` |
| SSL/TLS | ✅ Enabled |
| Auth | App Password (nie OAuth2) |

### 2.3 FastAPI Endpoint

| Parameter | Hodnota |
|-----------|---------|
| URL | `https://magerstav-invoices.icc.sk/invoice` |
| Method | `POST` |
| Auth | `X-API-Key` header |
| API Key | Environment variable `LS_API_KEY` |
| Timeout | `120s` |

### 2.4 Payload štruktúra

```python
class InvoicePayload(BaseModel):
    file_b64: str          # Base64 encoded PDF
    filename: str          # Názov súboru (napr. "faktura_123.pdf")
    from_email: str        # Odosielateľ emailu
    message_id: str        # Email Message-ID header
    gmail_id: str          # Gmail UID
    subject: str           # Predmet emailu
    received_date: str     # ISO datetime prijatia
```

### 2.5 Error Notification

| Parameter | Hodnota |
|-----------|---------|
| Recipient | `rausch@em-1.sk` |
| Subject | `Invoice Processing Error` |
| Method | Gmail OAuth2 (credential: `Gmail account`) |

### 2.6 Split PDF Logic

```javascript
// Kľúčová logika z n8n:
// 1. Spracuje VŠETKY emaily v batch
// 2. Hľadá prílohy s prefixom 'attachment_'
// 3. Filtruje len .pdf súbory
// 4. Podporuje viacero PDF v jednom emaile
// 5. Ak nenájde PDF → vráti error item
```

---

## 3. CIEĽOVÝ STAV (Temporal)

### 3.1 Nová architektúra

```
┌─────────────────────────────────────────────────────────────┐
│                   ZÁKAZNÍK SERVER (Mágerstav)               │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │  Gmail IMAP     │───→│  Temporal       │                 │
│  │  (polling)      │    │  Worker         │                 │
│  └─────────────────┘    └────────┬────────┘                 │
│                                  │                          │
│                                  ▼                          │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │  FastAPI        │←───│  Temporal       │                 │
│  │  /invoice       │    │  Activity       │                 │
│  │  (localhost)    │    │                 │                 │
│  └────────┬────────┘    └─────────────────┘                 │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │  PostgreSQL     │    │  Temporal       │                 │
│  │  (staging)      │    │  Server         │                 │
│  └─────────────────┘    └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘

✅ Žiadny Cloudflare Tunnel
✅ Žiadna závislosť na ICC serveri
✅ Všetko lokálne
```

### 3.2 Komponenty

| Komponent | Technológia | Účel |
|-----------|-------------|------|
| Temporal Server | Go binary (Windows) | Workflow orchestrácia |
| Temporal Worker | Python + temporalio | Vykonávanie activities |
| Temporal UI | Web (voliteľné) | Monitoring, debugging |
| FastAPI | Existujúci | Invoice processing |
| PostgreSQL | Existujúci | Staging + Temporal persistence |

---

## 4. ŠTRUKTÚRA PROJEKTU

```
apps/temporal-invoice-worker/
├── activities/
│   ├── __init__.py
│   ├── email_activities.py      # IMAP operations
│   ├── invoice_activities.py    # FastAPI calls
│   └── notification_activities.py # Error notifications
├── workflows/
│   ├── __init__.py
│   └── invoice_workflow.py      # Main workflow
├── workers/
│   ├── __init__.py
│   └── main_worker.py           # Temporal worker
├── scheduler/
│   ├── __init__.py
│   └── polling_scheduler.py     # Trigger workflows
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration
├── tests/
│   ├── __init__.py
│   ├── test_activities.py
│   └── test_workflows.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## 5. IMPLEMENTATION ROADMAP

### Phase 1: Setup (1 týždeň)

- [ ] Inštalácia Temporal Server na Windows (Go binary)
- [ ] Konfigurácia PostgreSQL pre Temporal persistence
- [ ] Vytvorenie `apps/temporal-invoice-worker/` štruktúry
- [ ] Python virtual environment + dependencies
- [ ] Základná konfigurácia (settings.py, .env)

### Phase 2: Core Activities (1-2 týždne)

- [ ] Implementácia `fetch_new_emails()` - IMAP polling
- [ ] Implementácia `extract_pdf_attachments()` - PDF extraction
- [ ] Implementácia `send_to_fastapi()` - HTTP POST
- [ ] Implementácia `send_error_notification()` - SMTP
- [ ] Implementácia `mark_email_processed()` - IMAP flag
- [ ] Unit testy pre každú activity

### Phase 3: Workflow (1 týždeň)

- [ ] Implementácia `InvoiceProcessingWorkflow`
- [ ] Retry policies a error handling
- [ ] Polling scheduler
- [ ] Integration testy

### Phase 4: Testing (1 týždeň)

- [ ] E2E test s reálnym emailom
- [ ] Test error scenarios
- [ ] Performance test (latency)
- [ ] Porovnanie s n8n výstupom

### Phase 5: Deployment (1 týždeň)

- [ ] Temporal Server ako Windows Service
- [ ] Worker ako Windows Service
- [ ] Scheduler ako Windows Service
- [ ] Monitoring setup (Temporal UI)
- [ ] Dokumentácia pre zákazníka

### Phase 6: Migration (1 týždeň)

- [ ] Parallel run (n8n + Temporal)
- [ ] Validácia výsledkov
- [ ] Prepnutie na Temporal
- [ ] Decommission n8n workflow

**Celková doba:** 6-8 týždňov

---

## 6. ENVIRONMENT VARIABLES

```bash
# .env.example

# IMAP (Gmail)
IMAP_USER=magerstavinvoice@gmail.com
IMAP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Gmail App Password

# FastAPI
FASTAPI_URL=http://localhost:8001/invoice
LS_API_KEY=your-api-key-here

# SMTP (Gmail)
SMTP_USER=magerstavinvoice@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Gmail App Password
NOTIFICATION_EMAIL=rausch@em-1.sk

# Temporal
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default

# Polling
POLLING_INTERVAL=60
```

---

## 7. PYTHON DEPENDENCIES

```text
# requirements.txt

# Temporal SDK
temporalio>=1.4.0

# HTTP client
httpx>=0.25.0

# Email
imapclient>=2.3.0

# Environment
python-dotenv>=1.0.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

---

## 8. WINDOWS SERVICES

### 8.1 Temporal Server Service

```powershell
# Inštalácia pomocou NSSM
nssm install TemporalServer "C:\\Temporal\\temporal-server.exe" start --config "C:\\Temporal\\config.yaml"
nssm set TemporalServer AppDirectory "C:\\Temporal"
nssm set TemporalServer Start SERVICE_AUTO_START
```

### 8.2 Temporal Worker Service

```powershell
nssm install TemporalInvoiceWorker "C:\\Python311\\python.exe" "-m" "workers.main_worker"
nssm set TemporalInvoiceWorker AppDirectory "C:\\Deployment\\nex-automat\\apps\\temporal-invoice-worker"
nssm set TemporalInvoiceWorker Start SERVICE_AUTO_START
```

### 8.3 Polling Scheduler Service

```powershell
nssm install TemporalInvoiceScheduler "C:\\Python311\\python.exe" "-m" "scheduler.polling_scheduler"
nssm set TemporalInvoiceScheduler AppDirectory "C:\\Deployment\\nex-automat\\apps\\temporal-invoice-worker"
nssm set TemporalInvoiceScheduler Start SERVICE_AUTO_START
```

---

## 9. SUCCESS CRITERIA

### Technical

| Kritérium | Cieľ |
|-----------|------|
| Functional parity | 100% s n8n |
| Latency | <5s od emailu po spracovanie |
| Uptime | 99.9% |
| Auto-retry | 3 pokusy s exponential backoff |

### Business

| Kritérium | Cieľ |
|-----------|------|
| Zero downtime migration | ✅ |
| Žiadna strata faktúr | ✅ |
| Eliminácia ICC závislosti | ✅ |
| GDPR compliance | ✅ (všetko lokálne) |

---

## 10. ROLLBACK PLAN

Ak migrácia zlyhá:

1. **Stop** Temporal services
2. **Enable** n8n workflow (set active: true)
3. **Verify** n8n processing emails
4. **Investigate** Temporal issues
5. **Retry** migration after fix

n8n workflow zostáva zachovaný až do úspešnej validácie Temporal riešenia.

---

**Status:** 📋 Planned  
**Next Step:** Phase 1 - Setup Temporal Server  
**Owner:** Zoltán  
**Last Updated:** 2025-12-20
'''


def main():
    print("=" * 70)
    print("SAVE: Temporal Migration Document")
    print("=" * 70)

    # Vytvor adresár ak neexistuje
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Ulož dokument
    DOC_PATH.write_text(CONTENT, encoding='utf-8')
    print(f"✅ Uložený: {DOC_PATH}")

    print()
    print("OBSAH:")
    print("  1. Executive Summary (prečo migrujeme)")
    print("  2. Aktuálny stav n8n (IMAP, FastAPI, Payload)")
    print("  3. Cieľový stav Temporal (architektúra)")
    print("  4. Štruktúra projektu")
    print("  5. Implementation Roadmap (6 fáz)")
    print("  6. Environment Variables")
    print("  7. Python Dependencies")
    print("  8. Windows Services (NSSM)")
    print("  9. Success Criteria")
    print(" 10. Rollback Plan")
    print()
    print("Ďalší krok: python tools/rag/rag_update.py --new")
    print("=" * 70)


if __name__ == "__main__":
    main()