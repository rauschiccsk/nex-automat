# NEX Automat - Migrácia z n8n na Temporal

**Kategória:** Strategic Technology Decision  
**Status:** 📋 Planned  
**Priority:** Medium  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Kontext projektu

**NEX Automat** je automatizačná platforma pre zákazníkov ERP systému NEX Genesis (Pascal, Btrieve/PostgreSQL). Cieľom je úspora 1-3 zamestnancov na zákazníka automatizáciou spracovania dokladov.

**Aktuálny zákazník:** Mágerstav s.r.o.

---

## Súčasná architektúra (na zrušenie)

```
ICC Server (Komárno)          Internet              Zákazník
┌─────────────────┐         ┌───────────┐         �┌──────────────┐
│  n8n workflow   │────────►│Cloudflare │────────►│   FastAPI    │
│                 │         │  Tunnel   │         │  PostgreSQL  │
└─────────────────┘         └───────────┘         │  NEX Genesis │
                                                  └──────────────┘
```

### Súčasné komponenty

**ICC Server (Komárno):**
- n8n workflow orchestration
- Email monitoring (IMAP)
- PDF extraction
- HTTP requests cez internet

**Internet layer:**
- Cloudflare tunnel
- SSL/TLS encryption
- DNS routing

**Zákazník (Mágerstav):**
- FastAPI backend
- PostgreSQL staging database
- NEX Genesis ERP integration

### Problémy súčasného riešenia

1. **Závislosť na ICC serveri a internete**
   - Single point of failure
   - Ak padne internet, prestane fungovať automatizácia

2. **Cloudflare tunnel = ďalší bod zlyhania**
   - Externá závislosť
   - Možné výpadky služby

3. **Dáta (faktúry) cestujú cez internet**
   - Bezpečnostné riziko
   - GDPR concerns
   - Citlivé firemné údaje mimo firmy

4. **Zložitá údržba dvoch prostredí**
   - ICC server + zákaznícke prostredie
   - Dvojnásobná konfigurácia
   - Komplikovaný debugging

---

## Nová architektúra (cieľ)

