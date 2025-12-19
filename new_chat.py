#!/usr/bin/env python
"""
Create new chat session files for NEX Automat project.
Creates: SESSION_*.md, updates ARCHIVE_INDEX, creates INIT_PROMPT, runs rag_update.py --new
"""

import subprocess
from datetime import datetime
from pathlib import Path

BASE_PATH = Path("C:/Development/nex-automat")
ARCHIVE_PATH = BASE_PATH / "docs" / "archive" / "sessions"
KNOWLEDGE_PATH = BASE_PATH / "docs" / "knowledge" / "development"
INIT_CHAT_PATH = BASE_PATH  # ROOT - INIT_PROMPT_NEW_CHAT.md in project root

TODAY = datetime.now().strftime("%Y-%m-%d")
SESSION_NAME = f"SESSION_{TODAY}_nex-brain-api-fixes"

SESSION_CONTENT = f"""# Session: NEX Brain API Fixes

**Dátum:** {TODAY}
**Projekt:** nex-automat
**Fokus:** NEX Brain - RAG a LLM opravy

---

## DOKONČENÉ V TEJTO SESSION

### 1. new_chat.py oprava
- ✅ INIT_PROMPT path zmenený na ROOT (nie docs/init_chat/)

### 2. NEX Brain API - FastAPI Server
- ✅ Server beží na http://127.0.0.1:8001
- ✅ Swagger UI na /docs
- ✅ Endpointy: /api/v1/chat, /api/v1/tenants, /health

### 3. Chat Endpoint Opravy
- ✅ Greeting detection - "Ahoj" bez RAG
- ✅ ASCII patterns pre slovenské znaky
- ✅ Diacritics removal v is_simple_greeting()

### 4. LLM Service Opravy
- ✅ Striktnejší prompt
- ✅ temperature=0.0 (deterministic)
- ✅ top_p=0.1 (focused)
- ✅ Kratšie odpovede (150-256 tokens)

### 5. RAG Service Opravy - HLAVNÝ FIX
- ✅ Boost pre chunks kde IMPLEMENTAČNÉ FÁZY je na ZAČIATKU
- ✅ Deduplicate best chunk per file
- ✅ Keyword extraction a boosting
- ✅ Relevance filtering
- ✅ Správny chunk selection pre fázy otázky

---

## ŠTRUKTÚRA OPRAVENÝCH SÚBOROV

```
apps/nex-brain/
├── api/
│   ├── routes/
│   │   └── chat.py              # Greeting detection, ASCII patterns
│   └── services/
│       ├── rag_service.py       # Boost logic, dedupe, chunk selection
│       └── llm_service.py       # Strict prompt, low temperature
```

---

## KĽÚČOVÉ OPRAVY

### RAG Chunk Selection Problem
- Problém: RAG vracal chunk "Dátové zdroje" namiesto "IMPLEMENTAČNÉ FÁZY"
- Príčina: Oba chunky obsahovali slovo IMPLEMENT, ale prvý mal vyšší score
- Riešenie: Boost +0.8 pre chunky kde sekcia je na ZAČIATKU (prvých 200 znakov)

### LLM Hallucination Problem
- Problém: llama3.1:8b vymýšľal informácie (Docker, GitHub Actions)
- Príčina: Zlý kontext z RAG
- Riešenie: Správny chunk selection + striktnejší prompt

---

## TESTY - FUNGUJE

```
Otázka: "Co je NEX Brain?"
Odpoveď: "NEX Brain je inteligentné rozhranie pre NEX ekosystém..."
✅ SPRÁVNE

Otázka: "Ake su fazy implementacie NEX Brain?"
Odpoveď: "Fáza 1: Foundation, Fáza 2: Knowledge Base, Fáza 3: NEX Genesis Integration, Fáza 4: User Interface"
✅ SPRÁVNE
```

---

## SCRIPTS VYTVORENÉ

1. `01_fix_new_chat_path.py` - INIT_PROMPT do ROOT
2. `02_fix_chat_rag_detection.py` - greeting detection
3. `03_fix_chat_encoding.py` - ASCII patterns
4. `04_fix_llm_prompt.py` - lepší prompt
5. `05_fix_llm_strict_prompt.py` - striktnejší prompt
6. `06_fix_rag_context.py` - kratší kontext
7. `07_fix_rag_relevance.py` - relevance filtering
8. `08_fix_rag_best_chunk.py` - best chunk selection
9. `09_fix_rag_boost_keywords.py` - keyword boosting
10. `10_fix_rag_impl_detection.py` - IMPLEMENT detection
11. `11_debug_rag.py` - debug (DOČASNÝ - zmazať)
12. `12_fix_rag_specific_boost.py` - specific boost
13. `13_fix_rag_dedupe_order.py` - dedupe fix
14. `14_fix_rag_start_boost.py` - START boost

---

## NEXT STEPS

### Priority #1: Git Commit
- Commitnúť všetky zmeny
- Zmazať dočasné scripty (11_debug_rag.py)

### Priority #2: .env Configuration
- Vytvoriť .env súbor pre nex-brain

### Priority #3: Fáza 2 - Knowledge Base
- Import dokumentov pre ICC
- Import dokumentov pre ANDROS

---

**Session Status:** ✅ COMPLETE
**Token Usage:** ~85,000 / 190,000 (45%)
"""

