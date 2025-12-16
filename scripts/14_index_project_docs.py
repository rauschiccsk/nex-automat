#!/usr/bin/env python
"""
Script 14: Index Project Documents
Indexes real project markdown documents into RAG database.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import numpy as np

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel
from tools.rag.chunker import DocumentChunker

# Documents to index
DOCS_TO_INDEX = [
    "docs/strategic/RAG_IMPLEMENTATION.md",
    "docs/strategic/00_STRATEGIC_INDEX.md",
    "docs/database/UNIVERSAL_LOOKUP_TABLES.md",
    "docs/COLLABORATION_RULES.md",
    "README.md",
]


async def index_documents():
    """Index project documents into RAG database."""
    print("=" * 60)
    print("RAG DOCUMENT INDEXER - Phase 3.2")
    print("=" * 60)
    print()

    # Initialize
    config = get_config()
    db = DatabaseManager(config.database)
    embedder = EmbeddingModel(config.embedding)
    chunker = DocumentChunker(config.chunking)

    await db.connect()
    embedder.load()

    # Stats
    total_docs = 0
    total_chunks = 0
    total_tokens = 0
    start_time = datetime.now()

    print(f"Indexing {len(DOCS_TO_INDEX)} documents...\n")

    for doc_path in DOCS_TO_INDEX:
        filepath = project_root / doc_path

        if not filepath.exists():
            print(f"⚠ Skipping (not found): {doc_path}")
            continue

        print(f"📄 {doc_path}")

        # Read document
        content = filepath.read_text(encoding='utf-8')
        print(f"   Size: {len(content)} chars")

        # Chunk document
        chunks = chunker.chunk_text(content)
        print(f"   Chunks: {len(chunks)}")

        # Generate embeddings
        embeddings = embedder.encode(chunks)
        if isinstance(embeddings, np.ndarray) and embeddings.ndim == 1:
            embeddings = np.array([embeddings])

        # Store document
        doc_id = await db.insert_document(
            filename=doc_path,
            content=content,
            metadata=json.dumps({
                "source": str(filepath),
                "indexed_at": datetime.now().isoformat(),
                "chunks": len(chunks)
            })
        )

        # Store chunks
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            token_count = chunker.count_tokens(chunk)
            await db.insert_chunk(
                document_id=doc_id,
                chunk_index=i,
                content=chunk,
                embedding=embedding,
                metadata=json.dumps({"token_count": token_count})
            )
            total_tokens += token_count

        total_docs += 1
        total_chunks += len(chunks)
        print(f"   ✓ Indexed (ID: {doc_id})")
        print()

    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()

    print("=" * 60)
    print("INDEXING COMPLETE")
    print("=" * 60)
    print(f"  Documents indexed: {total_docs}")
    print(f"  Total chunks: {total_chunks}")
    print(f"  Total tokens: {total_tokens:,}")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Speed: {total_chunks / elapsed:.1f} chunks/sec")

    # Verify in database
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
    print()
    print(f"Database status:")
    print(f"  Documents: {doc_count}")
    print(f"  Chunks: {chunk_count}")

    await db.close()
    return True


if __name__ == "__main__":
    try:
        asyncio.run(index_documents())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)