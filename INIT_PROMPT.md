INIT PROMPT - NEX Automat Development

Projekt: nex-automat
Current Status: UAE Legal Tenant Fully Operational
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 PREVIOUS SESSION: UAE Legal Tenant RAG Setup

## Dokončené v minulej session ✅

| Komponenta | Status |
|------------|--------|
| UAE dokumenty indexované | ✅ 19 docs, 37 chunks |
| Database metadata | ✅ tenant='uae' |
| hybrid_search.py | ✅ metadata support |
| api.py | ✅ JSON parsing |
| RAG Search | ✅ funguje |
| Tenant isolation | ✅ funguje |

## UAE Tenant Operational

### Tenants
- **icc** (ICC s.r.o.)
- **andros** (ANDROS s.r.o.)
- **uae** (UAE Legal Documentation) ✅ NEW

### RAG API
```
https://rag-api.icc.sk/search?query=...&tenant=uae&limit=5
```

### NexBrain API
```
http://127.0.0.1:8003/api/v1/chat
http://127.0.0.1:8003/api/v1/tenants
```

---

## Project Structure

```
C:\Development
ex-automat├── apps/
│   ├── nex-brain/              # Multi-tenant AI API (port 8003)
│   ├── supplier-invoice-worker/
│   └── supplier-invoice-loader/
├── docs/
│   └── knowledge/
│       ├── shared/             # Všetci tenants
│       └── tenants/
│           ├── icc/
│           ├── andros/
│           └── uae/            # ✅ OPERATIONAL
├── tools/
│   └── rag/                    # RAG-API (port 8765)
│       ├── hybrid_search.py    # ✅ FIXED
│       ├── api.py              # ✅ FIXED
│       └── server_app.py
└── scripts/
    └── 01_test_uae_legal_rag.py  # ✅ Test suite
```

---

## Token Budget
190,000 tokens

## Ready for
Nové úlohy podľa zadania
