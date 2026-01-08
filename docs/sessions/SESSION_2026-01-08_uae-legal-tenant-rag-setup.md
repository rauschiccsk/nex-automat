# Session: UAE Legal Tenant RAG Setup

**Dátum:** 2026-01-08
**Status:** ✅ DONE

---

## Dokončené úlohy

### 1. UAE Dokumenty Indexované ✅
- **19 dokumentov** indexovaných do RAG
- **37 chunks** vytvorených
- Dokumenty v `docs/knowledge/tenants/uae/`:
  - federal_laws/
  - court_decisions/
  - legal_procedures/
  - emirate_laws/

### 2. Database Metadata Opravené ✅
- Pridané `tenant='uae'` do 19 dokumentov
- SQL UPDATE na `documents` tabuľku
- Metadata obsahujú: tenant, filepath, file_size

### 3. RAG Pipeline Opravený ✅

**hybrid_search.py:**
- Pridané `metadata` field do SearchResult dataclass
- SQL SELECT obsahuje `d.metadata`
- SearchResult konštrukcia prenáša metadata

**api.py:**
- Import `json` pre parsing
- Parsing JSON string metadata: `json.loads(r.metadata)`
- Metadata merge s dodatočnými info (similarity, keyword_score)

**server_app.py:**
- Bez zmien, funguje správne s opravenými modules

### 4. Testovanie ✅

**RAG Search:**
- ✅ Vracia správne tenant='uae'
- ✅ Vracia source filename
- ✅ UAE dokumenty sú vyhľadávateľné

**Tenant Isolation:**
- ✅ UAE tenant vracia len UAE obsah
- ✅ ICC tenant vylučuje UAE obsah
- ✅ ANDROS tenant vylučuje UAE obsah

---

## Technické Detaily

### PostgreSQL Schema
```sql
-- Staré tabuľky (POUŽÍVANÉ)
documents (id, filename, content, metadata, created_at, updated_at)
chunks (id, document_id, chunk_index, content, embedding, metadata, created_at)

-- Nové tabuľky (NEPOUŽÍVANÉ)
rag_documents, rag_chunks, rag_keywords
```

### Metadata Štruktúra
```json
{
  "tenant": "uae",
  "filepath": "C:\Development\nex-automat\docs\knowledge\tenants\uae\...",
  "file_size": 8580,
  "similarity": 0.534,
  "keyword_score": 1.0,
  "document_id": 1037,
  "chunk_index": 1
}
```

### Kritické Zistenia
1. **PostgreSQL vracia JSON ako STRING** - potrebné `json.loads()`
2. **Nie `dict(json_string)`** - ValueError!
3. **RAG-API používa staré tabuľky** `documents`/`chunks`, nie `rag_*`
4. **Python cache problém** - potrebné zmazať `__pycache__` po zmenách

---

## Súbory Zmenené

### Production Fixes (Git commit)
```
tools/rag/hybrid_search.py  - pridaný metadata field + SQL
tools/rag/api.py            - pridaný json parsing metadata
```

### Session Scripts (Dočasné, NESKOMITOVAŤ)
```
scripts/01_test_uae_legal_rag.py           - testovací suite
scripts/02_diagnose_rag_metadata.py        - diagnostika (zlá tabuľka)
scripts/03_check_database_structure.py     - DB štruktúra
scripts/09_check_old_rag_tables.py         - diagnostika správnych tabuliek
scripts/10_fix_uae_tenant_metadata.py      - UPDATE tenant='uae'
scripts/11_inspect_null_tenant_metadata.py - inšpekcia NULL
scripts/12_patch_hybrid_search.py          - patch metadata support
scripts/13_test_hybrid_search_direct.py    - priamy test hybrid_search
scripts/14_fix_metadata_dict_conversion.py - fix dict() error v1
scripts/15_fix_api_metadata_passthrough.py - fix api.py unpacking
scripts/16_fix_api_metadata_v2.py          - fix api.py for loop
scripts/17_test_api_direct.py              - priamy test api.py
scripts/18_fix_api_dict_conversion.py      - fix dict() error v2
scripts/19_fix_api_json_parse.py           - fix JSON parsing
scripts/20_test_local_rag_api.py           - test lokálneho API
scripts/21_check_hybrid_search_code.py     - kontrola kódu
```

---

## Architektúra

### RAG-API (port 8765) = Development RAG
- PostgreSQL databáza `nex_automat_rag`
- Tabuľky: `documents`, `chunks`, `keywords`
- UAE dokumenty indexované TU ✅

### NexBrain (port 8003)
- **NIE JE** samostatný RAG
- Je **klient** RAG-API cez `https://rag-api.icc.sk`
- Konfigurácia: `RAG_API_URL=https://rag-api.icc.sk`

### Cloudflare Tunnel
- `https://rag-api.icc.sk` → `localhost:8765`
- Proxy pre RAG-API

---

## Next Steps (Budúce)

### 1. NexBrain Chat API (422 Error)
- Opraviť payload formát pre `/api/v1/chat`
- Nie kritické pre RAG funkčnosť

### 2. Optimalizácie
- Pridať cache pre embeddings
- Optimalizovať SQL queries
- Index na metadata->>'tenant'

### 3. Monitoring
- Logovanie RAG queries
- Metriky pre tenant usage
- Performance monitoring

---

## Dôležité Príkazy

### RAG Maintenance
```powershell
# Denná indexácia nových súborov
python tools/rag/rag_update.py --new

# Úplná reindexácia
python tools/rag/rag_update.py --all

# Štatistiky
python tools/rag/rag_update.py --stats
```

### RAG-API Server
```powershell
# Štart servera
python -m uvicorn tools.rag.server_app:app --host 127.0.0.1 --port 8765 --log-level info

# Reštart po zmenách (vymazať cache)
Remove-Item -Recurse -Force toolsag\__pycache__
```

### Testing
```powershell
# Priamy test hybrid_search
python scripts/13_test_hybrid_search_direct.py

# Priamy test api.py
python scripts/17_test_api_direct.py

# Test cez RAG-API server
python scripts/20_test_local_rag_api.py

# Kompletný test suite
python scripts/01_test_uae_legal_rag.py
```

### Database
```powershell
# Pripojenie na PostgreSQL
psql -U postgres -d nex_automat_rag

# Kontrola UAE dokumentov
SELECT COUNT(*) FROM documents WHERE metadata->>'tenant' = 'uae';

# Kontrola chunks
SELECT COUNT(*) FROM chunks c
JOIN documents d ON c.document_id = d.id
WHERE d.metadata->>'tenant' = 'uae';
```
