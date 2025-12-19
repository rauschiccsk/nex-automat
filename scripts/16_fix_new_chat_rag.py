#!/usr/bin/env python
"""
Fix new_chat.py - Fix RAG subprocess call
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/new_chat.py")

content = FILE_PATH.read_text(encoding="utf-8")

# Find and replace the subprocess section
old_lines = '''            ["python", "tools/rag/rag_update.py", "--new"],
            cwd=BASE_PATH,
            capture_output=True,'''

new_lines = '''            [__import__("sys").executable, "tools/rag/rag_update.py", "--new"],
            cwd=BASE_PATH,
            capture_output=False,'''

if old_lines in content:
    content = content.replace(old_lines, new_lines)
    FILE_PATH.write_text(content, encoding="utf-8")
    print("✅ Fixed: new_chat.py")
    print("   - Uses sys.executable instead of 'python'")
    print("   - Shows RAG output directly (capture_output=False)")
else:
    print("⚠️ Exact pattern not found")
    print("Trying line by line...")

    if '["python", "tools/rag/rag_update.py"' in content:
        content = content.replace(
            '["python", "tools/rag/rag_update.py"',
            '[__import__("sys").executable, "tools/rag/rag_update.py"'
        )
        content = content.replace(
            'capture_output=True,',
            'capture_output=False,'
        )
        FILE_PATH.write_text(content, encoding="utf-8")
        print("✅ Fixed via line-by-line replacement")
    else:
        print("❌ Could not find pattern to replace")