# Temporal Phase 5 Deployment - Mágerstav Server (Session 2)

**Dátum:** 2025-12-20 - 2025-12-21
**Server:** Mágerstav (testovacie prostredie)
**Status:** 🔄 IN PROGRESS - API Key fix pending test

---

## Dokončené úlohy ✅

### 1. Temporal Server Inštalácia
- Temporal CLI 1.5.1 (Server 1.29.1, UI 2.42.1)
- Cesta: `C:\Temporal\cli\temporal.exe`
- SQLite DB: `C:\Temporal\data\temporal.db`
- Porty: 7233 (gRPC), 8233 (UI)

### 2. NSSM Windows Services (všetky Running)
| Služba | Popis |
|--------|-------|
| NEX-Temporal-Server | Temporal Server + UI |
| NEX-Invoice-Worker | Python 3.12 64-bit worker |
| NEX-Polling-Scheduler | Email polling každých 300s |

### 3. Worker Deployment
- ZIP prenos z Development na Mágerstav
- 64-bit Python 3.12 venv (temporalio vyžaduje 64-bit)
- Cesta: `C:\Deployment\nex-automat\apps\supplier-invoice-worker`

### 4. invoice_activities.py Fix
- Endpoint: `/invoice` (nie `/api/v1/invoice/upload`)
- Payload: JSON s `file_b64` (base64)
- Pridaný `import base64`

### 5. Gmail OAuth2
- Tokeny fungujú
- `fetch_unread_emails` nachádza emaily ✅

### 6. new_chat_template.py
- Vytvorený otestovaný template pre session management
- Cesta: `scripts/templates/new_chat_template.py`

---

## Aktuálny problém ❌

### HTTP 401 - Invalid API key

**Symptóm:**
```
errors=['...pdf: HTTP 401: {"detail":"Invalid API key"}']
```

**Root cause:**
- `supplier-invoice-loader/config/config_customer.py`:
  ```python
  API_KEY = os.getenv("LS_API_KEY", "ls-dev-key-change-in-production-2025")
  ```
- Worker `.env` mal iný kľúč

**Riešenie (aplikované, čaká test):**
- Worker `.env` zmenený na `LS_API_KEY=ls-dev-key-change-in-production-2025`
- Treba reštartovať NEX-Invoice-Worker a otestovať

---

## Next Steps

1. **Reštart a test API key fix:**
   ```powershell
   C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart NEX-Invoice-Worker
   # Označ email ako neprečítaný v Gmail
   # Spusti manuálny workflow test
   ```

2. **End-to-end test** - faktúra spracovaná a uložená do DB

3. **Phase 5.2 Monitoring** - health checks, logging

---

## Dôležité cesty (Mágerstav)

| Komponenta | Cesta |
|------------|-------|
| Temporal CLI | `C:\Temporal\cli\temporal.exe` |
| Temporal DB | `C:\Temporal\data\temporal.db` |
| Worker | `C:\Deployment\nex-automat\apps\supplier-invoice-worker` |
| Worker venv | `...\supplier-invoice-worker\venv` (Python 3.12 64-bit) |
| NSSM | `C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe` |
| FastAPI | `C:\Deployment\nex-automat\apps\supplier-invoice-loader` |

## Dôležité príkazy

```powershell
# Stav služieb
Get-Service "NEX-*"

# Reštart služby
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart NEX-Invoice-Worker

# Temporal UI
http://localhost:8233

# Manuálny workflow test
cd C:\Deployment\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\Activate.ps1
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
