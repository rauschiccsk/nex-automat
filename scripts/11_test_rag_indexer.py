#!/usr/bin/env python
"""
Script 11: Test RAG Indexer Pipeline
Tests the complete indexing workflow with a sample document.
"""

import asyncio
import sys
import json
from pathlib import Path
import numpy as np
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel
from tools.rag.chunker import DocumentChunker
from tools.rag.indexer import DocumentIndexer

# Sample test document
SAMPLE_DOCUMENT = """
# NEX Automat - Test Document

## Overview

NEX Automat is a comprehensive automation platform for invoice processing.
It integrates with the NEX Genesis ERP system to provide automated supplier
invoice handling, product matching, and data synchronization.

## Key Features

### Invoice Processing
The system automatically extracts data from supplier invoices using OCR
and machine learning. It matches products against the existing catalog
and creates staging records for review.

### Product Matching
Products are matched using multiple algorithms:
- EAN barcode matching (exact match)
- Supplier product code matching
- Fuzzy text matching for product names
- AI-assisted matching for complex cases

### Database Integration
The system supports multiple database backends:
- PostgreSQL for staging and configuration
- Btrieve for legacy NEX Genesis data
- Vector databases for semantic search

## Architecture

The application follows a modular architecture with these components:
1. FastAPI backend for REST API
2. PyQt5 GUI for desktop editing
3. n8n workflows for automation
4. RAG system for intelligent search

## Technical Stack

- Python 3.12 for backend services
- PostgreSQL 15 with pgvector extension
- sentence-transformers for embeddings
- asyncio for asynchronous operations

This document serves as a test for the RAG indexing pipeline.
"""


async def test_indexer():
    """Test the complete indexing pipeline."""
    print("=" * 60)
    print("RAG INDEXER TEST - Phase 3.1")
    print("=" * 60)
    print()

    # Step 1: Load configuration
    print("[1/6] Loading configuration...")
    config = get_config()
    print(f"  ✓ Embedding model: {config.embedding.model_name}")
    print(f"  ✓ Chunk size: {config.chunking.chunk_size} tokens")
    print(f"  ✓ Chunk overlap: {config.chunking.chunk_overlap} tokens")
    print()

    # Step 2: Initialize components
    print("[2/6] Initializing components...")

    db = DatabaseManager(config.database)
    embedder = EmbeddingModel(config.embedding)
    chunker = DocumentChunker(config.chunking)

    await db.connect()
    print("  ✓ Database connected")

    embedder.load()
    print("  ✓ Embedding model loaded")
    print()

    # Step 3: Chunk the document
    print("[3/6] Chunking document...")
    chunks = chunker.chunk_text(SAMPLE_DOCUMENT)
    print(f"  ✓ Created {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        token_count = chunker.count_tokens(chunk)
        print(f"    Chunk {i + 1}: {token_count} tokens, {len(chunk)} chars")
    print()

    # Step 4: Generate embeddings
    print("[4/6] Generating embeddings...")
    start_time = datetime.now()

    texts = chunks
    embeddings = embedder.encode(texts)

    # Ensure embeddings is 2D array for iteration
    if isinstance(embeddings, np.ndarray):
        if embeddings.ndim == 1:
            embeddings = np.array([embeddings])

    embed_time = (datetime.now() - start_time).total_seconds()
    print(f"  ✓ Generated {len(embeddings)} embeddings")
    print(f"  ✓ Embedding dimension: {len(embeddings[0])}")
    print(f"  ✓ Time: {embed_time:.3f}s ({embed_time / len(chunks) * 1000:.1f}ms per chunk)")
    print()

    # Step 5: Store in database
    print("[5/6] Storing in database...")

    # Create document record
    doc_id = await db.insert_document(
        filename="test_document.md",
        content=SAMPLE_DOCUMENT,
        metadata=json.dumps({"type": "test", "phase": "3.1"})
    )
    print(f"  ✓ Document created: ID={doc_id}")

    # Store chunks with embeddings
    chunk_ids = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_id = await db.insert_chunk(
            document_id=doc_id,
            chunk_index=i,
            content=chunk,
            embedding=embedding,
            metadata=json.dumps({"token_count": chunker.count_tokens(chunk)})
        )
        chunk_ids.append(chunk_id)

    print(f"  ✓ Stored {len(chunk_ids)} chunks with embeddings")
    print()

    # Step 6: Verify storage
    print("[6/6] Verifying storage...")

    # Count records
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")

    print(f"  ✓ Documents in database: {doc_count}")
    print(f"  ✓ Chunks in database: {chunk_count}")

    # Test vector search (basic)
    test_query = "invoice processing automation"
    query_embedding = embedder.encode([test_query])[0]
    query_embedding_str = '[' + ','.join(str(x) for x in query_embedding.tolist()) + ']'

    results = await db.pool.fetch("""
        SELECT c.id, c.content, 
               1 - (c.embedding <=> $1::vector) as similarity
        FROM chunks c
        ORDER BY c.embedding <=> $1::vector
        LIMIT 3
    """, query_embedding_str)

    print()
    print(f"  Test search: '{test_query}'")
    print(f"  Found {len(results)} results:")
    for r in results:
        preview = r['content'][:80].replace('\n', ' ') + "..."
        print(f"    - Similarity: {r['similarity']:.4f}")
        print(f"      {preview}")

    # Cleanup
    await db.close()

    print()
    print("=" * 60)
    print("TEST COMPLETE - All steps successful!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_indexer())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)