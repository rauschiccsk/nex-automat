# server_app.py

**Path:** `tools\rag\server_app.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

FastAPI server application for RAG system.
Provides HTTP endpoints for document search and stats.

---

## Functions

### `async lifespan(app)`

Lifespan context manager for startup and shutdown events.

---

### `async root()`

Root endpoint with API information.

---

### `async health_check()`

Health check endpoint.

---

### `async search_endpoint(query, max_results, format)`

Search RAG database for relevant documents.

Args:
    query: Search query string
    max_results: Number of results to return (1-20)
    format: Response format - 'json' for raw data, 'context' for LLM-formatted text

Returns:
    JSON response with search results or formatted context

---

### `async stats_endpoint()`

Get RAG database statistics.

Returns:
    Statistics about indexed documents and chunks

---
