# NEX Brain - Tenant Filtering

**Aktualizované:** 2025-12-19
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
