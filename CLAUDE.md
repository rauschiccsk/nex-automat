# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NEX Automat is a monorepo for the NEX Genesis Automation Platform. It handles supplier invoice processing, RAG-based knowledge management, and multi-tenant AI assistant services.

## Monorepo Structure

Uses `uv` workspace with Python 3.11+ (some apps require 3.13+):

```
apps/
├── nex-brain/              # Multi-tenant RAG + LLM API (FastAPI + Ollama)
├── supplier-invoice-loader/  # Email-to-database invoice processing (FastAPI)
├── supplier-invoice-editor/  # Desktop approval app (PyQt5)
├── supplier-invoice-staging/ # PySide6 staging desktop app
├── supplier-invoice-staging-web/ # React + Vite web frontend
├── supplier-invoice-worker/  # Temporal.io workflow orchestration

packages/
├── nexdata/               # NEX Genesis Btrieve models & utilities
├── nex-staging/           # PostgreSQL models for invoice staging
├── shared-pyside6/        # Reusable PySide6 components (BaseWindow, BaseGrid)
├── nex-shared/            # FLAT structure: packages/nex-shared/models/ (no nested nex_shared/)

tools/
├── rag/                   # RAG indexing & search tools
```

## Common Commands

### Python Apps (in app directory with venv)
```bash
# Install dependencies
pip install -e .

# Run tests
pytest

# Lint
ruff check .
black --check .
```

### RAG System
```bash
# Daily update (files modified today)
python tools/rag/rag_update.py --new

# Full reindex
python tools/rag/rag_update.py --all

# Check stats
python tools/rag/rag_update.py --stats
```

### NEX Brain API
```bash
cd apps/nex-brain
uvicorn api.main:app --host 0.0.0.0 --port 8100 --reload
```

### Web Frontend
```bash
cd apps/supplier-invoice-staging-web
npm install
npm run dev     # Development
npm run build   # Production build
npm run lint    # ESLint
```

## Architecture

### Multi-Tenant RAG System
- Database: PostgreSQL (`nex_automat_rag`) with pgvector
- Embedding: `sentence-transformers/all-MiniLM-L6-v2` (384 dims)
- Tenants: ICC, ANDROS, UAE - each has isolated document space
- Documents for RAG indexing go to `docs/knowledge/` only

### Invoice Processing Pipeline
1. `supplier-invoice-loader` - Receives emails, extracts PDFs, OCR
2. `supplier-invoice-worker` - Temporal workflows for processing
3. `supplier-invoice-staging` / `supplier-invoice-staging-web` - Review UI
4. `supplier-invoice-editor` - Final approval (PyQt5)

### Shared Packages
- `nexdata`: Btrieve client, models (TSH, TSI, PAB, MGLST, Barcode, GScat)
- `nex-staging`: PostgreSQL connection, InvoiceHead/InvoiceItem models
- `shared-pyside6`: BaseWindow (persistence), BaseGrid (columns, export), QuickSearch

## Code Style

- Line length: 100
- Python target: 3.11+ (3.13+ for supplier-invoice-editor)
- Formatters: Black, Ruff
- Type hints required

## Key Configuration Files

- `config/rag_config.yaml` - RAG database and embedding settings
- `config/database.yaml` - General database configuration
- `.env` files in app directories - Environment-specific secrets

## Critical Rules

1. **GitHub URLs** - MUST use org `rauschiccsk`, NEVER `icc-zoltan`
   ```
   https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/...
   ```

2. **RAG API URL** - Parameter is `query` not `q`
   ```
   https://rag-api.icc.sk/search?query=KEYWORDS&limit=5
   ```

3. **PostgreSQL password** - Via `POSTGRES_PASSWORD` env variable, never in config.yaml

4. **Subprocess calls** - ALWAYS use `sys.executable` instead of `"python"` to ensure correct venv

5. **Sensitive data** - Passwords, tokens, API keys go ONLY to markdown artifacts, NEVER in .py scripts

## Collaboration Rules (from docs/COLLABORATION_RULES.md)

- Step-by-step execution - one action at a time
- Single solution approach - no alternatives unless requested
- All fixes via Python scripts only (no .ps1)
- Development -> Git -> Deployment workflow (never fix in deployment)
- Session scripts numbered sequentially (01_xxx.py, 02_xxx.py)
- `nex-shared` uses FLAT structure (critical)
