"""
Session Script 03: Check Database Structure
Projekt: nex-automat
Dočasný diagnostický skript - zistiť štruktúru nex_automat_rag databázy
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


def check_database_structure():
    """Check what tables and schemas exist in the database"""

    print_header("🔍 KONTROLA ŠTRUKTÚRY DATABÁZY: nex_automat_rag")

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Check all schemas
        print_header("1. Dostupné schémy")
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
            ORDER BY schema_name
        """)
        schemas = cursor.fetchall()

        if schemas:
            print_success(f"Found {len(schemas)} schemas:")
            for schema in schemas:
                print(f"  - {schema['schema_name']}")
        else:
            print_warning("No custom schemas found")

        # 2. Check all tables in public schema
        print_header("2. Tabuľky v 'public' schéme")
        cursor.execute("""
            SELECT table_name, table_type
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()

        if tables:
            print_success(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table['table_name']} ({table['table_type']})")
        else:
            print_warning("No tables in public schema")

        # 3. Check all tables in all schemas
        print_header("3. Všetky tabuľky vo všetkých schémach")
        cursor.execute("""
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """)
        all_tables = cursor.fetchall()

        if all_tables:
            print_success(f"Total tables: {len(all_tables)}")
            current_schema = None
            for table in all_tables:
                if table['table_schema'] != current_schema:
                    current_schema = table['table_schema']
                    print(f"\n{Colors.BOLD}Schema: {current_schema}{Colors.RESET}")
                print(f"  - {table['table_name']} ({table['table_type']})")
        else:
            print_error("No tables found in database!")

        # 4. Check for pgvector extension
        print_header("4. Kontrola pgvector extension")
        cursor.execute("""
            SELECT extname, extversion
            FROM pg_extension
            WHERE extname = 'vector'
        """)
        extension = cursor.fetchone()

        if extension:
            print_success(f"pgvector extension installed: v{extension['extversion']}")
        else:
            print_error("pgvector extension NOT installed!")

        # 5. Check for any table with 'embed' in name
        print_header("5. Hľadanie tabuliek s 'embed' v názve")
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name LIKE '%embed%'
            ORDER BY table_schema, table_name
        """)
        embed_tables = cursor.fetchall()

        if embed_tables:
            print_success(f"Found {len(embed_tables)} tables with 'embed':")
            for table in embed_tables:
                print(f"  - {table['table_schema']}.{table['table_name']}")
        else:
            print_warning("No tables with 'embed' in name")

        # 6. Check for any table with 'rag' in name
        print_header("6. Hľadanie tabuliek s 'rag' v názve")
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name LIKE '%rag%'
            ORDER BY table_schema, table_name
        """)
        rag_tables = cursor.fetchall()

        if rag_tables:
            print_success(f"Found {len(rag_tables)} tables with 'rag':")
            for table in rag_tables:
                print(f"  - {table['table_schema']}.{table['table_name']}")
        else:
            print_warning("No tables with 'rag' in name")

        # 7. If we found any tables, show their structure
        if all_tables:
            print_header("7. Štruktúra prvej tabuľky (vzorka)")
            first_table = all_tables[0]
            schema = first_table['table_schema']
            table = first_table['table_name']

            cursor.execute(f"""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = '{schema}'
                AND table_name = '{table}'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()

            print_info(f"Table: {schema}.{table}")
            print_info(f"Columns: {len(columns)}")
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
                print(f"  - {col['column_name']}: {col['data_type']} {nullable} {default}")

        cursor.close()

    except Exception as e:
        print_error(f"Database check failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

    # Summary
    print_header("📊 ZHRNUTIE")
    print_info("Kontrola databázy ukončená")
    print_info("Pozri výsledky vyššie pre zistenie skutočnej štruktúry")


if __name__ == "__main__":
    try:
        check_database_structure()
    except KeyboardInterrupt:
        print_warning("\n\nCheck interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nCheck failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)