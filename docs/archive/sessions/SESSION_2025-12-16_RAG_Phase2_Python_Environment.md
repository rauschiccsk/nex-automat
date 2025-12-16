# Session Notes: RAG Phase 2 - Python Environment Setup

**Date:** 2025-12-16  
**Developer:** Zoltán  
**Duration:** ~4 hours  
**Status:** ✅ COMPLETE  
**Phase:** RAG Implementation - Phase 2

---

## 🎯 Session Objectives

Nastaviť Python environment a vytvoriť základnú RAG module structure pre NEX Automat projekt.

**Planned Deliverables:**
- Virtual environment (Python 3.11+)
- RAG dependencies nainštalované
- RAG module structure v tools/rag/
- Database connection test úspešný
- Embedding model test úspešný

---

## ✅ Accomplishments

### 1. Python Environment Setup (2.1-2.2)

**Výzva:** Python 3.13 compatibility issues
- Pôvodne vytvorený venv s Python 3.13 32-bit
- Asyncpg a tiktoken vyžadovali Rust/C compiler
- **Riešenie:** Downgrade na Python 3.12.10 64-bit

**Kroky:**
1. Nainštalovaný Python 3.12.10 64-bit do `C:\Program Files\Python312\`
2. Recreated venv s Python 3.12 (64-bit)
3. Nainštalované všetky RAG dependencies (úspešne)

**Dependencies nainštalované:**
- sentence-transformers 2.5.1
- asyncpg 0.29.0 (prebuilt wheel)
- pydantic 2.10.5
- pydantic-settings 2.7.1
- tiktoken 0.6.0 (prebuilt wheel)
- torch 2.9.1 (110.9 MB)
- numpy 1.26.3
- PyYAML 6.0.1
- python-dotenv 1.0.1
- tqdm 4.66.1

### 2. RAG Module Structure (2.3)

**Vytvorené moduly v tools/rag/:**

1. **__init__.py** - Package initialization
2. **config.py** - Configuration management
   - Pydantic models pre validáciu
   - Load z config/rag_config.yaml
   - Environment variable support
3. **embeddings.py** - Embedding model wrapper
   - sentence-transformers integration
   - Batch processing
   - Singleton pattern
4. **database.py** - PostgreSQL + pgvector operations
   - Connection pool management
   - CRUD operations
   - Vector similarity search
5. **chunker.py** - Document chunking logic
   - Token-aware chunking
   - Overlap support
   - Sentence/paragraph boundaries
6. **indexer.py** - Document indexing pipeline
   - Koordinuje chunking, embedding, storage
   - Support pre single/batch indexing
7. **search.py** - Vector + hybrid search
   - Semantic search
   - Context retrieval
   - Search explanation

### 3. Database Setup

**Vytvorené tabuľky:**
- documents (id, filename, content, metadata, timestamps)
- chunks (id, document_id, chunk_index, content, embedding vector(384), metadata)
- keywords (id, chunk_id, keyword, weight)
- search_history (id, query, results_count, avg_similarity, execution_time_ms)

**Indexy:**
- HNSW vector index na chunks.embedding (m=16, ef_construction=64)
- B-tree indexy na FK a často používané stĺpce

**Triggers:**
- update_updated_at_column pre documents.updated_at

### 4. Configuration

**Aktualizovaný config/rag_config.yaml:**
```yaml
database:
  host: localhost
  port: 5432
  database: nex_automat_rag
  user: postgres
  password: [configured]
  pool_min_size: 2
  pool_max_size: 10

embedding:
  model_name: sentence-transformers/all-MiniLM-L6-v2
  dimension: 384
  batch_size: 32
  max_seq_length: 512

vector_index:
  index_type: hnsw
  m: 16
  ef_construction: 64
  ef_search: 40

chunking:
  chunk_size: 1000
  chunk_overlap: 200
  min_chunk_size: 100

search:
  default_limit: 10
  similarity_threshold: 0.7
  hybrid_alpha: 0.5
