#!/usr/bin/env python3
"""
Fix test_database_connection.py to expand environment variables
"""

from pathlib import Path

BASE_PATH = Path(r"C:\Development\nex-automat")
TEST_DB_PATH = BASE_PATH / "scripts" / "test_database_connection.py"


def fix_test_db():
    """Add environment variable expansion"""

    with open(TEST_DB_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the config loading section
    old_load = '''    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)'''

    new_load = '''    try:
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
        sys.exit(1)'''

    if old_load in content:
        content = content.replace(old_load, new_load)

        with open(TEST_DB_PATH, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Updated test_database_connection.py to expand environment variables")
        return True
    else:
        print("⚠️  Already updated or different format")
        return False


def main():
    print("=" * 70)
    print("FIX ENV VARS IN DATABASE TEST")
    print("=" * 70)
    print()

    if fix_test_db():
        print()
        print("=" * 70)
        print("✅ FIXED")
        print("=" * 70)
        print()
        print("Now run:")
        print("  python scripts/test_database_connection.py")
        print()


if __name__ == "__main__":
    main()