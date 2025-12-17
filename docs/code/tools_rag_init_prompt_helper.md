# init_prompt_helper.py

**Path:** `tools\rag\init_prompt_helper.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Init Prompt Helper
Generates RAG context for Claude chat initialization.

Usage:
  python -m tools.rag.init_prompt_helper "topic or task"
  python -m tools.rag.init_prompt_helper --interactive

---

## Functions

### `async generate_context(query, max_chunks, max_tokens, include_scores)`

Generate context section for init prompt.

Args:
    query: Topic or task description
    max_chunks: Maximum chunks to include
    max_tokens: Approximate token limit

Returns:
    Formatted context string

---

### `async generate_multi_context(queries, max_chunks_per_query)`

Generate context for multiple queries/topics.

---

### `async interactive_mode()`

Interactive context generation.

---

### `main()`

---
