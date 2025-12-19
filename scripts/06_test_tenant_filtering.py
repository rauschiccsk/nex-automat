"""
Test tenant filtering end-to-end.

1. Create test documents for ICC and ANDROS
2. Index them with tenant metadata
3. Test RAG API filtering
"""
import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")
sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag.indexer import DocumentIndexer
from tools.rag.database import DatabaseManager
import httpx

# Test documents
ICC_DOC = """# ICC Interné Procesy

## Firemná kultúra ICC

ICC Komárno je softvérová spoločnosť založená v roku 1990.
Špecializujeme sa na ERP systémy pre stredné a veľké podniky.

## Pracovná doba

- Pondelok - Piatok: 8:00 - 16:30
- Flexibilný začiatok: 7:00 - 9:00
- Home office: max 2 dni týždenne

## Kontakty

- IT podpora: it@icc.sk
- HR oddelenie: hr@icc.sk
"""

ANDROS_DOC = """# ANDROS Interné Procesy

## O spoločnosti ANDROS

ANDROS s.r.o. je distribučná spoločnosť so sídlom v Bratislave.
Zameriavame sa na distribúciu potravín a nápojov.

## Pracovná doba

- Pondelok - Piatok: 7:00 - 15:30
- Sklad: 6:00 - 22:00 (zmeny)
- Víkendy: podľa potreby

## Kontakty

- Sklad: sklad@andros.sk
- Objednávky: objednavky@andros.sk
"""

SHARED_DOC = """# Zdieľané pravidlá BOZP

## Bezpečnosť a ochrana zdravia pri práci

Tieto pravidlá platia pre všetkých zamestnancov bez ohľadu na spoločnosť.

## Základné pravidlá

1. Nosenie ochranných pomôcok v sklade
2. Dodržiavanie požiarnych predpisov
3. Hlásenie pracovných úrazov do 24 hodín
"""


async def create_test_documents():
    """Create test documents in tenant directories."""
    print("=" * 60)
    print("STEP 1: Create Test Documents")
    print("=" * 60)

    # ICC document
    icc_dir = PROJECT_ROOT / "docs" / "knowledge" / "tenants" / "icc" / "hr"
    icc_file = icc_dir / "ICC_INTERNE_PROCESY.md"
    icc_file.write_text(ICC_DOC, encoding="utf-8")
    print(f"✅ Created: {icc_file.relative_to(PROJECT_ROOT)}")

    # ANDROS document
    andros_dir = PROJECT_ROOT / "docs" / "knowledge" / "tenants" / "andros" / "hr"
    andros_file = andros_dir / "ANDROS_INTERNE_PROCESY.md"
    andros_file.write_text(ANDROS_DOC, encoding="utf-8")
    print(f"✅ Created: {andros_file.relative_to(PROJECT_ROOT)}")

    # Shared document
    shared_dir = PROJECT_ROOT / "docs" / "knowledge" / "shared"
    shared_file = shared_dir / "BOZP_PRAVIDLA.md"
    shared_file.write_text(SHARED_DOC, encoding="utf-8")
    print(f"✅ Created: {shared_file.relative_to(PROJECT_ROOT)}")

    return [icc_file, andros_file, shared_file]


async def index_test_documents(files):
    """Index test documents to RAG."""
    print("\n" + "=" * 60)
    print("STEP 2: Index Documents to RAG")
    print("=" * 60)

    async with DocumentIndexer() as indexer:
        for filepath in files:
            print(f"\nIndexing: {filepath.name}")
            result = await indexer.index_file(filepath, show_progress=True)
            print(f"  Document ID: {result['document_id']}")
            print(f"  Chunks: {result['chunk_count']}")


async def verify_tenant_metadata():
    """Verify tenant metadata in database."""
    print("\n" + "=" * 60)
    print("STEP 3: Verify Tenant Metadata in DB")
    print("=" * 60)

    db = DatabaseManager()
    await db.connect()

    try:
        # Check documents with tenant
        rows = await db.pool.fetch("""
            SELECT filename, metadata->>'tenant' as tenant
            FROM documents
            WHERE filename LIKE '%PROCESY%' OR filename LIKE '%BOZP%'
            ORDER BY filename
        """)

        print("\nDocuments in database:")
        for row in rows:
            tenant = row['tenant'] or '(shared)'
            print(f"  {row['filename']}: tenant={tenant}")
    finally:
        await db.close()


async def test_rag_api_filtering():
    """Test RAG API tenant filtering."""
    print("\n" + "=" * 60)
    print("STEP 4: Test RAG API Tenant Filtering")
    print("=" * 60)

    base_url = "https://rag-api.icc.sk"
    query = "pracovná doba"

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: No tenant filter (should return all)
        print(f"\n🔍 Query: '{query}' (no tenant filter)")
        resp = await client.get(f"{base_url}/search", params={"query": query, "limit": 5})
        data = resp.json()
        print(f"   Results: {len(data['results'])} documents")
        for r in data['results']:
            print(f"   - {r['filename']} (score: {r['score']:.3f})")

        # Test 2: ICC tenant filter
        print(f"\n🔍 Query: '{query}' (tenant=icc)")
        resp = await client.get(f"{base_url}/search", params={"query": query, "limit": 5, "tenant": "icc"})
        data = resp.json()
        print(f"   Results: {len(data['results'])} documents")
        for r in data['results']:
            print(f"   - {r['filename']} (score: {r['score']:.3f})")

        # Test 3: ANDROS tenant filter
        print(f"\n🔍 Query: '{query}' (tenant=andros)")
        resp = await client.get(f"{base_url}/search", params={"query": query, "limit": 5, "tenant": "andros"})
        data = resp.json()
        print(f"   Results: {len(data['results'])} documents")
        for r in data['results']:
            print(f"   - {r['filename']} (score: {r['score']:.3f})")


async def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " TENANT FILTERING END-TO-END TEST ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    # Step 1: Create test documents
    files = await create_test_documents()

    # Step 2: Index to RAG
    await index_test_documents(files)

    # Step 3: Verify metadata
    await verify_tenant_metadata()

    # Step 4: Test API filtering
    await test_rag_api_filtering()

    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())