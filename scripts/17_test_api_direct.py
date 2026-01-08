"""
Session Script 17: Direct test of api.py search function
Projekt: nex-automat
Dočasný skript - testuje api.py priamo
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def test_api_search():
    """Test api.py search directly"""
    print("🧪 Testing api.py search with tenant='uae'...\n")

    try:
        # First test hybrid_search directly to see what it returns
        from tools.rag.hybrid_search import search as hybrid_search

        print("Testing hybrid_search first...")
        hybrid_results = await hybrid_search("UAE force majeure", limit=1, tenant="uae")

        if hybrid_results:
            r = hybrid_results[0]
            print(f"\nHybrid search result metadata:")
            print(f"  Type: {type(r.metadata)}")
            print(f"  Value: {r.metadata}")
            print(f"  Content: {repr(r.metadata)}\n")

        # Now test api.py search
        from tools.rag.api import search

        response = await search("UAE force majeure", limit=3, tenant="uae")

        print(f"✓ API search successful!\n")
        print(f"Query: {response.query}")
        print(f"Total found: {response.total_found}")
        print(f"Search type: {response.search_type}\n")

        for i, r in enumerate(response.results, 1):
            print(f"Result {i}:")
            print(f"  Filename: {r.filename}")
            print(f"  Score: {r.score:.4f}")
            print(f"  Metadata: {r.metadata}")
            print(f"  Content: {r.content[:100]}...")
            print()

    except Exception as e:
        print(f"✗ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_api_search())