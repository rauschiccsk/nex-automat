"""
Session Script 06: Check RAG Tables Structure
Projekt: nex-automat
Dočasný skript - zistiť štruktúru rag_documents a rag_chunks
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


def show_table_structure(cursor, table_name):
    """Show complete structure of a table"""
    print_header(f"Štruktúra tabuľky: {table_name}")

    # Get columns
    cursor.execute(f"""
        SELECT 
            column_name, 
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        AND table_schema = 'public'
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()

    if columns:
        print_success(f"Found {len(columns)} columns:")
        for col in columns:
            max_len = f"({col['character_maximum_length']})" if col['character_maximum_length'] else ""
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  {col['column_name']:<25} {col['data_type']}{max_len:<15} {nullable:<10} {default}")
    else:
        print_error("No columns found")

    # Get row count
    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
    count = cursor.fetchone()
    print_info(f"Total rows: {count['count']}")

    # Show sample data
    if count['count'] > 0:
        print(f"\n{Colors.BOLD}Sample data (first 3 rows):{Colors.RESET}")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        samples = cursor.fetchall()

        for i, row in enumerate(samples, 1):
            print(f"\n{Colors.YELLOW}Row {i}:{Colors.RESET}")
            for key, value in row.items():
                if key == 'content' and value and len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                elif key == 'embedding':
                    print(f"  {key}: <vector data>")
                else:
                    print(f"  {key}: {value}")


def main():
    print_header("🔍 KONTROLA ŠTRUKTÚRY RAG TABULIEK")

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Check rag_documents
        show_table_structure(cursor, 'rag_documents')

        # Check rag_chunks
        show_table_structure(cursor, 'rag_chunks')

        # Check rag_keywords
        show_table_structure(cursor, 'rag_keywords')

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