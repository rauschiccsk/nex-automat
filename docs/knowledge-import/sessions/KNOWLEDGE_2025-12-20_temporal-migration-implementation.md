# Temporal Migration Implementation - Phase 1-4

**Dátum:** 2025-12-20  
**Trvanie:** ~4 hodiny  
**Cieľ:** Migrácia z n8n na Temporal pre spracovanie supplier invoices  
**Status:** ✅ COMPLETE - Phase 1-4 Done

---

## Summary

Úspešne implementovaný **Temporal Invoice Worker** ktorý nahrádza n8n workflow pre spracovanie dodávateľských faktúr. Worker používa OAuth2 autentifikáciu pre Gmail IMAP a posiela PDF faktúry do FastAPI Invoice Loader.

---

## Completed Work

### Phase 1: Setup ✅

**Adresárová štruktúra:**
```
apps/supplier-invoice-worker/
├── activities/
│   ├── __init__.py
│   ├── email_activities.py      # IMAP operácie s OAuth2
│   └── invoice_activities.py    # PDF upload do FastAPI
├── workflows/
│   ├── __init__.py
│   └── invoice_workflow.py      # Hlavný Temporal workflow
├── scheduler/
│   ├── __init__.py
│   └── polling_scheduler.py     # Spúšťa workflows
├── workers/
│   ├── __init__.py
│   └── main_worker.py           # Temporal worker
├── config/
│   ├── __init__.py
│   ├── settings.py              # Pydantic settings
│   ├── gmail_oauth.py           # OAuth2 helper
│   └── oauth_authorize.py       # Autorizačný skript
├── tests/
├── .env
├── .env.example
├── .gmail_tokens.json           # OAuth2 tokeny (gitignore)
├── .gitignore
└── requirements.txt
```

**Dependencies (requirements.txt):**
```
temporalio>=1.4.0
httpx>=0.25.0
imapclient>=2.3.0
python-dotenv>=1.0.0
pydantic-settings>=2.0.0
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.1.1
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

### Phase 2: Core Activities ✅

**email_activities.py:**
- `fetch_unread_emails()` - Fetch unread emails s OAuth2 autentifikáciou
- `mark_email_processed(uid)` - Označí email ako prečítaný
- Používa `imaplib` s XOAUTH2 autentifikáciou

**invoice_activities.py:**
- `upload_invoice_to_api(filename, content)` - Upload PDF do FastAPI
- `validate_pdf(content)` - Validácia PDF hlavičky

### Phase 3: Workflow ✅

**invoice_workflow.py - InvoiceProcessingWorkflow:**
```
Flow:
1. Fetch unread emails from IMAP (OAuth2)
2. Extract PDF attachments
3. Validate PDFs
4. Upload to FastAPI (/api/v1/invoice/upload)
5. Mark emails as processed
```

**Retry Policy:**
- initial_interval: 5 seconds
- backoff_coefficient: 2.0
- maximum_attempts: 3
- maximum_interval: 1 minute

### Phase 4: Testing ✅

**Úspešné testy:**
- Worker pripojenie k Temporal Server
- OAuth2 Gmail autentifikácia
- IMAP fetch unread emails
- FastAPI Invoice Loader integrácia
- End-to-end workflow execution

---

## OAuth2 Setup pre Gmail

### Google Cloud Console Setup

1. **Vytvor projekt:** `supplier-invoice-worker`
2. **OAuth consent screen:**
   - User Type: External
   - App name: Supplier Invoice Worker
   - User support email: magerstavinvoice@gmail.com
3. **Credentials:**
   - Application type: Desktop app
   - Name: Supplier Invoice Worker
4. **Test users:** Pridaj `magerstavinvoice@gmail.com`
5. **Enable Gmail API** v Library

### OAuth2 Client Config

```python
CLIENT_CONFIG = {
    "installed": {
        "client_id": "1078289465706-tpuet1lqt5ljqvtns0k9477tnj1pm7dh.apps.googleusercontent.com",
        "client_secret": "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",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"]
    }
}
```

### Autorizácia

```bash
cd C:\Development\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\activate
python -m config.oauth_authorize
```

Tokeny sa uložia do `.gmail_tokens.json` (v .gitignore).

---

## Spustenie Služieb

### Požadované terminály (8 tabov)

| Tab | Služba | Príkaz |
|-----|--------|--------|
| Temporal-Server | Temporal + UI | `cd C:\Temporal && .\cli\temporal.exe server start-dev` |
| worker | Supplier Invoice Worker | `cd apps\supplier-invoice-worker && .\venv\Scripts\activate && python -m workers.main_worker` |
| supplier-invoice-loader | Invoice API (8000) | `cd apps\supplier-invoice-loader && ..\..\venv32\Scripts\activate && python -m uvicorn main:app --reload --port 8000` |
| RAG-API | RAG Server (8765) | `cd C:\Development\nex-automat && .\venv\Scripts\activate && python -m uvicorn tools.rag.server_app:app --host 127.0.0.1 --port 8765 --log-level info` |
| NEX-Brain-API | NEX Brain (8001) | `cd apps\nex-brain && ..\..\venv\Scripts\activate && python -m uvicorn api.main:app --reload --port 8001` |
| Telegram-Bot | Telegram Bot | `cd C:\Development\nex-automat && .\venv\Scripts\activate && python apps/nex-brain/telegram/bot.py` |
| RAG Cloudflare | Cloudflare Tunnel | `cloudflared tunnel --config C:\Users\ZelenePC\.cloudflared\config.yml run n8n-tunnel` |
| DEV | Pracovný terminál | Pre príkazy a testovanie |

### Testovanie Workflow

```bash
cd C:\Development\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\activate
python -m scheduler.polling_scheduler --once
```

### Continuous Polling (produkcia)

```bash
python -m scheduler.polling_scheduler
# Polluje každých 5 minút (POLL_INTERVAL_SECONDS=300)
```

---

## Environment Variables (.env)

```env
# Temporal Server
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=supplier-invoice-queue

