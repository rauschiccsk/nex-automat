# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** supplier-invoice-staging - APPLY DB SCHEMA  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** rag-knowledge-system (2025-12-18)

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

### RAG Knowledge System
- ✅ Nová štruktúra `docs/knowledge/` (decisions, development, deployment, scripts, specifications)
- ✅ Upravený `rag_update.py` - indexuje knowledge docs
- ✅ Upravený `new_chat.py` - poradové čísla, knowledge docs, interaktívny vstup

### DB Schema Design
- ✅ Konvencia `xml_*` / `nex_*` prefixov
- ✅ `supplier_invoice_heads` - kompletná schéma
- ✅ `supplier_invoice_items` - kompletná schéma
- ✅ Knowledge dokument vytvorený

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Aplikovať DB schému
1. Uložiť SQL súbor: `database/schemas/supplier_invoice_staging.sql`
2. Spustiť v PostgreSQL
3. Overiť štruktúru

### Priority #2: Connect GUI to Real Data
1. Pridať `DatabaseService` do supplier-invoice-staging
2. Implementovať queries s novými `xml_*` / `nex_*` poliami
3. Nahradiť `_load_test_data()` reálnymi queries

---

## 📂 KEY PATHS

```
apps/supplier-invoice-staging/          # Main app
packages/shared-pyside6/                # Shared UI components
docs/knowledge/specifications/          # DB schémy (pre RAG)
tools/rag/rag_update.py                 # RAG workflow (v2)
new_chat.py                             # Session workflow (v2)
```

---

## 🗄️ DATABASE INFO

**Databáza:** `supplier_invoice_staging`

**Tabuľky:**
- `supplier_invoice_heads` - hlavičky faktúr
- `supplier_invoice_items` - položky faktúr

**Konvencia polí:**
- `xml_*` = z ISDOC XML (immutable)
- `nex_*` = z NEX Genesis (obohatenie)

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

**Knowledge docs location:** `docs/knowledge/`

---

## 📝 NEW CHAT WORKFLOW

Na konci session:
```powershell
python new_chat.py
```

Script sa interaktívne pýta na:
1. Session name a summary
2. Session content (paste markdown)
3. Knowledge documents (optional, multiple)
4. Init prompt content

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**