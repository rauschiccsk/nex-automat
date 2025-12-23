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

SESSION_DATE = "2025-12-23"  # YYYY-MM-DD
SESSION_NAME = "nex-staging-pg8000-deployment"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# Session: nex-staging pg8000 Migration & Deployment

**Dátum:** 2025-12-22 - 2025-12-23
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy ✅

1. **nex-staging package migrovaný z psycopg2 na pg8000**
   - `connection.py` - kompletne prepísaný pre pg8000 API
   - `staging_client.py` - prepísaný pre pg8000
   - `pyproject.toml` - dependency zmenená na pg8000>=1.30.0
   - Funguje vo venv32 (32-bit) aj venv64 (64-bit)

2. **Deployment na Mágerstav server**
   - Git checkout develop
   - nex-staging reinstalovaný
   - venv64 vytvorený s Python 3.12 64-bit pre GUI
   - PySide6, shared-pyside6, nex-staging nainštalované

3. **Konfigurácia opravená**
   - config_customer.py - nové cesty SUPPLIER-INVOICES/SUPPLIER-STAGING
   - main.py - StagingClient(config=pg_config) fix
   - Emoji odstránené z print statements

4. **Databáza supplier_invoice_staging vytvorená**
   - CREATE DATABASE supplier_invoice_staging
   - Schema 001_supplier_invoice_staging.sql aplikovaná

## Aktuálny problém ❌

```
[WARN] PostgreSQL staging error: list index out of range
```

Chyba v pg8000 kóde - pravdepodobne v Pg8000Cursor alebo StagingClient pri INSERT RETURNING.

## Riešenie (TODO)

Analyzovať stderr log a opraviť `list index out of range` chybu v:
- `packages/nex-staging/nex_staging/connection.py` - Pg8000Cursor.fetchone()
- `packages/nex-staging/nex_staging/staging_client.py` - insert_invoice_with_items()

## Dôležité príkazy

```powershell
# Development
cd C:\\Development\\nex-automat
python scripts/0X_fix_script.py
git add . && git commit -m "message" && git push

# Server Mágerstav
cd C:\\Deployment\\nex-automat
git pull
Stop-Service NEXAutomat
Start-Service NEXAutomat

# Logy
Get-Content C:\\Deployment\\nex-automat\\logs\\service-stdout.log -Tail 30
Get-Content C:\\Deployment\\nex-automat\\logs\\service-stderr.log -Tail 50

# GUI test
C:\\Deployment\\nex-automat\\venv64\\Scripts\\python.exe "C:\\Deployment\\nex-automat\\apps\\supplier-invoice-staging\\app.py"
```

## Štruktúra nex-staging

```
packages/nex-staging/
├── nex_staging/
│   ├── __init__.py
│   ├── connection.py        # pg8000 DatabaseConnection + Pg8000Cursor
│   ├── staging_client.py    # INSERT operácie
│   ├── models/
│   │   ├── invoice_head.py
│   │   └── invoice_item.py
│   └── repositories/
│       └── invoice_repository.py
└── pyproject.toml           # pg8000>=1.30.0
```
"""

INIT_PROMPT = """\
INIT PROMPT - Fix pg8000 list index out of range

Projekt: nex-automat
Current Status: pg8000 INSERT RETURNING zlyhá
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Opraviť "list index out of range" chybu v pg8000 kóde

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| nex-staging pg8000 migrácia | ✅ DONE |
| Deployment Mágerstav | ✅ DONE |
| config_customer.py cesty | ✅ DONE |
| DB supplier_invoice_staging | ✅ DONE |
| E2E test | ❌ FAIL - list index out of range |

## Problém

```
[WARN] PostgreSQL staging error: list index out of range
```

Chyba nastáva pri INSERT RETURNING v StagingClient.insert_invoice_with_items()

## Pravdepodobná príčina

V `connection.py` Pg8000Cursor.fetchone():
```python
def fetchone(self):
    if self._row_index >= len(self._rows):
        return None
    row = self._rows[self._row_index]  # <- možno prázdne self._rows
```

## Next Steps

1. [ ] Pozrieť stderr log na serveri pre full traceback
2. [ ] Analyzovať Pg8000Cursor implementáciu
3. [ ] Opraviť fetchone() pre RETURNING queries
4. [ ] Test na Development
5. [ ] Deploy a E2E test

## RAG Query

```
https://rag-api.icc.sk/search?query=nex-staging+connection+Pg8000Cursor+fetchone&limit=5
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
    print(f"SESSION saved: {session_file}")

    # 2. Save KNOWLEDGE file
    knowledge_file = KNOWLEDGE_DIR / knowledge_filename
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"KNOWLEDGE saved: {knowledge_file}")

    # 3. Save INIT_PROMPT
    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"INIT_PROMPT saved: {init_file}")

    # 4. Run RAG update
    print()
    print("=" * 60)
    print("Running RAG update...")
    print("=" * 60)

    rag_script = BASE_DIR / "tools" / "rag" / "rag_update.py"
    if not rag_script.exists():
        print(f"RAG script not found: {rag_script}")
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
            print("RAG updated")
        except subprocess.CalledProcessError as e:
            print(f"RAG update failed: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            print()
            print("Run manually:")
            print(f"   python tools/rag/rag_update.py --new")

    print()
    print("=" * 60)
    print("DONE!")
    print()
    print("Next steps:")
    print(f"  1. Git commit: git add -A && git commit -m 'Session {SESSION_DATE}'")
    print(f"  2. Start new chat with INIT_PROMPT.md")
    print("=" * 60)


if __name__ == "__main__":
    main()