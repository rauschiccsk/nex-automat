# INIT PROMPT - RAG Implementation: Fáza 3 Document Processing

**Projekt:** nex-automat  
**Current Status:** RAG Implementation - Fáza 3: Document Processing & Testing  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_SESSION_2025_12_16_RAG_PHASE2]  
**Status:** 🚀 Ready to Test & Index

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## ✅ ČO SME DOSIAHLI (Previous Sessions)

### 🎉 Fáza 1 COMPLETE - PostgreSQL Setup (4 hodiny)

**Deliverables:**
- ✅ PostgreSQL 15.14 funkčný
- ✅ pgvector 0.8.1 extension nainštalovaná
- ✅ Databáza `nex_automat_rag` vytvorená
- ✅ 4 tabuľky vytvorené (documents, chunks, keywords, search_history)
- ✅ HNSW vector index nakonfigurovaný (m=16, ef_construction=64)
- ✅ Vector operations testované a funkčné

### 🎉 Fáza 2 COMPLETE - Python Environment Setup (4 hodiny)

**Deliverables:**
- ✅ Python 3.12.10 64-bit venv vytvorený
- ✅ Všetky RAG dependencies nainštalované (~1.5 GB)
  - sentence-transformers 2.5.1
  - asyncpg 0.29.0
  - pydantic 2.10.5
  - tiktoken 0.6.0
  - torch 2.9.1
- ✅ RAG module structure vytvorená (7 modulov)
  - config.py, embeddings.py, database.py
  - chunker.py, indexer.py, search.py
- ✅ Database connection test úspešný
- ✅ Embedding model test úspešný
- ✅ Config/rag_config.yaml aktualizovaný

**Kľúčové rozhodnutia:**
- Python 3.12 (nie 3.13 - compatibility)
- sentence-transformers/all-MiniLM-L6-v2 (384 dim)
- HNSW index (m=16, ef_construction=64)
- 1000 tokens chunk size, 200 overlap

---

## 🎯 CURRENT TASK: Fáza 3 - Document Processing & Testing

### Cieľ Fázy 3

Otestovať a validovať kompletný RAG pipeline s reálnymi dokumentami.

**Časový odhad:** 2-3 hodiny

**Deliverables:**
- ✅ Test indexing pipeline s sample dokumentmi
- ✅ Validácia chunking quality
- ✅ Test semantic search functionality
- ✅ Performance metrics
- ✅ Dokumentácia výsledkov

---

## 📋 FÁZA 3: STEP-BY-STEP CHECKLIST

### 3.1 Test Indexing Pipeline

**Úloha:** Otestovať indexing s jednoduchým dokumentom

**Test 1 - Simple Document:**
```powershell
python -m tools.rag.indexer
```

**Expected output:**
- ✅ Document chunked (N chunks)
- ✅ Embeddings generated
- ✅ Chunks stored in database
- ✅ Vector index updated

**Status:** ⏸️ TODO

---

### 3.2 Index Sample Documents

**Úloha:** Indexovať niekoľko reálnych projektových dokumentov

