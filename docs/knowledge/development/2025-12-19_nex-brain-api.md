# NEX Brain API - Technical Documentation

**Dátum:** 2025-12-19
**Kategória:** Development
**Status:** ✅ Complete

---

## Prehľad

Táto dokumentácia popisuje technické riešenia implementované pre NEX Brain API.

## Kľúčové komponenty

### 1. FastAPI Server
- Endpoint: `http://127.0.0.1:8001`
- Swagger UI: `/docs`
- Hlavné routes: `/api/v1/chat`, `/api/v1/tenants`, `/health`

### 2. RAG Service (`api/services/rag_service.py`)

**Boost logika pre správny chunk selection:**
- Chunks kde sekcia je na ZAČIATKU (prvých 200 znakov) dostávajú +0.8 boost
- Deduplicate vyberá chunk s najvyšším adjusted_score per súbor
- Keyword extraction z query pre lepšie matching

**Kľúčové metódy:**
- `_boost_relevant()` - pridáva boost podľa query keywords
- `_deduplicate_best()` - vyberá najlepší chunk per súbor
- `format_context()` - formátuje kontext pre LLM

### 3. LLM Service (`api/services/llm_service.py`)

**Konfigurácia pre minimálne halucinácie:**
- `temperature=0.0` (deterministické)
- `top_p=0.1` (focused)
- `num_predict=150-256` (krátke odpovede)
- Striktný system prompt

### 4. Chat Endpoint (`api/routes/chat.py`)

**Greeting detection:**
- Jednoduché pozdravy (Ahoj, Čau, Hi) - bez RAG
- ASCII patterns pre slovenské znaky
- Diacritics removal funkcia

## Riešené problémy

### RAG Chunk Selection
- **Problém:** RAG vracal zlý chunk (Dátové zdroje namiesto IMPLEMENTAČNÉ FÁZY)
- **Príčina:** Oba chunky obsahovali kľúčové slová, ale prvý mal vyšší score
- **Riešenie:** Boost +0.8 pre chunky kde sekcia je na začiatku

### LLM Halucinácie
- **Problém:** Model vymýšľal informácie (Docker, GitHub Actions)
- **Príčina:** Zlý kontext z RAG + príliš kreatívne nastavenia
- **Riešenie:** Správny chunk + temperature=0.0

---

## Použitie

```powershell
# Start server
cd C:\Development
ex-automatpps
ex-brain
python -m uvicorn api.main:app --reload --port 8001

# Test API
Invoke-RestMethod -Uri "http://127.0.0.1:8001/api/v1/chat" -Method POST -ContentType "application/json" -Body '{"question": "Co je NEX Brain?", "tenant": "icc"}'
```

---

**Related:** NEX_BRAIN_PRODUCT.md, supplier-invoice-staging
