# chunker.py

**Path:** `tools\rag\chunker.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Chunker Module
Document chunking utilities for semantic text splitting

---

## Classes

### DocumentChunker

Handles document chunking with overlap

Splits documents into chunks of approximately equal token count
with configurable overlap for context preservation.

**Methods:**

#### `__init__(self, config)`

Initialize document chunker

Args:
    config: Chunking configuration, uses global config if None

#### `count_tokens(self, text)`

Count tokens in text

Args:
    text: Text to count tokens

Returns:
    Token count

#### `chunk_text(self, text)`

Chunk text into overlapping segments

Args:
    text: Text to chunk

Returns:
    List of text chunks

#### `_split_large_text(self, text)`

Split large text that exceeds chunk size

Uses sentence boundaries when possible.

Args:
    text: Text to split

Returns:
    List of chunks

#### `_split_sentences(self, text)`

Split text into sentences

Simple sentence splitter based on punctuation.

Args:
    text: Text to split

Returns:
    List of sentences

#### `_split_by_words(self, text)`

Split text by words when sentences are too large

Args:
    text: Text to split

Returns:
    List of chunks

#### `chunk_with_metadata(self, text, base_metadata)`

Chunk text and return chunks with metadata

Args:
    text: Text to chunk
    base_metadata: Base metadata to include in all chunks

Returns:
    List of dicts with 'content' and 'metadata' keys

---

## Functions

### `get_chunker(reload)`

Get global document chunker (singleton pattern)

Args:
    reload: Force reload

Returns:
    DocumentChunker instance

---

### `chunk_text(text)`

Quick helper to chunk text

Args:
    text: Text to chunk

Returns:
    List of chunks

---
