#!/usr/bin/env python3
"""
Fix database.py - remove wrongly placed imports.
"""

from pathlib import Path

db_file = Path(r"C:\Development\nex-automat\tools\rag\database.py")
content = db_file.read_text(encoding='utf-8')

# Remove the wrongly placed "import json" lines inside methods
# These appear after "import numpy as np" inside methods
content = content.replace(
    "        import numpy as np\nimport json\n        if isinstance(embedding",
    "        if isinstance(embedding"
)

content = content.replace(
    "        import numpy as np\nimport json\n        if isinstance(query_embedding",
    "        if isinstance(query_embedding"
)

db_file.write_text(content, encoding='utf-8')
print("✓ database.py fixed - removed wrongly placed imports")