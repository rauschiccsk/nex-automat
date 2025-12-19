"""
Add tenant detection to RAG indexer.

Updates indexer.py to detect tenant from file path and add to metadata.
"""
from pathlib import Path

INDEXER_FILE = Path(r"C:\Development\nex-automat\tools\rag\indexer.py")


def main():
    print("=" * 60)
    print("Add Tenant Detection to RAG Indexer")
    print("=" * 60)

    content = INDEXER_FILE.read_text(encoding="utf-8")

    # Check if already done
    if "detect_tenant" in content:
        print("\n✅ Tenant detection already added!")
        return

    # 1. Add detect_tenant function after imports
    IMPORT_MARKER = "from .chunker import DocumentChunker"

    TENANT_FUNCTION = '''from .chunker import DocumentChunker


def detect_tenant(filepath: Path) -> str | None:
    """
    Detect tenant from file path.
    
    Rules:
    - docs/knowledge/tenants/icc/... → 'icc'
    - docs/knowledge/tenants/andros/... → 'andros'  
    - Other paths → None (shared/all tenants)
    """
    path_str = str(filepath).replace("\\\\", "/").lower()
    
    if "/tenants/" in path_str:
        parts = path_str.split("/tenants/")
        if len(parts) > 1:
            tenant = parts[1].split("/")[0]
            if tenant in ["icc", "andros"]:
                return tenant
    
    return None'''

    if IMPORT_MARKER in content:
        content = content.replace(IMPORT_MARKER, TENANT_FUNCTION)
        print("✅ Added detect_tenant() function")
    else:
        print("❌ Could not find import marker")
        return

    # 2. Update index_file to use tenant detection
    OLD_INDEX_FILE = '''        # Add filepath to metadata
        if metadata is None:
            metadata = {}
        metadata['filepath'] = str(filepath.absolute())
        metadata['file_size'] = filepath.stat().st_size'''

    NEW_INDEX_FILE = '''        # Add filepath and tenant to metadata
        if metadata is None:
            metadata = {}
        metadata['filepath'] = str(filepath.absolute())
        metadata['file_size'] = filepath.stat().st_size
        
        # Detect tenant from path
        tenant = detect_tenant(filepath)
        if tenant:
            metadata['tenant'] = tenant'''

    if OLD_INDEX_FILE in content:
        content = content.replace(OLD_INDEX_FILE, NEW_INDEX_FILE)
        print("✅ Updated index_file() with tenant detection")
    else:
        print("⚠️  index_file pattern not found - may need manual update")

    # Write changes
    INDEXER_FILE.write_text(content, encoding="utf-8")

    print(f"\n✅ Updated: {INDEXER_FILE}")
    print("\nTenant detection rules:")
    print("  docs/knowledge/tenants/icc/*    → tenant='icc'")
    print("  docs/knowledge/tenants/andros/* → tenant='andros'")
    print("  Other paths                     → tenant=None (shared)")


if __name__ == "__main__":
    main()