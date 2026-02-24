# Temporal Migration Phase 5: Deployment Complete

**Dátum:** 2025-12-21
**Status:** ✅ DONE

---

## Dokončené úlohy

### 1. HTTP 401 Invalid API Key - VYRIEŠENÉ
**Root cause:** Worker posielal requesty na port 8000, kde bežal starý invoice-loader z `C:\invoice-loader\`, nie nový z `C:\Deployment\nex-automat\`.

**Riešenie:**
- Opravený `FASTAPI_URL` v worker `.env`: 8000 → 8001
- Worker reštartovaný

### 2. Služba SupplierInvoiceLoader - OPRAVENÁ
**Root cause:** NSSM služba bola nakonfigurovaná na starý adresár `C:\invoice-loader\`.

**Riešenie:**
```powershell
nssm set SupplierInvoiceLoader Application "C:\Deployment\nex-automat\venv32\Scripts\python.exe"
nssm set SupplierInvoiceLoader AppDirectory "C:\Deployment\nex-automat\apps\supplier-invoice-loader"
nssm set SupplierInvoiceLoader AppParameters "main.py"
nssm set SupplierInvoiceLoader AppStdout "C:\Deployment\nex-automat\apps\supplier-invoice-loader\logs\service.log"
nssm set SupplierInvoiceLoader AppStderr "C:\Deployment\nex-automat\apps\supplier-invoice-loader\logs\service_error.log"
```

### 3. Konfigurácia portov na Mágerstav

| Služba | Port | Aplikácia |
|--------|------|-----------|
| supplier-invoice-loader | 8001 | FastAPI Invoice API |
| Temporal Server | 7233 | Temporal gRPC |
| Temporal UI | 8233 | Web UI |

### 4. Monitoring - FUNKČNÝ

| Nástroj | URL | Stav |
|---------|-----|------|
| Invoice API Health | http://localhost:8001/health | ✅ |
| Temporal Web UI | http://localhost:8233 | ✅ |
| Workflow história | 24+ úspešných | ✅ |

### 5. SMTP Notifikácie
- Preskočené - Temporal UI stačí na sledovanie zlyhaní
- OAuth2 použité pre IMAP (nie App Password)

## Finálny stav služieb na Mágerstav

| Služba | Status |
|--------|--------|
| NEX-Temporal-Server | ✅ Running |
| NEX-Invoice-Worker | ✅ Running |
| NEX-Polling-Scheduler | ✅ Running |
| SupplierInvoiceLoader | ✅ Running (port 8001) |

## End-to-end test
```
WorkflowResult(emails_processed=1, invoices_uploaded=1, errors=[])
```
✅ **PASSED** - Faktúra úspešne spracovaná cez Temporal workflow.

## Dôležité príkazy

### Reštart služieb
```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart NEX-Invoice-Worker
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart NEX-Polling-Scheduler
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart SupplierInvoiceLoader
```

### Kontrola stavu
```powershell
Get-Service | Where-Object {$_.Name -like "*NEX*" -or $_.Name -like "*Invoice*" -or $_.Name -like "*Supplier*"}
```

### Manuálny test workflow
```powershell
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

## Next Steps

1. Phase 6: Migration - Parallel run s n8n, validácia, vypnutie n8n
2. Testovanie s reálnymi faktúrami v produkcii
3. Dokumentácia pre operátorov
