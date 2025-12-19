# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** NEX Brain API - FUNCTIONAL  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-api-fixes (2025-12-19)

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
cd C:\Development\nex-automat\apps\nex-brain
python -m uvicorn api.main:app --reload --port 8001

# Test
Invoke-RestMethod -Uri "http://127.0.0.1:8001/api/v1/chat" -Method POST -ContentType "application/json" -Body '{"question": "Co je NEX Brain?", "tenant": "icc"}'
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**
