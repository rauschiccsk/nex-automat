"""
Save COMPLETE Temporal Migration Document
Uloží kompletnú verziu s celým Python kódom
"""
from pathlib import Path

DOC_PATH = Path("docs/knowledge/strategic/N8N_TO_TEMPORAL_MIGRATION.md")

CONTENT = r'''# Migrácia n8n → Temporal (Natívne Windows)

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
| Method | Gmail OAuth2 |

### 2.6 Split PDF Logic (z n8n)

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

## 4. TEMPORAL WORKFLOW DEFINITION

### 4.1 Workflow

```python
# workflows/invoice_workflow.py

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities.email_activities import (
        fetch_new_emails,
        extract_pdf_attachments,
        mark_email_processed,
    )
    from activities.invoice_activities import send_to_fastapi
    from activities.notification_activities import send_error_notification


@workflow.defn
class InvoiceProcessingWorkflow:
    """
    Workflow pre spracovanie dodávateľských faktúr.
    Náhrada za n8n-SupplierInvoiceEmailLoader.
    """

    @workflow.run
    async def run(self) -> dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(minutes=5),
            maximum_attempts=3,
        )

        # 1. Fetch new emails from IMAP
        emails = await workflow.execute_activity(
            fetch_new_emails,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy,
        )

        results = {"processed": 0, "errors": 0, "skipped": 0}

        for email in emails:
            # 2. Extract PDF attachments
            pdfs = await workflow.execute_activity(
                extract_pdf_attachments,
                args=[email],
                start_to_close_timeout=timedelta(minutes=1),
            )

            if not pdfs:
                # No PDF found - send notification
                await workflow.execute_activity(
                    send_error_notification,
                    args=[email, "No PDF attachment found"],
                    start_to_close_timeout=timedelta(minutes=1),
                )
                results["skipped"] += 1
                continue

            # 3. Process each PDF
            for pdf_data in pdfs:
                try:
                    await workflow.execute_activity(
                        send_to_fastapi,
                        args=[pdf_data],
                        start_to_close_timeout=timedelta(minutes=3),
                        retry_policy=retry_policy,
                    )
                    results["processed"] += 1
                except Exception as e:
                    await workflow.execute_activity(
                        send_error_notification,
                        args=[email, str(e)],
                        start_to_close_timeout=timedelta(minutes=1),
                    )
                    results["errors"] += 1

            # 4. Mark email as processed
            await workflow.execute_activity(
                mark_email_processed,
                args=[email],
                start_to_close_timeout=timedelta(seconds=30),
            )

        return results
```

### 4.2 Email Activities

```python
# activities/email_activities.py

import imaplib
import email
from email.header import decode_header
from dataclasses import dataclass
from temporalio import activity
import base64

from config.settings import settings


@dataclass
class EmailData:
    uid: str
    message_id: str
    from_email: str
    subject: str
    received_date: str
    raw_message: bytes


@dataclass
class PDFAttachment:
    file_b64: str
    filename: str
    from_email: str
    message_id: str
    gmail_id: str
    subject: str
    received_date: str


@activity.defn
async def fetch_new_emails() -> list[EmailData]:
    """Fetch unread emails from IMAP."""

    mail = imaplib.IMAP4_SSL(
        host=settings.IMAP_HOST,
        port=settings.IMAP_PORT
    )
    mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
    mail.select("INBOX")

    # Search for unread emails
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    emails = []
    for eid in email_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Get from
        from_email = msg["From"]

        emails.append(EmailData(
            uid=eid.decode(),
            message_id=msg["Message-ID"] or "",
            from_email=from_email,
            subject=subject,
            received_date=msg["Date"] or "",
            raw_message=raw_email,
        ))

    mail.logout()
    return emails


@activity.defn
async def extract_pdf_attachments(email_data: EmailData) -> list[PDFAttachment]:
    """Extract PDF attachments from email."""

    msg = email.message_from_bytes(email_data.raw_message)
    pdfs = []

    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue

        filename = part.get_filename()
        if not filename:
            continue

        # Decode filename if needed
        if isinstance(filename, bytes):
            filename = filename.decode()

        # Filter only PDFs
        if not filename.lower().endswith(".pdf"):
            continue

        # Get content
        payload = part.get_payload(decode=True)
        file_b64 = base64.b64encode(payload).decode("utf-8")

        pdfs.append(PDFAttachment(
            file_b64=file_b64,
            filename=filename,
            from_email=email_data.from_email,
            message_id=email_data.message_id,
            gmail_id=email_data.uid,
            subject=email_data.subject,
            received_date=email_data.received_date,
        ))

    return pdfs


@activity.defn
async def mark_email_processed(email_data: EmailData) -> None:
    """Mark email as read in IMAP."""

    mail = imaplib.IMAP4_SSL(
        host=settings.IMAP_HOST,
        port=settings.IMAP_PORT
    )
    mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
    mail.select("INBOX")

    # Mark as seen
    mail.store(email_data.uid.encode(), "+FLAGS", "\\Seen")

    mail.logout()
```

### 4.3 Invoice Activities

```python
# activities/invoice_activities.py

import httpx
from temporalio import activity

from config.settings import settings
from activities.email_activities import PDFAttachment


@activity.defn
async def send_to_fastapi(pdf: PDFAttachment) -> dict:
    """Send PDF to FastAPI for processing."""

    payload = {
        "file_b64": pdf.file_b64,
        "filename": pdf.filename,
        "from_email": pdf.from_email,
        "message_id": pdf.message_id,
        "gmail_id": pdf.gmail_id,
        "subject": pdf.subject,
        "received_date": pdf.received_date,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            settings.FASTAPI_URL,
            json=payload,
            headers={
                "X-API-Key": settings.FASTAPI_API_KEY,
                "Content-Type": "application/json",
            }
        )
        response.raise_for_status()
        return response.json()
```

### 4.4 Notification Activities

```python
# activities/notification_activities.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from temporalio import activity

from config.settings import settings
from activities.email_activities import EmailData


@activity.defn
async def send_error_notification(email_data: EmailData, error: str) -> None:
    """Send error notification via SMTP."""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Invoice Processing Error"
    msg["From"] = settings.SMTP_FROM
    msg["To"] = settings.NOTIFICATION_EMAIL

    html = f"""
    <h2>⚠️ Nerozpoznaná faktúra</h2>
    <p>{error}</p>

    <h3>📧 DETAILY EMAILU</h3>
    <ul>
      <li><strong>Od:</strong> {email_data.from_email}</li>
      <li><strong>Predmet:</strong> {email_data.subject}</li>
      <li><strong>Dátum:</strong> {email_data.received_date}</li>
    </ul>

    <p>Prosím spracujte manuálne.</p>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(
            settings.SMTP_FROM,
            settings.NOTIFICATION_EMAIL,
            msg.as_string()
        )
```

### 4.5 Configuration

```python
# config/settings.py

import os
from dataclasses import dataclass


@dataclass
class Settings:
    # IMAP (Gmail)
    IMAP_HOST: str = "imap.gmail.com"
    IMAP_PORT: int = 993
    IMAP_USER: str = os.getenv("IMAP_USER", "magerstavinvoice@gmail.com")
    IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD", "")  # App Password

    # FastAPI (localhost - no tunnel needed!)
    FASTAPI_URL: str = os.getenv("FASTAPI_URL", "http://localhost:8001/invoice")
    FASTAPI_API_KEY: str = os.getenv("LS_API_KEY", "")

    # SMTP (for notifications)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = os.getenv("SMTP_USER", "magerstavinvoice@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")  # App Password
    SMTP_FROM: str = os.getenv("SMTP_FROM", "magerstavinvoice@gmail.com")
    NOTIFICATION_EMAIL: str = os.getenv("NOTIFICATION_EMAIL", "rausch@em-1.sk")

    # Temporal
    TEMPORAL_HOST: str = os.getenv("TEMPORAL_HOST", "localhost:7233")
    TEMPORAL_NAMESPACE: str = os.getenv("TEMPORAL_NAMESPACE", "default")
    TEMPORAL_TASK_QUEUE: str = "invoice-processing"

    # Polling interval (seconds)
    POLLING_INTERVAL: int = int(os.getenv("POLLING_INTERVAL", "60"))


settings = Settings()
```

### 4.6 Worker

```python
# workers/main_worker.py

import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from config.settings import settings
from workflows.invoice_workflow import InvoiceProcessingWorkflow
from activities.email_activities import (
    fetch_new_emails,
    extract_pdf_attachments,
    mark_email_processed,
)
from activities.invoice_activities import send_to_fastapi
from activities.notification_activities import send_error_notification


async def main():
    client = await Client.connect(settings.TEMPORAL_HOST)

    worker = Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[InvoiceProcessingWorkflow],
        activities=[
            fetch_new_emails,
            extract_pdf_attachments,
            mark_email_processed,
            send_to_fastapi,
            send_error_notification,
        ],
    )

    print(f"Worker started, listening on {settings.TEMPORAL_TASK_QUEUE}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### 4.7 Scheduler (Polling Trigger)

```python
# scheduler/polling_scheduler.py

import asyncio
from temporalio.client import Client

from config.settings import settings
from workflows.invoice_workflow import InvoiceProcessingWorkflow


async def main():
    client = await Client.connect(settings.TEMPORAL_HOST)

    print(f"Scheduler started, polling every {settings.POLLING_INTERVAL}s")

    while True:
        try:
            # Start workflow
            handle = await client.start_workflow(
                InvoiceProcessingWorkflow.run,
                id=f"invoice-processing-{asyncio.get_event_loop().time()}",
                task_queue=settings.TEMPORAL_TASK_QUEUE,
            )

            # Wait for result
            result = await handle.result()
            print(f"Workflow completed: {result}")

        except Exception as e:
            print(f"Workflow error: {e}")

        # Wait for next poll
        await asyncio.sleep(settings.POLLING_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. ŠTRUKTÚRA PROJEKTU

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

## 6. IMPLEMENTATION ROADMAP

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

## 7. WINDOWS SERVICES

### 7.1 Temporal Server Service

```powershell
# Inštalácia pomocou NSSM
nssm install TemporalServer "C:\Temporal\temporal-server.exe" start --config "C:\Temporal\config.yaml"
nssm set TemporalServer AppDirectory "C:\Temporal"
nssm set TemporalServer Start SERVICE_AUTO_START
```

### 7.2 Temporal Worker Service

```powershell
nssm install TemporalInvoiceWorker "C:\Python311\python.exe" "-m" "workers.main_worker"
nssm set TemporalInvoiceWorker AppDirectory "C:\Deployment\nex-automat\apps\temporal-invoice-worker"
nssm set TemporalInvoiceWorker AppEnvironmentExtra "PYTHONPATH=C:\Deployment\nex-automat\apps\temporal-invoice-worker"
nssm set TemporalInvoiceWorker Start SERVICE_AUTO_START
```

### 7.3 Polling Scheduler Service

```powershell
nssm install TemporalInvoiceScheduler "C:\Python311\python.exe" "-m" "scheduler.polling_scheduler"
nssm set TemporalInvoiceScheduler AppDirectory "C:\Deployment\nex-automat\apps\temporal-invoice-worker"
nssm set TemporalInvoiceScheduler Start SERVICE_AUTO_START
```

---

## 8. ENVIRONMENT VARIABLES

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

## 9. PYTHON DEPENDENCIES

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

## 10. SUCCESS CRITERIA

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

### Operational

| Kritérium | Cieľ |
|-----------|------|
| Windows Services | 3 služby (auto-start) |
| Monitoring | Temporal UI |
| Easy troubleshooting | Detailné logy |
| Rollback procedure | Zdokumentované |

---

## 11. ROLLBACK PLAN

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
    print("SAVE: COMPLETE Temporal Migration Document")
    print("=" * 70)

    # Vytvor adresár ak neexistuje
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Ulož dokument
    DOC_PATH.write_text(CONTENT, encoding='utf-8')
    print(f"✅ Uložený: {DOC_PATH}")

    # Štatistiky
    lines = CONTENT.count('\n')
    chars = len(CONTENT)

    print()
    print(f"ŠTATISTIKY:")
    print(f"  Riadkov: {lines}")
    print(f"  Znakov: {chars:,}")
    print()
    print("OBSAH:")
    print("  1. Executive Summary")
    print("  2. Aktuálny stav n8n (IMAP, FastAPI, Payload)")
    print("  3. Cieľový stav Temporal")
    print("  4. KOMPLETNÝ Python kód:")
    print("     - invoice_workflow.py")
    print("     - email_activities.py")
    print("     - invoice_activities.py")
    print("     - notification_activities.py")
    print("     - settings.py")
    print("     - main_worker.py")
    print("     - polling_scheduler.py")
    print("  5. Štruktúra projektu")
    print("  6. Implementation Roadmap (6 fáz)")
    print("  7. Windows Services (NSSM)")
    print("  8. Environment Variables")
    print("  9. Python Dependencies")
    print(" 10. Success Criteria")
    print(" 11. Rollback Plan")
    print()
    print("Ďalší krok: python tools/rag/rag_update.py --new")
    print("=" * 70)


if __name__ == "__main__":
    main()