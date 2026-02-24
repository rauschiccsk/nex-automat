"""
RAG Hybrid Search Module
Combines vector similarity with keyword matching for better results.
"""

import asyncio
import re
from dataclasses import dataclass
from typing import Any

from .config import get_config
from .database import DatabaseManager
from .embeddings import EmbeddingModel


@dataclass
class SearchResult:
    """Single search result."""

    chunk_id: int
    document_id: int
    filename: str
    chunk_index: int
    content: str
    similarity: float
    keyword_score: float
    combined_score: float
    metadata: dict[str, Any] | None = None


class HybridSearch:
    """
    Hybrid search combining vector similarity and keyword matching.

    Score = alpha * vector_similarity + (1-alpha) * keyword_score
    """

    def __init__(
        self,
        db: DatabaseManager | None = None,
        embedder: EmbeddingModel | None = None,
        alpha: float = 0.7,  # Weight for vector similarity
    ):
        config = get_config()
        self.db = db or DatabaseManager(config.database)
        self.embedder = embedder or EmbeddingModel(config.embedding)
        self.alpha = alpha
        self.config = config.search
        self._connected = False

    async def connect(self):
        """Initialize connections."""
        if not self._connected:
            await self.db.connect()
            self.embedder.load()
            self._connected = True

    async def close(self):
        """Close connections."""
        if self._connected:
            await self.db.close()
            self._connected = False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from query for matching."""
        # Remove common stop words
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "how",
            "what",
            "where",
            "when",
            "why",
            "which",
            "who",
            "to",
            "from",
            "in",
            "on",
            "at",
            "by",
            "for",
            "with",
            "and",
            "or",
            "but",
            "not",
            "do",
            "does",
            "did",
            "ako",
            "kde",
            "kedy",
            "prečo",
            "ktorý",
            "kto",
            "čo",
            "je",
            "sú",
            "bol",
            "bola",
            "boli",
            "pre",
            "na",
            "z",
        }

        # Tokenize and filter
        words = re.findall(r"\b\w+\b", query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        return keywords

    def _calculate_keyword_score(self, content: str, keywords: list[str]) -> float:
        """Calculate keyword match score (0-1)."""
        if not keywords:
            return 0.0

        content_lower = content.lower()
        matches = sum(1 for kw in keywords if kw in content_lower)

        return matches / len(keywords)

    async def search(
        self,
        query: str,
        limit: int = 10,
        min_similarity: float = 0.0,
        rerank: bool = True,
        tenant: str | None = None,
    ) -> list[SearchResult]:
        """
        Perform hybrid search.

        Args:
            query: Search query
            limit: Maximum results
            min_similarity: Minimum vector similarity threshold
            rerank: Whether to rerank by combined score

        Returns:
            List of SearchResult objects
        """
        await self.connect()

        # Extract keywords for matching
        keywords = self._extract_keywords(query)

        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0]
        query_str = (
            "[" + ",".join(str(float(x)) for x in query_embedding.tolist()) + "]"
        )

        # Fetch more results than needed for reranking
        fetch_limit = limit * 3 if rerank else limit

        # Vector search with optional tenant filter
        if tenant:
            results = await self.db.pool.fetch(
                """
                SELECT 
                    c.id as chunk_id,
                    c.document_id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    d.metadata,
                    1 - (c.embedding <=> $1::vector) as similarity
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE 1 - (c.embedding <=> $1::vector) >= $2
                  AND (d.metadata->>'tenant' = $4 OR d.metadata->>'tenant' IS NULL)
                ORDER BY c.embedding <=> $1::vector
                LIMIT $3
            """,
                query_str,
                min_similarity,
                fetch_limit,
                tenant,
            )
        else:
            results = await self.db.pool.fetch(
                """
                SELECT 
                    c.id as chunk_id,
                    c.document_id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    d.metadata,
                    1 - (c.embedding <=> $1::vector) as similarity
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE 1 - (c.embedding <=> $1::vector) >= $2
                ORDER BY c.embedding <=> $1::vector
                LIMIT $3
            """,
                query_str,
                min_similarity,
                fetch_limit,
            )

        # Calculate combined scores
        search_results = []
        for r in results:
            keyword_score = self._calculate_keyword_score(r["content"], keywords)
            combined_score = (
                self.alpha * r["similarity"] + (1 - self.alpha) * keyword_score
            )

            search_results.append(
                SearchResult(
                    chunk_id=r["chunk_id"],
                    document_id=r["document_id"],
                    filename=r["filename"],
                    chunk_index=r["chunk_index"],
                    content=r["content"],
                    similarity=r["similarity"],
                    keyword_score=keyword_score,
                    combined_score=combined_score,
                    metadata=r["metadata"] if r["metadata"] else None,
                )
            )

        # Rerank by combined score
        if rerank:
            search_results.sort(key=lambda x: x.combined_score, reverse=True)

        return search_results[:limit]

    async def search_with_context(
        self, query: str, limit: int = 5, context_chunks: int = 1
    ) -> list[dict[str, Any]]:
        """
        Search and include surrounding chunks for context.

        Args:
            query: Search query
            limit: Number of main results
            context_chunks: Number of chunks before/after to include

        Returns:
            List of results with context
        """
        results = await self.search(query, limit=limit)

        enriched_results = []
        for result in results:
            # Get surrounding chunks
            context = await self.db.pool.fetch(
                """
                SELECT chunk_index, content
                FROM chunks
                WHERE document_id = $1
                  AND chunk_index BETWEEN $2 AND $3
                ORDER BY chunk_index
            """,
                result.document_id,
                max(0, result.chunk_index - context_chunks),
                result.chunk_index + context_chunks,
            )

            # Combine content
            full_content = "\n\n".join(c["content"] for c in context)

            enriched_results.append(
                {
                    "filename": result.filename,
                    "chunk_index": result.chunk_index,
                    "similarity": result.similarity,
                    "keyword_score": result.keyword_score,
                    "combined_score": result.combined_score,
                    "content": result.content,
                    "full_context": full_content,
                    "context_range": (
                        context[0]["chunk_index"] if context else result.chunk_index,
                        context[-1]["chunk_index"] if context else result.chunk_index,
                    ),
                }
            )

        return enriched_results


# Convenience function
async def search(
    query: str, limit: int = 10, tenant: str | None = None, **kwargs
) -> list[SearchResult]:
    """Quick search function."""
    async with HybridSearch() as searcher:
        return await searcher.search(query, limit=limit, tenant=tenant, **kwargs)


if __name__ == "__main__":

    async def test():
        print("Testing Hybrid Search...")

        async with HybridSearch() as searcher:
            results = await searcher.search(
                "Btrieve databáza migrácia PostgreSQL", limit=5
            )

            print(f"\nFound {len(results)} results:\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r.filename}")
                print(
                    f"   Vector: {r.similarity:.3f} | Keyword: {r.keyword_score:.3f} | Combined: {r.combined_score:.3f}"
                )
                print(f"   {r.content[:100]}...")
                print()

    asyncio.run(test())
