# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** RAG Implementation COMPLETE  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** RAG Phase 3-6 Complete (2025-12-16)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## ✅ DOKONČENÉ - RAG Implementation

### 🎉 RAG System COMPLETE

**Databáza:**
- PostgreSQL 15.14 s pgvector 0.8.1
- Databáza: `nex_automat_rag`
- 107 dokumentov, 500 chunks, 415,891 tokens

**Python Environment:**
- Python 3.12.10 64-bit venv
- sentence-transformers, asyncpg, pydantic

**Features:**
- Hybrid search (70% vector + 30% keyword)
- 35ms average search latency
- CLI tools pre search a init prompt generation

**Použitie:**
```bash
# CLI Search
python -m tools.rag "your query"
python -m tools.rag "query" --context    # LLM format
python -m tools.rag --stats

# Init Prompt Helper
python -m tools.rag.init_prompt_helper "topic"
python -m tools.rag.init_prompt_helper -i  # Interactive

# Python API
from tools.rag.api import search, get_context
results = await search('your query')
context = await get_context('your query')
```

---

## 📂 PROJECT STRUCTURE

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/    # PyQt5 GUI
│   ├── supplier-invoice-loader/    # FastAPI backend
│   └── supplier-invoice-staging/   # Staging app
├── packages/
│   ├── nex-shared/                 # Shared GUI components
│   └── nexdata/                    # Btrieve access layer
├── tools/
│   ├── rag/                        # ✅ RAG system (COMPLETE)
│   │   ├── api.py                  # Search API
│   │   ├── hybrid_search.py        # Hybrid search
│   │   ├── __main__.py             # CLI tool
│   │   └── init_prompt_helper.py   # Context generator
│   └── setup/
├── config/
│   └── rag_config.yaml             # RAG configuration
├── docs/                           # 107 indexed documents
├── scripts/                        # Session scripts (01-23)
└── venv/                           # Python 3.12 64-bit
```

---

## 🎯 MOŽNÉ ĎALŠIE ÚLOHY

### RAG Enhancements
- [ ] Reindexovanie pri zmene dokumentov
- [ ] Keywords extraction a tagging
- [ ] Search history analytics
- [ ] Multi-language query expansion

### NEX Automat Core
- [ ] NEX Genesis Product Enrichment (v2.4 Phase 4)
- [ ] Btrieve → PostgreSQL migration pokračovanie
- [ ] n8n → Temporal migration

### Infrastructure
- [ ] FastAPI RAG endpoint integration
- [ ] Automated documentation updates
- [ ] CI/CD pipeline

---

## 📊 DATABASE STATUS

### RAG Database (nex_automat_rag)
```sql
-- Tables: documents, chunks, keywords, search_history
-- Documents: 107
-- Chunks: 500
-- Vector index: HNSW (m=16, ef_construction=64)
```

### Main PostgreSQL (nex_automat)
- Staging tables for invoice processing
- Customer configurations

### Btrieve (NEX Genesis)
- Legacy ERP data
- 25+ documented tables

---

## 📚 KEY DOCUMENTS

**Strategic:**
- docs/strategic/RAG_IMPLEMENTATION.md - RAG plán
- docs/strategic/PROJECT_ROADMAP.md - Roadmap

**Database:**
- docs/database/MIGRATION_MAPPING.md - Btrieve→PostgreSQL
- docs/database/DATABASE_PRINCIPLES.md - Konvencie

**Sessions:**
- docs/archive/sessions/ - Všetky session dokumenty

---

## 🔧 ENVIRONMENT

**Servers:**
- Development: C:\Development\nex-automat
- Deployment: C:\Deployment\nex-automat

**Python:**
- venv: Python 3.12.10 64-bit
- Activate: `.\venv\Scripts\Activate.ps1`

**PostgreSQL:**
- Port: 5432
- RAG DB: nex_automat_rag
- Main DB: nex_automat

---

## 📝 SESSION WORKFLOW

1. Načítaj tento INIT_PROMPT
2. Skontroluj memory_user_edits (22 pravidiel)
3. Identifikuj Current Status a Next Steps
4. Pracuj step-by-step s confirmations
5. Na konci: "novy chat" → 3 artifacts + archive update

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat  
**Status:** 🟢 Ready for new tasks

---

**KONIEC INIT PROMPTU**