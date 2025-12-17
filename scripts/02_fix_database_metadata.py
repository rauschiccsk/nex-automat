#!/usr/bin/env python3
"""
Fix database.py metadata serialization.
Converts dict metadata to JSON string for asyncpg.
"""

from pathlib import Path

# File to patch
db_file = Path(r"C:\Development\nex-automat\tools\rag\database.py")

content = db_file.read_text(encoding='utf-8')

# Check if json import exists
if "import json" not in content:
    # Add json import after other imports
    content = content.replace(
        "import numpy as np",
        "import numpy as np\nimport json"
    )
    print("✓ Added json import")

# Fix insert_document - serialize metadata
old_insert_doc = '''doc_id = await self.pool.fetchval(query, filename, content, metadata)'''
new_insert_doc = '''metadata_json = json.dumps(metadata) if metadata else None
        doc_id = await self.pool.fetchval(query, filename, content, metadata_json)'''

if old_insert_doc in content:
    content = content.replace(old_insert_doc, new_insert_doc)
    print("✓ Fixed insert_document metadata serialization")
else:
    print("⚠ insert_document already patched or not found")

# Fix insert_chunk - serialize metadata
old_insert_chunk = '''chunk_id = await self.pool.fetchval(
            query,
            document_id,
            chunk_index,
            content,
            embedding_str,
            metadata
        )'''

new_insert_chunk = '''metadata_json = json.dumps(metadata) if metadata else None
        chunk_id = await self.pool.fetchval(
            query,
            document_id,
            chunk_index,
            content,
            embedding_str,
            metadata_json
        )'''

if old_insert_chunk in content:
    content = content.replace(old_insert_chunk, new_insert_chunk)
    print("✓ Fixed insert_chunk metadata serialization")
else:
    print("⚠ insert_chunk already patched or not found")

# Save
db_file.write_text(content, encoding='utf-8')
print()
print("✓ database.py patched successfully")