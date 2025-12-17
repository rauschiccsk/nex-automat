# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** shared-pyside6 Package COMPLETE ✅  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** shared-pyside6 Package Complete (2025-12-17)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 24 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #20:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #24:** RAG Access - priamo požiadaj o Permission URL

---

## ✅ DOKONČENÉ: shared-pyside6 Package

### Package je pripravený na použitie:
```python
from shared_pyside6.ui import BaseWindow, BaseGrid, QuickSearchEdit
from shared_pyside6.database import SettingsRepository
from shared_pyside6.utils import normalize_for_search
```

### Testy: 29 passed
```powershell
cd packages/shared-pyside6
python -m pytest tests/ -v
```

### Features:
- BaseWindow - window persistence
- BaseGrid - column widths/order/visibility, custom headers, cursor memory, export
- QuickSearch - NEX Genesis style, diacritic-insensitive

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: supplier-invoice-staging aplikácia
- Nová PySide6 aplikácia od nuly
- Použiť shared-pyside6 package
- Základné UI pre staging invoices

### Priority #2: QuickSearch integrácia
- Automatický setup v BaseGrid
- Prepojenie s GreenHeaderView

---

## 📂 PROJECT STRUCTURE

```
packages/
├── nex-shared/              # PyQt5 (legacy)
└── shared-pyside6/          # PySide6 (NEW ✅)
    ├── shared_pyside6/
    │   ├── ui/              # BaseWindow, BaseGrid, QuickSearch
    │   ├── database/        # SettingsRepository
    │   └── utils/           # text_utils
    └── tests/               # 29 tests
```

---

## 🔍 RAG ACCESS

Keď potrebuješ info z RAG, priamo požiadaj o Permission URL:
```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat  
**Status:** 🟢 READY - shared-pyside6 Complete

---

**KONIEC INIT PROMPTU**
