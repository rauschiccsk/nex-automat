#!/usr/bin/env python3
"""
Script 10: Test RAG Module Connection
Session: RAG Implementation Phase 2

Tests all RAG modules and database connection
Location: scripts/10_test_rag_connection.py
"""

import sys
import asyncio
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel


def print_header(text):
    """Print formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def print_step(num, text):
    """Print formatted step"""
    print(f"\n{num}. {text}")
    print("-" * 60)


async def main():
    print_header("Script 10: Test RAG Module Connection")

    # Step 1: Test config loading
    print_step(1, "Testing config loading")
    try:
        config = get_config()
        print(f"✓ Config loaded")
        print(f"  Database: {config.database.host}:{config.database.port}")
        print(f"  Embedding model: {config.embedding.model_name}")
        print(f"  Vector dimension: {config.embedding.dimension}")
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return 1

    # Step 2: Test embedding model
    print_step(2, "Testing embedding model")
    try:
        model = EmbeddingModel()
        model.load()
        print(f"✓ Embedding model loaded")
        print(f"  Dimension: {model.dimension}")
        print(f"  Device: {model.device}")

        # Test embedding
        test_text = "This is a test sentence."
        embedding = model.encode(test_text)
        print(f"✓ Test embedding generated: shape={embedding.shape}")
    except Exception as e:
        print(f"✗ Embedding model failed: {e}")
        return 1

    # Step 3: Test database connection
    print_step(3, "Testing database connection")
    try:
        db = DatabaseManager()
        await db.connect()
        print(f"✓ Database connected")

        # Test stats query
        stats = await db.get_stats()
        print(f"✓ Database stats retrieved:")
        print(f"  Documents: {stats['document_count']}")
        print(f"  Chunks: {stats['chunk_count']}")
        print(f"  Avg chunks/doc: {stats['avg_chunks_per_doc']:.2f}")

        await db.close()
        print(f"✓ Database connection closed")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Check PostgreSQL is running")
        print("  2. Verify database 'nex_automat_rag' exists")
        print("  3. Check password in config/rag_config.yaml")
        print("  4. Verify pgvector extension is installed")
        return 1

    # Summary
    print_header("Script 10 Complete")
    print("✓ Config loading: OK")
    print("✓ Embedding model: OK")
    print("✓ Database connection: OK")
    print("\n✅ All RAG modules are working correctly!")
    print("\nNext step: Test full indexing pipeline")
    print("  python -m tools.rag.indexer")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))