**Možné zdroje:**
- docs/strategic/*.md
- docs/archive/sessions/*.md
- README.md
- Iné markdown dokumenty

**Test 2 - Batch Indexing:**
```python
from tools.rag.indexer import DocumentIndexer

async with DocumentIndexer() as indexer:
    results = await indexer.index_directory(
        directory="docs/strategic",
        pattern="*.md",
        show_progress=True
    )
```

**Status:** ⏸️ TODO

---

### 3.3 Test Search Functionality

**Úloha:** Otestovať semantic search na indexovaných dokumentoch

**Test 3 - Basic Search:**
```python
from tools.rag.search import SearchEngine

async with SearchEngine() as engine:
    results = await engine.search(
        query="document indexing",
        limit=5
    )
```

**Test 4 - Search with Context:**
```python
results = await engine.search_with_context(
    query="RAG implementation",
    limit=3,
    context_size=1
)
```

**Status:** ⏸️ TODO

---

### 3.4 Validate Results

**Úloha:** Overiť kvalitu chunking a search

**Validácia:**
1. Skontrolovať chunk sizes (mali by byť ~1000 tokens)
2. Overiť overlap medzi chunks
3. Testovať relevance scores
4. Validovať že context chunks majú zmysel

**Status:** ⏸️ TODO

---

### 3.5 Performance Metrics

**Úloha:** Zmerať performance RAG systému

**Metrics:**
- Indexing speed (docs/min, chunks/sec)
- Search latency (ms)
- Embedding generation time
- Database query time

**Status:** ⏸️ TODO

---

## 📊 SUCCESS CRITERIA FÁZY 3

**Po dokončení Fázy 3 musí:**

- ✅ Minimálne 5 dokumentov nainxovaných
- ✅ Search vracia relevantné výsledky
- ✅ Similarity scores > 0.7 pre relevantné queries
- ✅ Chunks majú správnu veľkosť (800-1200 tokens)
- ✅ Overlap funguje správne
- ✅ Performance je akceptovateľná (<100ms search)

---

## 📂 TECHNICAL INFO

### Project Structure

```
nex-automat/
├── config/
│   └── rag_config.yaml          # ✅ COMPLETE
├── tools/
│   ├── setup/
│   │   └── create_venv.py       # ✅ Permanent utility
│   └── rag/                     # ✅ COMPLETE
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── embeddings.py
│       ├── chunker.py
│       ├── indexer.py
│       └── search.py
├── venv/                        # ✅ Python 3.12 64-bit
├── scripts/                     # Session scripts (01-11)
└── requirements-rag.txt         # ✅ COMPLETE
```

### Environment

**Python:** 3.12.10 64-bit  
**OS:** Windows Server 2019+  
**PostgreSQL:** 15.14  
**pgvector:** 0.8.1  
**Embedding Model:** all-MiniLM-L6-v2 (384 dim, ~91 MB)

### Database Status

```sql
-- Tables: 4 (documents, chunks, keywords, search_history)
-- Indexes: 7 (including HNSW vector index)
-- Current data: 0 documents, 0 chunks
```

### Config Summary

```yaml
embedding:
  model_name: sentence-transformers/all-MiniLM-L6-v2
  dimension: 384
  batch_size: 32
  
chunking:
  chunk_size: 1000
  chunk_overlap: 200
  
search:
  default_limit: 10
  similarity_threshold: 0.7
```

---

## 🎯 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Potvrdenie že rozumieš úlohe
3. Začni s **Krokom 3.1: Test Indexing Pipeline**
   - Spusti test indexer
   - Analyzuj výsledky
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
- docs/archive/sessions/SESSION_2025-12-16_RAG_Phase1_PostgreSQL_Setup.md
- docs/archive/sessions/SESSION_2025-12-16_RAG_Phase2_Python_Environment.md
- docs/setup/PYTHON_312_INSTALLATION.md
- config/rag_config.yaml - Complete configuration

**Available for indexing:**
- docs/strategic/*.md
- docs/archive/sessions/*.md
- docs/database/*.md
- README.md

**Reference:**
- docs/COLLABORATION_RULES.md - 22 pravidiel
- init_chat/PROJECT_MANIFEST.json - Project structure

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### RAG System

- Embedding model je už načítaný do cache (~91 MB)
- Database je čistá (0 documents)
- Všetky moduly sú otestované a funkčné
- Search funguje len po indexovaní dokumentov

### Testing Strategy

- Začni s jednoduchým test dokumentom
- Potom postupne pridávaj reálne dokumenty
- Validuj každý krok pred pokračovaním
- Monitoruj performance metrics

### Token Budget

**Budget:** 190,000 tokens  
**Used in Phase 1:** 74,994 tokens  
**Used in Phase 2:** 92,124 tokens  
**Remaining:** 97,876 tokens  
**Estimated Phase 3:** 30,000-40,000 tokens  
**Strategy:** Focus na testing, minimize verbose output

---

## 📈 PROGRESS TRACKING

**RAG Implementation Timeline:**
- ✅ **Fáza 1:** PostgreSQL Setup (4 hodiny) - COMPLETE
- ✅ **Fáza 2:** Python Environment (4 hodiny) - COMPLETE
- 🔄 **Fáza 3:** Document Processing (2-3 hodiny) - CURRENT
- ⏸️ **Fáza 4:** Testing & Validation (1-2 hodiny)
- ⏸️ **Fáza 5:** Performance Optimization (2-3 hodiny)
- ⏸️ **Fáza 6:** Integration (1-2 hodiny)

**Total Estimated:** 14-19 hodín  
**Completed:** 8 hodín (Phases 1-2)  
**Remaining:** 6-11 hodín

---

**Token Budget:** 190,000  
**Ready to Start:** ✅ ÁNO  
**Current Phase:** 📄 Fáza 3: Document Processing & Testing  
**Status:** 🚀 Ready to Test

---

**KONIEC INIT PROMPTU**