# Check PostgreSQL tables

import os
import asyncio
import asyncpg


async def check_tables():
    print("=" * 70)
    print("CHECKING POSTGRESQL TABLES")
    print("=" * 70)

    postgres_password = os.getenv('POSTGRES_PASSWORD')
    if not postgres_password:
        print("❌ ERROR: POSTGRES_PASSWORD not set")
        return

    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        database='invoice_staging',
        user='postgres',
        password=postgres_password
    )

    print("✅ Connected to invoice_staging database\n")

    # List all tables
    tables = await conn.fetch("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)

    print(f"Tables in database ({len(tables)}):")
    print("-" * 70)
    for table in tables:
        table_name = table['table_name']

        # Get row count
        count = await conn.fetchval(f"SELECT COUNT(*) FROM {table_name}")

        # Get columns
        columns = await conn.fetch(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """)

        print(f"\n📋 {table_name} ({count} rows)")
        print("   Columns:")
        for col in columns:
            print(f"     - {col['column_name']}: {col['data_type']}")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(check_tables())