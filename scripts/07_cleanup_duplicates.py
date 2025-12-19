"""
Cleanup duplicate documents in RAG database.

Keeps only the most recent version of each document (by filename).
"""
import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")
sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag.database import DatabaseManager


async def main():
    print("=" * 60)
    print("RAG Database - Cleanup Duplicates")
    print("=" * 60)

    db = DatabaseManager()
    await db.connect()

    try:
        # Find duplicates
        duplicates = await db.pool.fetch("""
            SELECT filename, COUNT(*) as cnt,
                   array_agg(id ORDER BY id DESC) as ids
            FROM documents
            GROUP BY filename
            HAVING COUNT(*) > 1
            ORDER BY filename
        """)

        if not duplicates:
            print("\n✅ No duplicates found!")
            return

        print(f"\nFound {len(duplicates)} filenames with duplicates:\n")

        total_to_delete = 0
        for row in duplicates:
            ids = row['ids']
            keep_id = ids[0]  # Keep newest (highest ID)
            delete_ids = ids[1:]  # Delete older ones
            total_to_delete += len(delete_ids)

            print(f"  {row['filename']}")
            print(f"    Keep: ID {keep_id}")
            print(f"    Delete: IDs {delete_ids}")

        print(f"\nTotal documents to delete: {total_to_delete}")

        # Confirm
        response = input("\nProceed with cleanup? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return

        # Delete duplicates (keep newest)
        deleted = 0
        for row in duplicates:
            ids = row['ids']
            delete_ids = ids[1:]  # Keep first (newest), delete rest

            for doc_id in delete_ids:
                # Delete chunks first
                await db.pool.execute(
                    "DELETE FROM chunks WHERE document_id = $1", doc_id
                )
                # Delete document
                await db.pool.execute(
                    "DELETE FROM documents WHERE id = $1", doc_id
                )
                deleted += 1
                print(f"  Deleted document ID {doc_id}")

        print(f"\n✅ Deleted {deleted} duplicate documents")

        # Show final stats
        doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
        chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
        print(f"\nFinal stats: {doc_count} documents, {chunk_count} chunks")

    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())