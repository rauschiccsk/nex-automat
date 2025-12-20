# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** Temporal Migration - Phase 1 Setup
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-telegram-temporal-docs (2025-12-20)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = spustiť `python new_chat.py`
- **Rule #23:** RAG Workflow - Claude vypíše URL, user vloží, Claude fetchne

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### NEX Brain Telegram Bot - COMPLETE
- ✅ Telegram bot funguje
- ✅ RAG integrácia
- ✅ Multi-tenant (/tenant)
- ✅ UI rozhodnutie zdokumentované

### Temporal Migration Docs - COMPLETE
- ✅ Kompletný migračný dokument
- ✅ Python kód pre všetky komponenty
- ✅ Windows Services setup
- ✅ Zaindexované v RAG

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Temporal Setup (Phase 1)
1. Inštalácia Temporal Server na Windows (Go binary)
2. Konfigurácia PostgreSQL pre Temporal persistence
3. Vytvorenie `apps/temporal-invoice-worker/` štruktúry
4. Python dependencies

### Priority #2: Core Activities (Phase 2)
1. email_activities.py - IMAP polling
2. invoice_activities.py - FastAPI calls
3. notification_activities.py - SMTP

---

## 📂 KEY PATHS

```
apps/temporal-invoice-worker/          # NOVÝ - vytvoríme
├── activities/
├── workflows/
├── workers/
├── scheduler/
├── config/
└── tests/

docs/knowledge/strategic/
└── N8N_TO_TEMPORAL_MIGRATION.md      # Kompletný plán
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=temporal+migration+workflow&limit=10
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**
