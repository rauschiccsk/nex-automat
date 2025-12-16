# INIT PROMPT - RAG Implementation: Fáza 2 Python Environment

**Projekt:** nex-automat  
**Current Status:** RAG Implementation - Fáza 2: Python Environment Setup  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_SESSION_2025_12_16_RAG_PHASE1]  
**Status:** 🚀 Ready to Implement

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## ✅ ČO SME DOSIAHLI (Previous Session - Phase 1)

### 🎉 PostgreSQL Setup COMPLETE

**Status:** Fáza 1 dokončená (4 hodiny)

**Deliverables:**
- ✅ PostgreSQL 15.14 funkčný
- ✅ pgvector 0.8.1 extension nainštalovaná (prebuilt binary)
- ✅ Databáza `nex_automat_rag` vytvorená
- ✅ 4 tabuľky vytvorené (documents, chunks, keywords, search_history)
- ✅ HNSW vector index nakonfigurovaný (m=16, ef_construction=64)
- ✅ Vector operations testované a funkčné
- ✅ `config/rag_config.yaml` vytvorený

**Kľúčové rozhodnutia:**
- Použitý prebuilt pgvector binary (Windows MinGW issue)
- HNSW index s parametrami: m=16, ef_construction=64
- UTF8 encoding s template0
- all-MiniLM-L6-v2 model (384 dimensions)

---

## 🎯 CURRENT TASK: Fáza 2 - Python Environment Setup

### Cieľ Fázy 2

Nastaviť Python environment a základnú štruktúru RAG modulov.

**Časový odhad:** 1-2 hodiny

**Deliverables:**
- ✅ Python virtual environment vytvorený
- ✅ Dependencies nainštalované
- ✅ RAG module structure vytvorená
- ✅ Database connection test úspešný
- ✅ Embedding model test úspešný

---

## 📋 FÁZA 2: STEP-BY-STEP CHECKLIST

### 2.1 Virtual Environment Setup

**Python Version Check:**
```powershell
python --version
# Expected: Python 3.11+ (preferably 3.11 or 3.12)
```

**Create venv:**
```powershell
cd C:\Development\nex-automat
python -m venv venv
venv\Scripts\activate
```

**Status:** ⏸️ TODO

---

### 2.2 Dependencies Installation

**Create requirements file:**
`requirements-rag.txt`:
```
# Core RAG dependencies
sentence-transformers==2.5.1
asyncpg==0.29.0
pydantic==2.6.1
pydantic-settings==2.1.0
tiktoken==0.6.0
numpy==1.26.3
PyYAML==6.0.1

# Optional but recommended
python-dotenv==1.0.1
tqdm==4.66.1
```

**Install:**
```powershell
pip install -r requirements-rag.txt
```

**Status:** ⏸️ TODO

---

### 2.3 RAG Module Structure

**Create directory structure:**
```
tools/
  └── rag/
      ├── __init__.py
      ├── config.py           # Configuration management
      ├── database.py         # PostgreSQL + pgvector operations
      ├── embeddings.py       # Embedding model wrapper
      ├── chunker.py          # Document chunking logic
      ├── indexer.py          # Document indexing pipeline
      └── search.py           # Vector + hybrid search
```

**Status:** ⏸️ TODO

---

### 2.4 Config Module (config.py)

**Úloha:** Vytvoriť `tools/rag/config.py`

**Funkcie:**
- Load `config/rag_config.yaml`
- Pydantic models pre validáciu
- Environment variable support

**Status:** ⏸️ TODO

---

### 2.5 Database Module (database.py)

**Úloha:** Vytvoriť `tools/rag/database.py`

**Funkcie:**
- Asyncpg connection pool
- CRUD operations pre 4 tabuľky
- Vector similarity search queries
- Transaction management

**Status:** ⏸️ TODO

---

### 2.6 Embeddings Module (embeddings.py)

**Úloha:** Vytvoriť `tools/rag/embeddings.py`

**Funkcie:**
- sentence-transformers model loading
- Batch embedding generation
- Model caching
- GPU support (ak dostupné)

**Status:** ⏸️ TODO

---

### 2.7 Connection Test Script

**Úloha:** Vytvoriť `tools/rag/test_connection.py`

**Tests:**
1. Database connection
2. pgvector extension check
3. Embedding model loading
4. Vector operation test