```
Zákazník - jeden Docker compose
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │         NEX Automat (Docker)        │   │
│  │                                     │   │
│  │  Temporal Server + Python Workers   │   │
│  │  FastAPI Backend                    │   │
│  │  PostgreSQL (staging)               │   │
│  │              │                      │   │
│  │              ▼                      │   │
│  │        NEX Genesis (ERP)            │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Nové komponenty

**Temporal Server:**
- Workflow orchestration engine
- Durable execution
- Built-in retry logic
- Monitoring & observability

**Python Workers:**
- Email monitoring activities
- PDF extraction activities
- Invoice processing activities
- Notification activities

**FastAPI Backend:**
- REST API endpoints
- Business logic
- NEX Genesis integration

**PostgreSQL:**
- Temporal persistence
- Staging database
- Configuration storage

### Výhody novej architektúry

1. **Všetko beží lokálne u zákazníka**
   - Self-contained system
   - Žiadne externé závislosti

2. **Žiadna závislosť na ICC serveri**
   - Eliminácia single point of failure
   - Nezávislosť od ICC infrastruktúry

3. **Žiadny Cloudflare tunnel**
   - Menej bodov zlyhania
   - Jednoduchšia architektúra

4. **Funguje aj offline**
   - Plná funkcionalita bez internetu
   - Lokálne spracovanie emailov

5. **GDPR compliant**
   - Dáta neopustia firmu
   - Plná kontrola nad citlivými údajmi
   - Audit trail v lokálnej databáze

6. **Jednoduchý deployment**
   - `docker-compose up -d`
   - Jedna konfigurácia
   - Jednoduché updates

---

## Migračný plán

### 1. Prepísať n8n workflow do Temporal (Python)

Existujúci n8n workflow `n8n-SupplierInvoiceEmailLoader` robí:

1. **IMAP trigger** - sleduje emaily
2. **Split PDF** - extrahuje PDF prílohy (JavaScript)
3. **Switch** - kontrola či existuje PDF
4. **HTTP Request** - posiela na FastAPI `/invoice` endpoint
5. **Gmail** - notifikácia pri chybe

#### Nové Temporal workflow s activities

```python
# Workflow definition
@workflow.defn
class InvoiceProcessingWorkflow:
    @workflow.run
    async def run(self, email_config: EmailConfig) -> WorkflowResult:
        # Activity 1: Fetch emails
        emails = await workflow.execute_activity(
            fetch_emails_from_imap,
            email_config,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # Activity 2: Extract PDFs
        for email in emails:
            pdf = await workflow.execute_activity(
                extract_pdf_from_email,
                email,
                start_to_close_timeout=timedelta(minutes=2)
            )
            
            if pdf:
                # Activity 3: Process invoice
                result = await workflow.execute_activity(
                    send_to_fastapi,
                    pdf,
                    start_to_close_timeout=timedelta(minutes=10)
                )
                
                if not result.success:
                    # Activity 4: Send notification
                    await workflow.execute_activity(
                        send_error_notification,
                        result,
                        start_to_close_timeout=timedelta(minutes=1)
                    )
```

#### Activities mapping

| n8n Node | Temporal Activity | Popis |
|----------|-------------------|-------|
| Email Trigger (IMAP) | `fetch_emails_from_imap()` | Načítanie emailov z IMAP servera |
| Split PDF (Code) | `extract_pdf_from_email()` | Extrakcia PDF príloh z emailu |
| HTTP -> FastAPI | `send_to_fastapi()` | Spracovanie faktúry (lokálne volanie) |
| Send Error Notification | `send_error_notification()` | Email notifikácia pri chybe |
| Has PDF Attachment? | Python condition | Native workflow logic |

### 2. Docker compose pre zákazníka

```yaml
version: '3.8'

services:
  temporal:
    image: temporalio/auto-setup:latest
    ports:
      - "7233:7233"
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal
      - POSTGRES_SEEDS=postgres
    depends_on:
      - postgres

  temporal-ui:
    image: temporalio/ui:latest
    ports:
      - "8080:8080"
    environment:
      - TEMPORAL_ADDRESS=temporal:7233

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=temporal
      - POSTGRES_PASSWORD=temporal
      - POSTGRES_DB=temporal
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nex-automat:
    build: .
    environment:
      - TEMPORAL_HOST=temporal:7233
      - DB_HOST=postgres
      - NEX_GENESIS_PATH=/nex/data
    volumes:
      - /path/to/nex:/nex/data
    depends_on:
      - temporal
      - postgres

volumes:
  postgres_data:
```

### 3. Odstrániť

Po úspešnej migrácii:

- ✅ n8n workflow na ICC serveri
- ✅ Cloudflare tunel konfigurácia
- ✅ Verejné DNS záznamy pre API
- ✅ SSL certifikáty pre externý prístup
- ✅ n8n prístupové údaje a konfigurácia

---

## Technický stack

### Core Technologies

| Komponenta | Technológia | Verzia | Účel |
|------------|-------------|--------|------|
| Workflow Engine | Temporal | Latest | Orchestrácia |
| Backend | FastAPI | 0.104+ | REST API |
| Workers | Python | 3.11+ | Activity execution |
| Database | PostgreSQL | 15+ | Persistence |
| GUI (future) | PySide6 | Latest | Desktop forms |
| Deployment | Docker | Latest | Containerization |

### Python Dependencies

```python
# Temporal SDK
temporalio>=1.4.0

# FastAPI stack
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0

# Email processing
imapclient>=2.3.0
email-validator>=2.0.0

# PDF processing
PyPDF2>=3.0.0
pdfplumber>=0.10.0

# NEX Genesis
pyodbc>=5.0.0  # Btrieve ODBC

# Utilities
python-dotenv>=1.0.0
httpx>=0.25.0
```

---

## Existujúci n8n workflow (referencia)

### n8n-SupplierInvoiceEmailLoader

```json
{
  "name": "n8n-SupplierInvoiceEmailLoader",
  "nodes": [
    {
      "name": "Email Trigger (IMAP)",
      "type": "n8n-nodes-base.emailReadImap",
      "parameters": {
        "mailbox": "INBOX",
        "options": {
          "allowUnauthorizedCerts": true
        }
      }
    },
    {
      "name": "Split PDF",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "mode": "runOnceForAllItems",
        "jsCode": "// Extrahuje PDF prílohy\n// Vracia: file_b64, filename, from_email, message_id, gmail_id, subject, received_date"
      }
    },
    {
      "name": "Has PDF Attachment?",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.file_b64}}",
              "operation": "isNotEmpty"
            }
          ]
        }
      }
    },
    {
      "name": "HTTP -> FastAPI /invoice",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://magerstav-invoices.icc.sk/invoice",
        "method": "POST",
        "headers": {
          "X-API-Key": "={{$credentials.apiKey}}",
          "Content-Type": "application/json"
        },
        "bodyParametersJson": "={{JSON.stringify($json)}}"
      }
    },
    {
      "name": "Send Error Notification",
      "type": "n8n-nodes-base.gmail",
      "parameters": {
        "sendTo": "rausch@em-1.sk",
        "subject": "NEX Automat Error",
        "message": "={{$json.error}}"
      }
    }
  ]
}
```

### FastAPI payload štruktúra

```python
class InvoicePayload(BaseModel):
    file_b64: str          # Base64 encoded PDF
    filename: str          # Názov súboru
    from_email: str        # Odosielateľ
    message_id: str        # Email Message-ID
    gmail_id: str          # Gmail UID
    subject: str           # Predmet emailu
    received_date: str     # Dátum prijatia
