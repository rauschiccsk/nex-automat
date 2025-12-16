"""
RAG (Retrieval-Augmented Generation) Module
NEX Automat Project

Provides document indexing, embedding, and semantic search capabilities
using PostgreSQL with pgvector extension.

Components:
- config: Configuration management
- database: PostgreSQL operations with pgvector
- embeddings: Sentence transformer embeddings
- chunker: Document chunking utilities
- indexer: Document indexing pipeline
- search: Vector and hybrid search
"""

__version__ = "0.1.0"
