#!/usr/bin/env python
"""
Script 16: Validate RAG Chunks
Validates chunk sizes, token counts, and overlap quality.
"""

import asyncio
import sys
import json
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.chunker import DocumentChunker


async def validate_chunks():
    """Validate chunk quality and statistics."""
    print("=" * 60)
    print("RAG CHUNK VALIDATION - Phase 3.4")
    print("=" * 60)
    print()

    config = get_config()
    db = DatabaseManager(config.database)
    chunker = DocumentChunker(config.chunking)

    await db.connect()

    # Get all chunks with document info
    chunks = await db.pool.fetch("""
        SELECT 
            c.id, c.document_id, c.chunk_index, c.content, c.metadata,
            d.filename
        FROM chunks c
        JOIN documents d ON c.document_id = d.id
        ORDER BY c.document_id, c.chunk_index
    """)

    print(f"Total chunks: {len(chunks)}\n")
    print(f"Config: chunk_size={config.chunking.chunk_size}, overlap={config.chunking.chunk_overlap}\n")

    # Analyze each document
    current_doc = None
    doc_chunks = []
    all_token_counts = []

    for chunk in chunks:
        if current_doc != chunk['document_id']:
            if doc_chunks:
                analyze_document_chunks(doc_chunks, chunker, config)
            current_doc = chunk['document_id']
            doc_chunks = []
        doc_chunks.append(chunk)

        # Count tokens
        tokens = chunker.count_tokens(chunk['content'])
        all_token_counts.append(tokens)

    # Last document
    if doc_chunks:
        analyze_document_chunks(doc_chunks, chunker, config)

    # Overall statistics
    print("\n" + "=" * 60)
    print("OVERALL STATISTICS")
    print("=" * 60)

    if all_token_counts:
        avg_tokens = sum(all_token_counts) / len(all_token_counts)
        min_tokens = min(all_token_counts)
        max_tokens = max(all_token_counts)

        print(f"Token counts:")
        print(f"  Average: {avg_tokens:.0f}")
        print(f"  Min: {min_tokens}")
        print(f"  Max: {max_tokens}")
        print(f"  Target: {config.chunking.chunk_size}")

        # Distribution
        under_500 = sum(1 for t in all_token_counts if t < 500)
        between_500_1000 = sum(1 for t in all_token_counts if 500 <= t < 1000)
        between_1000_1500 = sum(1 for t in all_token_counts if 1000 <= t < 1500)
        over_1500 = sum(1 for t in all_token_counts if t >= 1500)

        print(f"\nDistribution:")
        print(f"  < 500 tokens: {under_500} ({under_500 / len(all_token_counts) * 100:.0f}%)")
        print(f"  500-1000 tokens: {between_500_1000} ({between_500_1000 / len(all_token_counts) * 100:.0f}%)")
        print(f"  1000-1500 tokens: {between_1000_1500} ({between_1000_1500 / len(all_token_counts) * 100:.0f}%)")
        print(f"  > 1500 tokens: {over_1500} ({over_1500 / len(all_token_counts) * 100:.0f}%)")

    await db.close()

    print("\n✅ Validation complete!")
    return True


def analyze_document_chunks(chunks, chunker, config):
    """Analyze chunks for a single document."""
    doc_name = chunks[0]['filename']
    print(f"📄 {doc_name}")
    print(f"   Chunks: {len(chunks)}")

    token_counts = []
    for chunk in chunks:
        tokens = chunker.count_tokens(chunk['content'])
        token_counts.append(tokens)

    print(
        f"   Tokens per chunk: {min(token_counts)}-{max(token_counts)} (avg: {sum(token_counts) / len(token_counts):.0f})")

    # Check overlap between consecutive chunks
    if len(chunks) > 1:
        overlaps = []
        for i in range(len(chunks) - 1):
            c1 = chunks[i]['content']
            c2 = chunks[i + 1]['content']

            # Find overlap by checking end of c1 vs start of c2
            overlap_chars = find_overlap(c1, c2)
            overlaps.append(overlap_chars)

        if overlaps:
            avg_overlap = sum(overlaps) / len(overlaps)
            print(f"   Overlap chars: {min(overlaps)}-{max(overlaps)} (avg: {avg_overlap:.0f})")

    print()


def find_overlap(text1, text2, min_overlap=50):
    """Find character overlap between end of text1 and start of text2."""
    max_check = min(len(text1), len(text2), 2000)

    for i in range(min_overlap, max_check):
        if text1[-i:] == text2[:i]:
            return i

    # No exact match, try approximate
    end_of_1 = text1[-500:] if len(text1) > 500 else text1
    start_of_2 = text2[:500] if len(text2) > 500 else text2

    # Check for common substring
    for length in range(min(200, len(end_of_1), len(start_of_2)), min_overlap, -10):
        if end_of_1[-length:] in start_of_2[:length * 2]:
            return length

    return 0


if __name__ == "__main__":
    try:
        asyncio.run(validate_chunks())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)