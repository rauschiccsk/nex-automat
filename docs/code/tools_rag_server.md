# server.py

**Path:** `tools\rag\server.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG API Server startup script.
Starts FastAPI server for RAG system endpoints.

---

## Classes

### RAGServer

RAG API Server manager.

**Methods:**

#### `__init__(self, host, port)`

#### `start(self, reload, log_level)`

Start RAG API server.

Args:
    reload: Enable auto-reload on code changes (development mode)
    log_level: Logging level (debug, info, warning, error)

#### `stop(self)`

Stop RAG API server.

#### `status(self)`

Check if server is running.

---

## Functions

### `main()`

Main entry point.

---
