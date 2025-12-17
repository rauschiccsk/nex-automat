#!/usr/bin/env python
"""
New Chat Script - Creates session archive, updates index, generates init prompt.
Run after completing a session to prepare for next chat.
"""
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(r"C:\Development\nex-automat")
ARCHIVE_DIR = BASE_DIR / "docs" / "archive" / "sessions"
INIT_CHAT_DIR = BASE_DIR / "init_chat"


def create_file(path: Path, content: str) -> None:
    """Create file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ Created: {path.relative_to(BASE_DIR)}")


def update_archive_index(session_filename: str, session_title: str) -> None:
    """Update 00_ARCHIVE_INDEX.md with new session."""
    index_path = BASE_DIR / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    if not index_path.exists():
        print(f"⚠️ Archive index not found: {index_path}")
        return

    content = index_path.read_text(encoding="utf-8")

    # Find insertion point (after "## Sessions" or similar header)
    new_entry = f"- [{session_filename}](sessions/{session_filename}) - {session_title}\n"

    # Insert after first "## " section that contains "Session" or "2025"
    lines = content.split("\n")
    inserted = False
    for i, line in enumerate(lines):
        if line.startswith("## ") and "2025" in line:
            # Insert after this line
            lines.insert(i + 1, new_entry.strip())
            inserted = True
            break

    if not inserted:
        # Append to end
        lines.append(new_entry.strip())

    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Updated: docs/archive/00_ARCHIVE_INDEX.md")


def run_scripts() -> None:
    """Run generate_projects_access.py and rag_reindex.py."""
    print("\n📦 Running additional scripts...")

    # Generate projects access
    try:
        subprocess.run(
            ["python", "tools/generate_projects_access.py"],
            cwd=BASE_DIR,
            check=True
        )
        print("✅ generate_projects_access.py completed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ generate_projects_access.py failed: {e}")
    except FileNotFoundError:
        print("⚠️ generate_projects_access.py not found")

    # RAG reindex
    try:
        subprocess.run(
            ["python", "tools/rag/rag_reindex.py", "--new"],
            cwd=BASE_DIR,
            check=True
        )
        print("✅ rag_reindex.py --new completed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ rag_reindex.py failed: {e}")
    except FileNotFoundError:
        print("⚠️ rag_reindex.py not found")


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    session_name = "shared-pyside6-package-complete"
    session_filename = f"SESSION_{today}_{session_name}.md"
    session_title = "shared-pyside6 Package Implementation Complete"

    print("=" * 60)
    print("NEW CHAT - Session Closure")
    print("=" * 60)

    # === 1. Create SESSION archive ===
    session_content = f'''# SESSION: shared-pyside6 Package Implementation

**Dátum:** {today}  
**Projekt:** nex-automat  
**Úloha:** PySide6 Migration - Create shared-pyside6 package  
**Developer:** Zoltán  
**Status:** ✅ COMPLETE

---

## ✅ DOKONČENÉ V TEJTO SESSION

### 1. Package Setup (Fáza 1)
- Vytvorená štruktúra `packages/shared-pyside6/`
- pyproject.toml s dependencies (PySide6, openpyxl, asyncpg)
- README.md dokumentácia

### 2. BaseWindow (Fáza 2)
- `SettingsRepository` - SQLite persistence pre window/grid settings
- `BaseWindow(QMainWindow)` - window persistence (position, size, maximize)
- Multi-user support cez user_id parameter
- 6 testov passed

### 3. BaseGrid (Fáza 3-4)
- `GreenHeaderView` - zelené zvýraznenie aktívneho stĺpca
- `BaseGrid(QWidget)` - kompletná grid funkcionalita:
  - Column widths persistence
  - Column order (drag & drop)
  - Column visibility (show/hide)
  - Custom headers (premenovanie)
  - Row cursor memory (zapamätanie pozície podľa ID)
  - Export CSV/Excel
  - Context menu
- 9 testov passed

### 4. QuickSearch (Fáza 5)
- `text_utils` - remove_diacritics, normalize_for_search
- `QuickSearchEdit` - zelený input s keyboard navigation
- `QuickSearchContainer` - poziciovanie pod aktívnym stĺpcom
- `QuickSearchController` - search logika, diacritic-insensitive
- 11 testov passed

### 5. Dokumentácia
- PYSIDE6_MIGRATION.md aktualizovaný na v2.1
- COLLABORATION_RULES.md aktualizovaný na v1.6 (pravidlá #23, #24)

---

## 📊 ŠTATISTIKY

| Metrika | Hodnota |
|---------|---------|
| Fázy dokončené | 5/5 |
| Testy | 29 passed |
| Súbory vytvorené | 15+ |
| Odhadovaný čas | 23h |
| Skutočný čas | ~4h |

---

## 📁 VYTVORENÉ SÚBORY

```
packages/shared-pyside6/
├── pyproject.toml
├── README.md
├── shared_pyside6/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── base_window.py
│   │   ├── base_grid.py
│   │   └── quick_search.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── settings_repository.py
│   └── utils/
│       ├── __init__.py
│       └── text_utils.py
└── tests/
    ├── __init__.py
    ├── test_imports.py
    ├── test_base_window.py
    ├── test_base_grid.py
    └── test_quick_search.py
```

---

## 🔧 WORKFLOW VYLEPŠENIA

### Nové pravidlo #24: RAG Access Protocol
- Keď Claude potrebuje RAG, priamo požiada o Permission URL
- Bez zbytočného pokusu o fetch ktorý zlyhá

### Aktualizované pravidlo #20: nový chat
- 2 artifacts: new_chat.py + commit-message.txt
- Script automatizuje: SESSION, ARCHIVE_INDEX, INIT_PROMPT, scripts

---

## 🎯 NEXT SESSION PRIORITIES

### Priority #1: supplier-invoice-staging aplikácia
- Nová aplikácia od nuly s PySide6
- Použiť shared-pyside6 package
- Implementovať základné UI

### Priority #2: Integrácia QuickSearch do BaseGrid
- Automatický setup v BaseGrid.__init__
- Prepojenie s GreenHeaderView

### Priority #3: ColumnChooserDialog
- UI dialóg pre výber viditeľných stĺpcov
- Drag & drop pre poradie

---

**Token Budget:** ~88,000 / 190,000  
**Status:** ✅ SUCCESS - Package Complete
'''

    create_file(ARCHIVE_DIR / session_filename, session_content)

    # === 2. Update Archive Index ===
    update_archive_index(session_filename, session_title)

    # === 3. Create INIT_PROMPT_NEW_CHAT.md ===
    init_prompt_content = f'''# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** shared-pyside6 Package COMPLETE ✅  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** shared-pyside6 Package Complete ({today})

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
**Location:** C:\\Development\\nex-automat  
**Status:** 🟢 READY - shared-pyside6 Complete

---

**KONIEC INIT PROMPTU**
'''

    create_file(INIT_CHAT_DIR / "INIT_PROMPT_NEW_CHAT.md", init_prompt_content)

    # === 4. Run additional scripts ===
    run_scripts()

    print()
    print("=" * 60)
    print("✅ NEW CHAT preparation complete!")
    print("=" * 60)
    print()
    print("Files created:")
    print(f"  - docs/archive/sessions/{session_filename}")
    print(f"  - docs/archive/00_ARCHIVE_INDEX.md (updated)")
    print(f"  - init_chat/INIT_PROMPT_NEW_CHAT.md")
    print()
    print("Next: Review and commit changes")
    print()


if __name__ == "__main__":
    main()