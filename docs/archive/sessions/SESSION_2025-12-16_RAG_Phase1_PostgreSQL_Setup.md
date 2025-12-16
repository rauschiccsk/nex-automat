# Session Notes: RAG Implementation Phase 1 - PostgreSQL Setup

**Date:** 2025-12-16  
**Project:** nex-automat  
**Developer:** Zoltán  
**Phase:** RAG Implementation - Phase 1  
**Status:** ✅ COMPLETED  
**Duration:** ~4 hours

---

## 🎯 Session Objective

Nastavenie PostgreSQL databázy s pgvector extension pre RAG systém nex-automat projektu.

---

## ✅ Accomplished Tasks

### 1. Environment Verification
- ✅ PostgreSQL 15.14 overený ako funkčný
- ✅ psql command-line tools dostupné

### 2. pgvector Installation Journey

**Attempted Method 1: MSVC Compilation (Failed)**
- ✅ Visual Studio Build Tools 2026 nainštalované (6.93 GB)
- ✅ Developer Command Prompt nakonfigurovaný
- ✅ pgvector source code stiahnutý z GitHub
- ❌ MSVC linking failed (PostgreSQL 15 kompilovaný s MinGW, nie MSVC)
- ❌ Makefile.win upravený (pridané libpgcommon.lib, libpgport.lib) - neriešilo problém
- ❌ WIN32 defines pridané - stále linking errors
- **Root cause:** PostgreSQL Windows binaries sú MinGW-based, vyžadujú GCC toolchain

**Attempted Method 2: Prebuilt Binary (Success)**
- ✅ Nájdený GitHub repo: andreiramani/pgvector_pgsql_windows
- ✅ Stiahnutý: vector.v0.8.1-pg15.14.zip (29.8 KB)
- ✅ Rozbalené súbory: vector.dll, vector.control, SQL scripts
- ✅ Skopírované do PostgreSQL 15 directories:
  - `lib/vector.dll`
  - `share/extension/vector.control`
  - `share/extension/vector--*.sql`
- ✅ Extension úspešne vytvorená: `CREATE EXTENSION vector;`

### 3. Database Creation
- ✅ Databáza `nex_automat_rag` vytvorená
- ✅ UTF8 encoding s `TEMPLATE template0` (workaround pre Slovak collation)
- ✅ pgvector extension aktivovaná (version 0.8.1)

### 4. Schema Implementation
**4 tabuľky vytvorené:**
1. `rag_documents` - Document metadata
   - UUID primary key
   - document_id UNIQUE
   - category, title, file_path
   - JSONB metadata column
   
2. `rag_chunks` - Text chunks with embeddings
   - UUID primary key
   - vector(384) embedding column (all-MiniLM-L6-v2)
   - Foreign key → rag_documents
   - CASCADE delete
   
3. `rag_keywords` - Keyword index
   - SERIAL primary key
   - Foreign key → rag_chunks
   - keyword + weight columns
   
4. `rag_search_history` - Search analytics
   - SERIAL primary key
   - UUID[] array for top_chunk_ids

### 5. Indexes Created
**15 indexov celkom:**
- Documents: category, status, updated_at, metadata (GIN)
- Chunks: document_id, chunk_type
- **CRITICAL:** `idx_chunks_embedding` - HNSW index
  - Parameters: m=16, ef_construction=64
  - Operator: vector_cosine_ops
- Keywords: chunk_id, keyword
- Search history: created_at

### 6. Testing & Validation
- ✅ Vector operations tested: `<=>` cosine distance operator
- ✅ Test table created, data inserted, similarity query successful
- ✅ HNSW index verified in pg_indexes
- ✅ All foreign key relationships validated

### 7. Configuration
- ✅ `config/rag_config.yaml` vytvorený
- Database connection settings
- Embedding model config (all-MiniLM-L6-v2, 384 dim)
- Chunking parameters
- Search configuration
- Performance tuning settings

---

## 🔑 Key Technical Decisions

### 1. pgvector Installation Method
**Decision:** Použiť prebuilt binary namiesto kompilácii  
**Reason:** PostgreSQL Windows je MinGW-based, MSVC build vyžaduje GCC toolchain setup  
**Trade-off:** Závislosť na third-party repo (andreiramani), ale overený a funkčný

### 2. Database Collation
**Decision:** `TEMPLATE template0` s `en_US.UTF-8`  
**Reason:** Default Slovak_Slovakia.1250 collation konflikt  
**Impact:** UTF8 encoding zachovaný, plná podpora Unicode

