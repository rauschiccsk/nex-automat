# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** supplier-invoice-staging v1.0 TESTING
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** supplier-invoice-staging-testing (2025-12-17)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #23:** RAG Access - priamo požiadaj o Permission URL

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### supplier-invoice-staging Fixes
- ✅ QuickSearch auto-sort pri zmene stĺpca
- ✅ Grid settings persistence (šírky, poradie stĺpcov)
- ✅ Search column persistence
- ✅ Numeric columns right-aligned, 2 decimal places
- ✅ Search text cleared on column change
- ✅ Visual order navigation (respects drag&drop)
- ✅ InvoiceItemsWindow grid refresh fix

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Continue supplier-invoice-staging Testing
- Test all functionality
- Fix any remaining issues

### Priority #2: Connect to Real Data
- PostgreSQL staging database connection
- Load actual invoices from staging

---

## 📂 KEY PATHS

```
apps/supplier-invoice-staging/          # Main app
packages/shared-pyside6/                # Shared UI components
tools/rag/rag_update.py                 # RAG workflow
```

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
