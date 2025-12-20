INIT PROMPT - Temporal Migration Phase 6: Migration

Projekt: nex-automat
Current Status: Phase 5 Complete, Ready for Phase 6
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-21

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Phase 6 - Parallel run a migrácia z n8n

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal Server na Mágerstav | ✅ Running (port 7233, 8233) |
| NEX-Temporal-Server služba | ✅ Running |
| NEX-Invoice-Worker služba | ✅ Running |
| NEX-Polling-Scheduler služba | ✅ Running |
| SupplierInvoiceLoader | ✅ Running (port 8001) |
| End-to-end test | ✅ PASSED |
| Monitoring (Temporal UI) | ✅ Funkčný |

## Phase 6 Tasks

1. [ ] Parallel run - Temporal + n8n súčasne
2. [ ] Validácia výsledkov - porovnanie oboch systémov
3. [ ] Vypnutie n8n workflow
4. [ ] Cleanup starých súborov

## RAG Query

```
https://rag-api.icc.sk/search?query=n8n+workflow+migration+parallel+run&limit=5
```

Session Priority: Parallel run → Validácia → n8n vypnutie → Cleanup
