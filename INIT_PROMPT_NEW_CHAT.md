# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** supplier-invoice-staging - FUNCTIONAL WITH DB  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** supplier-invoice-db-integration (2025-12-18)

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

### Database Integration Complete
- ✅ PostgreSQL schéma aplikovaná (`supplier_invoice_heads`, `supplier_invoice_items`)
- ✅ `InvoiceRepository` s reálnymi queries
- ✅ GUI napojené na databázu (18 + 19 stĺpcov)
- ✅ Testovacie dáta (5 faktúr, 7 položiek)
- ✅ `settings.db` v projektovom priečinku `data/`

### DB Field Convention
- `xml_*` = z ISDOC XML (immutable)
- `nex_*` = z NEX Genesis (obohatenie)

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Product Matching Logic
- Implementovať matching podľa EAN
- Implementovať matching podľa názvu (fuzzy)
- Implementovať matching podľa seller_code

### Priority #2: Save Functionality
- Ukladanie editovaných položiek do DB
- Ukladanie match výsledkov

### Priority #3: NEX Genesis Connection
- Lookup produktov cez Btrieve
- Obohatenie položiek o NEX data

---

## 📂 KEY PATHS

```
apps/supplier-invoice-staging/          # Main app
  database/repositories/                # InvoiceRepository
  database/schemas/                     # SQL schemas
  data/settings.db                      # Grid settings (per-app)
  ui/main_window.py                     # 18 columns
  ui/invoice_items_window.py            # 19 columns

packages/shared-pyside6/                # Shared UI components
  shared_pyside6/ui/base_grid.py        # Updated with settings_db_path

docs/knowledge/specifications/          # DB schémy (pre RAG)
```

---

## 🗄️ DATABASE INFO

**Databáza:** `supplier_invoice_staging`  
**Connection:** localhost:5432, user postgres, password via POSTGRES_PASSWORD

**Tabuľky:**
- `supplier_invoice_heads` - 36 stĺpcov
- `supplier_invoice_items` - 25 stĺpcov + triggers

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

**Knowledge docs location:** `docs/knowledge/`

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**