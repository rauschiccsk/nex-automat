# INIT PROMPT - RAG Implementation: Fáza 1 PostgreSQL Setup

**Projekt:** nex-automat  
**Current Status:** RAG Implementation - Fáza 1: PostgreSQL Setup  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_SESSION_2025_12_16_RAG_PLANNING]  
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

## ✅ ČO SME DOSIAHLI (Previous Session)

### 🎉 RAG Planning Complete

**Status:** RAG_IMPLEMENTATION.md dokument pripravený (45KB)

**Rozhodnutia:**
- ✅ **Stratégia:** HYBRID variant (RAG MVP → PySide6 → Temporal)
- ✅ **Tech Stack:** PostgreSQL + pgvector + sentence-transformers
- ✅ **Timeline:** 1 týždeň RAG MVP, potom 9 týždňov migrations
- ✅ **Benefit:** 30% rýchlejší vývoj, 64% úspora tokenov

**Dokumentácia:**
- ✅ `docs/strategic/RAG_IMPLEMENTATION.md` (kompletný plán)
- ✅ `docs/strategic/00_STRATEGIC_INDEX.md` (aktualizovaný)

---

## 🎯 CURRENT TASK: Fáza 1 - PostgreSQL Setup

### Cieľ Fázy 1

Nastaviť PostgreSQL databázu s pgvector extension pre RAG systém.

**Časový odhad:** 2-3 hodiny

**Deliverables:**
- ✅ PostgreSQL 16 nainštalovaný
- ✅ Databáza `nex_automat_rag` vytvorená
- ✅ pgvector extension aktívna
- ✅ 4 tabuľky vytvorené (rag_documents, rag_chunks, rag_keywords, rag_search_history)
- ✅ Indexy nakonfigurované (HNSW vector index)
- ✅ Test vector operations funguje

---

## 📋 FÁZA 1: STEP-BY-STEP CHECKLIST

### 1.1 PostgreSQL Inštalácia

**Windows Server:**

```powershell
# Možnosť A: Oficiálny installer
# https://www.postgresql.org/download/windows/

# Možnosť B: Chocolatey
choco install postgresql16

# Možnosť C: Scoop
scoop install postgresql
```

**After Install:**
```powershell
# Set PATH
$env:PATH += ";C:\Program Files\PostgreSQL\16\bin"

# Verify
psql --version
```

**Status:** ⏸️ TODO

---

### 1.2 pgvector Extension

**Inštalácia pgvector:**

```powershell
# Download pgvector pre PostgreSQL 16
# https://github.com/pgvector/pgvector/releases

# Alebo use prebuilt Windows binary
```

**Status:** ⏸️ TODO

---

### 1.3 Vytvorenie RAG Databázy

```sql
-- Connect as postgres user
psql -U postgres

-- Create database
CREATE DATABASE nex_automat_rag
    ENCODING 'UTF8'
    LC_COLLATE 'Slovak_Slovakia.1250'
    LC_CTYPE 'Slovak_Slovakia.1250';

-- Connect to new database
\c nex_automat_rag

-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify
SELECT * FROM pg_extension WHERE extname = 'vector';
```

**Status:** ⏸️ TODO

---

### 1.4 Vytvorenie Database Schema

**4 Tabuľky:**

```sql
-- 1. rag_documents (metadata)
CREATE TABLE rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    version VARCHAR(20) DEFAULT '1.0',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 2. rag_chunks (chunks + embeddings)
CREATE TABLE rag_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id VARCHAR(255) NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_type VARCHAR(50) NOT NULL,
    section_path TEXT,
    heading_level INTEGER,
    content TEXT NOT NULL,
    tokens INTEGER,
    embedding vector(384),  -- all-MiniLM-L6-v2
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_document 
        FOREIGN KEY (document_id) 
        REFERENCES rag_documents(document_id)
        ON DELETE CASCADE
);

-- 3. rag_keywords (keyword search)
CREATE TABLE rag_keywords (
    id SERIAL PRIMARY KEY,
    chunk_id UUID NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    weight FLOAT DEFAULT 1.0,
    
    CONSTRAINT fk_chunk 
        FOREIGN KEY (chunk_id) 
        REFERENCES rag_chunks(id)
        ON DELETE CASCADE
);

-- 4. rag_search_history (analytics)
CREATE TABLE rag_search_history (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    results_count INTEGER,
    top_chunk_ids UUID[],
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Status:** ⏸️ TODO

---

### 1.5 Vytvorenie Indexov

```sql
-- Documents indexes
CREATE INDEX idx_documents_category ON rag_documents(category);
CREATE INDEX idx_documents_status ON rag_documents(status);
CREATE INDEX idx_documents_updated ON rag_documents(updated_at);
CREATE INDEX idx_documents_metadata ON rag_documents USING GIN(metadata);

-- Chunks indexes
CREATE INDEX idx_chunks_document ON rag_chunks(document_id);
CREATE INDEX idx_chunks_type ON rag_chunks(chunk_type);

-- CRITICAL: HNSW vector index
CREATE INDEX idx_chunks_embedding 
    ON rag_chunks 
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Keywords indexes
CREATE INDEX idx_keywords_chunk ON rag_keywords(chunk_id);
CREATE INDEX idx_keywords_keyword ON rag_keywords(keyword);

