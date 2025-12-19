"""
High-level RAG search API.
Provides convenient async interface for document search.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .config import get_config, RAGConfig
from .database import DatabaseManager
from .embeddings import EmbeddingModel
from .hybrid_search import search as hybrid_search_func


@dataclass
class SearchResult:
    """Single search result."""
    filename: str
    content: str
    score: float
    chunk_id: str
    section: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class RAGResponse:
    """RAG search response."""
    query: str
    results: List[SearchResult]
    total_found: int
    search_type: str
    timestamp: datetime


class RAGSearchAPI:
    """High-level RAG search API."""

    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or get_config()
        self.db = DatabaseManager(self.config.database)  # Pass database config only
        self.embeddings = EmbeddingModel(self.config.embedding)  # Pass embedding config only
        self._connected = False

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def connect(self):
        """Connect to database and load models."""
        if not self._connected:
            await self.db.connect()
            self.embeddings.load()  # Sync method, no await
            self._connected = True

    async def close(self):
        """Close connections."""
        if self._connected:
            await self.db.close()
            self._connected = False

    async def search(
        self,
        query: str,
        limit: int = 5,
        mode: str = 'hybrid',
        tenant: Optional[str] = None
    ) -> RAGResponse:
        """
        Search documents.

        Args:
            query: Search query
            limit: Maximum results
            mode: Search mode ('hybrid', 'vector', 'keyword')

        Returns:
            RAGResponse with results
        """
        await self.connect()

        # hybrid_search returns list of its own SearchResult objects
        results = await hybrid_search_func(query, limit=limit, tenant=tenant)

        # Convert hybrid_search.SearchResult to api.SearchResult
        search_results = [
            SearchResult(
                filename=r.filename,
                content=r.content,
                score=r.combined_score,  # Use combined_score as main score
                chunk_id=str(r.chunk_id),
                section=None,  # hybrid_search doesn't have section
                metadata={
                    'similarity': r.similarity,
                    'keyword_score': r.keyword_score,
                    'document_id': r.document_id,
                    'chunk_index': r.chunk_index
                }
            )
            for r in results
        ]

        return RAGResponse(
            query=query,
            results=search_results,
            total_found=len(search_results),
            search_type=mode,
            timestamp=datetime.utcnow()
        )

    async def get_context_for_llm(
        self,
        query: str,
        max_chunks: int = 3,
        max_tokens: int = 4000,
        tenant: Optional[str] = None
    ) -> str:
        """
        Get formatted context for LLM.

        Args:
            query: Search query
            max_tokens: Approximate max tokens in response
            max_chunks: Maximum number of chunks

        Returns:
            Formatted context string
        """
        response = await self.search(query, limit=max_chunks, mode='hybrid', tenant=tenant)

        context_parts = []
        total_chars = 0
        char_limit = max_tokens * 4  # Approximate

        for r in response.results:
            if total_chars + len(r.content) > char_limit:
                break

            part = f"### Source: {r.filename} (relevance: {r.score:.2f})\n\n{r.content}"
            context_parts.append(part)
            total_chars += len(r.content)

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
async def search(query: str, limit: int = 5, mode: str = 'hybrid', tenant: Optional[str] = None) -> RAGResponse:
    """Quick search function."""
    async with RAGSearchAPI() as api:
        return await api.search(query, limit=limit, mode=mode, tenant=tenant)


async def get_context(query: str, max_chunks: int = 3, tenant: Optional[str] = None) -> str:
    """Quick context retrieval for LLM."""
    async with RAGSearchAPI() as api:
        return await api.get_context_for_llm(query, max_chunks=max_chunks, tenant=tenant)