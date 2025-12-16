#!/usr/bin/env python
"""
Script 12: Fix database.py for pgvector compatibility
Fixes embedding format conversion for asyncpg + pgvector.
"""

from pathlib import Path


def fix_database_py():
    """Fix database.py to use string format for pgvector."""

    db_file = Path("tools/rag/database.py")

    if not db_file.exists():
        print(f"❌ File not found: {db_file}")
        return False

    content = db_file.read_text(encoding='utf-8')
    original = content

    # Fix 1: insert_chunk - proper conversion to pgvector string
    old_code = """        # Convert numpy array to pgvector string format
        if hasattr(embedding, 'tolist'):
            embedding_list = embedding.tolist()
        else:
            embedding_list = list(embedding)
        embedding_str = '[' + ','.join(str(x) for x in embedding_list) + ']'"""

    new_code = """        # Convert numpy array to pgvector string format
        import numpy as np
        if isinstance(embedding, np.ndarray):
            # Flatten if 2D and convert to list
            if embedding.ndim > 1:
                embedding = embedding.flatten()
            embedding_list = embedding.tolist()
        elif hasattr(embedding, 'tolist'):
            embedding_list = embedding.tolist()
        else:
            embedding_list = list(embedding)
        # Create pgvector format string
        embedding_str = '[' + ','.join(str(float(x)) for x in embedding_list) + ']'"""

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("  ✓ Fixed insert_chunk: proper numpy to pgvector string")
    else:
        print("  ⚠ insert_chunk pattern not found - trying alternative fix")
        # Try original pattern
        old_original = """        # Convert numpy array to list for pgvector
        embedding_list = embedding.tolist()"""

        if old_original in content:
            content = content.replace(old_original, new_code)
            print("  ✓ Fixed insert_chunk from original pattern")

    # Fix 2: search_similar - proper conversion
    old_search = """        if hasattr(query_embedding, 'tolist'):
            embedding_list = query_embedding.tolist()
        else:
            embedding_list = list(query_embedding)
        embedding_str = '[' + ','.join(str(x) for x in embedding_list) + ']'"""

    new_search = """        import numpy as np
        if isinstance(query_embedding, np.ndarray):
            if query_embedding.ndim > 1:
                query_embedding = query_embedding.flatten()
            embedding_list = query_embedding.tolist()
        elif hasattr(query_embedding, 'tolist'):
            embedding_list = query_embedding.tolist()
        else:
            embedding_list = list(query_embedding)
        embedding_str = '[' + ','.join(str(float(x)) for x in embedding_list) + ']'"""

    if old_search in content:
        content = content.replace(old_search, new_search)
        print("  ✓ Fixed search_similar: proper numpy to pgvector string")

    # Check if anything changed
    if content == original:
        print("\n⚠ No changes made - file may already be fixed or patterns differ")
        return False

    # Write changes
    db_file.write_text(content, encoding='utf-8')
    print(f"\n✓ File updated: {db_file}")

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Fixing database.py for pgvector compatibility")
    print("=" * 50)
    print()

    success = fix_database_py()

    if success:
        print("\n✅ Fix complete! Run test again:")
        print("   python scripts/11_test_rag_indexer.py")
    else:
        print("\n⚠ Manual fix may be needed")