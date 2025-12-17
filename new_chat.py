"""
New Chat Setup Script
Creates SESSION_*.md, updates ARCHIVE_INDEX, creates INIT_PROMPT, runs rag_update.py --new
"""
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(r"C:\Development\nex-automat")
DOCS_ARCHIVE = PROJECT_ROOT / "docs" / "archive"
SESSIONS_DIR = DOCS_ARCHIVE / "sessions"
ARCHIVE_INDEX = DOCS_ARCHIVE / "00_ARCHIVE_INDEX.md"
INIT_PROMPT_FILE = PROJECT_ROOT / "init_chat" / "INIT_PROMPT_NEW_CHAT.md"

SESSION_NAME = "supplier-invoice-staging-testing"
DATE = datetime.now().strftime("%Y-%m-%d")
SESSION_FILENAME = f"SESSION_{DATE}_{SESSION_NAME}.md"


def create_session_file():
    """Create session markdown file."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    session_content = f"""# Session: {SESSION_NAME}
**Date:** {DATE}
**Status:** COMPLETED

---

## Summary

Testing and debugging supplier-invoice-staging PySide6 application.

## Completed Tasks

### 1. QuickSearch Auto-Sort (shared-pyside6)
- Added `_sort_by_column()` method to QuickSearchController
- Grid auto-sorts when search column changes

### 2. Grid Settings Persistence (shared-pyside6)
- Fixed `_loading` flag - now True from init until `apply_model_and_load_settings()` completes
- Column widths, order, visibility now properly saved/restored

### 3. Search Column Persistence (main_window.py)
- Active search column saved to grid settings
- Restored on application startup

### 4. Column Formatting (main_window.py)
- Suma and Match% columns right-aligned
- Numeric values formatted to 2 decimal places

### 5. QuickSearch UX Improvements (shared-pyside6)
- Search text cleared when changing column with arrow keys
- Text color changed to black for readability on green background
- Column navigation uses visual order (respects drag&drop reordering)

### 6. InvoiceItemsWindow Grid Fix
- Fixed empty grid on window open - using layoutChanged signal

## Modified Files

### shared-pyside6 Package
- `packages/shared-pyside6/shared_pyside6/ui/quick_search.py`
  - Added `_sort_by_column()` 
  - Clear search on column change
  - Visual order navigation
  - Black text color
- `packages/shared-pyside6/shared_pyside6/ui/base_grid.py`
  - Fixed `_loading` flag timing

### supplier-invoice-staging App
- `apps/supplier-invoice-staging/ui/main_window.py`
  - Column formatting and alignment
  - Search column persistence
- `apps/supplier-invoice-staging/ui/invoice_items_window.py`
  - layoutChanged signal for grid refresh

## Scripts Created
- 01_fix_quick_search_sort.py
- 03_fix_save_during_init.py
- 05_fix_init_loading_flag.py
- 06_remove_debug_output.py
- 07_fix_search_column_persistence.py
- 08_fix_column_alignment_format.py
- 09_fix_clear_search_on_column_change.py
- 10_fix_search_text_color.py
- 11_fix_column_navigation_visual.py
- 13_fix_items_grid_layout_changed.py

## Next Steps
- Continue testing supplier-invoice-staging
- Connect to real database
- Implement actual invoice loading from PostgreSQL staging

---
**Session End:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

    session_path = SESSIONS_DIR / SESSION_FILENAME
    with open(session_path, 'w', encoding='utf-8') as f:
        f.write(session_content)
    print(f"✅ Created: {session_path}")
    return session_path


def update_archive_index():
    """Update archive index with new session."""
    if not ARCHIVE_INDEX.exists():
        print(f"⚠️ Archive index not found: {ARCHIVE_INDEX}")
        return

    with open(ARCHIVE_INDEX, 'r', encoding='utf-8') as f:
        content = f.read()

    new_entry = f"| {DATE} | [{SESSION_NAME}](sessions/{SESSION_FILENAME}) | supplier-invoice-staging testing, grid fixes |"

    # Find sessions table and add entry
    if "| Date | Session |" in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("| Date"):
                # Insert after header and separator
                lines.insert(i + 2, new_entry)
                break
        content = '\n'.join(lines)

        with open(ARCHIVE_INDEX, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated: {ARCHIVE_INDEX}")
    else:
        print(f"⚠️ Could not find sessions table in archive index")


def create_init_prompt():
    """Create init prompt for next chat."""
    init_content = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** supplier-invoice-staging v1.0 TESTING
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** {SESSION_NAME} ({DATE})

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
**Location:** C:\Development\\nex-automat

---

**KONIEC INIT PROMPTU**
"""

    INIT_PROMPT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INIT_PROMPT_FILE, 'w', encoding='utf-8') as f:
        f.write(init_content)
    print(f"✅ Created: {INIT_PROMPT_FILE}")


def run_rag_update():
    """Run rag_update.py --new."""
    rag_script = PROJECT_ROOT / "tools" / "rag" / "rag_update.py"
    if rag_script.exists():
        print("🔄 Running RAG update...")
        result = subprocess.run(
            ["python", str(rag_script), "--new"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ RAG update completed")
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
        else:
            print(f"⚠️ RAG update failed: {result.stderr}")
    else:
        print(f"⚠️ RAG script not found: {rag_script}")


def main():
    print("=" * 50)
    print("NEW CHAT SETUP")
    print("=" * 50)

    create_session_file()
    update_archive_index()
    create_init_prompt()
    run_rag_update()

    print("=" * 50)
    print("✅ New chat setup complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()