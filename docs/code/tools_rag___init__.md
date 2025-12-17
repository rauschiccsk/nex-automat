# __init__.py

**Path:** `tools\rag\__init__.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG (Retrieval-Augmented Generation) Tools

This package provides document indexing and semantic search capabilities
for the NEX Automat project knowledge base.

Quick Usage:
    # Search
    from tools.rag.api import search, get_context
    results = await search('your query')
    context = await get_context('your query')

    # CLI
    python -m tools.rag "your query"
    python -m tools.rag.init_prompt_helper "topic"

Modules:
    - config: Configuration management
    - database: PostgreSQL/pgvector operations
    - embeddings: Sentence transformer embeddings
    - chunker: Document chunking
    - indexer: Document indexing
    - search: Basic search operations
    - hybrid_search: Vector + keyword hybrid search
    - api: High-level search API
    - init_prompt_helper: Init prompt context generator

---
