"""
New Chat - Create session archive and init prompt for next session.
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")
ARCHIVE_DIR = PROJECT_ROOT / "docs" / "archive" / "sessions"
KNOWLEDGE_DIR = PROJECT_ROOT / "docs" / "knowledge"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

SESSION_NAME = "nex-brain-tenant-filtering"
SESSION_DATE = datetime.now().strftime("%Y-%m-%d")

# =============================================================================
# SESSION CONTENT
# =============================================================================

SESSION_CONTENT = f"""# Session: NEX Brain Tenant Filtering

**Dátum:** {SESSION_DATE}
**Projekt:** nex-automat
**Fokus:** Knowledge Base - Tenant Filtering Implementation

---

## DOKONČENÉ V TEJTO SESSION

### 1. .env Configuration
- ✅ `apps/nex-brain/.env` vytvorený
- ✅ `apps/nex-brain/.gitignore` vytvorený
- Multi-tenant konfigurácia (MODE, TENANTS, RAG_API_URL, OLLAMA_*)

### 2. RAG Tenant Filtering
- ✅ `tools/rag/hybrid_search.py` - tenant filter v SQL query
- ✅ `tools/rag/api.py` - tenant parameter pass-through
- ✅ `tools/rag/server_app.py` - `?tenant=` endpoint parameter
- Filter logika: `metadata->>'tenant' = $tenant OR metadata->>'tenant' IS NULL`

### 3. NEX Brain Integration
- ✅ `apps/nex-brain/api/services/rag_service.py` - posiela tenant do RAG API

### 4. Knowledge Base Structure
- ✅ Vytvorená štruktúra:
  ```
  docs/knowledge/
  ├── shared/              # Všetci tenanti
  └── tenants/
      ├── icc/             # ICC-specific
      │   ├── processes/
      │   ├── hr/
      │   └── technical/
      └── andros/          # ANDROS-specific
          ├── processes/
          ├── hr/
          └── technical/
  ```

### 5. Tenant Detection v Indexeri
- ✅ `tools/rag/indexer.py` - `detect_tenant()` funkcia
- Automaticky pridáva `tenant` do metadata podľa cesty súboru

### 6. Testing & Cleanup
- ✅ End-to-end test tenant filtering - PASSED
- ✅ Duplikáty v DB vyčistené (137 docs, 517 chunks)

---

## SCRIPTS VYTVORENÉ

1. `01_create_env_file.py` - .env pre nex-brain
2. `02_add_tenant_filtering.py` - RAG API tenant filter
3. `03_fix_rag_service_tenant.py` - NEX Brain tenant pass-through
4. `04_create_tenant_knowledge_structure.py` - adresárová štruktúra
5. `05_add_tenant_indexer.py` - tenant detection v indexeri
6. `06_test_tenant_filtering.py` - E2E test
7. `07_cleanup_duplicates.py` - cleanup DB duplikátov

---

## TECHNICKÉ POZNÁMKY

### Tenant Filtering Logic
```sql
-- Documents with matching tenant OR no tenant (shared)
WHERE (d.metadata->>'tenant' = $tenant OR d.metadata->>'tenant' IS NULL)
```

### RAG API Usage
```
/search?query=...&tenant=icc      # ICC only + shared
/search?query=...&tenant=andros   # ANDROS only + shared
/search?query=...                 # All documents
```

### Test Documents Created
- `docs/knowledge/tenants/icc/hr/ICC_INTERNE_PROCESY.md`
- `docs/knowledge/tenants/andros/hr/ANDROS_INTERNE_PROCESY.md`
- `docs/knowledge/shared/BOZP_PRAVIDLA.md`

---

## NEXT STEPS

### Immediate
1. Git commit všetkých zmien
2. Zmazať dočasné scripty (01-07)

### Fáza 2 Continued
- Pridať reálne dokumenty pre ICC
- Pridať reálne dokumenty pre ANDROS
- Otestovať NEX Brain s tenant-specific responses

### Fáza 3: NEX Genesis Integration
- Connector pre ERP dáta
- Live queries

---

**Session Status:** ✅ COMPLETE
**Token Usage:** ~63,000 / 190,000 (33%)
"""

# =============================================================================
# KNOWLEDGE CONTENT (for RAG indexing)
# =============================================================================

KNOWLEDGE_CONTENT = f"""# NEX Brain - Tenant Filtering

**Aktualizované:** {SESSION_DATE}
**Kategória:** Technical Documentation

---

## Overview

NEX Brain podporuje multi-tenant architektúru s tenant-specific knowledge base.

## Tenant Filtering

