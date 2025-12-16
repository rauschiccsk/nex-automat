#!/usr/bin/env python
"""
Script 17: RAG Performance Metrics
Measures indexing speed, search latency, and embedding generation time.
"""

import asyncio
import sys
import time
from pathlib import Path
from statistics import mean, stdev

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel
from tools.rag.chunker import DocumentChunker

TEST_QUERIES = [
    "RAG implementation guide",
    "PostgreSQL vector database",
    "document chunking strategy",
    "collaboration rules",
    "embedding model setup",
    "invoice processing automation",
    "NEX Genesis integration",
    "Python asyncio patterns",
    "database migration plan",
    "semantic search configuration",
]


async def measure_performance():
    """Measure RAG system performance metrics."""
    print("=" * 60)
    print("RAG PERFORMANCE METRICS - Phase 3.5")
    print("=" * 60)
    print()

    config = get_config()
    db = DatabaseManager(config.database)
    embedder = EmbeddingModel(config.embedding)
    chunker = DocumentChunker(config.chunking)

    await db.connect()
    embedder.load()

    # 1. Embedding Generation Speed
    print("[1/4] Embedding Generation Speed")
    print("-" * 40)

    embed_times = []
    for query in TEST_QUERIES:
        start = time.perf_counter()
        _ = embedder.encode([query])
        elapsed = (time.perf_counter() - start) * 1000
        embed_times.append(elapsed)

    print(f"  Single query embedding:")
    print(f"    Average: {mean(embed_times):.2f} ms")
    print(f"    Min: {min(embed_times):.2f} ms")
    print(f"    Max: {max(embed_times):.2f} ms")
    if len(embed_times) > 1:
        print(f"    Std Dev: {stdev(embed_times):.2f} ms")

    # Batch embedding
    start = time.perf_counter()
    _ = embedder.encode(TEST_QUERIES)
    batch_time = (time.perf_counter() - start) * 1000
    print(f"  Batch ({len(TEST_QUERIES)} queries): {batch_time:.2f} ms ({batch_time / len(TEST_QUERIES):.2f} ms/query)")
    print()

    # 2. Database Query Speed
    print("[2/4] Database Query Speed")
    print("-" * 40)

    search_times = []
    for query in TEST_QUERIES:
        query_embedding = embedder.encode([query])[0]
        query_str = '[' + ','.join(str(float(x)) for x in query_embedding.tolist()) + ']'

        start = time.perf_counter()
        _ = await db.pool.fetch("""
            SELECT c.id, c.content, 1 - (c.embedding <=> $1::vector) as similarity
            FROM chunks c
            ORDER BY c.embedding <=> $1::vector
            LIMIT 5
        """, query_str)
        elapsed = (time.perf_counter() - start) * 1000
        search_times.append(elapsed)

    print(f"  Vector search (top 5):")
    print(f"    Average: {mean(search_times):.2f} ms")
    print(f"    Min: {min(search_times):.2f} ms")
    print(f"    Max: {max(search_times):.2f} ms")
    if len(search_times) > 1:
        print(f"    Std Dev: {stdev(search_times):.2f} ms")
    print()

    # 3. End-to-End Search Latency
    print("[3/4] End-to-End Search Latency")
    print("-" * 40)

    e2e_times = []
    for query in TEST_QUERIES:
        start = time.perf_counter()

        # Full pipeline: embed + search
        query_embedding = embedder.encode([query])[0]
        query_str = '[' + ','.join(str(float(x)) for x in query_embedding.tolist()) + ']'
        _ = await db.pool.fetch("""
            SELECT c.id, c.content, d.filename,
                   1 - (c.embedding <=> $1::vector) as similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            ORDER BY c.embedding <=> $1::vector
            LIMIT 5
        """, query_str)

        elapsed = (time.perf_counter() - start) * 1000
        e2e_times.append(elapsed)

    print(f"  Query → Results (embed + search + join):")
    print(f"    Average: {mean(e2e_times):.2f} ms")
    print(f"    Min: {min(e2e_times):.2f} ms")
    print(f"    Max: {max(e2e_times):.2f} ms")
    if len(e2e_times) > 1:
        print(f"    Std Dev: {stdev(e2e_times):.2f} ms")
    print()

    # 4. Chunking Speed
    print("[4/4] Chunking Speed")
    print("-" * 40)

    # Generate test text
    test_text = "This is a test document. " * 500  # ~5000 words

    chunk_times = []
    for _ in range(10):
        start = time.perf_counter()
        chunks = chunker.chunk_text(test_text)
        elapsed = (time.perf_counter() - start) * 1000
        chunk_times.append(elapsed)

    print(f"  Chunking ~5000 words:")
    print(f"    Average: {mean(chunk_times):.2f} ms")
    print(f"    Chunks produced: {len(chunks)}")
    print()

    # Summary
    print("=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"  Embedding (single):     {mean(embed_times):.1f} ms")
    print(f"  Embedding (batch/10):   {batch_time / len(TEST_QUERIES):.1f} ms/query")
    print(f"  Vector search:          {mean(search_times):.1f} ms")
    print(f"  End-to-end search:      {mean(e2e_times):.1f} ms")
    print(f"  Chunking:               {mean(chunk_times):.1f} ms")
    print()

    # Target check
    e2e_avg = mean(e2e_times)
    if e2e_avg < 100:
        print(f"✅ End-to-end latency {e2e_avg:.1f}ms < 100ms target")
    else:
        print(f"⚠️ End-to-end latency {e2e_avg:.1f}ms > 100ms target")

    await db.close()
    return True


if __name__ == "__main__":
    try:
        asyncio.run(measure_performance())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)