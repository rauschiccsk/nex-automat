#!/usr/bin/env python
"""
Fix new_chat.py - Fix subprocess call for rag_update.py
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/new_chat.py")

content = FILE_PATH.read_text(encoding="utf-8")

old_subprocess = '''    # 3. Run rag_update.py --new
    print("\\n🔄 Running RAG update...")
    try:
        result = subprocess.run(
            ["python", "tools/rag/rag_update.py", "--new"],
            cwd=BASE_PATH,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ RAG update complete")
        else:
            print(f"⚠️ RAG update warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️ RAG update skipped: {e}")'''

new_subprocess = '''    # 3. Run rag_update.py --new
    print("\\n🔄 Running RAG update...")
    try:
        import sys
        result = subprocess.run(
            [sys.executable, "tools/rag/rag_update.py", "--new"],
            cwd=BASE_PATH,
            capture_output=False,  # Show output directly
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": str(BASE_PATH)}
        )
        if result.returncode == 0:
            print("✅ RAG update complete")
        else:
            print(f"⚠️ RAG update failed with code {result.returncode}")
    except Exception as e:
        print(f"⚠️ RAG update skipped: {e}")'''

if old_subprocess in content:
    content = content.replace(old_subprocess, new_subprocess)
    FILE_PATH.write_text(content, encoding="utf-8")
    print("✅ Fixed: new_chat.py subprocess call")
    print("   - Uses sys.executable (correct Python)")
    print("   - Sets PYTHONPATH")
    print("   - Shows output directly")
else:
    print("⚠️ Pattern not found, checking...")
    if "rag_update.py" in content:
        idx = content.find("rag_update.py")
        print(content[idx-200:idx+300])