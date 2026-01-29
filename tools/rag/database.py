"""
RAG Database Module
PostgreSQL operations with pgvector for vector similarity search
"""

import json
from typing import Any

import asyncpg
import numpy as np

from .config import DatabaseConfig, get_config


class DatabaseManager:
    """
    Manages PostgreSQL connection pool and operations

    Handles document storage, vector operations, and search.
    """

    def __init__(self, config: DatabaseConfig | None = None):
        """
        Initialize database manager

        Args:
            config: Database configuration, uses global config if None
        """
        if config is None:
            config = get_config().database

        self.config = config
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        """Create connection pool"""
        if self.pool is not None:
            return  # Already connected

        print(f"Connecting to database: {self.config.host}:{self.config.port}/{self.config.database}")

        self.pool = await asyncpg.create_pool(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            min_size=self.config.pool_min_size,
            max_size=self.config.pool_max_size,
        )

        print("[OK] Database connection pool created")

    async def close(self) -> None:
        """Close connection pool"""
        if self.pool is not None:
            await self.pool.close()
            self.pool = None
            print("[OK] Database connection pool closed")

    async def insert_document(self, filename: str, content: str, metadata: dict[str, Any] | None = None) -> int:
        """
        Insert document into database

        Args:
            filename: Document filename
            content: Document content
            metadata: Optional metadata dict

        Returns:
            Document ID
        """
        if self.pool is None:
            await self.connect()

        query = """
            INSERT INTO documents (filename, content, metadata)
            VALUES ($1, $2, $3)
            RETURNING id
        """

        metadata_json = json.dumps(metadata) if metadata else None
        doc_id = await self.pool.fetchval(query, filename, content, metadata_json)
        return doc_id

    async def insert_chunk(
        self,
        document_id: int,
        chunk_index: int,
        content: str,
        embedding: np.ndarray,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """
        Insert document chunk with embedding

        Args:
            document_id: Parent document ID
            chunk_index: Chunk index within document
            content: Chunk content
            embedding: Embedding vector
            metadata: Optional metadata

        Returns:
            Chunk ID
        """
        if self.pool is None:
            await self.connect()

        # Convert numpy array to pgvector string format
        if isinstance(embedding, np.ndarray):
            # Flatten if 2D and convert to list
            if embedding.ndim > 1:
                embedding = embedding.flatten()
            embedding_list = embedding.tolist()
        elif hasattr(embedding, "tolist"):
            embedding_list = embedding.tolist()
        else:
            embedding_list = list(embedding)
        # Create pgvector format string
        embedding_str = "[" + ",".join(str(float(x)) for x in embedding_list) + "]"

        query = """
            INSERT INTO chunks (document_id, chunk_index, content, embedding, metadata)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """

        metadata_json = json.dumps(metadata) if metadata else None
        chunk_id = await self.pool.fetchval(query, document_id, chunk_index, content, embedding_str, metadata_json)

        return chunk_id

    async def search_similar(
        self,
        query_embedding: np.ndarray,
        limit: int = 10,
        similarity_threshold: float = 0.0,
        document_ids: list[int] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for similar chunks using vector similarity

        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score (0-1)
            document_ids: Optional list of document IDs to filter

        Returns:
            List of result dicts with chunk info and similarity scores
        """
        if self.pool is None:
            await self.connect()

        if isinstance(query_embedding, np.ndarray):
            if query_embedding.ndim > 1:
                query_embedding = query_embedding.flatten()
            embedding_list = query_embedding.tolist()
        elif hasattr(query_embedding, "tolist"):
            embedding_list = query_embedding.tolist()
        else:
            embedding_list = list(query_embedding)
        embedding_str = "[" + ",".join(str(float(x)) for x in embedding_list) + "]"

        # Build query
        query = """
            SELECT 
                c.id,
                c.document_id,
                c.chunk_index,
                c.content,
                c.metadata,
                d.filename,
                1 - (c.embedding <=> $1::vector) as similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
        """

        params = [embedding_list]

        if document_ids:
            query += " WHERE c.document_id = ANY($2)"
            params.append(document_ids)

        query += """
            ORDER BY c.embedding <=> $1::vector
            LIMIT $""" + str(len(params) + 1)

        params.append(limit)

        # Execute query
        rows = await self.pool.fetch(query, *params)

        # Filter by similarity threshold and convert to dicts
        results = []
        for row in rows:
            if row["similarity"] >= similarity_threshold:
                results.append(
                    {
                        "chunk_id": row["id"],
                        "document_id": row["document_id"],
                        "chunk_index": row["chunk_index"],
                        "content": row["content"],
                        "metadata": row["metadata"],
                        "filename": row["filename"],
                        "similarity": float(row["similarity"]),
                    }
                )

        return results

    async def get_document(self, document_id: int) -> dict[str, Any] | None:
        """Get document by ID"""
        if self.pool is None:
            await self.connect()

        query = "SELECT * FROM documents WHERE id = $1"
        row = await self.pool.fetchrow(query, document_id)

        if row is None:
            return None

        return dict(row)

    async def get_chunks(self, document_id: int) -> list[dict[str, Any]]:
        """Get all chunks for a document"""
        if self.pool is None:
            await self.connect()

        query = """
            SELECT id, document_id, chunk_index, content, metadata
            FROM chunks
            WHERE document_id = $1
            ORDER BY chunk_index
        """

        rows = await self.pool.fetch(query, document_id)
        return [dict(row) for row in rows]

    async def delete_document(self, document_id: int) -> bool:
        """
        Delete document and all its chunks

        Args:
            document_id: Document ID

        Returns:
            True if deleted, False if not found
        """
        if self.pool is None:
            await self.connect()

        # Delete chunks first (cascade should handle this, but explicit is good)
        await self.pool.execute("DELETE FROM chunks WHERE document_id = $1", document_id)

        # Delete document
        result = await self.pool.execute("DELETE FROM documents WHERE id = $1", document_id)

        # Check if any rows were deleted
        return result.split()[-1] != "0"

    async def list_documents(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        """List documents with pagination"""
        if self.pool is None:
            await self.connect()

        query = """
            SELECT id, filename, created_at, metadata
            FROM documents
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
        """

        rows = await self.pool.fetch(query, limit, offset)
        return [dict(row) for row in rows]

    async def get_stats(self) -> dict[str, Any]:
        """Get database statistics"""
        if self.pool is None:
            await self.connect()

        stats = {}

        # Document count
        stats["document_count"] = await self.pool.fetchval("SELECT COUNT(*) FROM documents")

        # Chunk count
        stats["chunk_count"] = await self.pool.fetchval("SELECT COUNT(*) FROM chunks")

        # Average chunks per document
        if stats["document_count"] > 0:
            stats["avg_chunks_per_doc"] = stats["chunk_count"] / stats["document_count"]
        else:
            stats["avg_chunks_per_doc"] = 0.0

        return stats

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


# Global database manager instance (lazy loaded)
_db_manager: DatabaseManager | None = None


async def get_db(reload: bool = False) -> DatabaseManager:
    """
    Get global database manager (singleton pattern)

    Args:
        reload: Force reload

    Returns:
        DatabaseManager instance
    """
    global _db_manager

    if _db_manager is None or reload:
        _db_manager = DatabaseManager()
        await _db_manager.connect()

    return _db_manager


if __name__ == "__main__":
    import asyncio

    async def test():
        """Test database operations"""
        print("Testing database operations...")

        async with DatabaseManager() as db:
            # Get stats
            stats = await db.get_stats()
            print(f"[OK] Database stats: {stats}")

            # List documents
            docs = await db.list_documents(limit=5)
            print(f"[OK] Found {len(docs)} documents")

            for doc in docs:
                print(f"  - {doc['filename']} (ID: {doc['id']})")

    asyncio.run(test())
