#!/usr/bin/env python
"""
Script 20: Test Hybrid Search
Compares vector-only vs hybrid search results.
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.hybrid_search import HybridSearch

TEST_QUERIES = [
    "Btrieve databáza migrácia PostgreSQL",
    "GSCAT produktový katalóg tabuľka",
    "supplier invoice ISH ISI",
    "stock cards STK movements",
    "RAG chunking embedding vector",
]


async def test_hybrid():
    """Compare vector vs hybrid search."""
    print("=" * 70)
    print("HYBRID SEARCH TEST - Vector vs Hybrid Comparison")
    print("=" * 70)
    print()

    async with HybridSearch(alpha=0.7) as searcher:
        for query in TEST_QUERIES:
            print(f"🔍 Query: \"{query}\"")
            print("-" * 70)

            # Vector-only search (alpha=1.0)
            searcher.alpha = 1.0
            vector_results = await searcher.search(query, limit=3, rerank=False)

            # Hybrid search (alpha=0.7)
            searcher.alpha = 0.7
            hybrid_results = await searcher.search(query, limit=3, rerank=True)

            print("\n  📊 VECTOR ONLY (alpha=1.0):")
            for i, r in enumerate(vector_results, 1):
                print(f"     {i}. [{r.similarity:.3f}] {r.filename}")

            print("\n  🔀 HYBRID (alpha=0.7, reranked):")
            for i, r in enumerate(hybrid_results, 1):
                kw = f"kw:{r.keyword_score:.2f}" if r.keyword_score > 0 else ""
                print(f"     {i}. [{r.combined_score:.3f}] {r.filename} {kw}")

            # Check if order changed
            v_order = [r.filename for r in vector_results]
            h_order = [r.filename for r in hybrid_results]
            if v_order != h_order:
                print("\n     ✨ Hybrid search changed ranking!")

            print("\n")

    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print("\nHybrid search boosts results with matching keywords.")
    print("alpha=0.7 means: 70% vector + 30% keyword score")


if __name__ == "__main__":
    try:
        asyncio.run(test_hybrid())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)