### 3. HNSW Index Parameters
**Decision:** m=16, ef_construction=64  
**Reason:** Vyvážené nastavenie pre:
- Build time (stredný)
- Search quality (dobrá recall)
- Memory usage (rozumná)

### 4. Vector Dimension
**Decision:** 384 dimensions (all-MiniLM-L6-v2)  
**Reason:** 
- Optimálny pomer kvalita/rýchlosť
- Dobre podporovaný model
- Rozumná memory footprint

---

## 📁 Files Created/Modified

### Created:
```
config/
  └── rag_config.yaml                 # RAG system configuration

PostgreSQL Database:
  └── nex_automat_rag
      ├── rag_documents (table)
      ├── rag_chunks (table)
      ├── rag_keywords (table)
      ├── rag_search_history (table)
      └── 15 indexes (včítane HNSW)
```

### Modified:
- None (new database)

---

## 🛠️ Tools & Technologies Used

- **PostgreSQL:** 15.14
- **pgvector:** 0.8.1
- **Visual Studio Build Tools:** 2026 (nainštalované ale nepoužité)
- **Git:** Pre clone pgvector source
- **PowerShell:** Scripting, file operations
- **psql:** PostgreSQL command-line client

---

## ⚠️ Issues Encountered & Solutions

### Issue 1: MSVC Compilation Failures
**Problem:** Linking errors (`__imp__errstart`, `__imp__pg_number_of_ones`)  
**Root Cause:** PostgreSQL Windows kompilovaný s MinGW (GCC), nie MSVC  
**Solution:** Použiť prebuilt binary namiesto kompilácie

### Issue 2: Database Collation Error
**Problem:** `new collation (en_US.UTF-8) is incompatible with template database`  
**Root Cause:** Default template má Slovak_Slovakia.1250 collation  
**Solution:** Použiť `TEMPLATE template0` pre clean UTF8 setup

### Issue 3: Visual Studio Build Tools Install
**Problem:** 6.93 GB download/install  
**Outcome:** Nainštalované ale nakoniec nepoužité (MSVC vs MinGW issue)  
**Learning:** Windows PostgreSQL extensions vyžadujú MinGW toolchain

---

## 📊 Statistics

**Session Duration:** ~4 hours  
**Tokens Used:** 74,994 / 190,000 (39.5%)  
**Database Objects:**
- Tables: 4
- Indexes: 15
- Extensions: 1 (vector)

**Installation Attempts:**
- MSVC compilation: Failed (3+ attempts)
- Prebuilt binary: Success (first try)

---

## 🎯 Success Criteria - All Met

- ✅ `psql --version` → PostgreSQL 15.14
- ✅ `CREATE EXTENSION vector` → Success
- ✅ 4 tabuľky vytvorené a validované
- ✅ HNSW vector index funkčný
- ✅ Vector operations (cosine distance) testované
- ✅ Konfiguračný súbor existuje

---

## 🚀 Next Steps (Phase 2)

**Phase 2: Python Environment Setup**
1. Virtual environment setup
2. Dependencies installation:
   - sentence-transformers
   - asyncpg
   - pydantic
   - tiktoken
3. Basic RAG modules structure
4. Database connection testing

**Estimated Duration:** 1-2 hours

---

## 💡 Lessons Learned

1. **Windows PostgreSQL Extensions:**
   - Väčšina extensions je MinGW-based
   - MSVC build často nie je podporovaný
   - Prebuilt binaries sú legitímna cesta

2. **pgvector Specifics:**
   - HNSW index je production-ready
   - 384-dim embeddings sú sweet spot
   - Cosine distance operator (<=>`) je štandardný

3. **Workflow Process:**
   - Step-by-step approach fungoval dobre
   - Troubleshooting systematic approach
   - User confirmation pred pokračovaním kľúčový

4. **Time Estimation:**
   - Original: 2-3 hodiny
   - Actual: 4 hodiny (compilation troubleshooting)
   - Learning: Windows-specific issues add time

---

## 📚 References

- pgvector GitHub: https://github.com/pgvector/pgvector
- Prebuilt binaries: https://github.com/andreiramani/pgvector_pgsql_windows
- PostgreSQL Docs: https://www.postgresql.org/docs/15/
- HNSW Algorithm: Hierarchical Navigable Small World graphs

---

**Session Status:** ✅ COMPLETED  
**Next Session:** Phase 2 - Python Environment Setup  
**Ready for:** Implementation of document processing pipeline

---

**END OF SESSION NOTES**