```

---

## Štruktúra projektu (návrh)

```
nex_automat/
├── workflows/
│   └── invoice_workflow.py        # Main workflow definition
├── activities/
│   ├── email_activities.py        # IMAP, email processing
│   ├── invoice_activities.py      # Invoice processing
│   └── notification_activities.py # Error notifications
├── api/
│   └── main.py                    # FastAPI application
├── workers/
│   └── main_worker.py             # Temporal worker
├── models/
│   ├── invoice.py                 # Invoice data models
│   └── email.py                   # Email data models
├── config/
│   └── settings.py                # Configuration
├── tests/
│   ├── test_workflows.py
│   └── test_activities.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Implementation Roadmap

### Phase 1: Setup (1-2 týždne)

- [ ] Setup Temporal development environment
- [ ] Create Docker compose configuration
- [ ] Setup PostgreSQL schemas
- [ ] Basic FastAPI structure

### Phase 2: Core Activities (2-3 týždne)

- [ ] Implement `fetch_emails_from_imap()`
- [ ] Implement `extract_pdf_from_email()`
- [ ] Implement `send_to_fastapi()` (local call)
- [ ] Implement `send_error_notification()`

### Phase 3: Workflow (1 týždeň)

- [ ] Create main workflow definition
- [ ] Add error handling
- [ ] Add retry logic
- [ ] Testing & debugging

### Phase 4: Testing (1-2 týždne)

- [ ] Unit tests for activities
- [ ] Integration tests
- [ ] End-to-end testing
- [ ] Performance testing

### Phase 5: Deployment (1 týždeň)

- [ ] Production Docker compose
- [ ] Mágerstav deployment
- [ ] Monitoring setup
- [ ] Documentation

### Phase 6: Migration (1 týždeň)

- [ ] Parallel run (n8n + Temporal)
- [ ] Validation of results
- [ ] Switch to Temporal only
- [ ] Decommission n8n

**Celková doba:** 7-10 týždňov

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Learning curve (Temporal) | Medium | Medium | Temporal má výbornú dokumentáciu, community support |
| Docker na Windows Server | Low | High | Docker Desktop for Windows Server je stable |
| NEX Genesis integration | Low | High | Už funguje s FastAPI, len local call |
| Data migration | Low | Medium | Žiadna migrácia dát, len workflow logic |

---

## Success Criteria

### Technical
- ✅ 100% functional parity s n8n workflow
- ✅ <5s latency pre email processing
- ✅ 99.9% uptime
- ✅ Automatic retry na failures

### Business
- ✅ Zero downtime migration
- ✅ Žiadna strata faktúr počas migrácie
- ✅ Elimination of ICC server dependency
- ✅ GDPR compliant architecture

### Operational
- ✅ Single command deployment (`docker-compose up`)
- ✅ Centralized monitoring (Temporal UI)
- ✅ Easy troubleshooting
- ✅ Documented rollback procedure

---

## Related Documents

- [Project Roadmap](PROJECT_ROADMAP.md)
- [Technology Decisions](TECHNOLOGY_DECISIONS.md)
- [System Architecture](../system/ARCHITECTURE.md)
- [Deployment Guide](../deployment/DEPLOYMENT_GUIDE.md)

---

**Status:** 📋 Planned  
**Next Step:** Setup Temporal development environment  
**Owner:** Zoltán  
**Last Updated:** 2025-12-15