#!/usr/bin/env python3
"""
NEX Automat - Database Connection Test
Tests PostgreSQL database connectivity and configuration
"""

import os
import sys
import asyncio
import asyncpg
import yaml
from pathlib import Path
from datetime import datetime


async def test_connection(config: dict) -> bool:
    """Test database connection"""
    db_config = config['database']['postgres']

    print("\n" + "=" * 70)
    print("DATABASE CONNECTION TEST")
    print("=" * 70)
    print(f"Host:     {db_config['host']}")
    print(f"Port:     {db_config['port']}")
    print(f"Database: {db_config['database']}")
    print(f"User:     {db_config['user']}")
    print("=" * 70)
    print()

    try:
        print("📡 Connecting to database...")

        conn = await asyncpg.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            timeout=10
        )

        print("✅ Connected successfully!")

        # Test 1: Get PostgreSQL version
        print("\n" + "-" * 70)
        print("TEST 1: PostgreSQL Version")
        print("-" * 70)

        version = await conn.fetchval('SELECT version()')
        print(f"✅ {version}")

        # Test 2: Check current timestamp
        print("\n" + "-" * 70)
        print("TEST 2: Server Timestamp")
        print("-" * 70)

        timestamp = await conn.fetchval('SELECT NOW()')
        print(f"✅ Server time: {timestamp}")
        local_time = datetime.now()
        print(f"   Local time:  {local_time}")

        # Test 3: List tables
        print("\n" + "-" * 70)
        print("TEST 3: Database Tables")
        print("-" * 70)

        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table['table_name']}")
        else:
            print("⚠️  No tables found (database is empty)")

        # Test 4: Check database size
        print("\n" + "-" * 70)
        print("TEST 4: Database Size")
        print("-" * 70)

        size = await conn.fetchval("""
            SELECT pg_size_pretty(pg_database_size(current_database()))
        """)
        print(f"✅ Database size: {size}")

        # Test 5: Check connection limits
        print("\n" + "-" * 70)
        print("TEST 5: Connection Limits")
        print("-" * 70)

        max_conn = await conn.fetchval('SHOW max_connections')
        current_conn = await conn.fetchval("""
            SELECT count(*) FROM pg_stat_activity 
            WHERE datname = current_database()
        """)
        print(f"✅ Max connections:     {max_conn}")
        print(f"✅ Current connections: {current_conn}")

        # Test 6: Check user privileges
        print("\n" + "-" * 70)
        print("TEST 6: User Privileges")
        print("-" * 70)

        privileges = await conn.fetch("""
            SELECT privilege_type 
            FROM information_schema.table_privileges 
            WHERE grantee = current_user 
            AND table_schema = 'public'
            GROUP BY privilege_type
            ORDER BY privilege_type
        """)

        if privileges:
            print(f"✅ User '{db_config['user']}' has privileges:")
            for priv in privileges:
                print(f"   - {priv['privilege_type']}")
        else:
            print("⚠️  No specific table privileges found")

        # Test 7: Test write capability
        print("\n" + "-" * 70)
        print("TEST 7: Write Capability")
        print("-" * 70)

        await conn.execute("""
            CREATE TEMP TABLE test_write (
                id SERIAL PRIMARY KEY,
                test_data TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        print("✅ Created temporary table")

        await conn.execute("""
            INSERT INTO test_write (test_data) 
            VALUES ('Connection test successful')
        """)
        print("✅ Inserted test data")

        result = await conn.fetchval("""
            SELECT test_data FROM test_write LIMIT 1
        """)
        print(f"✅ Retrieved: {result}")

        await conn.execute("DROP TABLE test_write")
        print("✅ Dropped temporary table")

        await conn.close()
        print("\n✅ Connection closed")

        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        print("Database connection is working correctly!")
        print()

        return True

    except asyncpg.exceptions.InvalidPasswordError:
        print("❌ ERROR: Invalid password")
        return False

    except asyncpg.exceptions.InvalidCatalogNameError:
        print(f"❌ ERROR: Database '{db_config['database']}' does not exist")
        print("\nTo create the database, run:")
        print(f"  createdb -h {db_config['host']} -p {db_config['port']} "
              f"-U {db_config['user']} {db_config['database']}")
        return False

    except asyncpg.exceptions.CannotConnectNowError:
        print("❌ ERROR: Cannot connect to database server")
        print("Check if PostgreSQL service is running")
        return False

    except ConnectionRefusedError:
        print(f"❌ ERROR: Connection refused to {db_config['host']}:{db_config['port']}")
        print("Check if PostgreSQL is running and accepting connections")
        return False

    except asyncio.TimeoutError:
        print("❌ ERROR: Connection timeout")
        print("Check network connectivity and firewall settings")
        return False

    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False


def main():
    config_path = Path(__file__).parent.parent / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"

    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        print("\nRun this first:")
        print("  python scripts/create_production_config.py")
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Expand environment variables in config
        import re
        def expand_env_vars(obj):
            """Recursively expand ${ENV:VAR_NAME} in config"""
            if isinstance(obj, dict):
                return {k: expand_env_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [expand_env_vars(item) for item in obj]
            elif isinstance(obj, str):
                # Replace ${ENV:VAR_NAME} with environment variable value
                match = re.match(r'^\$\{ENV:([^}]+)\}$', obj)
                if match:
                    var_name = match.group(1)
                    return os.environ.get(var_name, '')
                return obj
            else:
                return obj

        config = expand_env_vars(config)

    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

    success = asyncio.run(test_connection(config))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
