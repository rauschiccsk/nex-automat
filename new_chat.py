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
INIT_CHAT_PATH = BASE_PATH / "docs" / "init_chat"

TODAY = datetime.now().strftime("%Y-%m-%d")
SESSION_NAME = f"SESSION_{TODAY}_nex-brain-foundation"

SESSION_CONTENT = f"""# Session: NEX Brain Foundation

**Dátum:** {TODAY}
**Projekt:** nex-automat
**Fokus:** NEX Brain - Fáza 1 Foundation Complete

---

## DOKONČENÉ V TEJTO SESSION

### 1. Strategický dokument NEX Brain
- ✅ `docs/knowledge/strategic/NEX_BRAIN_PRODUCT.md`
- Vízia: Mozog NEX ekosystému
- Architektúra: RAG + Ollama + NEX Genesis
- Podrobné porovnanie Ollama modelov (plusy/mínusy)
- Kedy sa oplatí premium model
- Nákladová analýza
- Migrácia medzi modelmi
- Pilot plán (ICC, ANDROS)
- Zaindexované v RAG

### 2. NEX Brain Application Structure
- ✅ `apps/nex-brain/` vytvorená
- Multi-tenant architektúra (ICC, ANDROS)
- FastAPI backend (`api/main.py`)
- Chat endpoint (`api/routes/chat.py`)
- RAG service (`api/services/rag_service.py`)
- LLM service (`api/services/llm_service.py`)
- CLI pre testovanie (`cli/chat_cli.py`)
- Konfigurácia (`config/settings.py`)

### 3. Ollama Integration
- ✅ Ollama nainštalovaná
- ✅ llama3.1:8b model stiahnutý (4.9 GB)
- ✅ Beží na GPU (Quadro M4000, 8GB VRAM)
- ✅ Prompt tuning - opravené halucinácie

### 4. Testovanie
- ✅ CLI funguje
- ✅ RAG integrácia funguje
- ✅ LLM odpovede v slovenčine
- ⚠️ Pomalšie odpovede (~40s) kvôli staršej GPU

---

## ŠTRUKTÚRA PROJEKTU

```
apps/nex-brain/
├── api/
│   ├── main.py              # FastAPI app
│   ├── routes/
│   │   └── chat.py          # /chat endpoint (multi-tenant)
│   └── services/
│       ├── rag_service.py   # RAG integration
│       └── llm_service.py   # Ollama integration
├── cli/
│   └── chat_cli.py          # CLI pre testovanie
├── config/
│   └── settings.py          # Multi-tenant config
├── requirements.txt
└── README.md
```

---

## KĽÚČOVÉ ROZHODNUTIA

1. **Názov produktu:** NEX Brain (nie CorpBrain)
2. **Positioning:** Core komponent NEX ekosystému (mozog)
3. **Architektúra:** Multi-tenant (jeden server pre ICC + ANDROS)
4. **LLM Model:** llama3.1:8b (odporúčaný, SK podpora)
5. **Migrácia:** Triviálna - zmena 1 parametra

---

## NEXT STEPS

### Immediate (nasledujúca session)
1. Git commit všetkých zmien
2. FastAPI server testovanie
3. `.env` súbor pre konfiguráciu

### Fáza 2: Knowledge Base
- Import dokumentov pre ICC
- Import dokumentov pre ANDROS
- Tenant-specific RAG filtering

### Fáza 3: NEX Genesis Integration
- Connector pre ERP dáta
- Live queries

---

## TECHNICKÉ POZNÁMKY

### HW na dev serveri
- GPU: Quadro M4000 (8GB VRAM, staršia)
- Ollama: 100% GPU, ~10-15 tok/s
- Odpovede: ~30-40 sekúnd

### Odporúčanie pre produkciu
- RTX 4060 (8GB) = ~350 EUR = 4x rýchlejšie

### Multi-tenant konfigurácia
```env
MODE=multi-tenant
TENANTS=icc,andros
```

---

## SCRIPTS VYTVORENÉ

1. `01_save_nex_brain_product.py` - strategický dokument
2. `02_fix_nex_brain_location.py` - presun do knowledge/
3. `03_create_nex_brain_structure.py` - app štruktúra
4. `04_fix_llm_prompt.py` - oprava halucinácie

---

**Session Status:** ✅ COMPLETE - Fáza 1 Foundation hotová
**Token Usage:** ~84,000 / 190,000 (44%)
"""

INIT_PROMPT_CONTENT = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** NEX Brain - Fáza 1 COMPLETE  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-foundation ({TODAY})

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

### NEX Brain Foundation Complete
- ✅ Strategický dokument `docs/knowledge/strategic/NEX_BRAIN_PRODUCT.md`
- ✅ App štruktúra `apps/nex-brain/` (multi-tenant)
- ✅ Ollama integrácia (llama3.1:8b na GPU)
- ✅ RAG integrácia funguje
- ✅ CLI funguje (`python cli/chat_cli.py`)
- ✅ Prompt tuning - opravené halucinácie

### Multi-tenant Architecture
- MODE=multi-tenant / single-tenant
- Tenants: icc, andros
- Tenant-specific prompts a RAG filtering

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Git Commit
- Commitnúť všetky zmeny z tejto session

### Priority #2: FastAPI Server
- Otestovať `uvicorn api.main:app`
- Curl test na `/api/v1/chat`

### Priority #3: .env Configuration
- Vytvoriť `.env` súbor pre nex-brain

### Priority #4: Fáza 2 - Knowledge Base
- Import dokumentov pre ICC
- Import dokumentov pre ANDROS

---

## 📂 KEY PATHS

```
apps/nex-brain/                         # NEX Brain app
  api/main.py                           # FastAPI
  api/routes/chat.py                    # Chat endpoint
  api/services/rag_service.py           # RAG
  api/services/llm_service.py           # Ollama
  cli/chat_cli.py                       # CLI testing
  config/settings.py                    # Multi-tenant config

docs/knowledge/strategic/               # Strategic docs
  NEX_BRAIN_PRODUCT.md                  # Product strategy

tools/rag/                              # RAG tools
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

## 🛠️ OLLAMA

```powershell
# Check status
& "$env:LOCALAPPDATA\\Programs\\Ollama\\ollama.exe" ps

# Model: llama3.1:8b (4.9 GB, 100% GPU)
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

    # 2. Archive index removed - skipping

    # 3. Create INIT_PROMPT
    init_file = INIT_CHAT_PATH / "INIT_PROMPT_NEW_CHAT.md"
    init_file.parent.mkdir(parents=True, exist_ok=True)
    init_file.write_text(INIT_PROMPT_CONTENT, encoding="utf-8")
    print(f"✅ Created: INIT_PROMPT_NEW_CHAT.md")

    # 4. Run rag_update.py --new
    print("\n🔄 Running RAG update...")
    try:
        result = subprocess.run(
            ["python", "tools/rag/rag_update.py", "--new"],
            cwd=BASE_PATH,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ RAG update complete")
        else:
            print(f"⚠️ RAG update warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️ RAG update skipped: {e}")

    print("\n" + "=" * 60)
    print("✅ New chat session ready!")
    print("=" * 60)
    print(f"\nSession: {SESSION_NAME}")
    print("\nNext: Start new Claude chat with INIT_PROMPT_NEW_CHAT.md")

if __name__ == "__main__":
    main()