"""
Script: 01_add_root_path.py
Purpose: Add root_path support to RAG FastAPI server for Cloudflare Tunnel path routing

Usage: python scripts/session/01_add_root_path.py
"""

import sys
from pathlib import Path

def add_root_path():
    """Add root_path="/rag" to FastAPI app in server_app.py"""

    server_app_path = Path("tools/rag/server_app.py")

    if not server_app_path.exists():
        print(f"❌ File not found: {server_app_path}")
        return False

    # Read current content
    content = server_app_path.read_text(encoding='utf-8')

    # Check if already patched
    if 'root_path="/rag"' in content:
        print("✅ Already patched - root_path is present")
        return True

    # Find FastAPI app initialization
    old_line = "app = FastAPI("

    if old_line not in content:
        print(f"❌ Cannot find FastAPI initialization")
        return False

    # Add root_path parameter
    new_content = content.replace(
        'app = FastAPI(',
        'app = FastAPI(\n    root_path="/rag",  # For Cloudflare Tunnel path routing'
    )

    # Write updated content
    server_app_path.write_text(new_content, encoding='utf-8')

    print("✅ Patched server_app.py")
    print("   - Added root_path='/rag' to FastAPI app")
    print("\n📝 Restart RAG server:")
    print("   python -m tools.rag.server start")

    return True

if __name__ == "__main__":
    success = add_root_path()
    sys.exit(0 if success else 1)