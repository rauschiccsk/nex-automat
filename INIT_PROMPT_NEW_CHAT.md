# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat
**Current Status:** supplier-invoice-staging App CREATED
**Developer:** Zoltan (40 rokov skusenosti)
**Jazyk:** Slovencina
**Previous Session:** supplier-invoice-staging-app-created (2025-12-17)

---

## KRITICKE: COLLABORATION RULES

**MUSIS dodrzovat 24 pravidiel z memory_user_edits!**

Klucove pravidla:
- **Rule #7:** CRITICAL artifacts pre vsetky dokumenty/kod
- **Rule #8:** Step-by-step, confirmation pred pokracovanim
- **Rule #5:** Slovak language, presna terminologia projektov
- **Rule #20:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #24:** RAG Access - priamo poziadaj o Permission URL

---

## DOKONCENE: supplier-invoice-staging App

### Aplikacia je pripravena na testovanie:
```powershell
cd apps/supplier-invoice-staging
python app.py
```

### Features:
- MainWindow - zoznam faktur s QuickSearch
- InvoiceItemsWindow - polozky v samostatnom okne (dvojklik/Enter)
- QuickSearch pod aktivnym stlpcom (sipky menia stlpec)
- BaseGrid - column persistence, GreenHeaderView
- Editable margin/selling price s prepoctom

### Database:
- PostgreSQL: `supplier_invoice_staging`
- Tables: `invoices`, `invoice_items`
- Triggers pre auto-vypocet cien

---

## IMMEDIATE NEXT STEPS

### Priority #1: Testovanie QuickSearch
- Overit vsetky funkcie (sipky, vyhladavanie, beep)
- Testovat column persistence

### Priority #2: Connect to Database
- Nacitanie realnych faktur z PostgreSQL
- Repository pattern pre CRUD operacie

### Priority #3: Color Coding
- Farebne rozlisenie matched/unmatched poloziek
- Zelena = matched, cervena = unmatched

---

## PROJECT STRUCTURE

```
apps/supplier-invoice-staging/
├── app.py
├── config/settings.py, config.yaml
├── database/schemas/001_staging_schema.sql
├── ui/main_window.py, invoice_items_window.py
└── data/settings.db

packages/shared-pyside6/
├── ui/base_window.py, base_grid.py, quick_search.py
├── database/settings_repository.py
└── utils/text_utils.py
```

---

## RAG ACCESS

Ked potrebujes info z RAG, priamo poziadaj o Permission URL:
```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

**Token Budget:** 190,000
**Location:** C:\Development\nex-automat
**Status:** READY - Testing Phase

---

**KONIEC INIT PROMPTU**
