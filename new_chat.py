"""
New Chat Script - Creates session archive, updates index, generates init prompt
Run from: C:/Development/nex-automat
"""
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("C:/Development/nex-automat")
ARCHIVE_DIR = PROJECT_ROOT / "docs/archive/sessions"
ARCHIVE_INDEX = PROJECT_ROOT / "docs/archive/00_ARCHIVE_INDEX.md"
INIT_PROMPT_PATH = PROJECT_ROOT / "INIT_PROMPT_NEW_CHAT.md"

SESSION_NAME = "supplier-invoice-staging-app-created"
SESSION_DATE = datetime.now().strftime("%Y-%m-%d")
SESSION_FILENAME = f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"

# =============================================================================
# SESSION CONTENT
# =============================================================================
SESSION_CONTENT = f"""# Session: {SESSION_NAME}
**Date:** {SESSION_DATE}
**Status:** COMPLETE

---

## Summary

Vytvorenie novej PySide6 aplikacie **supplier-invoice-staging** od nuly s pouzitim shared-pyside6 package.

---

## Completed

### 1. Database Schema
- Nova PostgreSQL databaza `supplier_invoice_staging`
- Tabulky: `invoices` (hlavicky), `invoice_items` (polozky)
- Triggery pre auto-update timestamp a vypocet predajnej ceny z marze
- View `v_invoice_summary` pre GUI

### 2. Application Structure
```
apps/supplier-invoice-staging/
├── app.py                      # Entry point
├── config/
│   ├── settings.py             # Configuration (DB, defaults)
│   └── config.yaml             # YAML config
├── database/
│   └── schemas/
│       └── 001_staging_schema.sql
├── ui/
│   ├── main_window.py          # Invoice list (hlavne okno)
│   └── invoice_items_window.py # Items (samostatne okno)
└── data/
    └── settings.db             # Grid/window persistence
```

### 3. Features Implemented
- **MainWindow**: Zoznam faktur s QuickSearch
- **InvoiceItemsWindow**: Samostatne okno pre polozky (otvorenie dvojklikom/Enter)
- **QuickSearch integration**: Editor pod aktivnym stlpcom, sipky menia stlpec
- **BaseGrid**: Column persistence (sirky, poradie), GreenHeaderView
- **BaseWindow**: Window position/size persistence
- **Editable cells**: Marza % a PC - vzajomny prepocet

### 4. Scripts Created
- `01_create_app_structure.py` - Zakladna struktura
- `02_fix_and_add_schema.py` - DB schema
- `03_recreate_schema.py` - Oprava encoding
- `04_create_app_files.py` - Vsetky Python subory
- `05_fix_main_window.py` - BaseWindow API fix
- `06_fix_widgets.py` - QuickSearchEdit API fix
- `07_fix_widgets_with_model.py` - QStandardItemModel
- `08_refactor_to_separate_windows.py` - Oddelene okna
- `09_add_quicksearch_to_grids.py` - QuickSearch integration

---

## Technical Notes

### BaseGrid API (shared-pyside6)
```python
BaseGrid(window_name, grid_name, user_id, auto_load, parent)
# Attributes: table_view, header (GreenHeaderView)
# Methods: apply_model_and_load_settings()
# Signals: row_selected, row_activated
```

### QuickSearch Components
- `QuickSearchContainer` - pozicionuje editor pod aktivny stlpec
- `QuickSearchController` - search logika, klavesove skratky
- Integration: rucne v okne, nie automaticky v BaseGrid

### Database
- Name: `supplier_invoice_staging`
- Tables: `invoices`, `invoice_items`
- xml_* fields: immutable data from XML
- margin_percent, selling_price_*: editable

---

## Next Steps

1. **Connect to database** - nacitanie realnych dat z PostgreSQL
2. **Test QuickSearch** - overit vsetky funkcie
3. **Color coding** - farebne rozlisenie matched/unmatched
4. **Save functionality** - ulozenie zmien do DB
5. **Import XML** - import faktur z ISDOC/XML

---

## Related Documents
- `docs/architecture/database/accounting/tables/ISH-supplier_invoice_heads.md`
- `docs/architecture/database/accounting/tables/ISI-supplier_invoice_items.md`
- `packages/shared-pyside6/` - PySide6 shared components

---

**End of session**
"""

# =============================================================================
# INIT PROMPT CONTENT
# =============================================================================
INIT_PROMPT_CONTENT = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat
**Current Status:** supplier-invoice-staging App CREATED
**Developer:** Zoltan (40 rokov skusenosti)
**Jazyk:** Slovencina
**Previous Session:** {SESSION_NAME} ({SESSION_DATE})

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
**Location:** C:\\Development\\nex-automat
**Status:** READY - Testing Phase

---

**KONIEC INIT PROMPTU**
"""


# =============================================================================
# MAIN
# =============================================================================
def main():
    # 1. Create session file
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    session_path = ARCHIVE_DIR / SESSION_FILENAME
    session_path.write_text(SESSION_CONTENT, encoding="utf-8")
    print(f"[SESSION] {session_path}")

    # 2. Update archive index
    if ARCHIVE_INDEX.exists():
        index_content = ARCHIVE_INDEX.read_text(encoding="utf-8")
        # Find insertion point (after header, before first entry)
        new_entry = f"| {SESSION_DATE} | [{SESSION_NAME}](sessions/{SESSION_FILENAME}) | supplier-invoice-staging app created |"

        if new_entry not in index_content:
            # Insert after table header
            lines = index_content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("|---"):
                    lines.insert(i + 1, new_entry)
                    break
            ARCHIVE_INDEX.write_text("\n".join(lines), encoding="utf-8")
            print(f"[INDEX] Updated {ARCHIVE_INDEX}")

    # 3. Create init prompt
    INIT_PROMPT_PATH.write_text(INIT_PROMPT_CONTENT, encoding="utf-8")
    print(f"[INIT] {INIT_PROMPT_PATH}")

    # 4. Run generate_projects_access.py if exists
    gen_script = PROJECT_ROOT / "tools/rag/generate_projects_access.py"
    if gen_script.exists():
        print("[RAG] Running generate_projects_access.py...")
        subprocess.run(["python", str(gen_script)], cwd=PROJECT_ROOT)

    # 5. Run rag_reindex.py --new if exists
    reindex_script = PROJECT_ROOT / "tools/rag/rag_reindex.py"
    if reindex_script.exists():
        print("[RAG] Running rag_reindex.py --new...")
        subprocess.run(["python", str(reindex_script), "--new"], cwd=PROJECT_ROOT)

    print("\n" + "=" * 50)
    print("DONE! Ready for new chat.")
    print("=" * 50)


if __name__ == "__main__":
    main()