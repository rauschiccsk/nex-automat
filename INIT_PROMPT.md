INIT PROMPT - NEX Automat Development

Projekt: nex-automat
Current Status: UAE Tenant Setup Complete
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 PREVIOUS SESSION: UAE Legal Tenant Setup

## Dokončené v minulej session ✅

| Komponenta | Status |
|------------|--------|
| UAE tenant štruktúra | ✅ |
| Vzorové dokumenty (27,500 slov) | ✅ |
| Indexácia do RAG | ✅ |
| NexBrain API test | ✅ |

## NexBrain Multi-tenant Setup

### Aktuálne tenants
- icc (ICC s.r.o.)
- andros (ANDROS s.r.o.)
- uae (UAE Legal Documentation)

### Konfigurácia
```
apps/nex-brain/.env:
MODE=multi-tenant
TENANTS=icc,andros,uae
```

### Database
- Shared PostgreSQL: nex_automat_rag
- Tenant filtering: metadata->>'tenant'

---

## Dostupné nástroje

### RAG System
```
https://rag-api.icc.sk/search?query=...&limit=5
```

### NexBrain API (lokálne)
```
http://127.0.0.1:8003/api/v1/chat
http://127.0.0.1:8003/api/v1/tenants
```

### Indexácia
```powershell
python tools/rag/rag_update.py --new
python tools/rag/rag_update.py --stats
```

---

## Project Structure

```
C:\Development\nex-automat\
├── apps/
│   ├── nex-brain/              # Multi-tenant AI API
│   ├── supplier-invoice-worker/
│   └── supplier-invoice-loader/
├── docs/
│   └── knowledge/
│       ├── shared/             # Všetci tenants
│       └── tenants/
│           ├── icc/
│           ├── andros/
│           └── uae/            # NOVÝ
└── tools/
    └── rag/                    # RAG indexer
```

---

## Token Budget
190,000 tokens

## Ready for
Nové úlohy podľa zadania
