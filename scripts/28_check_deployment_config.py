# Check Deployment configuration

from pathlib import Path
import yaml

DEPLOY_ROOT = Path(r"C:\Deployment\nex-automat")
CONFIG_FILE = DEPLOY_ROOT / "config" / "database.yaml"
LOADER_CONFIG = DEPLOY_ROOT / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"

print("=" * 70)
print("CHECK DEPLOYMENT CONFIGURATION")
print("=" * 70)

# Check database.yaml
print("\nSTEP 1: Check config/database.yaml")
print("-" * 70)
if CONFIG_FILE.exists():
    print(f"✅ Found: {CONFIG_FILE}")
    config = yaml.safe_load(CONFIG_FILE.read_text(encoding='utf-8'))

    if 'nex_genesis' in config:
        nex_config = config['nex_genesis']
        root_path = nex_config.get('root_path', 'NOT SET')
        yearact_path = nex_config.get('yearact_path', 'NOT SET')

        print(f"\nNEX Genesis config:")
        print(f"  root_path: {root_path}")
        print(f"  yearact_path: {yearact_path}")

        # Check paths exist
        if Path(root_path).exists():
            print(f"  ✅ root_path exists")
        else:
            print(f"  ❌ root_path NOT FOUND: {root_path}")

        if Path(yearact_path).exists():
            print(f"  ✅ yearact_path exists")
        else:
            print(f"  ❌ yearact_path NOT FOUND: {yearact_path}")

        # Check GSCAT table path
        if 'tables' in nex_config and 'gscat' in nex_config['tables']:
            gscat_path = Path(nex_config['tables']['gscat'])
            print(f"\nGSCAT table: {gscat_path}")
            if gscat_path.exists():
                print(f"  ✅ GSCAT.BTR exists ({gscat_path.stat().st_size:,} bytes)")
            else:
                print(f"  ❌ GSCAT.BTR NOT FOUND")
    else:
        print("⚠️  No nex_genesis section in config")
else:
    print(f"❌ Not found: {CONFIG_FILE}")

# Check loader config.yaml
print("\n" + "=" * 70)
print("STEP 2: Check supplier-invoice-loader config")
print("-" * 70)
if LOADER_CONFIG.exists():
    print(f"✅ Found: {LOADER_CONFIG}")
    config = yaml.safe_load(LOADER_CONFIG.read_text(encoding='utf-8'))

    # Check for database paths
    if 'database' in config:
        print("\nDatabase config:")
        for key, value in config['database'].items():
            print(f"  {key}: {value}")

    # Check for NEX paths
    nex_keys = [k for k in config.keys() if 'nex' in k.lower()]
    if nex_keys:
        print("\nNEX-related config:")
        for key in nex_keys:
            print(f"  {key}: {config[key]}")
else:
    print(f"❌ Not found: {LOADER_CONFIG}")

# Check Btrieve DLL paths
print("\n" + "=" * 70)
print("STEP 3: Check Btrieve DLL locations")
print("-" * 70)

btrieve_paths = [
    r"C:\Program Files (x86)\Pervasive Software\PSQL\bin",
    r"C:\PVSW\bin",
    r"C:\Windows\SysWOW64",
]

dll_names = ["w3btrv7.dll", "wbtrv32.dll"]

found_dll = False
for search_path in btrieve_paths:
    path = Path(search_path)
    print(f"\nChecking: {path}")

    if path.exists():
        print(f"  ✅ Directory exists")

        for dll in dll_names:
            dll_path = path / dll
            if dll_path.exists():
                size = dll_path.stat().st_size
                print(f"  ✅ Found {dll} ({size:,} bytes)")
                found_dll = True
            else:
                print(f"  ⚪ {dll} not found")
    else:
        print(f"  ❌ Directory NOT FOUND")

if not found_dll:
    print("\n" + "=" * 70)
    print("❌ NO BTRIEVE DLL FOUND!")
    print("=" * 70)
    print("\nThis server does not have Btrieve installed.")
    print("NEX Genesis requires Btrieve/Pervasive PSQL to be installed.")
    print("\nOptions:")
    print("1. Install Pervasive PSQL Client on this server")
    print("2. Copy Btrieve DLLs from Development server")
    print("3. Use remote NEX Genesis server (if available)")

print("\n" + "=" * 70)
print("CONFIGURATION CHECK COMPLETE")
print("=" * 70)