# search.py

**Path:** `tools\rag\search.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Search Module
Semantic and hybrid search capabilities

---

## Classes

### SearchEngine

Handles semantic and hybrid search operations

Provides vector similarity search and keyword-based search.

**Methods:**

#### `__init__(self, db, embedding_model, config)`

Initialize search engine

Args:
    db: Database manager, creates new if None
    embedding_model: Embedding model, creates new if None
    config: Search configuration, uses global config if None

#### `async search(self, query, limit, similarity_threshold, document_ids)`

Perform semantic vector search

Args:
    query: Search query
    limit: Maximum number of results, uses config default if None
    similarity_threshold: Minimum similarity score, uses config default if None
    document_ids: Optional list of document IDs to filter

Returns:
    List of search results with relevance scores

#### `async search_with_context(self, query, limit, context_size)`

Search with surrounding context chunks

Retrieves matching chunks plus N chunks before and after for context.

Args:
    query: Search query
    limit: Maximum number of results
    context_size: Number of chunks before/after to include (0-3)
    **kwargs: Additional arguments passed to search()

Returns:
    List of results with context chunks

#### `async search_documents(self, query, limit)`

Search and group results by document

Args:
    query: Search query
    limit: Maximum number of documents
    **kwargs: Additional arguments passed to search()

Returns:
    List of documents with their matching chunks

#### `async explain_search(self, query, limit)`

Search with explanation of results

Provides detailed information about why results were returned.

Args:
    query: Search query
    limit: Number of results to explain

Returns:
    Dict with query info and explained results

#### `_explain_similarity(self, similarity)`

Generate human-readable similarity explanation

#### `async __aenter__(self)`

Async context manager entry

#### `async __aexit__(self, exc_type, exc_val, exc_tb)`

Async context manager exit

---

## Functions

### `async search(query, limit)`

Quick helper for semantic search

Args:
    query: Search query
    limit: Maximum results

Returns:
    List of search results

---
