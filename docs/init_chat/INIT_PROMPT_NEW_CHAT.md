# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** NEX Brain - Fáza 1 COMPLETE  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-foundation (2025-12-19)

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
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" ps

# Model: llama3.1:8b (4.9 GB, 100% GPU)
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**
