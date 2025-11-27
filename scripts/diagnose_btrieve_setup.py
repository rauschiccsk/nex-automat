#!/usr/bin/env python3
"""
Diagnose Btrieve setup and file access
"""

import subprocess
from pathlib import Path
import os

print("=" * 70)
print("Btrieve Setup Diagnostics")
print("=" * 70)
print()

# 1. Check Btrieve service
print("1. Btrieve Service Status:")
try:
    result = subprocess.run(
        ['sc', 'query', 'psqlWGE'],
        capture_output=True,
        text=True
    )
    if 'RUNNING' in result.stdout:
        print("   ✅ psqlWGE service is RUNNING")
    elif 'STOPPED' in result.stdout:
        print("   ❌ psqlWGE service is STOPPED")
        print("   Run: net start psqlWGE")
    else:
        print("   ⚠️  Service status unknown")
        print(result.stdout)
except Exception as e:
    print(f"   ❌ Error checking service: {e}")

print()

# 2. Check file exists and permissions
print("2. File Access Check:")
test_file = Path(r"C:\NEX\YEARACT\STORES\GSCAT.BTR")
print(f"   File: {test_file}")
print(f"   Exists: {test_file.exists()}")

if test_file.exists():
    stat = test_file.stat()
    print(f"   Size: {stat.st_size:,} bytes")
    print(f"   Readable: {os.access(test_file, os.R_OK)}")
    print(f"   Writable: {os.access(test_file, os.W_OK)}")
else:
    print("   ❌ File does not exist!")

print()

# 3. Check Btrieve DLL
print("3. Btrieve DLL Check:")
dll_path = Path(r"C:\Program Files (x86)\Pervasive Software\PSQL\bin\w3btrv7.dll")
print(f"   DLL: {dll_path}")
print(f"   Exists: {dll_path.exists()}")

if dll_path.exists():
    stat = dll_path.stat()
    print(f"   Size: {stat.st_size:,} bytes")

print()

# 4. Check for Btrieve config
print("4. Btrieve Configuration:")
possible_configs = [
    r"C:\Program Files (x86)\Pervasive Software\PSQL\pvsw.ini",
    r"C:\ProgramData\Pervasive Software\PSQL\pvsw.ini",
    r"C:\NEX\btrieve.cfg",
]

for config_path in possible_configs:
    config = Path(config_path)
    if config.exists():
        print(f"   ✓ Found: {config}")
    else:
        print(f"   ✗ Not found: {config}")

print()

# 5. Check if nex-genesis-server can access the file
print("5. NEX Genesis Server Check:")
nex_server = Path(r"C:\Development\nex-genesis-server")
if nex_server.exists():
    print(f"   ✓ nex-genesis-server found: {nex_server}")

    # Check if it has Btrieve client
    btrieve_client = nex_server / "src" / "database" / "btrieve_client.py"
    if btrieve_client.exists():
        print(f"   ✓ btrieve_client.py exists")
else:
    print(f"   ✗ nex-genesis-server not found")

print()

# 6. Test with nex-genesis-server approach
print("6. Quick Reference Check:")
print("   Compare our implementation with nex-genesis-server:")
print("   - Same DLL path?")
print("   - Same parameter types?")
print("   - Same operation codes?")

print()
print("=" * 70)
print()
print("Recommendation:")
print("  If psqlWGE service is running and file exists,")
print("  check nex-genesis-server implementation for differences.")
print()
print("=" * 70)