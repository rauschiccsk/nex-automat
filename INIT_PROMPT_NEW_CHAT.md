# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** supplier-invoice-staging v1.0 - CONNECT TO REAL DATA
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** supplier-invoice-staging-gui-testing (2025-12-18)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #23:** RAG Workflow - Claude vypíše URL, user vloží, Claude fetchne

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### GUI Testing & Improvements
- ✅ Klávesové skratky (Enter, ESC) pre obe okná
- ✅ Modálne okno položiek faktúry
- ✅ Grid settings persistence pri zatvorení okna
- ✅ Header context menu (premenovanie stĺpcov, viditeľnosť)
- ✅ BaseGrid.create_item() - automatické formátovanie a zarovnanie
- ✅ Boolean ikony (✓/✗) s farbami
- ✅ Initial row selection a focus

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Connect to Real PostgreSQL Data
- Aplikácia pobeží na **Mágerstav serveri**
- **Lokálna PostgreSQL** databáza `invoice_staging`
- Existujúci klient: `packages/nex-shared/database/postgres_staging.py`

### Úlohy:
1. Pridať database service do supplier-invoice-staging
2. Konfigurácia pripojenia (localhost, invoice_staging)
3. Nahradiť `_load_test_data()` → query z `invoices_pending`
4. Nahradiť `_load_test_items()` → query z `invoice_items_pending`

---

## 📂 KEY PATHS

```
apps/supplier-invoice-staging/          # Main app
packages/shared-pyside6/                # Shared UI components
packages/nex-shared/database/           # PostgresStagingClient
tools/rag/rag_update.py                 # RAG workflow
```

---

## 🗄️ DATABASE INFO

**Connection:**
```python
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'invoice_staging',
    'user': 'postgres',
    'password': '<from_env_POSTGRES_PASSWORD>'
}
```

**Tables:**
- `invoices_pending` - hlavičky faktúr
- `invoice_items_pending` - položky faktúr

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**
