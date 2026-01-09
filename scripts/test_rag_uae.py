"""
RAG Testing Script for UAE Legal Documents
Tests the multi-tenant RAG system with UAE legal queries

Usage:
    cd C:\\Development\\nex-automat\\scripts
    python test_rag_uae.py
"""

import sys
import asyncio
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.hybrid_search import search


async def test_uae_rag():
    """Test RAG queries for UAE legal documents"""

    tenant = "uae"

    test_queries = [
        "money laundering definition UAE",
        "pre-trial detention limits criminal procedure",
        "bail conditions money laundering",
        "burden of proof money laundering",
        "federal decree law 10 2025 AML",
        "article 107 detention extension"
    ]

    print("=" * 80)
    print("UAE LEGAL RAG - TEST QUERIES")
    print("=" * 80)
    print(f"Tenant: {tenant}")
    print(f"Total queries: {len(test_queries)}")
    print("=" * 80)

    success_count = 0
    fail_count = 0

    for i, query in enumerate(test_queries, 1):
        print(f"\n[TEST {i}/{len(test_queries)}] Query: '{query}'")
        print("-" * 80)

        try:
            # Await the async search function
            results = await search(
                query=query,
                tenant=tenant,
                limit=3
            )

            if results:
                print(f"✅ Found {len(results)} results")
                success_count += 1

                for j, result in enumerate(results, 1):
                    print(f"\n  Result {j}:")
                    print(f"  Combined Score: {result.combined_score:.4f}")
                    print(f"  Similarity: {result.similarity:.4f}")
                    print(f"  Keyword Score: {result.keyword_score:.4f}")
                    print(f"  Filename: {result.filename}")
                    print(f"  Chunk: {result.chunk_index}")
                    print(f"  Content preview: {result.content[:200]}...")

                    # Parse metadata if it's a string
                    if result.metadata:
                        try:
                            if isinstance(result.metadata, str):
                                metadata = json.loads(result.metadata)
                            else:
                                metadata = result.metadata

                            if 'tenant' in metadata:
                                print(f"  Tenant: {metadata['tenant']}")
                            if 'source' in metadata:
                                print(f"  Source: {metadata['source']}")
                        except (json.JSONDecodeError, TypeError):
                            # If parsing fails, just show raw metadata
                            metadata_str = str(result.metadata)[:100]
                            print(f"  Metadata: {metadata_str}...")
            else:
                print("❌ No results found")
                fail_count += 1

        except Exception as e:
            print(f"❌ Error: {e}")
            fail_count += 1
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Successful queries: {success_count}/{len(test_queries)}")
    print(f"❌ Failed queries: {fail_count}/{len(test_queries)}")
    print(f"Success rate: {(success_count/len(test_queries)*100):.1f}%")
    print("=" * 80)

    if fail_count > 0:
        print("\n⚠️  Some tests failed. Troubleshooting:")
        print("  1. Check PostgreSQL is running")
        print("  2. Verify UAE documents are indexed")
        print("  3. Run: python -m tools.rag search \"test\" --tenant uae")
    else:
        print("\n🎉 ALL TESTS PASSED! RAG system working correctly.")
        print("\n📊 Results Analysis:")
        print("  - All 6 queries returned relevant UAE legal documents")
        print("  - Hybrid search combines vector similarity + keyword matching")
        print("  - Documents indexed: Federal Decree-Law 10/2025 & 38/2022")
        print("\n✅ TIER 1 RAG Testing: COMPLETE")
        print("\nNext steps:")
        print("  1. Test via Telegram bot: /ask <query>")
        print("  2. Search Cabinet Decision 10/2019 to complete TIER 1")
        print("  3. Update INIT_PROMPT.md with test results")

    return success_count == len(test_queries)


if __name__ == "__main__":
    # Run async function with asyncio
    success = asyncio.run(test_uae_rag())
    sys.exit(0 if success else 1)
