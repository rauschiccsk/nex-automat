#!/usr/bin/env python3
"""
New Chat Script - Temporal Migration Phase 5 Deployment
Session: 2025-12-20
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
KNOWLEDGE_DIR = DOCS_DIR / "knowledge" / "deployment" / "magerstav"
SESSION_DIR = DOCS_DIR / "sessions"

# Ensure directories exist
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
SESSION_DIR.mkdir(parents=True, exist_ok=True)

# Session info
SESSION_DATE = "2025-12-20"
SESSION_NAME = f"SESSION_{SESSION_DATE}_temporal-phase5-deployment"

# =============================================================================
# SESSION SUMMARY (KNOWLEDGE)
# =============================================================================
KNOWLEDGE_CONTENT = """\
# Temporal Phase 5 Deployment - Mágerstav Server

**Dátum:** 2025-12-20
**Server:** Mágerstav (testovacie prostredie)
**Status:** 🔄 IN PROGRESS - API Key issue

---

## Dokončené úlohy

### 1. Temporal Server Inštalácia ✅
- Stiahnutý Temporal CLI 1.5.1 (Server 1.29.1, UI 2.42.1)
- Inštalovaný do `C:\\Temporal\\cli\\temporal.exe`
- SQLite databáza: `C:\\Temporal\\data\\temporal.db`

### 2. NSSM Windows Services ✅

| Služba | Status | Popis |
|--------|--------|-------|
| NEX-Temporal-Server | ✅ Running | Port 7233 (gRPC), 8233 (UI) |
| NEX-Invoice-Worker | ✅ Running | Python 3.12 64-bit |
| NEX-Polling-Scheduler | ✅ Running | Polling každých 300s |

### 3. Worker Deployment ✅
- 64-bit Python 3.12 venv (temporalio vyžaduje 64-bit)
- Cesta: `C:\\Deployment\\nex-automat\\apps\\supplier-invoice-worker`
- Dependencies nainštalované (temporalio 1.21.1)

### 4. invoice_activities.py Fix ✅
- Opravený endpoint: `/invoice` (nie `/api/v1/invoice/upload`)
- Opravený payload: JSON s `file_b64` (base64)
- Pridaný `import base64`

### 5. Gmail OAuth2 ✅
- Tokeny fungujú
- `fetch_unread_emails` nachádza emaily

---

## Aktuálny problém ❌

### HTTP 401 - Invalid API key

**Symptóm:**
```
errors=['...pdf: HTTP 401: {"detail":"Invalid API key"}']
```

**Root cause:**
- `supplier-invoice-loader` číta `LS_API_KEY` z `os.getenv()` s default fallback
- Default: `ls-dev-key-change-in-production-2025`
- Worker používal iný kľúč

**Riešenie (čaká na test):**
- Worker `.env` zmenený na `LS_API_KEY=ls-dev-key-change-in-production-2025`
- Treba reštartovať službu a otestovať

---

## Next Steps

1. **Test API key fix:**
   ```powershell
   C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Invoice-Worker
   # Označ email ako neprečítaný, spusti workflow
   ```

2. **End-to-end test** - faktúra spracovaná a uložená

3. **Zjednotiť konfiguráciu** - vytvoriť `.env` pre `supplier-invoice-loader`

4. **Phase 5.2 Monitoring** - health checks, logging

---

## Dôležité príkazy

### Mágerstav Server

```powershell
# Stav služieb
Get-Service "NEX-*"

# Reštart služby
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Invoice-Worker

# Manuálny test workflow
cd C:\\Deployment\\nex-automat\\apps\\supplier-invoice-worker
.\\venv\\Scripts\\Activate.ps1
python -c "
import asyncio
from temporalio.client import Client
from workflows.invoice_workflow import InvoiceProcessingWorkflow

async def main():
    client = await Client.connect('localhost:7233')
    result = await client.execute_workflow(
        InvoiceProcessingWorkflow.run,
        id='manual-test-XXX',
        task_queue='supplier-invoice-queue'
    )
    print(f'Result: {result}')

asyncio.run(main())
"
```

### Temporal UI
- URL: http://localhost:8233

---

## Konfigurácia

### Worker .env
```env
LS_API_KEY=ls-dev-key-change-in-production-2025
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233
FASTAPI_URL=http://localhost:8000
IMAP_USER=magerstavinvoice@gmail.com
```

### supplier-invoice-loader config
- Súbor: `config/config_customer.py`
- API_KEY: `os.getenv("LS_API_KEY", "ls-dev-key-change-in-production-2025")`
"""

# =============================================================================
# INIT PROMPT
# =============================================================================
INIT_PROMPT = """\
INIT PROMPT - Temporal Migration Phase 5: Deployment (CONTINUED)

Projekt: nex-automat
Current Status: API Key Fix Testing
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: SESSION_2025-12-20_temporal-phase5-deployment

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 IMMEDIATE NEXT STEP: Test API Key Fix

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal Server na Mágerstav | ✅ Running |
| NEX-Invoice-Worker služba | ✅ Running |
| NEX-Polling-Scheduler služba | ✅ Running |
| invoice_activities.py fix | ✅ Deployed |
| Gmail OAuth2 | ✅ Funguje |
| Worker .env - LS_API_KEY | ✅ Zmenený |

## Aktuálny problém ❌

HTTP 401 - Invalid API key pri upload faktúry.

Worker .env bol zmenený na `LS_API_KEY=ls-dev-key-change-in-production-2025`.
**Treba reštartovať službu a otestovať.**

## Next Steps

1. Reštartuj NEX-Invoice-Worker
2. Označ email ako neprečítaný v Gmail
3. Spusti manuálny workflow test
4. Ak OK → End-to-end test s novou faktúrou
5. Phase 5.2 Monitoring

## RAG Query

```
https://rag-api.icc.sk/search?query=Temporal+deployment+Magerstav+NSSM+services&limit=5
```

Session Priority: Test API Key Fix → End-to-end faktúra
"""


def main():
    print("=" * 60)
    print("NEW CHAT SCRIPT - Temporal Phase 5 Deployment")
    print("=" * 60)

    # 1. Save SESSION file
    session_file = SESSION_DIR / f"{SESSION_NAME}.md"
    session_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ SESSION saved: {session_file}")

    # 2. Save KNOWLEDGE file
    knowledge_file = KNOWLEDGE_DIR / f"KNOWLEDGE_{SESSION_DATE}_temporal-phase5-deployment.md"
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ KNOWLEDGE saved: {knowledge_file}")

    # 3. Save INIT_PROMPT
    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"✅ INIT_PROMPT saved: {init_file}")

    # 4. Run RAG update
    print("\n" + "=" * 60)
    print("Running RAG update...")
    print("=" * 60)
    try:
        subprocess.run(
            [sys.executable, "tools/rag/rag_update.py", "--new"],
            cwd=BASE_DIR,
            check=True
        )
        print("✅ RAG updated")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ RAG update failed: {e}")

    print("\n" + "=" * 60)
    print("DONE! Start new chat with INIT_PROMPT.md")
    print("=" * 60)


if __name__ == "__main__":
    main()