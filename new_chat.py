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
import sys
import subprocess
from pathlib import Path

# =============================================================================
# CONFIG - CLAUDE DOPLNÍ TIETO PREMENNÉ
# =============================================================================

SESSION_DATE = "2025-12-22"  # YYYY-MM-DD
SESSION_NAME = "file-organization-phase-d-documentation"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# Fáza D File Mover Service & RAG Dokumentácia

**Dátum:** 2025-12-22
**Status:** ✅ DONE

---

## Dokončené úlohy

- Fáza D - received → staged (main.py úprava s move_files_to_staging)
- Fáza D - staged → archived funkcia (file_mover.py v supplier-invoice-staging)
- Fix POSTGRES_DATABASE na supplier_invoice_staging
- RAG dokumentácia - KNOWLEDGE_2025-12-22_project-structure.md
- Skutočná štruktúra projektu zdokumentovaná (04_scan_project_structure.py)
- Fáza E preskočená (migrácia bezpredmetná - čistý štart)

## Aktuálny stav

- Temporal validácia 14/14 PASSED
- n8n zastavený
- Fázy A-D DONE
- RAG dokumentácia aktuálna

## Zmenené súbory

- apps/supplier-invoice-loader/main.py - move_files_to_staging()
- apps/supplier-invoice-loader/config/config_customer.py - POSTGRES_DATABASE fix
- apps/supplier-invoice-staging/services/file_mover.py - NEW
- apps/supplier-invoice-staging/services/__init__.py - export
- docs/knowledge/KNOWLEDGE_2025-12-22_project-structure.md - NEW

## Vytvorené skripty

- 00_check_db_tables.py - diagnostika (môže byť zmazaný)
- 01_add_file_mover_to_loader.py
- 02_fix_postgres_database_name.py
- 03_add_archive_function.py
- 04_scan_project_structure.py

## Next Steps

1. Overiť vplyv DB zmien na supplier-invoice-staging GUI
2. Otestovať invoice_repository.py s novými stĺpcami
3. Deploy zmien na Mágerstav
4. E2E test - poslať faktúru cez email
"""

INIT_PROMPT = """\
INIT PROMPT - Supplier Invoice Staging Verification

Projekt: nex-automat
Current Status: Fáza D Complete, Documentation Updated
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-22

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Verify GUI compatibility with DB changes

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal validácia (14/14 XML) | ✅ PASSED |
| n8n zastavený | ✅ DONE |
| Fáza A - DB zmeny | ✅ DONE |
| Fáza B - Adresáre | ✅ DONE |
| Fáza C - Kód loader | ✅ DONE |
| Fáza D - File Mover | ✅ DONE |
| RAG dokumentácia | ✅ DONE |

## Pending Tasks

1. [ ] Overiť invoice_repository.py kompatibilitu s novými DB stĺpcami
2. [ ] Deploy na Mágerstav
3. [ ] E2E test - poslať faktúru cez email

## RAG Query

```
https://rag-api.icc.sk/search?query=invoice_repository+supplier_invoice_heads+file_status&limit=5
```

Session Priority: GUI verification → Deploy → E2E Test
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
    print(f"Base directory: {BASE_DIR}")

    # Verify we're in correct directory
    if not (BASE_DIR / "apps").exists():
        print(f"ERROR: Not in nex-automat directory!")
        print(f"   Current: {Path.cwd()}")
        print(f"   Expected: C:\\Development\\nex-automat")
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
    print(f"[OK] SESSION saved: {session_file}")

    # 2. Save KNOWLEDGE file
    knowledge_file = KNOWLEDGE_DIR / knowledge_filename
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"[OK] KNOWLEDGE saved: {knowledge_file}")

    # 3. Save INIT_PROMPT
    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"[OK] INIT_PROMPT saved: {init_file}")

    # 4. Run RAG update
    print()
    print("=" * 60)
    print("Running RAG update...")
    print("=" * 60)

    rag_script = BASE_DIR / "tools" / "rag" / "rag_update.py"
    if not rag_script.exists():
        print(f"[WARN] RAG script not found: {rag_script}")
    else:
        # Use sys.executable to ensure correct venv
        try:
            # Set UTF-8 encoding for subprocess
            env = {**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
            result = subprocess.run(
                [sys.executable, str(rag_script), "--new"],
                cwd=str(BASE_DIR),
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env
            )
            print(result.stdout)
            print("[OK] RAG updated")
        except subprocess.CalledProcessError as e:
            print(f"[WARN] RAG update failed: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            print()
            print("Run manually:")
            print(f"   python tools/rag/rag_update.py --new")

    print()
    print("=" * 60)
    print("[OK] DONE!")
    print()
    print("Next steps:")
    print(f"  1. Git commit: git add -A && git commit -m 'Session {SESSION_DATE}'")
    print(f"  2. Start new chat with INIT_PROMPT.md")
    print("=" * 60)


if __name__ == "__main__":
    main()