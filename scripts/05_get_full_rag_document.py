"""
Session Script 05: Get Full Document from RAG by document_id
Projekt: nex-automat
Dočasný skript - načítať kompletný dokument 962 o NexBrain konfigurácii
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


def get_document_metadata(cursor, doc_id):
    """Get document metadata from rag_documents"""
    cursor.execute("""
        SELECT 
            id,
            title,
            source_path,
            file_hash,
            metadata,
            created_at,
            updated_at
        FROM rag_documents
        WHERE id = %s
    """, (doc_id,))
    return cursor.fetchone()


def get_document_chunks(cursor, doc_id):
    """Get all chunks for a document from rag_chunks"""
    cursor.execute("""
        SELECT 
            id,
            document_id,
            chunk_index,
            content,
            metadata,
            created_at
        FROM rag_chunks
        WHERE document_id = %s
        ORDER BY chunk_index
    """, (doc_id,))
    return cursor.fetchall()


def reconstruct_full_document(chunks):
    """Reconstruct full document from chunks"""
    if not chunks:
        return ""

    full_text = []
    for chunk in chunks:
        full_text.append(chunk['content'])

    return "\n\n".join(full_text)


def main():
    print_header("🔍 NAČÍTANIE KOMPLETNÉHO DOKUMENTU Z RAG")

    document_id = 962  # NEX Brain - Tenant Filtering document

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Get document metadata
        print_header(f"1. Metadata dokumentu ID={document_id}")
        doc_meta = get_document_metadata(cursor, document_id)

        if not doc_meta:
            print_error(f"Document ID {document_id} not found!")
            return

        print_success("Document found:")
        print(f"  Title: {doc_meta['title']}")
        print(f"  Source: {doc_meta['source_path']}")
        print(f"  Hash: {doc_meta['file_hash']}")
        print(f"  Created: {doc_meta['created_at']}")
        print(f"  Updated: {doc_meta['updated_at']}")
        if doc_meta['metadata']:
            print(f"  Metadata: {doc_meta['metadata']}")

        # 2. Get all chunks
        print_header(f"2. Načítanie chunks pre dokument ID={document_id}")
        chunks = get_document_chunks(cursor, document_id)

        if not chunks:
            print_error("No chunks found for this document!")
            return

        print_success(f"Found {len(chunks)} chunks")

        # 3. Reconstruct full document
        print_header("3. Rekonštrukcia kompletného dokumentu")
        full_text = reconstruct_full_document(chunks)

        print_success(f"Document reconstructed: {len(full_text)} characters")

        # 4. Display full document
        print_header("4. KOMPLETNÝ OBSAH DOKUMENTU")
        print(full_text)

        # 5. Save to file
        output_file = Path(__file__).parent / f"document_{document_id}_full.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Document ID: {document_id}\n")
            f.write(f"# Title: {doc_meta['title']}\n")
            f.write(f"# Source: {doc_meta['source_path']}\n")
            f.write(f"# Created: {doc_meta['created_at']}\n\n")
            f.write("---\n\n")
            f.write(full_text)

        print_header("5. ULOŽENÉ DO SÚBORU")
        print_success(f"Saved to: {output_file}")

        cursor.close()

    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

    print_header("📊 DOKONČENÉ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Interrupted{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nFailed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)