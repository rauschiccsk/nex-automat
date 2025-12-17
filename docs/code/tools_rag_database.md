# database.py

**Path:** `tools\rag\database.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Database Module
PostgreSQL operations with pgvector for vector similarity search

---

## Classes

### DatabaseManager

Manages PostgreSQL connection pool and operations

Handles document storage, vector operations, and search.

**Methods:**

#### `__init__(self, config)`

Initialize database manager

Args:
    config: Database configuration, uses global config if None

#### `async connect(self)`

Create connection pool

#### `async close(self)`

Close connection pool

#### `async insert_document(self, filename, content, metadata)`

Insert document into database

Args:
    filename: Document filename
    content: Document content
    metadata: Optional metadata dict

Returns:
    Document ID

#### `async insert_chunk(self, document_id, chunk_index, content, embedding, metadata)`

Insert document chunk with embedding

Args:
    document_id: Parent document ID
    chunk_index: Chunk index within document
    content: Chunk content
    embedding: Embedding vector
    metadata: Optional metadata

Returns:
    Chunk ID

#### `async search_similar(self, query_embedding, limit, similarity_threshold, document_ids)`

Search for similar chunks using vector similarity

Args:
    query_embedding: Query embedding vector
    limit: Maximum number of results
    similarity_threshold: Minimum similarity score (0-1)
    document_ids: Optional list of document IDs to filter

Returns:
    List of result dicts with chunk info and similarity scores

#### `async get_document(self, document_id)`

Get document by ID

#### `async get_chunks(self, document_id)`

Get all chunks for a document

#### `async delete_document(self, document_id)`

Delete document and all its chunks

Args:
    document_id: Document ID

Returns:
    True if deleted, False if not found

#### `async list_documents(self, limit, offset)`

List documents with pagination

#### `async get_stats(self)`

Get database statistics

#### `async __aenter__(self)`

Async context manager entry

#### `async __aexit__(self, exc_type, exc_val, exc_tb)`

Async context manager exit

---

## Functions

### `async get_db(reload)`

Get global database manager (singleton pattern)

Args:
    reload: Force reload

Returns:
    DatabaseManager instance

---
