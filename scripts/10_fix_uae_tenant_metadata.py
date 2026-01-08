"""
Session Script 10: Fix UAE Tenant Metadata
Projekt: nex-automat
Dočasný skript - doplniť tenant='uae' do metadata pre UAE dokumenty
"""

import sys
import os
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import json

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


def find_uae_documents(cursor):
    """Find documents that should have tenant='uae'"""
    cursor.execute("""
        SELECT 
            id,
            filename,
            metadata
        FROM documents
        WHERE metadata->>'tenant' IS NULL
        AND (
            metadata->>'filepath' ILIKE '%uae%'
            OR filename ILIKE '%uae%'
        )
    """)
    return cursor.fetchall()


def update_document_metadata(cursor, doc_id, metadata):
    """Update document metadata with tenant='uae'"""
    # Add tenant to metadata
    if metadata is None:
        metadata = {}
    metadata['tenant'] = 'uae'

    cursor.execute("""
        UPDATE documents
        SET 
            metadata = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (json.dumps(metadata), doc_id))


def main():
    print_header("🔧 OPRAVA UAE TENANT METADATA")

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Find UAE documents
        print_header("1. Hľadanie UAE dokumentov bez tenant metadata")
        uae_docs = find_uae_documents(cursor)

        if not uae_docs:
            print_success("Všetky UAE dokumenty už mají správne metadata")
            return

        print_success(f"Nájdených {len(uae_docs)} UAE dokumentov bez tenant")

        # Show sample
        print(f"\n{Colors.BOLD}Vzorka dokumentov na opravu:{Colors.RESET}")
        for i, doc in enumerate(uae_docs[:5], 1):
            filepath = doc['metadata'].get('filepath', 'N/A') if doc['metadata'] else 'N/A'
            print(f"  {i}. ID={doc['id']}: {doc['filename']}")
            print(f"     Path: {filepath}")

        if len(uae_docs) > 5:
            print(f"  ... a ďalších {len(uae_docs) - 5} dokumentov")

        # 2. Confirm update
        print_header("2. Potvrdenie aktualizácie")
        print_warning(f"Budete aktualizovať {len(uae_docs)} dokumentov")
        print_info("Pridá sa metadata: tenant='uae'")

        response = input(f"\n{Colors.YELLOW}Pokračovať s UPDATE? (yes/no): {Colors.RESET}")

        if response.lower() not in ['yes', 'y']:
            print_warning("Aktualizácia zrušená používateľom")
            return

        # 3. Update documents
        print_header("3. Aktualizácia metadata")
        updated_count = 0

        for doc in uae_docs:
            try:
                update_document_metadata(cursor, doc['id'], doc['metadata'])
                updated_count += 1

                if updated_count % 10 == 0:
                    print_info(f"Aktualizovaných: {updated_count}/{len(uae_docs)}")

            except Exception as e:
                print_error(f"Chyba pri aktualizácii dokumentu ID={doc['id']}: {e}")

        # Commit changes
        conn.commit()
        print_success(f"Úspešne aktualizovaných {updated_count} dokumentov")

        # 4. Verify update
        print_header("4. Verifikácia aktualizácie")

        cursor.execute("""
            SELECT COUNT(*) as count
            FROM documents
            WHERE metadata->>'tenant' = 'uae'
        """)
        result = cursor.fetchone()
        print_success(f"Dokumentov s tenant='uae': {result['count']}")

        # Check chunks
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE d.metadata->>'tenant' = 'uae'
        """)
        result = cursor.fetchone()
        print_success(f"Chunks pre UAE tenant: {result['count']}")

        # Show sample updated document
        cursor.execute("""
            SELECT id, filename, metadata
            FROM documents
            WHERE metadata->>'tenant' = 'uae'
            LIMIT 1
        """)
        sample = cursor.fetchone()

        if sample:
            print(f"\n{Colors.BOLD}Vzorový aktualizovaný dokument:{Colors.RESET}")
            print(f"  ID: {sample['id']}")
            print(f"  Filename: {sample['filename']}")
            print(f"  Metadata tenant: {sample['metadata'].get('tenant')}")

        cursor.close()

    except Exception as e:
        print_error(f"Chyba: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

    print_header("✅ AKTUALIZÁCIA DOKONČENÁ")
    print_info("Spustite test 01_test_uae_legal_rag.py pre overenie")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nPrerušené používateľom")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nChyba: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)