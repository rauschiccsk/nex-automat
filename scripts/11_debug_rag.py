#!/usr/bin/env python
"""Debug RAG boost scores."""

import asyncio
import sys

sys.path.insert(0, "C:/Development/nex-automat/apps/nex-brain")

from api.services.rag_service import RAGService


async def test():
    rag = RAGService()

    # Get RAW results before processing
    import httpx
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"query": "Ake su fazy implementacie NEX Brain", "limit": 10}
        response = await client.get(f"{rag.base_url}/search", params=params)
        raw = response.json().get("results", [])

    print("=== RAW from API (before boost) ===")
    for r in raw[:6]:
        content = r.get("content", "")
        has_impl_section = "IMPLEMENTAČNÉ FÁZY" in content
        has_faza1 = "Fáza 1:" in content
        print(
            f"score={r.get('score', 0):.3f} section={has_impl_section} faza1={has_faza1} {r.get('filename', '')[:40]}")
        print(f"  LEN={len(content)} FIRST100: {content[:100]}...")

    print("\n=== After boost and dedupe ===")
    results = await rag.search("Ake su fazy implementacie NEX Brain", limit=10)
    for r in results:
        adj = r.get("adjusted_score", 0)
        has_impl = "IMPLEMENT" in r.get("content", "").upper()
        print(f"adj={adj:.3f} impl={has_impl} {r.get('filename', '')[:40]}")
        print(f"  CONTENT: {r.get('content', '')[:100]}...")


asyncio.run(test())