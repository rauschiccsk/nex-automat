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

SESSION_DATE = "2025-12-21"  # YYYY-MM-DD
SESSION_NAME = "temporal-phase5-deployment-continued"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# Temporal Phase 5 Deployment - Mágerstav Server (Session 2)

**Dátum:** 2025-12-20 - 2025-12-21
**Server:** Mágerstav (testovacie prostredie)
**Status:** 🔄 IN PROGRESS - API Key fix pending test

---

## Dokončené úlohy ✅

### 1. Temporal Server Inštalácia
- Temporal CLI 1.5.1 (Server 1.29.1, UI 2.42.1)
- Cesta: `C:\\Temporal\\cli\\temporal.exe`
- SQLite DB: `C:\\Temporal\\data\\temporal.db`
- Porty: 7233 (gRPC), 8233 (UI)

### 2. NSSM Windows Services (všetky Running)
| Služba | Popis |
|--------|-------|
| NEX-Temporal-Server | Temporal Server + UI |
| NEX-Invoice-Worker | Python 3.12 64-bit worker |
| NEX-Polling-Scheduler | Email polling každých 300s |

### 3. Worker Deployment
- ZIP prenos z Development na Mágerstav
- 64-bit Python 3.12 venv (temporalio vyžaduje 64-bit)
- Cesta: `C:\\Deployment\\nex-automat\\apps\\supplier-invoice-worker`

### 4. invoice_activities.py Fix
- Endpoint: `/invoice` (nie `/api/v1/invoice/upload`)
- Payload: JSON s `file_b64` (base64)
- Pridaný `import base64`

### 5. Gmail OAuth2
- Tokeny fungujú
- `fetch_unread_emails` nachádza emaily ✅

### 6. new_chat_template.py
- Vytvorený otestovaný template pre session management
- Cesta: `scripts/templates/new_chat_template.py`

---

## Aktuálny problém ❌

### HTTP 401 - Invalid API key

**Symptóm:**
```
errors=['...pdf: HTTP 401: {"detail":"Invalid API key"}']
```

**Root cause:**
- `supplier-invoice-loader/config/config_customer.py`:
  ```python
  API_KEY = os.getenv("LS_API_KEY", "ls-dev-key-change-in-production-2025")
  ```
- Worker `.env` mal iný kľúč

**Riešenie (aplikované, čaká test):**
- Worker `.env` zmenený na `LS_API_KEY=ls-dev-key-change-in-production-2025`
- Treba reštartovať NEX-Invoice-Worker a otestovať

---

## Next Steps

1. **Reštart a test API key fix:**
   ```powershell
   C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Invoice-Worker
   # Označ email ako neprečítaný v Gmail
   # Spusti manuálny workflow test
   ```

2. **End-to-end test** - faktúra spracovaná a uložená do DB

3. **Phase 5.2 Monitoring** - health checks, logging

---

## Dôležité cesty (Mágerstav)

| Komponenta | Cesta |
|------------|-------|
| Temporal CLI | `C:\\Temporal\\cli\\temporal.exe` |
| Temporal DB | `C:\\Temporal\\data\\temporal.db` |
| Worker | `C:\\Deployment\\nex-automat\\apps\\supplier-invoice-worker` |
| Worker venv | `...\\supplier-invoice-worker\\venv` (Python 3.12 64-bit) |
| NSSM | `C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe` |
| FastAPI | `C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader` |

## Dôležité príkazy

```powershell
# Stav služieb
Get-Service "NEX-*"

# Reštart služby
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Invoice-Worker

# Temporal UI
http://localhost:8233

# Manuálny workflow test
cd C:\\Deployment\\nex-automat\\apps\\supplier-invoice-worker
.\\venv\\Scripts\\Activate.ps1
python -c "
import asyncio
from temporalio.client import Client
from workflows.invoice_workflow import InvoiceProcessingWorkflow

async def main():
    client = await Client.connect('localhost:7233')
    result = await client.execute_workflow(
        InvoiceProcessingWorkflow.run,
        id='manual-test-XXX',
        task_queue='supplier-invoice-queue'
    )
    print(f'Result: {result}')

asyncio.run(main())
"
```
"""

INIT_PROMPT = """\
INIT PROMPT - Temporal Migration Phase 5: Deployment (CONTINUED)

Projekt: nex-automat
Current Status: API Key Fix - Ready for Test
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-20

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 IMMEDIATE NEXT STEP: Test API Key Fix

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal Server na Mágerstav | ✅ Running (port 7233, 8233) |
| NEX-Temporal-Server služba | ✅ Running |
| NEX-Invoice-Worker služba | ✅ Running |
| NEX-Polling-Scheduler služba | ✅ Running |
| invoice_activities.py fix | ✅ Deployed |
| Gmail OAuth2 | ✅ Funguje |
| Worker .env LS_API_KEY | ✅ Zmenený na správny kľúč |
| new_chat_template.py | ✅ Otestovaný |

## Aktuálny problém ❌

HTTP 401 - Invalid API key pri upload faktúry.

**Fix aplikovaný:** Worker `.env` zmenený na `LS_API_KEY=ls-dev-key-change-in-production-2025`

**TREBA:** Reštartovať službu a otestovať!

## Immediate Actions

1. Na Mágerstav serveri:
   ```powershell
   C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Invoice-Worker
   ```

2. Označ email ako neprečítaný v Gmail (`magerstavinvoice@gmail.com`)

3. Spusti test:
   ```powershell
   cd C:\\Deployment\\nex-automat\\apps\\supplier-invoice-worker
   .\\venv\\Scripts\\Activate.ps1
   python -c "
   import asyncio
   from temporalio.client import Client
   from workflows.invoice_workflow import InvoiceProcessingWorkflow
   async def main():
       client = await Client.connect('localhost:7233')
       result = await client.execute_workflow(
           InvoiceProcessingWorkflow.run,
           id='manual-test-005',
           task_queue='supplier-invoice-queue'
       )
       print(f'Result: {result}')
   asyncio.run(main())
   "
   ```

4. Očakávaný výsledok: `invoices_uploaded: 1`

## RAG Query

```
https://rag-api.icc.sk/search?query=Temporal+deployment+Magerstav+API+key+invoice&limit=5
```

Session Priority: Test API Key Fix → End-to-end faktúra → Phase 5.2 Monitoring
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
        print(f"❌ ERROR: Not in nex-automat directory!")
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
            print(f"   .\\venv\\Scripts\\Activate.ps1")
            print(f"   python tools/rag/rag_update.py --new")
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
                    env=env
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
                print(f"   .\\venv\\Scripts\\Activate.ps1")
                print(f"   python tools/rag/rag_update.py --new")

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