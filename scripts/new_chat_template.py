#!/usr/bin/env python3
"""
New Chat Template - NEX Automat
===============================
TEMPLATE: Tento súbor je template. Claude doplní len premenné v sekcii CONFIG.

Použitie:
1. Claude skopíruje tento template
2. Doplní SESSION_DATE, SESSION_NAME, KNOWLEDGE_CONTENT, INIT_PROMPT
3. User uloží ako scripts/new_chat.py a spustí

Tento template NEMENÍME - je otestovaný a funkčný.
"""

import subprocess
import sys
from pathlib import Path

# =============================================================================
# CONFIG - CLAUDE DOPLNÍ TIETO PREMENNÉ
# =============================================================================

SESSION_DATE = "2025-12-20"  # YYYY-MM-DD
SESSION_NAME = "temporal-phase5-deployment"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# Session Title

**Dátum:** SESSION_DATE
**Status:** ✅ DONE / 🔄 IN PROGRESS

---

## Dokončené úlohy

- Task 1
- Task 2

## Aktuálny problém (ak existuje)

Popis problému...

## Next Steps

1. Step 1
2. Step 2

## Dôležité príkazy

```powershell
# príklad
```
"""

INIT_PROMPT = """\
INIT PROMPT - Session Title

Projekt: nex-automat
Current Status: Status description
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Focus description

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Item 1 | ✅ |

## Next Steps

1. Step 1
2. Step 2

## RAG Query

```
https://rag-api.icc.sk/search?query=relevant+search+terms&limit=5
```
"""


# =============================================================================
# TEMPLATE CODE - NEMENÍME
# =============================================================================


def get_base_dir() -> Path:
    """Získa base directory projektu."""
    # Ak sme v nex-automat adresári
    cwd = Path.cwd()
    if cwd.name == "nex-automat":
        return cwd
    # Ak sme v scripts/
    if cwd.name == "scripts" and cwd.parent.name == "nex-automat":
        return cwd.parent
    # Ak sme niekde inde, skús nájsť nex-automat
    for parent in cwd.parents:
        if parent.name == "nex-automat":
            return parent
    # Fallback na cwd
    return cwd


def main():
    print("=" * 60)
    print("NEW CHAT SCRIPT")
    print("=" * 60)

    BASE_DIR = get_base_dir()
    print(f"📁 Base directory: {BASE_DIR}")

    # Verify we're in correct directory
    if not (BASE_DIR / "apps").exists():
        print("❌ ERROR: Not in nex-automat directory!")
        print(f"   Current: {Path.cwd()}")
        print("   Expected: C:\\Development\\nex-automat")
        sys.exit(1)

    DOCS_DIR = BASE_DIR / "docs"
    KNOWLEDGE_DIR = DOCS_DIR / "knowledge" / "sessions"
    SESSION_DIR = DOCS_DIR / "sessions"

    # Ensure directories exist
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    session_filename = f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"
    knowledge_filename = f"KNOWLEDGE_{SESSION_DATE}_{SESSION_NAME}.md"

    # 1. Save SESSION file
    session_file = SESSION_DIR / session_filename
    session_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ SESSION saved: {session_file}")

    # 2. Save KNOWLEDGE file
    knowledge_file = KNOWLEDGE_DIR / knowledge_filename
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ KNOWLEDGE saved: {knowledge_file}")

    # 3. Save INIT_PROMPT
    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"✅ INIT_PROMPT saved: {init_file}")

    # 4. Run RAG update
    print()
    print("=" * 60)
    print("Running RAG update...")
    print("=" * 60)

    rag_script = BASE_DIR / "tools" / "rag" / "rag_update.py"
    if not rag_script.exists():
        print(f"⚠️ RAG script not found: {rag_script}")
    else:
        # Use main venv Python, not worker venv
        main_venv_python = BASE_DIR / "venv" / "Scripts" / "python.exe"
        if not main_venv_python.exists():
            print(f"⚠️ Main venv not found: {main_venv_python}")
            print("   Skipping RAG update. Run manually:")
            print(f"   cd {BASE_DIR}")
            print("   .\\venv\\Scripts\\Activate.ps1")
            print("   python tools/rag/rag_update.py --new")
        else:
            try:
                # Set UTF-8 encoding for subprocess
                env = {**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
                result = subprocess.run(
                    [str(main_venv_python), str(rag_script), "--new"],
                    cwd=str(BASE_DIR),
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    env=env,
                )
                print(result.stdout)
                print("✅ RAG updated")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ RAG update failed: {e}")
                if e.stdout:
                    print(f"STDOUT: {e.stdout}")
                if e.stderr:
                    print(f"STDERR: {e.stderr}")
                print()
                print("Run manually:")
                print("   .\\venv\\Scripts\\Activate.ps1")
                print("   python tools/rag/rag_update.py --new")

    print()
    print("=" * 60)
    print("✅ DONE!")
    print()
    print("Next steps:")
    print(f"  1. Git commit: git add -A && git commit -m 'Session {SESSION_DATE}'")
    print("  2. Start new chat with INIT_PROMPT.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
