#!/usr/bin/env python
"""
Script 21: Test RAG Search API
Demonstrates the unified RAG API usage.
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.api import RAGSearchAPI, search, get_context


async def test_api():
    """Test RAG Search API."""
    print("=" * 60)
    print("RAG SEARCH API TEST")
    print("=" * 60)
    print()

    async with RAGSearchAPI() as api:
        # 1. Stats
        print("[1] Database Stats")
        print("-" * 40)
        stats = await api.get_stats()
        print(f"  Documents: {stats['documents']}")
        print(f"  Chunks: {stats['chunks']}")
        print(f"  Model: {stats['embedding_model']}")
        print()

        # 2. Hybrid Search
        print("[2] Hybrid Search")
        print("-" * 40)
        query = "Btrieve migrácia na PostgreSQL"
        response = await api.search(query, limit=3, mode='hybrid')

        print(f"  Query: \"{query}\"")
        print(f"  Mode: {response.search_type}")
        print(f"  Results: {response.total_found}\n")

        for i, r in enumerate(response.results, 1):
            print(f"  {i}. [{r['score']:.3f}] {r['filename']}")
            if r['keyword_score'] > 0:
                print(f"     (vector: {r['vector_score']:.3f}, keyword: {r['keyword_score']:.3f})")
        print()

        # 3. Vector-only Search
        print("[3] Vector-only Search")
        print("-" * 40)
        response_v = await api.search(query, limit=3, mode='vector')

        print(f"  Query: \"{query}\"")
        print(f"  Mode: {response_v.search_type}\n")

        for i, r in enumerate(response_v.results, 1):
            print(f"  {i}. [{r['score']:.3f}] {r['filename']}")
        print()

        # 4. LLM Context
        print("[4] LLM Context Generation")
        print("-" * 40)
        context = await api.get_context_for_llm(
            "ako funguje supplier invoice workflow",
            max_chunks=2
        )
        print(f"  Context length: {len(context)} chars")
        print(f"  Preview:\n")
        # Show first 500 chars
        preview = context[:500].replace('\n', '\n  ')
        print(f"  {preview}...")
        print()

    # 5. Convenience Functions
    print("[5] Convenience Functions")
    print("-" * 40)

    # Quick search
    result = await search("stock cards management", limit=2)
    print(f"  search(): Found {result.total_found} results")

    # Quick context
    ctx = await get_context("deployment guide", max_chunks=1)
    print(f"  get_context(): {len(ctx)} chars")
    print()

    print("=" * 60)
    print("API TEST COMPLETE ✅")
    print("=" * 60)
    print("\nUsage examples:")
    print("  from tools.rag.api import RAGSearchAPI, search, get_context")
    print("  ")
    print("  # Quick search")
    print("  results = await search('your query')")
    print("  ")
    print("  # Get context for LLM")
    print("  context = await get_context('your query')")


if __name__ == "__main__":
    try:
        asyncio.run(test_api())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)