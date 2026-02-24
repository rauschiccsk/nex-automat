"""
Initialize PostgreSQL Database
Creates invoice_staging database and runs schema migrations
"""

import os
import sys
from pathlib import Path

try:
    import pg8000.native
except ImportError:
    print("ERROR: pg8000 not installed")
    print("Run: pip install pg8000")
    sys.exit(1)


def get_postgres_password():
    """Get PostgreSQL password from environment"""
    password = os.environ.get("POSTGRES_PASSWORD")
    if not password:
        print("ERROR: POSTGRES_PASSWORD environment variable not set")
        sys.exit(1)
    return password


def database_exists(password: str, db_name: str) -> bool:
    """Check if database exists"""
    try:
        conn = pg8000.native.Connection(
            user="postgres",
            password=password,
            host="localhost",
            port=5432,
            database="postgres",
        )
        result = conn.run(
            "SELECT 1 FROM pg_database WHERE datname = :db_name", db_name=db_name
        )
        conn.close()
        return len(result) > 0
    except Exception as e:
        print(f"ERROR: Failed to check database: {e}")
        return False


def create_database(password: str, db_name: str):
    """Create database if it doesn't exist"""
    try:
        conn = pg8000.native.Connection(
            user="postgres",
            password=password,
            host="localhost",
            port=5432,
            database="postgres",
        )
        conn.run(f"CREATE DATABASE {db_name}")
        conn.close()
        print(f"[OK] Database '{db_name}' created")
    except Exception as e:
        if "already exists" in str(e):
            print(f"[OK] Database '{db_name}' already exists")
        else:
            print(f"ERROR: Failed to create database: {e}")
            raise


def run_schema(password: str, db_name: str, schema_file: Path):
    """Run SQL schema file"""
    try:
        # Read schema file
        with open(schema_file, encoding="utf-8") as f:
            schema_sql = f.read()

        # Connect to target database
        conn = pg8000.native.Connection(
            user="postgres",
            password=password,
            host="localhost",
            port=5432,
            database=db_name,
        )

        # Split by semicolons and execute each statement
        statements = [s.strip() for s in schema_sql.split(";") if s.strip()]

        for i, statement in enumerate(statements, 1):
            if statement and not statement.startswith("--"):
                try:
                    conn.run(statement)
                except Exception as e:
                    # Ignore certain expected errors
                    if "already exists" not in str(e).lower():
                        print(f"Warning on statement {i}: {e}")

        conn.close()
        print(f"[OK] Schema applied from {schema_file.name}")

    except Exception as e:
        print(f"ERROR: Failed to run schema: {e}")
        raise


def main():
    """Main initialization"""
    print("=" * 60)
    print("NEX AUTOMAT - Database Initialization")
    print("=" * 60)

    # Get password
    password = get_postgres_password()
    db_name = "invoice_staging"

    # Project paths
    project_root = Path(__file__).parent.parent
    schema_dir = (
        project_root / "apps" / "supplier-invoice-editor" / "database" / "schemas"
    )

    # Schema files in order
    schema_files = [
        schema_dir / "001_initial_schema.sql",
        schema_dir / "002_add_nex_columns.sql",
    ]

    print(f"Database: {db_name}")
    print(f"Schema directory: {schema_dir}")
    print("-" * 60)

    # Step 1: Create database
    print(f"\n>>> Creating database '{db_name}'...")
    if not database_exists(password, db_name):
        create_database(password, db_name)
    else:
        print(f"[OK] Database '{db_name}' already exists")

    # Step 2: Run schema migrations
    print("\n>>> Running schema migrations...")
    for schema_file in schema_files:
        if schema_file.exists():
            print(f"Applying: {schema_file.name}")
            run_schema(password, db_name, schema_file)
        else:
            print(f"[SKIP] Schema file not found: {schema_file.name}")

    print("\n" + "=" * 60)
    print("[OK] Database initialization complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
