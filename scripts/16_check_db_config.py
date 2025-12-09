# Check database config

from pathlib import Path
import yaml

DEV_ROOT = Path(r"C:\Development\nex-automat")
CONFIG_FILE = DEV_ROOT / "config" / "database.yaml"

print("=" * 70)
print("CHECKING DATABASE CONFIG")
print("=" * 70)

if not CONFIG_FILE.exists():
    print(f"❌ Config file not found: {CONFIG_FILE}")
    print("\nSearching for config files...")
    for config in DEV_ROOT.rglob("*.yaml"):
        if 'database' in config.name.lower() or 'config' in config.name.lower():
            print(f"  Found: {config.relative_to(DEV_ROOT)}")
else:
    print(f"✅ Config file: {CONFIG_FILE}\n")

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    print("Config content:")
    print(yaml.dump(config, default_flow_style=False, allow_unicode=True))

    # Extract PostgreSQL connection info
    if 'postgresql' in config:
        pg_config = config['postgresql']
        print("\n" + "=" * 70)
        print("POSTGRESQL CONNECTION INFO:")
        print("=" * 70)
        print(f"Host:     {pg_config.get('host', 'N/A')}")
        print(f"Port:     {pg_config.get('port', 'N/A')}")
        print(f"Database: {pg_config.get('database', 'N/A')}")
        print(f"User:     {pg_config.get('user', 'N/A')}")
        print(f"Password: {'***' if pg_config.get('password') else 'NOT SET'}")