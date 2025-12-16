#!/usr/bin/env python
"""
Script 19: Test Search on Large Dataset
Tests semantic search on 500+ chunks.
"""

import asyncio
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel

TEST_QUERIES = [
    # Slovak queries
    "ako funguje Btrieve databáza",
    "migrácia z Pervasive na PostgreSQL",
    "faktúry dodávateľov workflow",
    "produktový katalóg GSCAT",
    # English queries
    "supplier invoice processing",
    "stock management cards",
    "deployment guide production",
    "RAG implementation chunks",
    # Technical queries
    "asyncio Python patterns",
    "PyQt5 GUI base window",
]


async def test_search():
    """Test search on large dataset."""
    print("=" * 60)
    print("RAG SEARCH TEST - Large Dataset (500 chunks)")
    print("=" * 60)
    print()

    config = get_config()
    db = DatabaseManager(config.database)
    embedder = EmbeddingModel(config.embedding)

    await db.connect()
    embedder.load()

    # Stats
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
    print(f"Database: {doc_count} documents, {chunk_count} chunks\n")

    total_time = 0
    high_relevance = 0

    for query in TEST_QUERIES:
        print(f"🔍 \"{query}\"")

        start = time.perf_counter()

        # Generate embedding and search
        query_embedding = embedder.encode([query])[0]
        query_str = '[' + ','.join(str(float(x)) for x in query_embedding.tolist()) + ']'

        results = await db.pool.fetch("""
            SELECT 
                c.id, d.filename, c.chunk_index,
                LEFT(c.content, 120) as preview,
                1 - (c.embedding <=> $1::vector) as similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            ORDER BY c.embedding <=> $1::vector
            LIMIT 3
        """, query_str)

        elapsed = (time.perf_counter() - start) * 1000
        total_time += elapsed

        if results:
            top_sim = results[0]['similarity']
            if top_sim > 0.4:
                high_relevance += 1

            sim_indicator = "🟢" if top_sim > 0.5 else "🟡" if top_sim > 0.3 else "🔴"
            print(f"   {sim_indicator} Top: {top_sim:.3f} | {elapsed:.1f}ms")
            print(f"   📄 {results[0]['filename']}")
            preview = results[0]['preview'].replace('\n', ' ')[:80]
            print(f"   \"{preview}...\"")
        print()

    # Summary
    avg_time = total_time / len(TEST_QUERIES)
    relevance_rate = high_relevance / len(TEST_QUERIES) * 100

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Queries tested: {len(TEST_QUERIES)}")
    print(f"  Avg search time: {avg_time:.1f} ms")
    print(f"  High relevance (>0.4): {high_relevance}/{len(TEST_QUERIES)} ({relevance_rate:.0f}%)")

    await db.close()
    return True


if __name__ == "__main__":
    try:
        asyncio.run(test_search())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)