"""
RAG Search API
Unified interface for RAG search operations.
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

from .config import get_config
from .database import DatabaseManager
from .embeddings import EmbeddingModel
from .hybrid_search import HybridSearch, SearchResult


@dataclass
class RAGResponse:
    """Structured RAG response."""
    query: str
    results: List[Dict[str, Any]]
    total_found: int
    search_type: str  # 'vector', 'hybrid', 'keyword'

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def get_context(self, max_chunks: int = 3) -> str:
        """Get combined context from top results."""
        contexts = []
        for r in self.results[:max_chunks]:
            source = f"[{r['filename']}]"
            contexts.append(f"{source}\n{r['content']}")
        return "\n\n---\n\n".join(contexts)


class RAGSearchAPI:
    """
    High-level RAG Search API.

    Usage:
        async with RAGSearchAPI() as rag:
            response = await rag.search("your query")
            context = response.get_context()
    """

    def __init__(self):
        self.config = get_config()
        self.db = DatabaseManager(self.config.database)
        self.embedder = EmbeddingModel(self.config.embedding)
        self.hybrid = HybridSearch(self.db, self.embedder)
        self._connected = False

    async def connect(self):
        """Initialize all connections."""
        if not self._connected:
            await self.db.connect()
            self.embedder.load()
            self._connected = True

    async def close(self):
        """Close all connections."""
        if self._connected:
            await self.db.close()
            self._connected = False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def search(
            self,
            query: str,
            limit: int = 5,
            mode: str = 'hybrid',  # 'vector', 'hybrid'
            min_score: float = 0.0,
            include_context: bool = False
    ) -> RAGResponse:
        """
        Search the knowledge base.

        Args:
            query: Search query (Slovak or English)
            limit: Maximum number of results
            mode: 'vector' for pure semantic, 'hybrid' for semantic+keyword
            min_score: Minimum relevance score (0-1)
            include_context: Include surrounding chunks

        Returns:
            RAGResponse with results
        """
        await self.connect()

        if mode == 'hybrid':
            self.hybrid.alpha = 0.7
            results = await self.hybrid.search(query, limit=limit, min_similarity=min_score)

            formatted = []
            for r in results:
                formatted.append({
                    'filename': r.filename,
                    'chunk_index': r.chunk_index,
                    'content': r.content,
                    'score': r.combined_score,
                    'vector_score': r.similarity,
                    'keyword_score': r.keyword_score
                })
        else:
            # Vector-only search
            self.hybrid.alpha = 1.0
            results = await self.hybrid.search(query, limit=limit, min_similarity=min_score, rerank=False)

            formatted = []
            for r in results:
                formatted.append({
                    'filename': r.filename,
                    'chunk_index': r.chunk_index,
                    'content': r.content,
                    'score': r.similarity,
                    'vector_score': r.similarity,
                    'keyword_score': 0.0
                })

        return RAGResponse(
            query=query,
            results=formatted,
            total_found=len(formatted),
            search_type=mode
        )

    async def get_context_for_llm(
            self,
            query: str,
            max_tokens: int = 4000,
            max_chunks: int = 5
    ) -> str:
        """
        Get formatted context for LLM consumption.

        Args:
            query: Search query
            max_tokens: Approximate max tokens in response
            max_chunks: Maximum number of chunks

        Returns:
            Formatted context string
        """
        response = await self.search(query, limit=max_chunks, mode='hybrid')

        context_parts = []
        total_chars = 0
        char_limit = max_tokens * 4  # Approximate

        for r in response.results:
            if total_chars + len(r['content']) > char_limit:
                break

            part = f"### Source: {r['filename']} (relevance: {r['score']:.2f})\n\n{r['content']}"
            context_parts.append(part)
            total_chars += len(r['content'])

        header = f"## Retrieved Context for: \"{query}\"\n\n"
        return header + "\n\n---\n\n".join(context_parts)

    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        await self.connect()

        doc_count = await self.db.pool.fetchval("SELECT COUNT(*) FROM documents")
        chunk_count = await self.db.pool.fetchval("SELECT COUNT(*) FROM chunks")

        return {
            'documents': doc_count,
            'chunks': chunk_count,
            'embedding_model': self.config.embedding.model_name,
            'embedding_dimension': self.config.embedding.dimension
        }


# Convenience functions for quick usage
async def search(query: str, limit: int = 5, mode: str = 'hybrid') -> RAGResponse:
    """Quick search function."""
    async with RAGSearchAPI() as api:
        return await api.search(query, limit=limit, mode=mode)


async def get_context(query: str, max_chunks: int = 3) -> str:
    """Quick context retrieval for LLM."""
    async with RAGSearchAPI() as api:
        return await api.get_context_for_llm(query, max_chunks=max_chunks)


if __name__ == "__main__":
    async def demo():
        print("RAG Search API Demo\n")

        async with RAGSearchAPI() as api:
            # Get stats
            stats = await api.get_stats()
            print(f"Database: {stats['documents']} docs, {stats['chunks']} chunks\n")

            # Search demo
            query = "supplier invoice processing workflow"
            print(f"Query: \"{query}\"\n")

            response = await api.search(query, limit=3)
            print(f"Found {response.total_found} results ({response.search_type} mode):\n")

            for i, r in enumerate(response.results, 1):
                print(f"{i}. [{r['score']:.3f}] {r['filename']}")
                print(f"   {r['content'][:100]}...\n")

            # Context for LLM
            print("\n--- LLM Context ---\n")
            context = await api.get_context_for_llm(query, max_chunks=2)
            print(context[:500] + "...")


    asyncio.run(demo())