# IMAP (Gmail) - OAuth2, heslo sa nepoužíva
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=magerstavinvoice@gmail.com
IMAP_PASSWORD=
IMAP_FOLDER=INBOX

# FastAPI Invoice Service
FASTAPI_URL=http://localhost:8000
LS_API_KEY=<from_system_env>

# Logging
LOG_LEVEL=INFO
```

---

## Dôležité Poznámky

### Btrieve a venv32

**supplier-invoice-loader** vyžaduje 32-bit Python pre Btrieve DLL:
```bash
..\..\venv32\Scripts\activate
```

**supplier-invoice-worker** používa štandardný venv (64-bit):
```bash
.\venv\Scripts\activate
```

### Temporal Server

Používame `temporal server start-dev` ktorý má **vstavaný UI na porte 8233**.
- Server: localhost:7233 (gRPC)
- UI: http://localhost:8233

### OAuth2 vs App Password

Zvolili sme OAuth2 namiesto App Password pre:
- Lepšiu bezpečnosť (tokeny expirujú, revokable)
- Google odporúčaný prístup
- Auto-refresh tokenov
- Production-ready riešenie

---

## Ďalšie Kroky (Phase 5-6)

### Phase 5: Deployment
- [ ] Windows Service cez NSSM pre worker
- [ ] Windows Service pre scheduler
- [ ] Monitoring a alerting

### Phase 6: Migration
- [ ] Parallel run (n8n + Temporal)
- [ ] Validácia výsledkov
- [ ] Vypnutie n8n workflow
- [ ] Cleanup

---

## Vytvorené Skripty

| Skript | Účel |
|--------|------|
| 01_create_temporal_structure.py | Adresárová štruktúra |
| 02_create_requirements_env.py | requirements.txt, .env.example |
| 03_create_settings.py | config/settings.py |
| 04_create_email_activities.py | activities/email_activities.py |
| 05_create_invoice_activities.py | activities/invoice_activities.py |
| 06_create_invoice_workflow.py | workflows/invoice_workflow.py |
| 07_create_main_worker.py | workers/main_worker.py |
| 08_fix_escape_sequence.py | Fix \\Seen escape |
| 09_create_scheduler.py | scheduler/polling_scheduler.py |
| 10_create_env_file.py | .env súbor |
| 11_add_oauth_dependencies.py | google-auth dependencies |
| 12_create_oauth_helper.py | gmail_oauth.py, oauth_authorize.py |
| 13_update_oauth_credentials.py | Nové OAuth2 credentials |
| 14_update_email_activities_oauth.py | OAuth2 IMAP autentifikácia |

---

## Architektúra

```
                    ┌─────────────────┐
                    │  Gmail IMAP     │
                    │  (OAuth2)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Temporal       │
                    │  Worker         │
                    │  (Python)       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼───────┐ ┌────▼────┐ ┌──────▼──────┐
    │ fetch_unread    │ │validate │ │ upload_to   │
    │ _emails()       │ │_pdf()   │ │ _api()      │
    └─────────────────┘ └─────────┘ └──────┬──────┘
                                           │
                                  ┌────────▼────────┐
                                  │  FastAPI        │
                                  │  Invoice Loader │
                                  │  (port 8000)    │
                                  └────────┬────────┘
                                           │
                                  ┌────────▼────────┐
                                  │  PostgreSQL     │
                                  │  invoice_staging│
                                  └─────────────────┘
```