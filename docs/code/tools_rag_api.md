# api.py

**Path:** `tools\rag\api.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

High-level RAG search API.
Provides convenient async interface for document search.

---

## Classes

### SearchResult

Single search result.

---

### RAGResponse

RAG search response.

---

### RAGSearchAPI

High-level RAG search API.

**Methods:**

#### `__init__(self, config)`

#### `async __aenter__(self)`

Async context manager entry.

#### `async __aexit__(self, exc_type, exc_val, exc_tb)`

Async context manager exit.

#### `async connect(self)`

Connect to database and load models.

#### `async close(self)`

Close connections.

#### `async search(self, query, limit, mode)`

Search documents.

Args:
    query: Search query
    limit: Maximum results
    mode: Search mode ('hybrid', 'vector', 'keyword')

Returns:
    RAGResponse with results

#### `async get_context_for_llm(self, query, max_chunks, max_tokens)`

Get formatted context for LLM.

Args:
    query: Search query
    max_tokens: Approximate max tokens in response
    max_chunks: Maximum number of chunks

Returns:
    Formatted context string

#### `async get_stats(self)`

Get database statistics.

---

## Functions

### `async search(query, limit, mode)`

Quick search function.

---

### `async get_context(query, max_chunks)`

Quick context retrieval for LLM.

---
