"""
Session Script 13: Direct test of hybrid_search with metadata
Projekt: nex-automat
Dočasný skript - testuje hybrid_search priamo bez FastAPI
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def test_hybrid_search():
    """Test hybrid search directly"""
    print("🧪 Testing hybrid_search with tenant='uae'...\n")

    try:
        from tools.rag.hybrid_search import search

        results = await search("UAE force majeure", limit=3, tenant="uae")

        print(f"✓ Search successful! Found {len(results)} results\n")

        for i, r in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Filename: {r.filename}")
            print(f"  Score: {r.combined_score:.4f}")
            print(f"  Metadata: {r.metadata}")
            print(f"  Content: {r.content[:100]}...")
            print()

    except Exception as e:
        print(f"✗ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_hybrid_search())