# hybrid_search.py

**Path:** `tools\rag\hybrid_search.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Hybrid Search Module
Combines vector similarity with keyword matching for better results.

---

## Classes

### SearchResult

Single search result.

---

### HybridSearch

Hybrid search combining vector similarity and keyword matching.

Score = alpha * vector_similarity + (1-alpha) * keyword_score

**Methods:**

#### `__init__(self, db, embedder, alpha)`

#### `async connect(self)`

Initialize connections.

#### `async close(self)`

Close connections.

#### `async __aenter__(self)`

#### `async __aexit__(self)`

#### `_extract_keywords(self, query)`

Extract keywords from query for matching.

#### `_calculate_keyword_score(self, content, keywords)`

Calculate keyword match score (0-1).

#### `async search(self, query, limit, min_similarity, rerank)`

Perform hybrid search.

Args:
    query: Search query
    limit: Maximum results
    min_similarity: Minimum vector similarity threshold
    rerank: Whether to rerank by combined score

Returns:
    List of SearchResult objects

#### `async search_with_context(self, query, limit, context_chunks)`

Search and include surrounding chunks for context.

Args:
    query: Search query
    limit: Number of main results
    context_chunks: Number of chunks before/after to include

Returns:
    List of results with context

---

## Functions

### `async search(query, limit)`

Quick search function.

---
