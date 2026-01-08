"""
Session Script 02: Diagnose RAG Metadata for UAE Documents
Projekt: nex-automat
Dočasný diagnostický skript
"""

import sys
import os
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        password = os.environ.get('POSTGRES_PASSWORD')
        if not password:
            print_error("POSTGRES_PASSWORD environment variable not set")
            return None

        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="nex_automat_rag",
            user="postgres",
            password=password
        )
        return conn
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        return None


def diagnose_embeddings():
    """Diagnose embeddings table structure and data"""

    print_header("🔍 DIAGNOSTIKA RAG EMBEDDINGS")

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Check total count
        print_header("1. Celkový počet embeddings")
        cursor.execute("SELECT COUNT(*) as total FROM rag_chunks")
        result = cursor.fetchone()
        print_info(f"Total embeddings: {result['total']}")

        # 2. Count by tenant
        print_header("2. Počet embeddings podľa tenanta")
        cursor.execute("""
            SELECT 
                metadata->>'tenant' as tenant,
                COUNT(*) as count
            FROM rag_chunks
            GROUP BY metadata->>'tenant'
            ORDER BY count DESC
        """)
        results = cursor.fetchall()

        if results:
            for row in results:
                tenant = row['tenant'] if row['tenant'] else 'NULL'
                print_info(f"Tenant '{tenant}': {row['count']} embeddings")
        else:
            print_warning("No embeddings found")

        # 3. Check UAE specific embeddings
        print_header("3. UAE tenant embeddings - vzorka")
        cursor.execute("""
            SELECT 
                id,
                metadata->>'tenant' as tenant,
                metadata->>'source' as source,
                metadata->>'chunk_index' as chunk_index,
                LEFT(content, 100) as content_preview
            FROM rag_chunks
            WHERE metadata->>'tenant' = 'uae'
            LIMIT 5
        """)
        results = cursor.fetchall()

        if results:
            print_success(f"Found {len(results)} UAE embeddings")
            for i, row in enumerate(results, 1):
                print(f"\n{Colors.YELLOW}Sample {i}:{Colors.RESET}")
                print(f"  ID: {row['id']}")
                print(f"  Tenant: {row['tenant']}")
                print(f"  Source: {row['source']}")
                print(f"  Chunk: {row['chunk_index']}")
                print(f"  Content: {row['content_preview']}...")
        else:
            print_error("No UAE embeddings found!")

        # 4. Check all metadata keys
        print_header("4. Dostupné metadata keys")
        cursor.execute("""
            SELECT DISTINCT jsonb_object_keys(metadata) as key
            FROM rag_chunks
            LIMIT 100
        """)
        results = cursor.fetchall()

        if results:
            keys = [row['key'] for row in results]
            print_info(f"Metadata keys: {', '.join(keys)}")
        else:
            print_warning("No metadata keys found")

        # 5. Check embeddings without tenant
        print_header("5. Embeddings bez tenant metadata")
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM rag_chunks
            WHERE metadata->>'tenant' IS NULL
        """)
        result = cursor.fetchone()

        if result['count'] > 0:
            print_warning(f"Found {result['count']} embeddings without tenant!")

            # Show sample
            cursor.execute("""
                SELECT 
                    id,
                    metadata,
                    LEFT(content, 100) as content_preview
                FROM rag_chunks
                WHERE metadata->>'tenant' IS NULL
                LIMIT 3
            """)
            samples = cursor.fetchall()

            for i, row in enumerate(samples, 1):
                print(f"\n{Colors.YELLOW}Sample {i}:{Colors.RESET}")
                print(f"  ID: {row['id']}")
                print(f"  Metadata: {row['metadata']}")
                print(f"  Content: {row['content_preview']}...")
        else:
            print_success("All embeddings have tenant metadata")

        # 6. Check embeddings without source
        print_header("6. Embeddings bez source metadata")
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM rag_chunks
            WHERE metadata->>'source' IS NULL
        """)
        result = cursor.fetchone()

        if result['count'] > 0:
            print_warning(f"Found {result['count']} embeddings without source!")
        else:
            print_success("All embeddings have source metadata")

        # 7. Check UAE documents structure
        print_header("7. UAE dokumenty - zdroje")
        cursor.execute("""
            SELECT 
                metadata->>'source' as source,
                COUNT(*) as chunks
            FROM rag_chunks
            WHERE metadata->>'tenant' = 'uae'
            GROUP BY metadata->>'source'
            ORDER BY chunks DESC
        """)
        results = cursor.fetchall()

        if results:
            print_info(f"UAE documents indexed: {len(results)}")
            for row in results:
                source = row['source'] if row['source'] else 'UNKNOWN'
                print(f"  {source}: {row['chunks']} chunks")
        else:
            print_error("No UAE documents found!")

        cursor.close()

    except Exception as e:
        print_error(f"Diagnostic query failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

    # Summary
    print_header("📊 ZHRNUTIE DIAGNOSTIKY")
    print_info("Kontrola ukončená - pozri výsledky vyššie")


if __name__ == "__main__":
    try:
        diagnose_embeddings()
    except KeyboardInterrupt:
        print_warning("\n\nDiagnostic interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nDiagnostic failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)