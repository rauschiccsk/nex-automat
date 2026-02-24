# ANDROS Knowledge Base

Tenant-specific documents for **ANDROS**.

## Structure

```
ANDROS/
├── processes/     # Business processes
├── hr/            # HR documentation  
├── technical/     # Technical guides
└── README.md
```

## Indexing

Documents in this directory are automatically tagged with `tenant: ANDROS` 
when indexed to RAG. They will only appear in searches for this tenant.

## Adding Documents

1. Place `.md` files in appropriate subdirectory
2. Run: `python tools/rag/rag_update.py --tenant ANDROS`

