#!/usr/bin/env python3
"""
Script 11: Create RAG Database Tables
Session: RAG Implementation Phase 2

Creates all necessary tables for RAG system
Location: scripts/11_create_rag_tables.py
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncpg
from tools.rag.config import get_config

# SQL for creating tables
CREATE_TABLES_SQL = """
-- Enable pgvector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chunks table with vector embeddings
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);

-- Keywords table for hybrid search
CREATE TABLE IF NOT EXISTS keywords (
    id SERIAL PRIMARY KEY,
    chunk_id INTEGER NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
    keyword VARCHAR(100) NOT NULL,
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search history table
CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    results_count INTEGER,
    avg_similarity FLOAT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 64);
CREATE INDEX IF NOT EXISTS idx_keywords_chunk_id ON keywords(chunk_id);
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);
CREATE INDEX IF NOT EXISTS idx_search_history_created_at ON search_history(created_at);

-- Create function for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for documents table
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""


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
    print_header("Script 11: Create RAG Database Tables")

    # Load config
    config = get_config()
    db_config = config.database

    print(f"Database: {db_config.host}:{db_config.port}/{db_config.database}")
    print(f"User: {db_config.user}")
    print()

    # Connect to database
    print_step(1, "Connecting to database")

    try:
        conn = await asyncpg.connect(
            host=db_config.host,
            port=db_config.port,
            database=db_config.database,
            user=db_config.user,
            password=db_config.password
        )
        print("✓ Connected to database")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return 1

    # Create tables
    print_step(2, "Creating tables and indexes")

    try:
        # Execute SQL
        await conn.execute(CREATE_TABLES_SQL)
        print("✓ Tables created successfully")
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        await conn.close()
        return 1

    # Verify tables
    print_step(3, "Verifying tables")

    tables = ['documents', 'chunks', 'keywords', 'search_history']

    for table in tables:
        query = """
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = $1
        """
        count = await conn.fetchval(query, table)

        if count > 0:
            print(f"✓ Table '{table}' exists")
        else:
            print(f"✗ Table '{table}' not found")

    # Verify pgvector extension
    print_step(4, "Verifying pgvector extension")

    query = """
        SELECT COUNT(*) 
        FROM pg_extension 
        WHERE extname = 'vector'
    """
    count = await conn.fetchval(query)

    if count > 0:
        print("✓ pgvector extension is installed")
    else:
        print("✗ pgvector extension not found")

    # Check indexes
    print_step(5, "Verifying indexes")

    query = """
        SELECT indexname 
        FROM pg_indexes 
        WHERE tablename = 'chunks' AND indexname LIKE '%embedding%'
    """
    indexes = await conn.fetch(query)

    if indexes:
        print(f"✓ Vector index created: {indexes[0]['indexname']}")
    else:
        print("⚠ Vector index not found (may be creating in background)")

    # Close connection
    await conn.close()
    print("\n✓ Database connection closed")

    # Summary
    print_header("Script 11 Complete")
    print("✓ All tables created")
    print("✓ Indexes created")
    print("✓ Triggers created")
    print("\n✅ Database is ready for RAG operations!")
    print("\nNext step: Test RAG connection again")
    print("  python scripts/10_test_rag_connection.py")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))