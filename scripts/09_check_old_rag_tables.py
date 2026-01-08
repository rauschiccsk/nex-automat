"""
Session Script 09: Check Old RAG Tables (documents, chunks)
Projekt: nex-automat
Dočasný skript - diagnostika starých RAG tabuliek
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


def diagnose_old_tables():
    """Diagnose old RAG tables (documents, chunks)"""

    print_header("🔍 DIAGNOSTIKA STARÝCH RAG TABULIEK")

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Check documents table
        print_header("1. Tabuľka 'documents'")
        cursor.execute("SELECT COUNT(*) as total FROM documents")
        result = cursor.fetchone()
        print_info(f"Total documents: {result['total']}")

        if result['total'] > 0:
            # Show columns
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'documents'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print_success(f"Columns: {', '.join([c['column_name'] for c in columns])}")

            # Show sample
            cursor.execute("SELECT * FROM documents LIMIT 3")
            samples = cursor.fetchall()
            for i, doc in enumerate(samples, 1):
                print(f"\n{Colors.YELLOW}Document {i}:{Colors.RESET}")
                for key, value in doc.items():
                    print(f"  {key}: {value}")

        # 2. Check chunks table
        print_header("2. Tabuľka 'chunks'")
        cursor.execute("SELECT COUNT(*) as total FROM chunks")
        result = cursor.fetchone()
        print_info(f"Total chunks: {result['total']}")

        if result['total'] > 0:
            # Show columns
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'chunks'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print_success(f"Columns: {', '.join([c['column_name'] for c in columns])}")

        # 3. Check for UAE content
        print_header("3. UAE dokumenty v 'documents'")
        cursor.execute("""
            SELECT 
                id,
                metadata->>'tenant' as tenant,
                metadata->>'source' as source,
                metadata
            FROM documents
            WHERE metadata->>'tenant' = 'uae'
            LIMIT 5
        """)
        uae_docs = cursor.fetchall()

        if uae_docs:
            print_success(f"Found {len(uae_docs)} UAE documents")
            for doc in uae_docs:
                print(f"\n{Colors.YELLOW}Document ID {doc['id']}:{Colors.RESET}")
                print(f"  Tenant: {doc['tenant']}")
                print(f"  Source: {doc['source']}")
                print(f"  Metadata: {doc['metadata']}")
        else:
            print_error("No UAE documents found!")

        # 4. Check UAE chunks
        print_header("4. UAE chunks v 'chunks'")
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE d.metadata->>'tenant' = 'uae'
        """)
        result = cursor.fetchone()
        print_info(f"UAE chunks: {result['count']}")

        if result['count'] > 0:
            # Sample chunks
            cursor.execute("""
                SELECT 
                    c.id,
                    c.document_id,
                    c.chunk_index,
                    d.metadata->>'source' as source,
                    LEFT(c.content, 100) as content_preview
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE d.metadata->>'tenant' = 'uae'
                LIMIT 3
            """)
            samples = cursor.fetchall()

            for i, chunk in enumerate(samples, 1):
                print(f"\n{Colors.YELLOW}Chunk {i}:{Colors.RESET}")
                print(f"  Chunk ID: {chunk['id']}")
                print(f"  Document ID: {chunk['document_id']}")
                print(f"  Chunk Index: {chunk['chunk_index']}")
                print(f"  Source: {chunk['source']}")
                print(f"  Content: {chunk['content_preview']}...")

        # 5. Count by tenant
        print_header("5. Dokumenty podľa tenanta")
        cursor.execute("""
            SELECT 
                metadata->>'tenant' as tenant,
                COUNT(*) as count
            FROM documents
            GROUP BY metadata->>'tenant'
            ORDER BY count DESC
        """)
        results = cursor.fetchall()

        if results:
            for row in results:
                tenant = row['tenant'] if row['tenant'] else 'NULL'
                print_info(f"Tenant '{tenant}': {row['count']} documents")

        # 6. UAE sources
        print_header("6. UAE zdroje (source files)")
        cursor.execute("""
            SELECT 
                metadata->>'source' as source,
                COUNT(*) as chunk_count
            FROM documents d
            JOIN chunks c ON d.id = c.document_id
            WHERE d.metadata->>'tenant' = 'uae'
            GROUP BY metadata->>'source'
            ORDER BY chunk_count DESC
        """)
        sources = cursor.fetchall()

        if sources:
            print_success(f"Found {len(sources)} UAE source files")
            for src in sources:
                print(f"  {src['source']}: {src['chunk_count']} chunks")
        else:
            print_error("No UAE sources found!")

        cursor.close()

    except Exception as e:
        print_error(f"Diagnostic query failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

    print_header("📊 DIAGNOSTIKA DOKONČENÁ")


if __name__ == "__main__":
    try:
        diagnose_old_tables()
    except KeyboardInterrupt:
        print_warning("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nFailed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)