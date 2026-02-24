#!/usr/bin/env python3
"""
A2: Batch ingest knowledge documents into Qdrant via direct API.
Reads manifest.json and ingests documents into appropriate tenant collections.
"""

import asyncio
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

import httpx

# Configuration
QDRANT_URL = "http://localhost:9130"
OLLAMA_URL = "http://localhost:9132"
EMBEDDING_MODEL = "nomic-embed-text"
KNOWLEDGE_DIR = Path("/opt/nex-automat-src/docs/knowledge-import")
MANIFEST_PATH = Path("/opt/nex-automat-src/docs/manifest.json")

# Chunk settings
CHUNK_SIZE = 1500  # chars per chunk
CHUNK_OVERLAP = 200  # overlap between chunks


def resolve_filepath(rel_path: str) -> Path | None:
    """
    Resolve filepath handling both forward and backslash formats.
    ZIP extracted files have backslashes in filenames on Linux.
    """
    # Try direct path first (forward slashes)
    direct = KNOWLEDGE_DIR / rel_path
    if direct.exists():
        return direct

    # Try with backslashes (how ZIP extracted them)
    backslash_name = rel_path.replace("/", "\\")
    backslash_path = KNOWLEDGE_DIR / backslash_name
    if backslash_path.exists():
        return backslash_path

    # Try just the filename (for root-level files)
    filename = rel_path.split("/")[-1]
    root_file = KNOWLEDGE_DIR / filename
    if root_file.exists():
        return root_file

    return None


async def get_embedding(text: str) -> list[float]:
    """Get embedding from Ollama."""
    async with httpx.AsyncClient(timeout=120) as client:
        # Truncate to ~2000 tokens (~8000 chars) for nomic-embed-text
        truncated = text[:8000]
        response = await client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBEDDING_MODEL, "prompt": truncated},
        )
        response.raise_for_status()
        return response.json()["embedding"]


async def ingest_to_qdrant(collection: str, doc_id: str, text: str, metadata: dict):
    """Ingest single document into Qdrant collection."""
    # Generate deterministic point ID from doc path
    point_id = int(hashlib.md5(doc_id.encode()).hexdigest()[:16], 16) % (2**63)

    embedding = await get_embedding(text)

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.put(
            f"{QDRANT_URL}/collections/{collection}/points",
            json={
                "points": [
                    {
                        "id": point_id,
                        "vector": embedding,
                        "payload": {
                            "content": text[:10000],  # Store first 10K chars
                            "filename": doc_id,
                            "tenant": metadata.get("tenant", ""),
                            "ingested_at": datetime.now().isoformat(),
                            **metadata,
                        },
                    }
                ]
            },
        )
        response.raise_for_status()


def chunk_document(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """Split document into chunks for better RAG retrieval."""
    # Split by sections (## headers) first
    sections = text.split("\n## ")
    chunks = []

    for i, section in enumerate(sections):
        if i > 0:
            section = "## " + section

        # If section is small enough, keep as one chunk
        if len(section) <= chunk_size:
            if section.strip():
                chunks.append(section.strip())
        else:
            # Split large sections by words
            words = section.split()
            current_chunk = []
            current_len = 0

            for word in words:
                current_chunk.append(word)
                current_len += len(word) + 1

                if current_len >= chunk_size:
                    chunks.append(" ".join(current_chunk))
                    # Overlap: keep last N chars worth of words
                    overlap_words = " ".join(current_chunk).split()[-30:]
                    current_chunk = overlap_words
                    current_len = sum(len(w) + 1 for w in current_chunk)

            if current_chunk:
                chunk_text = " ".join(current_chunk)
                if chunk_text.strip():
                    chunks.append(chunk_text)

    return [c for c in chunks if len(c.strip()) > 50]  # Skip tiny chunks


async def main():
    start_time = datetime.now()

    # Load manifest
    if not MANIFEST_PATH.exists():
        print(f"ERROR: Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    print(f"{'=' * 60}")
    print("  A2: Batch Ingest Knowledge Documents")
    print(f"{'=' * 60}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Knowledge dir: {KNOWLEDGE_DIR}")
    print(f"Total files in manifest: {manifest['total_files']}")
    print()

    # Verify Qdrant connectivity
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{QDRANT_URL}/collections")
            collections = resp.json()["result"]["collections"]
            print(f"Qdrant collections: {[c['name'] for c in collections]}")
    except Exception as e:
        print(f"ERROR: Cannot connect to Qdrant: {e}")
        sys.exit(1)

    # Verify Ollama connectivity
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            models = [m["name"] for m in resp.json()["models"]]
            print(f"Ollama models: {models}")
    except Exception as e:
        print(f"ERROR: Cannot connect to Ollama: {e}")
        sys.exit(1)

    print()

    stats = {"total": 0, "success": 0, "errors": 0, "skipped": 0, "chunks": 0}
    errors_list = []

    for tenant, tenant_data in manifest["tenants"].items():
        files = tenant_data["files"]
        print(f"\n{'─' * 40}")
        print(f"Tenant: {tenant} ({len(files)} files)")
        print(f"{'─' * 40}")

        for i, rel_path in enumerate(files, 1):
            filepath = resolve_filepath(rel_path)

            if filepath is None:
                if i <= 5 or i == len(files):
                    print(f"  [{i:3d}/{len(files)}] SKIP (not found): {rel_path}")
                stats["skipped"] += 1
                continue

            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")

                if len(text.strip()) < 100:
                    stats["skipped"] += 1
                    continue

                chunks = chunk_document(text)

                for j, chunk in enumerate(chunks):
                    doc_id = f"{rel_path}#chunk{j}"
                    await ingest_to_qdrant(
                        collection=tenant,
                        doc_id=doc_id,
                        text=chunk,
                        metadata={
                            "tenant": tenant,
                            "source_file": rel_path,
                            "chunk_index": j,
                            "total_chunks": len(chunks),
                        },
                    )
                    stats["chunks"] += 1

                stats["success"] += 1

                # Progress reporting
                if i % 50 == 0 or i == len(files):
                    print(
                        f"  [{i:3d}/{len(files)}] Progress: {stats['success']} files, {stats['chunks']} chunks"
                    )

            except Exception as e:
                error_msg = f"{rel_path}: {str(e)[:50]}"
                errors_list.append(error_msg)
                if len(errors_list) <= 5:
                    print(f"  [{i:3d}/{len(files)}] ERROR: {error_msg}")
                stats["errors"] += 1

            stats["total"] += 1

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{'=' * 60}")
    print("  INGEST COMPLETE")
    print(f"{'=' * 60}")
    print(f"Duration: {duration}")
    print(f"Files processed: {stats['total']}")
    print(f"  - Success: {stats['success']}")
    print(f"  - Skipped: {stats['skipped']}")
    print(f"  - Errors: {stats['errors']}")
    print(f"Total chunks ingested: {stats['chunks']}")

    if errors_list and len(errors_list) > 5:
        print(f"\nFirst 5 errors shown, {len(errors_list) - 5} more errors occurred")

    # Final verification
    print(f"\n{'─' * 40}")
    print("Collection Statistics")
    print(f"{'─' * 40}")
    async with httpx.AsyncClient(timeout=10) as client:
        for tenant in manifest["tenants"]:
            try:
                resp = await client.get(f"{QDRANT_URL}/collections/{tenant}")
                info = resp.json()["result"]
                print(
                    f"  {tenant}: {info['points_count']} points, status={info['status']}"
                )
            except Exception as e:
                print(f"  {tenant}: ERROR - {e}")


if __name__ == "__main__":
    asyncio.run(main())
