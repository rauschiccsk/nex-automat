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
SESSION_NAME = "temporal-phase5-deployment-complete"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# Temporal Migration Phase 5: Deployment Complete

**Dátum:** 2025-12-21
**Status:** ✅ DONE

---

## Dokončené úlohy

### 1. HTTP 401 Invalid API Key - VYRIEŠENÉ
**Root cause:** Worker posielal requesty na port 8000, kde bežal starý invoice-loader z `C:\\invoice-loader\\`, nie nový z `C:\\Deployment\\nex-automat\\`.

**Riešenie:**
- Opravený `FASTAPI_URL` v worker `.env`: 8000 → 8001
- Worker reštartovaný

### 2. Služba SupplierInvoiceLoader - OPRAVENÁ
**Root cause:** NSSM služba bola nakonfigurovaná na starý adresár `C:\\invoice-loader\\`.

**Riešenie:**
```powershell
nssm set SupplierInvoiceLoader Application "C:\\Deployment\\nex-automat\\venv32\\Scripts\\python.exe"
nssm set SupplierInvoiceLoader AppDirectory "C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader"
nssm set SupplierInvoiceLoader AppParameters "main.py"
nssm set SupplierInvoiceLoader AppStdout "C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader\\logs\\service.log"
nssm set SupplierInvoiceLoader AppStderr "C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader\\logs\\service_error.log"
```

### 3. Konfigurácia portov na Mágerstav

| Služba | Port | Aplikácia |
|--------|------|-----------|
| supplier-invoice-loader | 8001 | FastAPI Invoice API |
| Temporal Server | 7233 | Temporal gRPC |
| Temporal UI | 8233 | Web UI |

### 4. Monitoring - FUNKČNÝ

| Nástroj | URL | Stav |
|---------|-----|------|
| Invoice API Health | http://localhost:8001/health | ✅ |
| Temporal Web UI | http://localhost:8233 | ✅ |
| Workflow história | 24+ úspešných | ✅ |

### 5. SMTP Notifikácie
- Preskočené - Temporal UI stačí na sledovanie zlyhaní
- OAuth2 použité pre IMAP (nie App Password)

## Finálny stav služieb na Mágerstav

| Služba | Status |
|--------|--------|
| NEX-Temporal-Server | ✅ Running |
| NEX-Invoice-Worker | ✅ Running |
| NEX-Polling-Scheduler | ✅ Running |
| SupplierInvoiceLoader | ✅ Running (port 8001) |

## End-to-end test
```
WorkflowResult(emails_processed=1, invoices_uploaded=1, errors=[])
```
✅ **PASSED** - Faktúra úspešne spracovaná cez Temporal workflow.

## Dôležité príkazy

### Reštart služieb
```powershell
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Invoice-Worker
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Polling-Scheduler
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart SupplierInvoiceLoader
```

### Kontrola stavu
```powershell
Get-Service | Where-Object {$_.Name -like "*NEX*" -or $_.Name -like "*Invoice*" -or $_.Name -like "*Supplier*"}
```

### Manuálny test workflow
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
        id='manual-test-XXX',
        task_queue='supplier-invoice-queue'
    )
    print(f'Result: {result}')
asyncio.run(main())
"
```

## Next Steps

1. Phase 6: Migration - Parallel run s n8n, validácia, vypnutie n8n
2. Testovanie s reálnymi faktúrami v produkcii
3. Dokumentácia pre operátorov
"""

INIT_PROMPT = """\
INIT PROMPT - Temporal Migration Phase 6: Migration

Projekt: nex-automat
Current Status: Phase 5 Complete, Ready for Phase 6
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-21

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Phase 6 - Parallel run a migrácia z n8n

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal Server na Mágerstav | ✅ Running (port 7233, 8233) |
| NEX-Temporal-Server služba | ✅ Running |
| NEX-Invoice-Worker služba | ✅ Running |
| NEX-Polling-Scheduler služba | ✅ Running |
| SupplierInvoiceLoader | ✅ Running (port 8001) |
| End-to-end test | ✅ PASSED |
| Monitoring (Temporal UI) | ✅ Funkčný |

## Phase 6 Tasks

1. [ ] Parallel run - Temporal + n8n súčasne
2. [ ] Validácia výsledkov - porovnanie oboch systémov
3. [ ] Vypnutie n8n workflow
4. [ ] Cleanup starých súborov

## RAG Query

```
https://rag-api.icc.sk/search?query=n8n+workflow+migration+parallel+run&limit=5
```

Session Priority: Parallel run → Validácia → n8n vypnutie → Cleanup
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