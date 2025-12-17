# rag_reindex.py

**Path:** `tools\rag\rag_reindex.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Reindex Tool
Reindex documents in the RAG database.

Usage:
    python tools/rag/rag_reindex.py --all              # Reindex all docs
    python tools/rag/rag_reindex.py --file <path>      # Index single file
    python tools/rag/rag_reindex.py --dir <path>       # Index directory
    python tools/rag/rag_reindex.py --new              # Index only new files
    python tools/rag/rag_reindex.py --stats            # Show stats only

Location: tools/rag/rag_reindex.py

---

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--all` | Full reindex (drop and recreate |
| `--new` | Index only new files (incremental |
| `--file` | Index single file |
| `--dir` | Index directory |
| `--stats` | Show statistics only |

---

## Functions

### `async get_indexed_files(db)`

Get set of already indexed filenames.

---

### `async reindex_all(docs_path)`

Reindex all documents (drop and recreate).

---

### `async index_new_files(docs_path)`

Index only new files (incremental).

---

### `async index_single_file(filepath)`

Index a single file.

---

### `async index_directory(dir_path)`

Index all files in a directory.

---

### `async show_stats()`

Show database statistics.

---

### `main()`

---
