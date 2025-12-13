# NEX Automat - Migrácia z n8n na Temporal

## Kontext projektu

**NEX Automat** je automatizačná platforma pre zákazníkov ERP systému NEX Genesis (Pascal, Btrieve/PostgreSQL). Cieľom je úspora 1-3 zamestnancov na zákazníka automatizáciou spracovania dokladov.

**Aktuálny zákazník:** Mágerstav s.r.o.

## Súčasná architektúra (na zrušenie)

```
ICC Server (Komárno)          Internet              Zákazník
┌─────────────────┐         ┌───────────┐         ┌──────────────┐
│  n8n workflow   │────────►│Cloudflare │────────►│   FastAPI    │
│                 │         │  Tunnel   │         │  PostgreSQL  │
└─────────────────┘         └───────────┘         │  NEX Genesis │
                                                  └──────────────┘
```

**Problémy:**
- Závislosť na ICC serveri a internete
- Cloudflare tunel = ďalší bod zlyhania
- Dáta (faktúry) cestujú cez internet
- Zložitá údržba dvoch prostredí

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

**Výhody:**
- Všetko beží lokálne u zákazníka
- Žiadna závislosť na ICC serveri
- Žiadny Cloudflare tunel
- Funguje aj offline
- GDPR compliant (dáta neopustia firmu)
- Jednoduchý deployment: `docker-compose up -d`

## Čo treba spraviť

### 1. Prepísať n8n workflow do Temporal (Python)

Existujúci n8n workflow `n8n-SupplierInvoiceEmailLoader` robí:
1. IMAP trigger - sleduje emaily
2. Split PDF - extrahuje PDF prílohy (JavaScript)
3. Switch - kontrola či existuje PDF
4. HTTP Request - posiela na FastAPI `/invoice` endpoint
5. Gmail - notifikácia pri chybe

Toto prepísať ako Temporal workflow s activities:
- `fetch_emails_from_imap()` - načítanie emailov
- `extract_pdf_from_email()` - extrakcia PDF
- `send_to_fastapi()` - spracovanie faktúry (lokálne volanie)
- `send_error_notification()` - email notifikácia

### 2. Docker compose pre zákazníka

Služby:
- `temporal` - Temporal server
- `temporal-ui` - Web UI pre monitoring (voliteľné)
- `postgres` - PostgreSQL pre Temporal + staging dáta
- `nex-automat` - Python workers + FastAPI

### 3. Odstrániť

- n8n workflow na ICC serveri
- Cloudflare tunel
- Verejné DNS záznamy pre API
- SSL certifikáty pre externý prístup

## Technický stack

- **Python 3.11+**
- **Temporal** - workflow orchestrácia
- **FastAPI** - REST API backend
- **PostgreSQL** - databáza
- **PySide6 + Qt Widgets** - GUI (budúce formuláre)
- **Docker** - deployment

## Existujúci n8n workflow (referencia)

```json
{
  "name": "n8n-SupplierInvoiceEmailLoader",
  "nodes": [
    {
      "name": "Email Trigger (IMAP)",
      "type": "n8n-nodes-base.emailReadImap"
    },
    {
      "name": "Split PDF",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "// Extrahuje PDF prílohy, vracia: file_b64, filename, from_email, message_id, gmail_id, subject, received_date"
      }
    },
    {
      "name": "Has PDF Attachment?",
      "type": "n8n-nodes-base.switch"
    },
    {
      "name": "HTTP -> FastAPI /invoice",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://magerstav-invoices.icc.sk/invoice",
        "headers": "X-API-Key, Content-Type: application/json"
      }
    },
    {
      "name": "Send Error Notification",
      "type": "n8n-nodes-base.gmail",
      "parameters": {
        "sendTo": "rausch@em-1.sk"
      }
    }
  ]
}
```

## FastAPI payload štruktúra

```python
{
    "file_b64": str,      # Base64 encoded PDF
    "filename": str,       # Názov súboru
    "from_email": str,     # Odosielateľ
    "message_id": str,     # Email Message-ID
    "gmail_id": str,       # Gmail UID
    "subject": str,        # Predmet emailu
    "received_date": str   # Dátum prijatia
}
```

## Štruktúra projektu (návrh)

```
nex_automat/
├── workflows/
│   └── invoice_workflow.py
├── activities/
│   ├── email_activities.py
│   ├── invoice_activities.py
│   └── notification_activities.py
├── api/
│   └── main.py (FastAPI)
├── workers/
│   └── main_worker.py
├── tests/
├── docker-compose.yml
├── Dockerfile
└── config.py
```

## Prvý krok

Vytvoriť Temporal workflow pre spracovanie dodávateľských faktúr, ktorý nahradí n8n-SupplierInvoiceEmailLoader.