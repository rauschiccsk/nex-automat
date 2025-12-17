# embeddings.py

**Path:** `tools\rag\embeddings.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Embeddings Module
Handles text embedding generation using sentence-transformers

---

## Classes

### EmbeddingModel

Wrapper for sentence-transformers embedding model

Handles model loading, caching, and batch embedding generation.

**Methods:**

#### `__init__(self, config)`

Initialize embedding model

Args:
    config: Embedding configuration, uses global config if None

#### `load(self)`

Load the embedding model

#### `encode(self, texts, batch_size, show_progress, normalize)`

Generate embeddings for text(s)

Args:
    texts: Single text or list of texts
    batch_size: Batch size for processing, uses config default if None
    show_progress: Show progress bar
    normalize: Normalize embeddings to unit length

Returns:
    Numpy array of embeddings (N x dimension)

#### `encode_batch(self, texts, batch_size, show_progress)`

Generate embeddings for batch of texts

Convenience method that always shows progress and returns array.

Args:
    texts: List of texts
    batch_size: Batch size for processing
    show_progress: Show progress bar

Returns:
    Numpy array of embeddings (N x dimension)

#### `dimension(self)`

Get embedding dimension

#### `device(self)`

Get device being used

#### `__repr__(self)`

---

## Functions

### `get_model(reload)`

Get global embedding model (singleton pattern)

Args:
    reload: Force reload model

Returns:
    EmbeddingModel instance

---

### `embed_text(text, normalize)`

Quick helper to embed single text

Args:
    text: Text to embed
    normalize: Normalize embedding

Returns:
    Embedding vector

---

### `embed_texts(texts, batch_size)`

Quick helper to embed multiple texts

Args:
    texts: List of texts
    batch_size: Batch size

Returns:
    Array of embeddings

---
