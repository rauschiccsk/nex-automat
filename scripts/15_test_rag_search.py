#!/usr/bin/env python
"""
Script 15: Test RAG Search
Tests semantic search functionality on indexed documents.
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel

# Test queries
TEST_QUERIES = [
    "How to implement RAG system?",
    "PostgreSQL vector database setup",
    "document chunking strategy",
    "collaboration rules for Claude",
    "embedding model configuration",
]


async def test_search():
    """Test semantic search on indexed documents."""
    print("=" * 60)
    print("RAG SEARCH TEST - Phase 3.3")
    print("=" * 60)
    print()

    config = get_config()
    db = DatabaseManager(config.database)
    embedder = EmbeddingModel(config.embedding)

    await db.connect()
    embedder.load()

    # Database stats
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
    print(f"Database: {doc_count} documents, {chunk_count} chunks\n")

    for query in TEST_QUERIES:
        print(f"🔍 Query: \"{query}\"")
        print("-" * 50)

        # Generate query embedding
        query_embedding = embedder.encode([query])[0]
        query_str = '[' + ','.join(str(float(x)) for x in query_embedding.tolist()) + ']'

        # Search
        results = await db.pool.fetch("""
            SELECT 
                c.id,
                c.document_id,
                d.filename,
                c.chunk_index,
                c.content,
                1 - (c.embedding <=> $1::vector) as similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            ORDER BY c.embedding <=> $1::vector
            LIMIT 3
        """, query_str)

        if results:
            for i, r in enumerate(results, 1):
                sim = r['similarity']
                sim_indicator = "🟢" if sim > 0.5 else "🟡" if sim > 0.3 else "🔴"

                # Truncate content preview
                preview = r['content'][:150].replace('\n', ' ').strip()
                if len(r['content']) > 150:
                    preview += "..."

                print(f"  {i}. {sim_indicator} Similarity: {sim:.4f}")
                print(f"     Source: {r['filename']} (chunk {r['chunk_index']})")
                print(f"     Preview: {preview}")
                print()
        else:
            print("  No results found\n")

        print()

    await db.close()

    print("=" * 60)
    print("SEARCH TEST COMPLETE")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        asyncio.run(test_search())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)