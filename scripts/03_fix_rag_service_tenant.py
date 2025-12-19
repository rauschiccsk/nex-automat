"""
Fix RAG Service to pass tenant parameter to RAG API.

Current issue: tenant parameter exists but is not sent to API.
"""
from pathlib import Path

RAG_SERVICE = Path(r"C:\Development\nex-automat\apps\nex-brain\api\services\rag_service.py")

# The fix: add tenant to params when calling RAG API
OLD_CODE = '''        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": query, "limit": limit}
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )'''

NEW_CODE = '''        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": query, "limit": limit}
                if tenant:
                    params["tenant"] = tenant
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )'''


def main():
    print("=" * 60)
    print("Fix RAG Service - Pass tenant to API")
    print("=" * 60)

    content = RAG_SERVICE.read_text(encoding="utf-8")

    if OLD_CODE not in content:
        if NEW_CODE in content:
            print("\n✅ Already fixed!")
            return
        else:
            print("\n❌ Pattern not found - manual fix needed")
            return

    content = content.replace(OLD_CODE, NEW_CODE)
    RAG_SERVICE.write_text(content, encoding="utf-8")

    print(f"\n✅ Fixed: {RAG_SERVICE}")
    print("\nNow tenant parameter is passed to RAG API:")
    print("  /search?query=...&tenant=icc")


if __name__ == "__main__":
    main()