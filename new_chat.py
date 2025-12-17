#!/usr/bin/env python3
"""
New Chat Setup Script
Creates session archive, updates index, generates init prompt, and runs RAG reindex.

Usage:
    python new_chat.py

Location: Run from project root (C:\Development\nex-automat)
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent if Path(__file__).parent.name != "scripts" else Path(__file__).parent.parent
PYTHON = sys.executable  # Use same Python as current script


def main():
    print("=" * 60)
    print("NEW CHAT SETUP")
    print("=" * 60)
    print()

    # === 1. CREATE SESSION ARCHIVE ===
    session_date = datetime.now().strftime("%Y-%m-%d")
    session_name = "md-old-cleanup-rag-optimization"
    session_filename = f"SESSION_{session_date}_{session_name}.md"
    session_path = PROJECT_ROOT / "docs" / "archive" / "sessions" / session_filename

    session_content = f"""# Session: .md-old Cleanup & RAG Optimization

**Date:** {session_date}
**Focus:** Documentation cleanup, RAG workflow optimization, project maintenance
**Status:** IN PROGRESS

---

## Completed This Session

### 1. RAG Workflow Optimization
- ✅ Created unified `tools/rag/rag_update.py` script
- ✅ Combined generate_code_docs.py + rag_reindex.py + cleanup into single command
- ✅ `--new` flag processes only files modified TODAY
- ✅ `--all` flag does full reindex
- ✅ `--stats` shows RAG statistics
- ✅ Updated memory rule #22 for new workflow

### 2. Scripts Cleanup
- ✅ Analyzed 50+ scripts in scripts/ folder
- ✅ Created cleanup script to remove obsolete scripts
- ✅ Removed ~40 old session/diagnostic/test scripts
- ✅ Kept ~10 useful utility scripts
- ✅ Created scripts/README.md documentation

### 3. Index Files Removal
- ✅ Removed 15 obsolete `00_*_INDEX.md` files
- ✅ RAG replaces manual index maintenance

### 4. Memory Rules Optimization
- ✅ Removed rule #14 (manifest generation - obsolete)
- ✅ Updated rule #22 (RAG maintenance - new rag_update.py)
- ✅ Current: 23 active rules

### 5. .md-old Files Analysis (IN PROGRESS)
- ✅ Fixed venv32/.pytest_cache .md-old files (renamed back to .md)
- ✅ Analyzed deployment docs - most covered by new documentation
- ✅ DELETED: DEPLOYMENT_CHECKLIST.md-old (covered by existing docs)
- ✅ DELETED: INSTALL_CUSTOMER.md-old (covered by DEPLOYMENT_GUIDE.md)
- ✅ DELETED: WINDOWS_SERVICE_GUIDE.md-old (covered by SERVICE_MANAGEMENT.md)
- ✅ DELETED: N8N_WORKFLOW_SETUP.md-old (obsolete - switching to Temporal)
- ✅ DELETED: USER_GUIDE.md-old (have USER_GUIDE_TEMPLATE.md)
- ✅ MOVED: RELEASE_NOTES_v2.0.0.md-old → docs/archive/releases/
- ✅ MOVED: TROUBLESHOOTING.md-old → docs/operations/TROUBLESHOOTING.md
- ⏳ ~25 README.md-old files remaining (mostly placeholders)

---

## Files Created/Modified

### New Files
- `tools/rag/rag_update.py` - Unified RAG workflow
- `scripts/README.md` - Scripts documentation
- `docs/archive/releases/RELEASE_NOTES_v2.0.0.md` - Preserved release notes
- `docs/operations/TROUBLESHOOTING.md` - Comprehensive troubleshooting guide

### Deleted Files
- 15x `00_*_INDEX.md` files
- ~40 obsolete scripts
- Multiple .md-old deployment docs

---

## Next Steps (Next Session)

### Priority #1: Complete .md-old Cleanup
- Analyze remaining ~25 README.md-old files
- Most are likely empty placeholders → delete
- Create bulk cleanup script if needed

### Priority #2: supplier-invoice-staging Application
- New PySide6 application from scratch
- Use shared-pyside6 package
- Basic UI for staging invoices

### Priority #3: QuickSearch Integration
- Automatic setup in BaseGrid
- Connect with GreenHeaderView

---

## Technical Notes

