#!/usr/bin/env python
"""
Fix rag_service.py - Better detection of implementation phases chunk.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

# Read current content
content = FILE_PATH.read_text(encoding="utf-8")

# Fix the detection - check for IMPLEMENT anywhere, case insensitive
old_line = 'if re.search(r"faz[ae]\\s*[123456]", content) or "## 5. IMPLEMENT" in r.get("content", ""):'
new_line = 'if re.search(r"faz[ae]\\s*[123456]", content) or "IMPLEMENT" in r.get("content", "").upper():'

if old_line in content:
    content = content.replace(old_line, new_line)
    FILE_PATH.write_text(content, encoding="utf-8")
    print("✅ Fixed: IMPLEMENT detection now case-insensitive")
else:
    print("⚠️ Pattern not found, trying alternative...")
    # Try to find and fix
    import re
    pattern = r'if re\.search.*IMPLEMENT.*:'
    matches = re.findall(pattern, content)
    print(f"Found patterns: {matches}")