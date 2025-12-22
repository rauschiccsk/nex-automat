#!/usr/bin/env python3
"""
New Chat Template - NEX Automat
===============================
"""
import sys
import subprocess
from pathlib import Path

# =============================================================================
# CONFIG - CLAUDE DOPLNÍ TIETO PREMENNÉ
# =============================================================================

SESSION_DATE = "2025-12-22"
SESSION_NAME = "nex-staging-package-migration"

KNOWLEDGE_CONTENT = """\
# Session: nex-staging Package Migration

**Dátum:** 2025-12-22
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy ✅

1. **Package nex-staging vytvorený** (packages/nex-staging/)
   - `connection.py` - DatabaseConnection manager
   - `models/invoice_head.py` - Pydantic model (41 stĺpcov)
   - `models/invoice_item.py` - Pydantic model
   - `repositories/invoice_repository.py` - SELECT operácie
   - `staging_client.py` - INSERT operácie (nahrada PostgresStagingClient)

2. **supplier-invoice-staging migrovaný**
   - Import z nex_staging namiesto database.repositories
   - GUI otestované - funguje ✅

3. **supplier-invoice-loader aktualizovaný**
   - Import zmenený: `from nex_staging import StagingClient`
   - PostgresStagingClient -> StagingClient

4. **nex-shared vyčistený**
   - postgres_staging.py odstránený
   - PostgresStagingClient export odstránený

## Aktuálny problém ❌

- supplier-invoice-loader používa venv32 (32-bit pre Btrieve)
- pip install nex-staging vo venv32 zlyháva (psycopg2-binary problém)

## Riešenie

- Použiť pg8000 namiesto psycopg2 vo venv32
- Alebo: nex-staging podporuje oba drivery

## Štruktúra nex-staging

```
packages/nex-staging/
├── nex_staging/
│   ├── __init__.py
│   ├── connection.py
│   ├── staging_client.py      # INSERT operácie
│   ├── models/
│   │   ├── invoice_head.py
│   │   └── invoice_item.py
│   └── repositories/
│       └── invoice_repository.py  # SELECT operácie
└── pyproject.toml
```

## Databáza

- **Správna DB:** supplier_invoice_staging
- **Správne tabuľky:** supplier_invoice_heads, supplier_invoice_items
- **Staré (VYMAZAŤ):** invoices_pending, invoice_items_pending, invoice_staging DB

## Dôležité príkazy

```powershell
# Test nex-staging
python -c "from nex_staging import StagingClient, InvoiceRepository; print('OK')"

# GUI test
cd apps/supplier-invoice-staging
python app.py

# Loader test (vo venv32)
cd apps/supplier-invoice-loader
python -c "from main import app; print('OK')"
```
"""

INIT_PROMPT = """\
INIT PROMPT - nex-staging Package Migration

Projekt: nex-automat
Current Status: Package vytvorený, loader inštalácia zlyháva
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Vyriešiť pg8000/psycopg2 kompatibilitu pre venv32

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| nex-staging package | ✅ DONE |
| supplier-invoice-staging migrácia | ✅ DONE |
| supplier-invoice-loader import update | ✅ DONE |
| nex-shared cleanup | ✅ DONE |
| Loader test vo venv32 | ❌ FAIL - psycopg2 |

## Problém

supplier-invoice-loader používa venv32 (32-bit Python pre Btrieve DLL).
psycopg2-binary nefunguje v 32-bit Python.
Loader pôvodne používal pg8000.

## Riešenie

Upraviť nex-staging aby podporoval pg8000 (už v connection.py je základ).

## Pending Tasks

1. [ ] Upraviť nex-staging pre pg8000 kompatibilitu
2. [ ] Test loader vo venv32
3. [ ] Git commit všetkých zmien
4. [ ] Deploy na Mágerstav

## RAG Query

```
https://rag-api.icc.sk/search?query=nex-staging+supplier_invoice_heads+StagingClient&limit=5
```
"""


# =============================================================================
# TEMPLATE CODE - NEMENÍME
# =============================================================================

def get_base_dir() -> Path:
    """Získa base directory projektu."""
    cwd = Path.cwd()
    if cwd.name == "nex-automat":
        return cwd
    if cwd.name == "scripts" and cwd.parent.name == "nex-automat":
        return cwd.parent
    for parent in cwd.parents:
        if parent.name == "nex-automat":
            return parent
    return cwd


def main():
    print("=" * 60)
    print("NEW CHAT SCRIPT")
    print("=" * 60)

    BASE_DIR = get_base_dir()
    print(f"📁 Base directory: {BASE_DIR}")

    if not (BASE_DIR / "apps").exists():
        print(f"❌ ERROR: Not in nex-automat directory!")
        print(f"   Current: {Path.cwd()}")
        sys.exit(1)

    DOCS_DIR = BASE_DIR / "docs"
    KNOWLEDGE_DIR = DOCS_DIR / "knowledge" / "sessions"
    SESSION_DIR = DOCS_DIR / "sessions"

    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    session_filename = f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"
    knowledge_filename = f"KNOWLEDGE_{SESSION_DATE}_{SESSION_NAME}.md"

    session_file = SESSION_DIR / session_filename
    session_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ SESSION saved: {session_file}")

    knowledge_file = KNOWLEDGE_DIR / knowledge_filename
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ KNOWLEDGE saved: {knowledge_file}")

    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"✅ INIT_PROMPT saved: {init_file}")

    print()
    print("=" * 60)
    print("Running RAG update...")
    print("=" * 60)

    rag_script = BASE_DIR / "tools" / "rag" / "rag_update.py"
    if not rag_script.exists():
        print(f"⚠️ RAG script not found: {rag_script}")
    else:
        main_venv_python = BASE_DIR / "venv" / "Scripts" / "python.exe"
        if not main_venv_python.exists():
            print(f"⚠️ Main venv not found, skipping RAG update")
        else:
            try:
                env = {**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
                result = subprocess.run(
                    [str(main_venv_python), str(rag_script), "--new"],
                    cwd=str(BASE_DIR),
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    env=env
                )
                print(result.stdout)
                print("✅ RAG updated")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ RAG update failed: {e}")

    print()
    print("=" * 60)
    print("✅ DONE!")
    print()
    print("Next steps:")
    print(f"  1. Git commit: git add -A && git commit -m 'Session {SESSION_DATE}'")
    print(f"  2. Start new chat with INIT_PROMPT.md")
    print("=" * 60)


if __name__ == "__main__":
    main()