KNOWLEDGE_CONTENT = f"""# NEX Brain API - Technical Documentation

**Dátum:** {TODAY}
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
cd C:\Development\nex-automat\apps\nex-brain
python -m uvicorn api.main:app --reload --port 8001

# Test API
Invoke-RestMethod -Uri "http://127.0.0.1:8001/api/v1/chat" -Method POST -ContentType "application/json" -Body '{{"question": "Co je NEX Brain?", "tenant": "icc"}}'
```

---

**Related:** NEX_BRAIN_PRODUCT.md, supplier-invoice-staging
"""

INIT_PROMPT_CONTENT = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** NEX Brain API - FUNCTIONAL  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-api-fixes ({TODAY})

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

### NEX Brain API - FUNCTIONAL
- ✅ FastAPI server na http://127.0.0.1:8001
- ✅ Swagger UI na /docs
- ✅ Greeting detection funguje
- ✅ RAG chunk selection opravený
- ✅ LLM odpovede bez halucinácie
- ✅ Testy "Co je NEX Brain?" a "fázy implementácie" fungujú

### Kľúčové opravy
- RAG: Boost pre chunky kde sekcia je na ZAČIATKU
- LLM: temperature=0.0, striktný prompt
- Chat: ASCII patterns pre slovenské znaky

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Git Commit
- Commitnúť všetky zmeny z minulej session
- Zmazať dočasné scripty

### Priority #2: .env Configuration
- Vytvoriť .env súbor pre nex-brain app

### Priority #3: Fáza 2 - Knowledge Base
- Import dokumentov pre ICC
- Import dokumentov pre ANDROS
- Tenant-specific RAG filtering

---

## 📂 KEY PATHS

```
apps/nex-brain/                         # NEX Brain app
  api/main.py                           # FastAPI
  api/routes/chat.py                    # Chat endpoint (greeting detection)
  api/services/rag_service.py           # RAG (boost logic)
  api/services/llm_service.py           # Ollama (strict prompt)
  cli/chat_cli.py                       # CLI testing
  config/settings.py                    # Multi-tenant config

docs/knowledge/strategic/               # Strategic docs
  NEX_BRAIN_PRODUCT.md                  # Product strategy
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

## 🛠️ NEX Brain Server

```powershell
# Start server
cd C:\\Development\\nex-automat\\apps\\nex-brain
python -m uvicorn api.main:app --reload --port 8001

# Test
Invoke-RestMethod -Uri "http://127.0.0.1:8001/api/v1/chat" -Method POST -ContentType "application/json" -Body '{{"question": "Co je NEX Brain?", "tenant": "icc"}}'
```

---

**Token Budget:** 190,000  
**Location:** C:\\Development\\nex-automat

---

**KONIEC INIT PROMPTU**
"""

def main():
    print("=" * 60)
    print("  Creating New Chat Session Files")
    print("=" * 60)

    # 1. Create SESSION file
    session_file = ARCHIVE_PATH / f"{SESSION_NAME}.md"
    session_file.parent.mkdir(parents=True, exist_ok=True)
    session_file.write_text(SESSION_CONTENT, encoding="utf-8")
    print(f"✅ Created: {session_file.name}")

    # 2. Create KNOWLEDGE document (for RAG indexing)
    knowledge_file = KNOWLEDGE_PATH / f"{TODAY}_nex-brain-api.md"
    knowledge_file.parent.mkdir(parents=True, exist_ok=True)
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ Created: {knowledge_file.name} (in docs/knowledge/)")

    # 3. Create INIT_PROMPT in ROOT
    init_file = INIT_CHAT_PATH / "INIT_PROMPT_NEW_CHAT.md"
    init_file.write_text(INIT_PROMPT_CONTENT, encoding="utf-8")
    print(f"✅ Created: INIT_PROMPT_NEW_CHAT.md (in ROOT)")

    # 4. Run rag_update.py --new
    print("\\n🔄 Running RAG update...")
    try:
        result = subprocess.run(
            [__import__("sys").executable, "tools/rag/rag_update.py", "--new"],
            cwd=BASE_PATH,
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print("✅ RAG update complete")
        else:
            print(f"⚠️ RAG update warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️ RAG update skipped: {e}")

    print("\\n" + "=" * 60)
    print("✅ New chat session ready!")
    print("=" * 60)
    print(f"\\nSession: {SESSION_NAME}")
    print("\\nNext: Start new Claude chat with INIT_PROMPT_NEW_CHAT.md")

if __name__ == "__main__":
    main()