### RAG Update Commands
```powershell
# Daily - files modified today
python tools/rag/rag_update.py --new

# Weekly - full reindex
python tools/rag/rag_update.py --all

# Check statistics
python tools/rag/rag_update.py --stats
```

### Memory Rules Count: 23

---

**Session Duration:** ~2 hours
**Token Usage:** ~82,000/190,000
"""

    session_path.parent.mkdir(parents=True, exist_ok=True)
    session_path.write_text(session_content, encoding='utf-8')
    print(f"✓ Created: {session_path.name}")

    # === 2. UPDATE ARCHIVE INDEX ===
    archive_index_path = PROJECT_ROOT / "docs" / "archive" / "00_ARCHIVE_INDEX.md"
    if archive_index_path.exists():
        content = archive_index_path.read_text(encoding='utf-8')
        new_entry = f"- [{session_date}] [{session_name}](sessions/{session_filename}) - .md-old cleanup, RAG optimization"

        # Find sessions section and add entry
        if "## Sessions" in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() == "## Sessions":
                    # Insert after the header
                    lines.insert(i + 2, new_entry)
                    break
            content = '\n'.join(lines)
            archive_index_path.write_text(content, encoding='utf-8')
            print(f"✓ Updated: 00_ARCHIVE_INDEX.md")

    # === 3. CREATE INIT PROMPT ===
    init_prompt_path = PROJECT_ROOT / "docs" / "INIT_PROMPT_NEW_CHAT.md"

    init_content = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** .md-old Cleanup IN PROGRESS
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** .md-old Cleanup & RAG Optimization ({session_date})

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 23 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #23:** RAG Access - priamo požiadaj o Permission URL

---

## 🔄 DOKONČENÉ TÚTO SESSION

### RAG Workflow
- ✅ `tools/rag/rag_update.py` - unified command
- ✅ `--new` = files modified today, `--all` = full reindex

### Scripts Cleanup
- ✅ ~40 obsolete scripts removed
- ✅ scripts/README.md created

### Index Files
- ✅ 15x `00_*_INDEX.md` removed (RAG replaces)

### .md-old Analysis (PARTIAL)
- ✅ Deployment docs analyzed and cleaned
- ⏳ ~25 README.md-old files remaining

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Complete .md-old Cleanup
- Analyze remaining README.md-old files
- Bulk delete empty placeholders

### Priority #2: supplier-invoice-staging Application  
- New PySide6 app using shared-pyside6 package
- Basic staging invoice UI

---

## 📂 KEY PATHS

```
tools/rag/rag_update.py          # RAG workflow
scripts/README.md                 # Scripts docs
docs/operations/TROUBLESHOOTING.md  # NEW
docs/archive/releases/            # NEW folder
packages/shared-pyside6/          # Ready ✅
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

## Remaining .md-old Files (~25)

```
README.md-old (root + apps folders)
apps/supplier-invoice-editor/*.md-old
apps/supplier-invoice-loader/*.md-old  
docs/giudes/CONTRIBUTING.md-old
packages/nexdata/README.md-old
tools/INSTALLATION_GUIDE.md-old
```

---

**Token Budget:** 190,000  
**Location:** C:\\Development\\nex-automat  
**Memory Rules:** 23 active

---

**KONIEC INIT PROMPTU**
"""

    init_prompt_path.write_text(init_content, encoding='utf-8')
    print(f"✓ Created: INIT_PROMPT_NEW_CHAT.md")

    # === 4. RUN RAG UPDATE ===
    print()
    print("Running RAG update...")

    rag_update = PROJECT_ROOT / "tools" / "rag" / "rag_update.py"
    if rag_update.exists():
        try:
            subprocess.run([PYTHON, str(rag_update), "--new"], cwd=PROJECT_ROOT, check=True)
            print("✓ rag_update.py --new completed")
        except subprocess.CalledProcessError:
            print("⚠ rag_update.py --new failed")
    else:
        print("⚠ rag_update.py not found")

    print()
    print("=" * 60)
    print("NEW CHAT SETUP COMPLETE")
    print("=" * 60)
    print()
    print("Created files:")
    print(f"  1. {session_path}")
    print(f"  2. {init_prompt_path}")
    print()
    print("Next: Create commit-message.txt and commit changes")


if __name__ == "__main__":
    main()