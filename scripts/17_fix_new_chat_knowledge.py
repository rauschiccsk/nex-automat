#!/usr/bin/env python
"""
Fix new_chat.py - Add KNOWLEDGE document creation.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/new_chat.py")

content = FILE_PATH.read_text(encoding="utf-8")

# Add KNOWLEDGE_PATH after other paths
old_paths = '''ARCHIVE_PATH = BASE_PATH / "docs" / "archive" / "sessions"
INIT_CHAT_PATH = BASE_PATH  # ROOT - INIT_PROMPT_NEW_CHAT.md in project root'''

new_paths = '''ARCHIVE_PATH = BASE_PATH / "docs" / "archive" / "sessions"
KNOWLEDGE_PATH = BASE_PATH / "docs" / "knowledge" / "development"
INIT_CHAT_PATH = BASE_PATH  # ROOT - INIT_PROMPT_NEW_CHAT.md in project root'''

content = content.replace(old_paths, new_paths)

# Find SESSION_CONTENT end and add KNOWLEDGE_CONTENT after it
# We need to add a new constant for knowledge content

# Find where SESSION_CONTENT ends (before INIT_PROMPT_CONTENT)
marker = 'INIT_PROMPT_CONTENT = f"""'

knowledge_content = '''KNOWLEDGE_CONTENT = f"""# NEX Brain API - Technical Documentation

**Dátum:** {TODAY}
**Kategória:** Development
**Status:** ✅ Complete

---

## Prehľad

Táto dokumentácia popisuje technické riešenia implementované pre NEX Brain API.

## Kľúčové komponenty

### 1. FastAPI Server
- Endpoint: `http://127.0.0.1:8001`
- Swagger UI: `/docs`
- Hlavné routes: `/api/v1/chat`, `/api/v1/tenants`, `/health`

### 2. RAG Service (`api/services/rag_service.py`)

**Boost logika pre správny chunk selection:**
- Chunks kde sekcia je na ZAČIATKU (prvých 200 znakov) dostávajú +0.8 boost
- Deduplicate vyberá chunk s najvyšším adjusted_score per súbor
- Keyword extraction z query pre lepšie matching

**Kľúčové metódy:**
- `_boost_relevant()` - pridáva boost podľa query keywords
- `_deduplicate_best()` - vyberá najlepší chunk per súbor
- `format_context()` - formátuje kontext pre LLM

### 3. LLM Service (`api/services/llm_service.py`)

**Konfigurácia pre minimálne halucinácie:**
- `temperature=0.0` (deterministické)
- `top_p=0.1` (focused)
- `num_predict=150-256` (krátke odpovede)
- Striktný system prompt

### 4. Chat Endpoint (`api/routes/chat.py`)

**Greeting detection:**
- Jednoduché pozdravy (Ahoj, Čau, Hi) - bez RAG
- ASCII patterns pre slovenské znaky
- Diacritics removal funkcia

## Riešené problémy

### RAG Chunk Selection
- **Problém:** RAG vracal zlý chunk (Dátové zdroje namiesto IMPLEMENTAČNÉ FÁZY)
- **Príčina:** Oba chunky obsahovali kľúčové slová, ale prvý mal vyšší score
- **Riešenie:** Boost +0.8 pre chunky kde sekcia je na začiatku

### LLM Halucinácie
- **Problém:** Model vymýšľal informácie (Docker, GitHub Actions)
- **Príčina:** Zlý kontext z RAG + príliš kreatívne nastavenia
- **Riešenie:** Správny chunk + temperature=0.0

---

## Použitie

```powershell
# Start server
cd C:\\Development\\nex-automat\\apps\\nex-brain
python -m uvicorn api.main:app --reload --port 8001

# Test API
Invoke-RestMethod -Uri "http://127.0.0.1:8001/api/v1/chat" -Method POST -ContentType "application/json" -Body '{{"question": "Co je NEX Brain?", "tenant": "icc"}}'
```

---

**Related:** NEX_BRAIN_PRODUCT.md, supplier-invoice-staging
"""

'''

content = content.replace(marker, knowledge_content + marker)

# Add knowledge file creation in main()
old_init_section = '''    # 2. Create INIT_PROMPT in ROOT
    init_file = INIT_CHAT_PATH / "INIT_PROMPT_NEW_CHAT.md"
    init_file.write_text(INIT_PROMPT_CONTENT, encoding="utf-8")
    print(f"✅ Created: INIT_PROMPT_NEW_CHAT.md (in ROOT)")'''

new_init_section = '''    # 2. Create KNOWLEDGE document (for RAG indexing)
    knowledge_file = KNOWLEDGE_PATH / f"{TODAY}_nex-brain-api.md"
    knowledge_file.parent.mkdir(parents=True, exist_ok=True)
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ Created: {knowledge_file.name} (in docs/knowledge/)")

    # 3. Create INIT_PROMPT in ROOT
    init_file = INIT_CHAT_PATH / "INIT_PROMPT_NEW_CHAT.md"
    init_file.write_text(INIT_PROMPT_CONTENT, encoding="utf-8")
    print(f"✅ Created: INIT_PROMPT_NEW_CHAT.md (in ROOT)")'''

content = content.replace(old_init_section, new_init_section)

# Update comment numbers
content = content.replace("# 3. Run rag_update.py", "# 4. Run rag_update.py")

FILE_PATH.write_text(content, encoding="utf-8")
print("✅ Fixed: new_chat.py")
print("   - Added KNOWLEDGE_PATH")
print("   - Added KNOWLEDGE_CONTENT")
print("   - Creates knowledge doc before RAG update")