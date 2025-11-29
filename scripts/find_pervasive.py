"""
Find all Pervasive executables, DLLs and configuration files.
"""
import os
from pathlib import Path


def find_pervasive_files():
    """Find all Pervasive related files."""

    search_roots = [
        r"C:\PVSW",
        r"C:\Program Files (x86)\Pervasive Software",
        r"C:\Program Files\Pervasive Software",
    ]

    print("\n" + "=" * 80)
    print("PERVASIVE FILES SEARCH")
    print("=" * 80)

    all_files = []

    for root in search_roots:
        if not os.path.exists(root):
            print(f"\n⚠️  {root} - NOT FOUND")
            continue

        print(f"\n📁 Searching: {root}")
        print("-" * 80)

        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                # Filter interesting files
                ext = filename.upper()
                if any(x in ext for x in ['.EXE', '.DLL', '.INI', '.CFG', '.DAT']):
                    full_path = os.path.join(dirpath, filename)
                    size = os.path.getsize(full_path)

                    all_files.append({
                        'path': full_path,
                        'name': filename,
                        'dir': dirpath,
                        'size': size,
                        'ext': os.path.splitext(filename)[1].upper()
                    })

    # Group by type
    executables = [f for f in all_files if f['ext'] == '.EXE']
    dlls = [f for f in all_files if f['ext'] == '.DLL']
    configs = [f for f in all_files if f['ext'] in ['.INI', '.CFG', '.DAT']]

    # Print executables
    if executables:
        print("\n" + "=" * 80)
        print("EXECUTABLES (.EXE)")
        print("=" * 80)
        for f in sorted(executables, key=lambda x: x['name']):
            print(f"   {f['name']:<30} {f['path']}")

    # Print DLLs
    if dlls:
        print("\n" + "=" * 80)
        print("DLLs")
        print("=" * 80)
        for f in sorted(dlls, key=lambda x: x['name']):
            print(f"   {f['name']:<30} {f['path']}")

    # Print configs
    if configs:
        print("\n" + "=" * 80)
        print("CONFIGURATION FILES")
        print("=" * 80)
        for f in sorted(configs, key=lambda x: x['name']):
            print(f"   {f['name']:<30} {f['path']}")

    # Look for Control Center specifically
    print("\n" + "=" * 80)
    print("CONTROL CENTER CANDIDATES:")
    print("=" * 80)

    cc_keywords = ['CONTROL', 'CENTER', 'MKDE', 'ADMIN', 'MANAGE', 'CONFIG']
    cc_candidates = [f for f in executables if any(k in f['name'].upper() for k in cc_keywords)]

    if cc_candidates:
        for f in cc_candidates:
            print(f"   ✅ {f['name']:<30} {f['path']}")
    else:
        print("   ❌ No Control Center executable found")

    # Look for w3btrv7.dll
    print("\n" + "=" * 80)
    print("BTRIEVE DLL LOCATION:")
    print("=" * 80)

    btr_dlls = [f for f in dlls if 'W3BTRV' in f['name'].upper()]
    if btr_dlls:
        for f in btr_dlls:
            print(f"   ✅ {f['name']:<30} {f['path']}")
    else:
        print("   ❌ w3btrv7.dll not found")

    print("\n" + "=" * 80 + "\n")


def check_nex_genesis_config():
    """Check NEX Genesis configuration files."""

    print("\n" + "=" * 80)
    print("NEX GENESIS CONFIGURATION")
    print("=" * 80)

    nex_dirs = [
        r"C:\NEX",
        r"C:\Program Files (x86)\NEX",
        r"C:\Program Files\NEX",
    ]

    for nex_dir in nex_dirs:
        if not os.path.exists(nex_dir):
            continue

        print(f"\n📁 Searching: {nex_dir}")

        # Look for .ini, .cfg files
        for dirpath, dirnames, filenames in os.walk(nex_dir):
            for filename in filenames:
                if filename.upper().endswith(('.INI', '.CFG', '.CONF', '.CONFIG')):
                    full_path = os.path.join(dirpath, filename)
                    print(f"   {filename:<30} {full_path}")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    find_pervasive_files()
    check_nex_genesis_config()