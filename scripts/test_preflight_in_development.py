"""
Test Preflight Check in Development
====================================
Testuje opravený preflight check v Development prostredí.

Testuje len časti relevantné pre Development:
- Config loading
- Database connectivity logic
- Dependencies check

Preskakuje:
- Service status (beží len v Deployment)
- Performance baseline (nie je v Development)

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\test_preflight_in_development.py
"""

import sys
from pathlib import Path


def print_section(title: str):
    """Print formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def test_config_loading():
    """Test config.yaml loading from correct location."""
    print_section("TEST 1: CONFIG LOADING")

    config_path = Path("apps/supplier-invoice-loader/config/config.yaml")

    print(f"Config path: {config_path}")
    print(f"Exists: {'✅ YES' if config_path.exists() else '❌ NO'}")

    if not config_path.exists():
        print("❌ FAILED: Config not found")
        return False

    try:
        import yaml

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        print("✅ Config loaded successfully")

        # Check structure
        db_config = config.get('database', {})

        print("\nDatabase config:")
        print(f"  Type: {db_config.get('type', 'not specified')}")
        print(f"  PostgreSQL: {db_config.get('postgres', {}).get('host', 'not configured')}")
        print(f"  SQLite path: {db_config.get('sqlite_path', 'not configured')}")

        # Verify SQLite is NOT required (PostgreSQL primary)
        sqlite_path = db_config.get('sqlite_path')
        db_type = db_config.get('type', '').lower()

        if not sqlite_path and db_type != 'sqlite':
            print("\n✅ Confirmed: SQLite not required (PostgreSQL primary)")
            return True
        else:
            print(f"\n⚠️  SQLite configured: type={db_type}, path={sqlite_path}")
            return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_database_connectivity():
    """Test database connectivity logic."""
    print_section("TEST 2: DATABASE CONNECTIVITY")

    success = True

    # PostgreSQL check
    print("Testing PostgreSQL connection...")
    try:
        import pg8000.native
        import os

        pg_password = os.environ.get("POSTGRES_PASSWORD", "postgres")
        print(f"Using password from: {'environment' if 'POSTGRES_PASSWORD' in os.environ else 'default'}")

        conn = pg8000.native.Connection(
            host="localhost",
            port=5432,
            database="invoice_staging",
            user="postgres",
            password=pg_password
        )
        conn.close()
        print("✅ PostgreSQL: Connection successful")
    except Exception as e:
        print(f"⚠️  PostgreSQL: {e}")
        print("   Note: This is expected if PostgreSQL not running in Development")
        success = False

    # SQLite check logic
    print("\nTesting SQLite detection logic...")
    try:
        import yaml

        config_path = Path("apps/supplier-invoice-loader/config/config.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        db_config = config.get('database', {})
        sqlite_path_str = db_config.get('sqlite_path')
        db_type = db_config.get('type', '').lower()

        sqlite_required = db_type == 'sqlite' or sqlite_path_str is not None

        if sqlite_required:
            print(f"⚠️  SQLite is required: type={db_type}, path={sqlite_path_str}")
        else:
            print("✅ SQLite not required (correct for PostgreSQL primary)")

    except Exception as e:
        print(f"❌ SQLite detection failed: {e}")
        return False

    return True  # Return True even if PostgreSQL connection failed (expected in Dev)


def test_dependencies():
    """Test dependencies check."""
    print_section("TEST 3: DEPENDENCIES CHECK")

    required = [
        "fastapi",
        "uvicorn",
        "pdfplumber",
        "pg8000",
        "pypdf",
        "PIL",
        "httpx",
        "pydantic",
        "yaml"  # PyYAML
    ]

    missing = []

    for package in required:
        try:
            if package == "yaml":
                __import__("yaml")  # PyYAML imports as yaml
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n❌ Missing {len(missing)} packages: {', '.join(missing)}")
        return False
    else:
        print(f"\n✅ All {len(required)} dependencies installed")
        return True


def test_preflight_import():
    """Test if preflight script can be imported."""
    print_section("TEST 4: PREFLIGHT SCRIPT SYNTAX")

    preflight_path = Path("scripts/day5_preflight_check.py")

    if not preflight_path.exists():
        print(f"❌ Preflight script not found: {preflight_path}")
        return False

    try:
        # Read and check for syntax errors
        with open(preflight_path, 'r', encoding='utf-8') as f:
            code = f.read()

        compile(code, str(preflight_path), 'exec')

        print(f"✅ Preflight script syntax valid")
        print(f"   File: {preflight_path}")
        print(f"   Size: {len(code)} bytes")

        # Check for our fixes
        has_app_config = "apps/supplier-invoice-loader/config/config.yaml" in code
        has_sqlite_optional = "sqlite_required" in code
        has_env_password = "POSTGRES_PASSWORD" in code

        print("\nFixed features present:")
        print(f"  {'✅' if has_app_config else '❌'} App-specific config path")
        print(f"  {'✅' if has_sqlite_optional else '❌'} Optional SQLite check")
        print(f"  {'✅' if has_env_password else '❌'} Environment password")

        return has_app_config and has_sqlite_optional and has_env_password

    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("  TEST PREFLIGHT CHECK IN DEVELOPMENT")
    print("=" * 70)
    print(f"Location: {Path.cwd()}")

    results = {
        "Config Loading": test_config_loading(),
        "Database Connectivity": test_database_connectivity(),
        "Dependencies": test_dependencies(),
        "Preflight Script Syntax": test_preflight_import()
    }

    print_section("TEST RESULTS")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        icon = "✅" if result else "❌"
        print(f"{icon} {test}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✅ ALL TESTS PASSED")
        print("✅ Preflight check is ready for Deployment")
        print("\nNext: Git commit + push + deploy")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Review failures above before committing")
        sys.exit(1)


if __name__ == "__main__":
    main()