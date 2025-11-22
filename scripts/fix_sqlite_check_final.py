"""
Fix SQLite Check - Final
=========================
Kompletne prepíše SQLite check funkciu v preflight script.

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\fix_sqlite_check_final.py
"""

from pathlib import Path
import re


def fix_sqlite_check():
    """Replace entire check_database_connectivity function."""

    preflight_path = Path("scripts/day5_preflight_check.py")

    if not preflight_path.exists():
        print(f"❌ Not found: {preflight_path}")
        return False

    try:
        content = preflight_path.read_text(encoding='utf-8')

        # Find the function start and end
        func_start = content.find("def check_database_connectivity() -> bool:")
        if func_start == -1:
            print("❌ Function not found")
            return False

        # Find next function (end of current function)
        next_func = content.find("\ndef ", func_start + 1)
        if next_func == -1:
            print("❌ Could not determine function end")
            return False

        # New function implementation
        new_function = '''def check_database_connectivity() -> bool:
    """Check PostgreSQL and SQLite connectivity."""
    print_section("2. DATABASE CONNECTIVITY")

    success = True

    # PostgreSQL check - use environment variable for password
    try:
        import pg8000.native
        pg_password = os.environ.get("POSTGRES_PASSWORD", "postgres")

        conn = pg8000.native.Connection(
            host="localhost",
            port=5432,
            database="invoice_staging",
            user="postgres",
            password=pg_password
        )
        conn.close()
        print("✅ PostgreSQL: Connected (localhost:5432/invoice_staging)")
    except Exception as e:
        print(f"❌ PostgreSQL: Failed - {e}")
        print("   Hint: Set POSTGRES_PASSWORD environment variable")
        success = False

    # SQLite check - only if configured in config.yaml
    sqlite_required = False
    sqlite_path = None

    try:
        config_path = Path("apps/supplier-invoice-loader/config/config.yaml")
        if config_path.exists():
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                db_config = config.get('database', {})

                # Check if SQLite is configured
                sqlite_path_str = db_config.get('sqlite_path')
                db_type = db_config.get('type', '').lower()

                sqlite_required = db_type == 'sqlite' or sqlite_path_str is not None

                if sqlite_path_str:
                    sqlite_path = Path(sqlite_path_str)
    except Exception as e:
        print(f"⚠️  Could not read config for SQLite check: {e}")

    # Perform SQLite check if required
    if sqlite_required:
        if sqlite_path and sqlite_path.exists():
            print(f"✅ SQLite: Database exists ({sqlite_path})")
        elif sqlite_path:
            print(f"❌ SQLite: Database NOT found at {sqlite_path}")
            success = False
        else:
            print("❌ SQLite: Required but path not configured in config.yaml")
            success = False
    else:
        print("✅ SQLite: Not required (using PostgreSQL primary)")

    return success
'''

        # Replace the function
        before = content[:func_start]
        after = content[next_func:]

        new_content = before + new_function + "\n" + after

        preflight_path.write_text(new_content, encoding='utf-8')

        print("=" * 70)
        print("  FIXING SQLITE CHECK")
        print("=" * 70)
        print("\n✅ Successfully replaced check_database_connectivity()")
        print("✅ SQLite check is now config-based")
        print("✅ PostgreSQL check uses environment variable")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    if fix_sqlite_check():
        print("\n✅ Preflight script fully updated")
        print("\nReady for Git commit!")
    else:
        print("\n❌ Fix failed")