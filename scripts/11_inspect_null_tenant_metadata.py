"""
Session Script 11: Inspect NULL Tenant Metadata
Projekt: nex-automat
Dočasný skript - zistiť štruktúru metadata pre dokumenty bez tenant
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


def main():
    print_header("🔍 INŠPEKCIA METADATA PRE tenant=NULL")

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Get documents with NULL tenant
        print_header("1. Dokumenty s tenant=NULL (prvých 10)")
        cursor.execute("""
            SELECT 
                id,
                filename,
                metadata,
                created_at
            FROM documents
            WHERE metadata->>'tenant' IS NULL
            LIMIT 10
        """)
        docs = cursor.fetchall()

        if not docs:
            print_success("Žiadne dokumenty s NULL tenant")
            return

        print_success(f"Nájdených {len(docs)} dokumentov s NULL tenant")

        for i, doc in enumerate(docs, 1):
            print(f"\n{Colors.YELLOW}═══ Dokument {i} ═══{Colors.RESET}")
            print(f"{Colors.BOLD}ID:{Colors.RESET} {doc['id']}")
            print(f"{Colors.BOLD}Filename:{Colors.RESET} {doc['filename']}")
            print(f"{Colors.BOLD}Created:{Colors.RESET} {doc['created_at']}")
            print(f"{Colors.BOLD}Metadata:{Colors.RESET}")

            if doc['metadata']:
                for key, value in doc['metadata'].items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
            else:
                print("  (prázdne)")

        # 2. Check what metadata keys exist
        print_header("2. Všetky metadata keys v dokumentoch s NULL tenant")
        cursor.execute("""
            SELECT DISTINCT jsonb_object_keys(metadata) as key
            FROM documents
            WHERE metadata->>'tenant' IS NULL
        """)
        keys = cursor.fetchall()

        if keys:
            print_success("Dostupné metadata keys:")
            for key in keys:
                print(f"  - {key['key']}")

        # 3. Check if filepath contains 'uae'
        print_header("3. Dokumenty s 'uae' v filepath")
        cursor.execute("""
            SELECT 
                id,
                filename,
                metadata->>'filepath' as filepath
            FROM documents
            WHERE metadata->>'tenant' IS NULL
            AND (
                metadata->>'filepath' ILIKE '%uae%'
                OR filename ILIKE '%uae%'
            )
        """)
        uae_docs = cursor.fetchall()

        if uae_docs:
            print_success(f"Nájdených {len(uae_docs)} dokumentov s 'uae'")
            for doc in uae_docs:
                print(f"  ID={doc['id']}: {doc['filename']}")
                print(f"    Path: {doc['filepath']}")
        else:
            print_error("Žiadne dokumenty s 'uae' v ceste")

        # 4. Count total NULL tenant
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM documents
            WHERE metadata->>'tenant' IS NULL
        """)
        result = cursor.fetchone()
        print_header("4. Štatistiky")
        print_info(f"Celkovo dokumentov s NULL tenant: {result['count']}")

        cursor.close()

    except Exception as e:
        print_error(f"Chyba: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn:
            conn.close()

    print_header("📊 INŠPEKCIA DOKONČENÁ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Prerušené{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nChyba: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)