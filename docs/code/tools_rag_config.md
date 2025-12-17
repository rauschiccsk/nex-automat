# config.py

**Path:** `tools\rag\config.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Configuration Module
Loads and validates configuration from config/rag_config.yaml

---

## Classes

### DatabaseConfig(BaseModel)

PostgreSQL database configuration

**Methods:**

#### `validate_pool_size(cls, v, info)`

---

### EmbeddingConfig(BaseModel)

Embedding model configuration

---

### VectorIndexConfig(BaseModel)

Vector index configuration (HNSW)

---

### ChunkingConfig(BaseModel)

Document chunking configuration

**Methods:**

#### `validate_overlap(cls, v, info)`

---

### SearchConfig(BaseModel)

Search configuration

---

### RAGConfig(BaseSettings)

Main RAG configuration

---

## Functions

### `load_config(config_path)`

Load RAG configuration from YAML file

Args:
    config_path: Path to config file, defaults to config/rag_config.yaml

Returns:
    RAGConfig instance

Raises:
    FileNotFoundError: If config file not found
    ValueError: If config validation fails

---

### `get_config(reload)`

Get global RAG configuration (singleton pattern)

Args:
    reload: Force reload from file

Returns:
    RAGConfig instance

---
