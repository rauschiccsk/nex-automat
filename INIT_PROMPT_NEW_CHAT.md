# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** NEX Brain - Tenant Filtering Complete
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-tenant-filtering (2025-12-19)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = spustiť `python new_chat.py`
- **Rule #23:** RAG Workflow - Claude vypíše URL, user vloží, Claude fetchne
- **Rule #24:** PostgreSQL password via POSTGRES_PASSWORD env variable

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### Tenant Filtering - COMPLETE
- ✅ RAG API `?tenant=` parameter
- ✅ NEX Brain tenant integration
- ✅ Knowledge base štruktúra (shared/ + tenants/icc,andros/)
- ✅ Indexer tenant detection
- ✅ E2E test PASSED
- ✅ DB cleanup (137 docs, 517 chunks)

### Kľúčové súbory
- `tools/rag/hybrid_search.py` - tenant SQL filter
- `tools/rag/indexer.py` - detect_tenant()
- `apps/nex-brain/.env` - konfigurácia

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Git Commit
- Commitnúť všetky zmeny z tenant filtering session
- Zmazať dočasné scripty (01-07)

### Priority #2: Real Knowledge Base
- Pridať reálne dokumenty pre ICC
- Pridať reálne dokumenty pre ANDROS

### Priority #3: Fáza 3 - NEX Genesis Integration
- Connector pre ERP dáta
- Live queries

---

## 📂 KEY PATHS

```
apps/nex-brain/                         # NEX Brain app
  .env                                  # Multi-tenant config
  api/services/rag_service.py           # Tenant pass-through

tools/rag/                              # RAG system
  hybrid_search.py                      # Tenant SQL filter
  indexer.py                            # detect_tenant()
  server_app.py                         # ?tenant= endpoint

docs/knowledge/                         # Knowledge base
  shared/                               # All tenants
  tenants/icc/                          # ICC only
  tenants/andros/                       # ANDROS only
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&tenant=icc
https://rag-api.icc.sk/search?query=...&tenant=andros
```

---

**Token Budget:** 190,000  
**Location:** C:\Development
ex-automat

---

**KONIEC INIT PROMPTU**
