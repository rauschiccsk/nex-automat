#!/usr/bin/env python
"""
Fix rag_service.py - Better context formatting to prevent hallucinations.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

CONTENT = '''"""
RAG Service - Integration with existing RAG API.
"""

import httpx
from typing import List, Dict, Any, Optional
from config.settings import settings


class RAGService:
    """Service for RAG queries."""

    def __init__(self):
        self.base_url = settings.RAG_API_URL

    async def search(
        self, 
        query: str, 
        limit: int = 3,  # Reduced from 5
        tenant: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search RAG knowledge base."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": query, "limit": limit}
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])

                if tenant:
                    results = self._filter_by_tenant(results, tenant)

                # Deduplicate by filename - keep only best chunk per file
                results = self._deduplicate(results)

                return results[:2]  # Max 2 results

        except httpx.RequestError as e:
            print(f"RAG API error: {e}")
            return []

    def _deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only best chunk per unique filename."""
        seen = {}
        for r in results:
            filename = r.get("filename", "")
            if filename not in seen:
                seen[filename] = r
        return list(seen.values())

    def _filter_by_tenant(
        self, 
        results: List[Dict[str, Any]], 
        tenant: str
    ) -> List[Dict[str, Any]]:
        """Filter results by tenant."""
        filtered = []
        for r in results:
            filename = r.get("filename", "").lower()
            if (
                f"{tenant}/" in filename or
                "shared/" in filename or
                "/" not in filename
            ):
                filtered.append(r)
        return filtered

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format RAG results as concise context for LLM."""
        if not results:
            return ""

        context_parts = []
        for r in results:
            content = r.get("content", "")
            # Truncate to max 600 chars
            if len(content) > 600:
                content = content[:600] + "..."

            # Clean up content - remove code blocks and excessive whitespace
            content = self._clean_content(content)

            context_parts.append(content)

        return "\\n\\n".join(context_parts)

    def _clean_content(self, content: str) -> str:
        """Clean content for better LLM understanding."""
        lines = content.split("\\n")
        cleaned = []
        in_code_block = False

        for line in lines:
            # Skip code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            # Skip empty lines and headers with just symbols
            if line.strip() and not line.strip().startswith("---"):
                cleaned.append(line)

        return "\\n".join(cleaned[:15])  # Max 15 lines
'''


def main():
    FILE_PATH.write_text(CONTENT, encoding="utf-8")
    print("✅ Fixed: rag_service.py")
    print("   - Max 2 results (was 5)")
    print("   - Deduplicate by filename")
    print("   - Truncate to 600 chars")
    print("   - Remove code blocks")


if __name__ == "__main__":
    main()