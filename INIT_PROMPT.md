INIT PROMPT - Temporal Migration Phase 5: Deployment (CONTINUED)

Projekt: nex-automat
Current Status: API Key Fix - Ready for Test
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-20

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 IMMEDIATE NEXT STEP: Test API Key Fix

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal Server na Mágerstav | ✅ Running (port 7233, 8233) |
| NEX-Temporal-Server služba | ✅ Running |
| NEX-Invoice-Worker služba | ✅ Running |
| NEX-Polling-Scheduler služba | ✅ Running |
| invoice_activities.py fix | ✅ Deployed |
| Gmail OAuth2 | ✅ Funguje |
| Worker .env LS_API_KEY | ✅ Zmenený na správny kľúč |
| new_chat_template.py | ✅ Otestovaný |

## Aktuálny problém ❌

HTTP 401 - Invalid API key pri upload faktúry.

**Fix aplikovaný:** Worker `.env` zmenený na `LS_API_KEY=ls-dev-key-change-in-production-2025`

**TREBA:** Reštartovať službu a otestovať!

## Immediate Actions

1. Na Mágerstav serveri:
   ```powershell
   C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart NEX-Invoice-Worker
   ```

2. Označ email ako neprečítaný v Gmail (`magerstavinvoice@gmail.com`)

3. Spusti test:
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
           id='manual-test-005',
           task_queue='supplier-invoice-queue'
       )
       print(f'Result: {result}')
   asyncio.run(main())
   "
   ```

4. Očakávaný výsledok: `invoices_uploaded: 1`

## RAG Query

```
https://rag-api.icc.sk/search?query=Temporal+deployment+Magerstav+API+key+invoice&limit=5
```

Session Priority: Test API Key Fix → End-to-end faktúra → Phase 5.2 Monitoring