```

### 5. Testing & Validation

**Test Results:**
- ✅ Config loading: OK
- ✅ Embedding model: OK
  - Model: all-MiniLM-L6-v2
  - Dimension: 384
  - Device: cpu
  - Test embedding: shape=(384,)
- ✅ Database connection: OK
  - PostgreSQL 15.14
  - pgvector 0.8.1
  - Stats: 0 documents, 0 chunks

---

## 🛠️ Scripts Created

### Temporary Session Scripts (scripts/)

1. **01_setup_tools_setup_dir.py** - Vytvorí tools/setup/ adresár
2. **02a_create_requirements_file.py** - Generuje requirements-rag.txt
3. **02_install_rag_dependencies.py** - Inštaluje RAG dependencies
4. **03_check_python_architecture.py** - Kontroluje 32-bit vs 64-bit
5. **04_recreate_venv_64bit.py** - Recreate venv s 64-bit Python
6. **05_find_python_versions.py** - Hľadá Python inštalácie
7. **06_verify_python312.py** - Overuje Python 3.12 inštaláciu
8. **07_recreate_venv_python312.py** - Recreate venv s Python 3.12
9. **08_create_rag_structure.py** - Vytvorí tools/rag/ adresár
10. **09_update_rag_config.py** - Aktualizuje config/rag_config.yaml
11. **10_test_rag_connection.py** - Testuje všetky RAG moduly
12. **11_create_rag_tables.py** - Vytvorí databázové tabuľky

### Permanent Utilities

1. **tools/setup/create_venv.py** - Virtual environment utility
   - Support pre custom names
   - Auto-detect project root
   - Force mode
   - Cross-platform

---

## 📚 Documentation Created

1. **docs/setup/PYTHON_312_INSTALLATION.md** - Python 3.12 installation guide
2. **requirements-rag.txt** - RAG dependencies specification

---

## 🔧 Technical Decisions

### 1. Python Version: 3.12 vs 3.13

**Decision:** Use Python 3.12.10 64-bit  
**Reason:**
- Python 3.13 je príliš nový (release December 2024)
- Asyncpg a tiktoken nemajú prebuilt wheels pre 3.13
- Vyžadovali by Rust/C compiler
- Python 3.12 má vynikajúcu podporu balíčkov

### 2. Embedding Model: all-MiniLM-L6-v2

**Decision:** Use sentence-transformers/all-MiniLM-L6-v2  
**Reason:**
- Malý model (90.9 MB)
- Rýchly inference
- Dobrý balance kvalita/rýchlosť
- 384 dimensions (optimálne pre pgvector)

### 3. Vector Index: HNSW

**Decision:** HNSW (m=16, ef_construction=64)  
**Reason:**
- Najlepší performance pre similarity search
- Podporovaný pgvector
- Dobrý trade-off presnosť/rýchlosť

### 4. Chunking Strategy: Token-aware with overlap

**Decision:** 1000 tokens per chunk, 200 token overlap  
**Reason:**
- Zachováva kontext medzi chunks
- Optimálne pre embedding model
- Flexible pre rôzne typy dokumentov

---

## ⚠️ Issues & Resolutions

### Issue 1: Python 3.13 Compatibility

**Problem:** asyncpg, tiktoken vyžadovali kompiláciu  
**Root Cause:** Chýbajúce prebuilt wheels pre Python 3.13  
**Resolution:** Downgrade na Python 3.12.10 64-bit  
**Lesson:** Pre production použiť stabilnú Python verziu (3.11/3.12)

### Issue 2: 32-bit vs 64-bit Python

**Problem:** Pôvodný venv vytvorený s 32-bit Python  
**Root Cause:** Nesprávny Python executable použitý  
**Resolution:** Created check script, recreated venv s 64-bit Python  
**Lesson:** Vždy overiť architektúru pred vytvorením venv

### Issue 3: Missing Database Tables

**Problem:** "relation 'documents' does not exist"  
**Root Cause:** V Fáze 1 vytvorená len databáza, nie tabuľky  
**Resolution:** Created migration script (11_create_rag_tables.py)  
**Lesson:** Databázové migrations by mali byť súčasťou setup procesu

### Issue 4: Missing vector_index Config

**Problem:** Config validation failed - missing vector_index  
**Root Cause:** Neúplná config z Fázy 1  
**Resolution:** Updated config s kompletnou štruktúrou  
**Lesson:** Config validation je kritická pred použitím

---

## 📊 Metrics

**Token Usage:** 92,124 / 190,000 (48.5%)  
**Time:** ~4 hours  
**Scripts Created:** 12 temporary + 1 permanent  
**Modules Created:** 7 RAG modules  
**Documentation:** 2 guides  

**Dependencies Size:**
- Total download: ~1.5 GB
- Installed size: ~2.0 GB

**Database:**
- Tables: 4
- Indexes: 7
- Triggers: 1

---

## 🎯 Next Steps

### Immediate (Fáza 3)
1. Test full indexing pipeline
2. Index sample documents
3. Test search functionality
4. Validate embedding quality

### Future (Fáza 4-6)
1. Implement hybrid search (vector + keyword)
2. Add document metadata enrichment
3. Create CLI interface
4. Integration s NEX Automat dokumentáciou
5. Performance optimization
6. Production deployment

---

## 💡 Key Learnings

1. **Python Version Matters:** Vždy použiť stabilnú verziu s dobrou podporou balíčkov
2. **Architecture Matters:** 64-bit Python je kritický pre ML/AI dependencies
3. **Incremental Testing:** Test po každom významnom kroku odhalí problémy skoro
4. **Documentation:** Step-by-step guides šetria čas pri troubleshooting
5. **Configuration Management:** Validované konfigurácie predchádzajú runtime errors

---

## 📁 Files Modified/Created

### Created
- tools/setup/create_venv.py
- tools/rag/__init__.py
- tools/rag/config.py
- tools/rag/embeddings.py
- tools/rag/database.py
- tools/rag/chunker.py
- tools/rag/indexer.py
- tools/rag/search.py
- scripts/01-11_*.py (12 scripts)
- docs/setup/PYTHON_312_INSTALLATION.md
- requirements-rag.txt

### Modified
- config/rag_config.yaml (updated with complete structure)
- config/rag_config.yaml.backup (backup of Phase 1 config)

---

## 🔗 Related Sessions

- **Previous:** SESSION_2025-12-16_RAG_Phase1_PostgreSQL_Setup.md
- **Next:** [Planned] RAG Phase 3 - Document Processing

---

**Session End:** 2025-12-16  
**Status:** ✅ COMPLETE - Ready for Phase 3  
**Next Session Focus:** Document indexing and search testing