**Status:** ⏸️ TODO

---

## 📊 SUCCESS CRITERIA FÁZY 2

**Po dokončení Fázy 2 musí:**

- ✅ `python --version` → Python 3.11+
- ✅ Virtual environment aktivovaný
- ✅ Všetky dependencies nainštalované
- ✅ `tools/rag/` adresár existuje so 6 modulmi
- ✅ `test_connection.py` prebehol úspešne:
  - Database connection OK
  - pgvector extension OK
  - Embedding model loaded
  - Vector similarity query OK

---

## 📂 TECHNICAL INFO

### Project Structure

```
nex-automat/
├── config/
│   └── rag_config.yaml          # ← EXISTUJE (Phase 1)
├── tools/
│   └── rag/                     # ← NEW (Phase 2)
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── embeddings.py
│       ├── chunker.py
│       ├── indexer.py
│       ├── search.py
│       └── test_connection.py
├── venv/                        # ← NEW (Phase 2)
└── requirements-rag.txt         # ← NEW (Phase 2)
```

### Environment

**OS:** Windows Server 2019+  
**Python:** 3.11+ required  
**PostgreSQL:** 15.14 (už nainštalovaný)  
**pgvector:** 0.8.1 (už nainštalovaný)

### Database Connection Info

```yaml
Host: localhost
Port: 5432
Database: nex_automat_rag
User: postgres
Password: [from user]
```

---

## 🎯 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Potvrdenie že rozumieš úlohe
3. Začni s **Krokom 2.1: Virtual Environment Setup**
   - Check Python version
   - Create venv
   - Čakaj na user confirmation
4. Postupuj step-by-step cez checklist

**Pripomienka:**
- VŽDY artifacts pre Python súbory
- VŽDY čakaj na confirmation pred next step
- VŽDY test po každom kroku
- Slovak language komunikácia

---

## 📚 SÚVISIACE DOKUMENTY

**Already processed:**
- docs/strategic/RAG_IMPLEMENTATION.md - Kompletný implementačný plán
- docs/strategic/00_STRATEGIC_INDEX.md - Aktualizovaný index
- docs/archive/sessions/SESSION_2025-12-16_RAG_Phase1_PostgreSQL_Setup.md - Previous session
- config/rag_config.yaml - Configuration file

**To be created (Fáza 2):**
- tools/rag/*.py - Python moduly (6 súborov)
- requirements-rag.txt - Dependencies
- tools/rag/test_connection.py - Connection test

**Reference:**
- docs/COLLABORATION_RULES.md - 22 pravidiel
- init_chat/PROJECT_MANIFEST.json - Project structure

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### Python Environment

- Python 3.11+ je preferovaný (pre performance)
- sentence-transformers vyžaduje torch (auto-install)
- První download modelu trvá ~2-3 minúty

### Dependencies Size

- sentence-transformers: ~500 MB (model + dependencies)
- torch: ~1 GB (CPU version)
- Celkovo: ~1.5 GB download

### Token Budget

**Budget:** 190,000 tokens  
**Used in Phase 1:** 74,994 tokens  
**Remaining:** 115,006 tokens  
**Estimated Phase 2:** 30,000-40,000 tokens  
**Strategy:** Step-by-step, artifacts, minimálny verbose output

---

## 📈 PROGRESS TRACKING

**RAG Implementation Timeline:**
- ✅ **Fáza 1:** PostgreSQL Setup (4 hodiny) - COMPLETE
- 🔄 **Fáza 2:** Python Environment (1-2 hodiny) - CURRENT
- ⏸️ **Fáza 3:** Document Processing (2-3 hodiny)
- ⏸️ **Fáza 4:** Embedding & Indexing (2-3 hodiny)
- ⏸️ **Fáza 5:** Testing & Validation (1-2 hodiny)
- ⏸️ **Fáza 6:** Integration (1-2 hodiny)

**Total Estimated:** 11-16 hodín  
**Completed:** 4 hodiny (Phase 1)  
**Remaining:** 7-12 hodín

---

**Token Budget:** 190,000  
**Ready to Start:** ✅ ÁNO  
**Current Phase:** 🐍 Fáza 2: Python Environment Setup  
**Status:** 🚀 Ready to Implement

---

**KONIEC INIT PROMPTU**