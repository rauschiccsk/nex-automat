# indexer.py

**Path:** `tools\rag\indexer.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

RAG Indexer Module
Document indexing pipeline for RAG system

---

## Classes

### DocumentIndexer

Handles document indexing pipeline

Coordinates chunking, embedding, and storage of documents.

**Methods:**

#### `__init__(self, db, embedding_model, chunker)`

Initialize document indexer

Args:
    db: Database manager, creates new if None
    embedding_model: Embedding model, creates new if None
    chunker: Document chunker, creates new if None

#### `async index_document(self, filename, content, metadata, show_progress)`

Index a document

Workflow:
1. Insert document into database
2. Chunk document
3. Generate embeddings for chunks
4. Store chunks with embeddings

Args:
    filename: Document filename
    content: Document content
    metadata: Optional document metadata
    show_progress: Show progress output

Returns:
    Dict with indexing results

#### `async index_file(self, filepath, metadata, show_progress)`

Index a file from disk

Args:
    filepath: Path to file
    metadata: Optional document metadata
    show_progress: Show progress output

Returns:
    Dict with indexing results

#### `async index_directory(self, directory, pattern, recursive, show_progress)`

Index all files in a directory

Args:
    directory: Directory path
    pattern: File pattern (glob)
    recursive: Search recursively
    show_progress: Show progress output

Returns:
    List of indexing results

#### `async reindex_document(self, document_id, show_progress)`

Reindex an existing document

Deletes old chunks and creates new ones.

Args:
    document_id: Document ID
    show_progress: Show progress output

Returns:
    Dict with indexing results

#### `async __aenter__(self)`

Async context manager entry

#### `async __aexit__(self, exc_type, exc_val, exc_tb)`

Async context manager exit

---