-- Search history index
CREATE INDEX idx_search_created ON rag_search_history(created_at);
```

**Status:** ⏸️ TODO

---

### 1.6 Test Vector Operations

```sql
-- Test cosine distance
SELECT '[0.1, 0.2, 0.3]'::vector <=> '[0.2, 0.3, 0.4]'::vector AS distance;

-- Expected output: distance value (0.0 to 2.0)
-- If works, pgvector is OK!
```

**Status:** ⏸️ TODO

---

### 1.7 Konfiguračný Súbor

**Vytvor:** `config/rag_config.yaml`

```yaml
database:
  host: localhost
  port: 5432
  database: nex_automat_rag
  user: postgres
  password: your_password_here

embedding:
  model_name: all-MiniLM-L6-v2
  dimension: 384
  batch_size: 32

chunking:
  min_chunk_size: 100
  target_chunk_size: 750
  max_chunk_size: 1500
  overlap_tokens: 150

paths:
  docs_root: C:/Development/nex-automat/docs
  output_dir: C:/Development/nex-automat/rag_output

search:
  top_k: 5
  similarity_threshold: 0.5
  vector_weight: 0.7
  keyword_weight: 0.3
```

**Status:** ⏸️ TODO

---

## 📊 SUCCESS CRITERIA FÁZY 1

**Po dokončení Fázy 1 musí:**

- ✅ `psql --version` → PostgreSQL 16.x
- ✅ `psql -U postgres -d nex_automat_rag -c "\dx"` → vector extension listed
- ✅ `psql -U postgres -d nex_automat_rag -c "\dt"` → 4 tabuľky viditeľné
- ✅ Vector test query vracia výsledok
- ✅ Konfiguračný súbor existuje a je validný

---

## 🔄 WORKFLOW BEST PRACTICES

### Overený Proces

1. **Začni malým krokom** - Inštalácia PostgreSQL
2. **Vytvor artifact** - SQL skripty
3. **User skopíruje** - Do správneho umiestnenia
4. **Čakaj na confirmation** - Pred pokračovaním
5. **Test** - Vždy otestuj každý krok
6. **Next step** - Len po úspešnom teste

### Komunikácia

✅ **Stručne** - Žiadny verbose output  
✅ **Akcie** - Artifacts, konkrétne kroky  
✅ **Čakanie** - Po každom artifacte čakať na potvrdenie  
✅ **Progress** - Token stats na konci každej odpovede

---

## 📂 TECHNICAL INFO

### Project Structure

```
nex-automat/
├── config/
│   └── rag_config.yaml          # ← NEW (Fáza 1)
├── tools/
│   └── rag/                     # ← NEW (Fáza 2-6)
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       └── ...
├── docs/
│   ├── strategic/
│   │   ├── RAG_IMPLEMENTATION.md  # ← EXISTUJE
│   │   └── 00_STRATEGIC_INDEX.md  # ← AKTUALIZOVANÝ
│   └── ...
└── tests/
    └── test_rag_system.py       # ← NEW (Fáza 5)
```

### Environment

**OS:** Windows Server 2019+  
**PostgreSQL:** 16+ required  
**Python:** 3.11+ (pre Fázy 2-6)  
**RAM:** 16GB minimum  
**HDD:** 20GB free space

---

## 🎯 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Potvrdenie že rozumieš úlohe
3. Začni s **Krokom 1.1: PostgreSQL Inštalácia**
   - Artifact s inštalačným guide
   - Čakaj na user confirmation
4. Postupuj step-by-step cez checklist

**Pripomienka:**
- VŽDY artifacts pre SQL skripty
- VŽDY čakaj na confirmation pred next step
- VŽDY test po každom kroku
- Slovak language komunikácia

---

## 📚 SÚVISIACE DOKUMENTY

**Already processed:**
- docs/strategic/RAG_IMPLEMENTATION.md - Kompletný implementačný plán
- docs/strategic/00_STRATEGIC_INDEX.md - Aktualizovaný index
- docs/archive/sessions/SESSION_2025-12-16_RAG_Planning.md - Previous session

**To be created (Fáza 2-6):**
- tools/rag/*.py - Python moduly (Fáza 2-4)
- tests/test_rag_system.py - Test suite (Fáza 5)

**Reference:**
- docs/COLLABORATION_RULES.md - 22 pravidiel
- init_chat/PROJECT_MANIFEST.json - Project structure

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### PostgreSQL Windows Špecifiká

- PATH environment variable musí byť nastavená
- pgvector pre Windows môže vyžadovať prebuilt binary
- Collation: Slovak_Slovakia.1250 môže byť nedostupná (fallback: en_US.UTF8)

### Token Budget

**Budget:** 190,000 tokens  
**Estimated session:** 30,000-40,000 tokens (Fáza 1 je krátka, hlavne SQL)  
**Strategy:** Step-by-step, potvrdenie po každom kroku

---

**Token Budget:** 190,000  
**Ready to Start:** ✅ ÁNO  
**Current Phase:** 🔧 Fáza 1: PostgreSQL Setup  
**Status:** 🚀 Ready to Implement

---

**KONIEC INIT PROMPTU**