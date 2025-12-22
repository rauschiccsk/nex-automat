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
SESSION_NAME = "temporal-phase6-validation-file-organization"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# Temporal Phase 6 Validation & File Organization System

**Dátum:** 2025-12-22
**Status:** ✅ DONE (Fázy A, B, C)

---

## Dokončené úlohy

### 1. Temporal Phase 6 - Validácia
- n8n workflow zastavený na ICC serveri
- Temporal prevzal produkciu na Mágerstav
- Validačný test: 14/14 XML súborov PASSED (100% match s n8n)
- Temporal je plne validovaný a produkčný

### 2. File Organization System - Nová architektúra
Implementovaný nový systém organizácie súborov založený na životnom cykle:

**Fáza 1 - Received:** `C:\\NEX\\IMPORT\\SUPPLIER-INVOICES\\`
**Fáza 2 - Staged:** `C:\\NEX\\IMPORT\\SUPPLIER-STAGING\\`
**Fáza 3 - Archived:** `C:\\NEX\\YEARACT\\ARCHIV\\SUPPLIER-INVOICES\\PDF|XML\\`

### 3. Implementované fázy

| Fáza | Úloha | Status |
|------|-------|--------|
| A | Databázové zmeny (file_basename, file_status, nex_*_doc_id) | ✅ DONE |
| B | Vytvorenie adresárovej štruktúry | ✅ DONE |
| C | Úprava SupplierInvoiceLoader kódu | ✅ DONE |
| D | File Mover Service | ⏳ TODO |
| E | Migrácia existujúcich súborov | ⏳ TODO |

### 4. Databázové zmeny (supplier_invoice_heads)

Nové stĺpce:
- `file_basename` VARCHAR(100) - názov súboru bez ext
- `file_status` VARCHAR(20) - received/staged/archived
- `nex_invoice_doc_id` VARCHAR(20) - číslo faktúry v NEX
- `nex_delivery_doc_id` VARCHAR(20) - číslo DL v NEX

### 5. Konvencia pomenovania súborov

**Fáza 1-2:** `{timestamp}_{invoice_number}.pdf|xml`
Príklad: `20251222_125701_32506183.pdf`

**Fáza 3:** `{DF_number}-{DD_number}.pdf|xml`
Príklad: `DF2500100123-DD2500100205.pdf`

## Dôležité súbory

- `apps/supplier-invoice-loader/config/config_customer.py` - nové cesty
- `apps/supplier-invoice-loader/main.py` - file_basename logika
- `apps/supplier-invoice-loader/database/migrations/003_add_file_tracking_columns.sql`
- `docs/knowledge/KNOWLEDGE_2025-12-22_file-organization-system.md`

## Next Steps

1. Fáza D: File Mover Service (presun súborov medzi fázami)
2. Fáza E: Migrácia existujúcich súborov z LS/PDF a LS/XML
3. Otestovať SupplierInvoiceLoader s novými cestami
4. Cleanup n8n workflow súborov
"""

INIT_PROMPT = """\
INIT PROMPT - File Mover Service Implementation

Projekt: nex-automat
Current Status: Phase 6 Complete, File Organization Fázy A-C Done
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-22

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Fáza D - File Mover Service

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal validácia (14/14 XML) | ✅ PASSED |
| n8n zastavený | ✅ DONE |
| Temporal produkcia | ✅ Running |
| Fáza A - DB zmeny | ✅ DONE |
| Fáza B - Adresáre | ✅ DONE |
| Fáza C - Kód loader | ✅ DONE |

## Nová adresárová štruktúra

```
C:\\NEX\\IMPORT\\SUPPLIER-INVOICES\\  <- received
C:\\NEX\\IMPORT\\SUPPLIER-STAGING\\   <- staged
C:\\NEX\\YEARACT\\ARCHIV\\SUPPLIER-INVOICES\\PDF|XML\\  <- archived
```

## Fáza D Tasks

1. [ ] Vytvoriť File Mover Service
2. [ ] Presun received → staged (po PostgreSQL uložení)
3. [ ] Presun staged → archived (po NEX Genesis importe)
4. [ ] Premenovanie na finálny názov pri archivácii

## Fáza E Tasks

1. [ ] Migračný skript pre existujúce súbory z LS/PDF a LS/XML

## RAG Query

```
https://rag-api.icc.sk/search?query=file+mover+service+staging+archive&limit=5
```

Session Priority: File Mover Service → Migrácia → Testovanie
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