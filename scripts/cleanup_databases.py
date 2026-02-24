#!/usr/bin/env python
"""
Cleanup Databases - SQLite + PostgreSQL
Vymaže všetky údaje z databáz.

Použitie:
    python scripts/cleanup_databases.py

Vyžaduje:
    - POSTGRES_PASSWORD environment variable
"""

import os
import sqlite3
import sys
from pathlib import Path

# Určenie root projektu
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Cesty k databázam
SQLITE_DB_PATH = (
    PROJECT_ROOT / "apps" / "supplier-invoice-loader" / "data" / "invoices.db"
)
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "supplier_invoice_staging",
    "user": "postgres",
}


def cleanup_sqlite() -> tuple[int, int]:
    """Vymaže všetky záznamy zo SQLite databázy."""
    if not SQLITE_DB_PATH.exists():
        print(f"[SKIP] SQLite DB neexistuje: {SQLITE_DB_PATH}")
        return 0, 0

    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Zistíme počet záznamov pred vymazaním
    cursor.execute("SELECT COUNT(*) FROM invoices")
    invoices_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM invoice_items")
    items_count = cursor.fetchone()[0]

    # Vymazanie
    cursor.execute("DELETE FROM invoice_items")
    cursor.execute("DELETE FROM invoices")

    conn.commit()
    conn.close()

    return invoices_count, items_count


def cleanup_postgresql() -> tuple[int, int]:
    """Vymaže všetky záznamy z PostgreSQL staging databázy."""
    try:
        import pg8000.native
    except ImportError:
        print("[ERROR] pg8000 nie je nainštalovaný")
        print("        pip install pg8000")
        return 0, 0

    password = os.environ.get("POSTGRES_PASSWORD")
    if not password:
        print("[ERROR] POSTGRES_PASSWORD environment variable nie je nastavená")
        return 0, 0

    conn = pg8000.native.Connection(
        host=POSTGRES_CONFIG["host"],
        port=POSTGRES_CONFIG["port"],
        database=POSTGRES_CONFIG["database"],
        user=POSTGRES_CONFIG["user"],
        password=password,
    )

    # Počet záznamov pred vymazaním
    result = conn.run("SELECT COUNT(*) FROM supplier_invoice_heads")
    heads_count = result[0][0]

    result = conn.run("SELECT COUNT(*) FROM supplier_invoice_items")
    items_count = result[0][0]

    # Vymazanie (items first kvôli FK)
    conn.run("DELETE FROM supplier_invoice_items")
    conn.run("DELETE FROM supplier_invoice_heads")

    # Reset sequences
    conn.run("ALTER SEQUENCE supplier_invoice_heads_id_seq RESTART WITH 1")
    conn.run("ALTER SEQUENCE supplier_invoice_items_id_seq RESTART WITH 1")

    conn.close()

    return heads_count, items_count


def main():
    print("=" * 60)
    print("CLEANUP DATABASES")
    print("=" * 60)
    print()

    # Potvrdenie
    print("⚠️  POZOR: Toto vymaže VŠETKY dáta z:")
    print(f"    - SQLite:     {SQLITE_DB_PATH}")
    print(f"    - PostgreSQL: {POSTGRES_CONFIG['database']}")
    print()

    confirm = input("Pokračovať? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("[CANCELLED] Operácia zrušená.")
        sys.exit(0)

    print()

    # SQLite cleanup
    print("[1/2] SQLite cleanup...")
    sqlite_invoices, sqlite_items = cleanup_sqlite()
    print(f"      Vymazané: {sqlite_invoices} faktúr, {sqlite_items} položiek")

    # PostgreSQL cleanup
    print("[2/2] PostgreSQL cleanup...")
    pg_heads, pg_items = cleanup_postgresql()
    print(f"      Vymazané: {pg_heads} faktúr, {pg_items} položiek")

    print()
    print("=" * 60)
    print("✅ CLEANUP DOKONČENÝ")
    print("=" * 60)
    print()
    print("Štatistika:")
    print(f"  SQLite:     {sqlite_invoices} faktúr, {sqlite_items} položiek")
    print(f"  PostgreSQL: {pg_heads} faktúr, {pg_items} položiek")
    print(
        f"  TOTAL:      {sqlite_invoices + pg_heads} faktúr, {sqlite_items + pg_items} položiek"
    )


if __name__ == "__main__":
    main()