### RAG API
```
/search?query=...&tenant=icc      # ICC documents + shared
/search?query=...&tenant=andros   # ANDROS documents + shared  
/search?query=...                 # All documents
```

### Knowledge Base Structure
```
docs/knowledge/
├── shared/           # Available to all tenants
└── tenants/
    ├── icc/          # ICC-specific (tenant='icc' in metadata)
    └── andros/       # ANDROS-specific (tenant='andros' in metadata)
```

### Automatic Tenant Detection
Indexer automatically detects tenant from file path:
- `docs/knowledge/tenants/icc/*` → tenant='icc'
- `docs/knowledge/tenants/andros/*` → tenant='andros'
- Other paths → no tenant (shared)

## Configuration

### .env file (apps/nex-brain/.env)
```env
MODE=multi-tenant
TENANTS=icc,andros
RAG_API_URL=https://rag-api.icc.sk
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
API_PORT=8001
```

## Files Modified

- `tools/rag/hybrid_search.py` - SQL tenant filter
- `tools/rag/api.py` - tenant parameter
- `tools/rag/server_app.py` - ?tenant= endpoint
- `tools/rag/indexer.py` - detect_tenant() function
- `apps/nex-brain/api/services/rag_service.py` - tenant pass-through
"""

# =============================================================================
# INIT PROMPT
# =============================================================================

INIT_PROMPT = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** NEX Brain - Tenant Filtering Complete
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** {SESSION_NAME} ({SESSION_DATE})

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = spustiť `python new_chat.py`
- **Rule #23:** RAG Workflow - Claude vypíše URL, user vloží, Claude fetchne
- **Rule #24:** PostgreSQL password via POSTGRES_PASSWORD env variable

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### Tenant Filtering - COMPLETE
- ✅ RAG API `?tenant=` parameter
- ✅ NEX Brain tenant integration
- ✅ Knowledge base štruktúra (shared/ + tenants/icc,andros/)
- ✅ Indexer tenant detection
- ✅ E2E test PASSED
- ✅ DB cleanup (137 docs, 517 chunks)

### Kľúčové súbory
- `tools/rag/hybrid_search.py` - tenant SQL filter
- `tools/rag/indexer.py` - detect_tenant()
- `apps/nex-brain/.env` - konfigurácia

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Git Commit
- Commitnúť všetky zmeny z tenant filtering session
- Zmazať dočasné scripty (01-07)

### Priority #2: Real Knowledge Base
- Pridať reálne dokumenty pre ICC
- Pridať reálne dokumenty pre ANDROS

### Priority #3: Fáza 3 - NEX Genesis Integration
- Connector pre ERP dáta
- Live queries

---

## 📂 KEY PATHS

```
apps/nex-brain/                         # NEX Brain app
  .env                                  # Multi-tenant config
  api/services/rag_service.py           # Tenant pass-through

tools/rag/                              # RAG system
  hybrid_search.py                      # Tenant SQL filter
  indexer.py                            # detect_tenant()
  server_app.py                         # ?tenant= endpoint

docs/knowledge/                         # Knowledge base
  shared/                               # All tenants
  tenants/icc/                          # ICC only
  tenants/andros/                       # ANDROS only
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&tenant=icc
https://rag-api.icc.sk/search?query=...&tenant=andros
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat

---

**KONIEC INIT PROMPTU**
"""


def main():
    print("=" * 60)
    print("NEW CHAT - Session Archive & Init Prompt")
    print("=" * 60)

    # 1. Create session archive
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    session_file = ARCHIVE_DIR / f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"
    session_file.write_text(SESSION_CONTENT, encoding="utf-8")
    print(f"\n✅ Session archive: {session_file.name}")

    # 2. Create knowledge doc (for RAG)
    knowledge_file = KNOWLEDGE_DIR / f"KNOWLEDGE_{SESSION_DATE}_{SESSION_NAME}.md"
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ Knowledge doc: {knowledge_file.name}")

    # 3. Create init prompt
    init_file = PROJECT_ROOT / "INIT_PROMPT_NEW_CHAT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"✅ Init prompt: {init_file.name}")

    # 4. Run RAG update
    print("\n" + "-" * 60)
    print("Running RAG update (--new)...")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, "tools/rag/rag_update.py", "--new"],
        cwd=PROJECT_ROOT,
        capture_output=False
    )

    print("\n" + "=" * 60)
    print("✅ NEW CHAT READY")
    print("=" * 60)
    print(f"\nFiles created:")
    print(f"  1. {session_file}")
    print(f"  2. {knowledge_file}")
    print(f"  3. {init_file}")
    print(f"\nNext: Start new chat and paste INIT_PROMPT_NEW_CHAT.md")


if __name__ == "__main__":
    main()