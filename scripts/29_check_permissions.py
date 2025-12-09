# Check file permissions for LocalSystem account

import subprocess
from pathlib import Path

critical_paths = [
    r"C:\PVSW\bin\w3btrv7.dll",
    r"C:\NEX\YEARACT\STORES\GSCAT.BTR",
    r"C:\Deployment\nex-automat",
]

print("=" * 70)
print("CHECK FILE/DIRECTORY PERMISSIONS")
print("=" * 70)
print("\nService runs as: LocalSystem")
print("Checking access to critical paths...")
print("=" * 70)

for path_str in critical_paths:
    path = Path(path_str)
    print(f"\n📁 {path}")
    print("-" * 70)

    if not path.exists():
        print(f"❌ Path does not exist!")
        continue

    # Get ACL using icacls
    result = subprocess.run(
        f'icacls "{path}"',
        capture_output=True,
        text=True,
        shell=True
    )

    if result.returncode == 0:
        acl_lines = result.stdout.strip().split('\n')

        # Check for SYSTEM permissions
        has_system = False
        system_perms = []

        for line in acl_lines:
            if 'NT AUTHORITY\\SYSTEM' in line or 'SYSTEM' in line:
                has_system = True
                system_perms.append(line.strip())

        if has_system:
            print(f"✅ SYSTEM account has access:")
            for perm in system_perms:
                print(f"   {perm}")
        else:
            print(f"⚠️  No explicit SYSTEM permissions found")
            print(f"   First few ACL entries:")
            for line in acl_lines[:5]:
                print(f"   {line}")
    else:
        print(f"❌ Could not read ACL: {result.stderr}")

# Check if we can actually read the files as current user
print("\n" + "=" * 70)
print("TEST FILE ACCESS (as current user)")
print("=" * 70)

dll_path = Path(r"C:\PVSW\bin\w3btrv7.dll")
if dll_path.exists():
    try:
        # Try to open DLL
        with open(dll_path, 'rb') as f:
            f.read(10)
        print(f"✅ Can read: {dll_path}")
    except Exception as e:
        print(f"❌ Cannot read {dll_path}: {e}")

gscat_path = Path(r"C:\NEX\YEARACT\STORES\GSCAT.BTR")
if gscat_path.exists():
    try:
        # Try to open GSCAT
        with open(gscat_path, 'rb') as f:
            f.read(10)
        print(f"✅ Can read: {gscat_path}")
    except Exception as e:
        print(f"❌ Cannot read {gscat_path}: {e}")

print("\n" + "=" * 70)
print("SOLUTION IF PERMISSIONS ARE THE PROBLEM:")
print("=" * 70)
print("\nOption 1: Grant SYSTEM account access")
print(f'  icacls "C:\\PVSW\\bin" /grant "NT AUTHORITY\\SYSTEM:(OI)(CI)RX"')
print(f'  icacls "C:\\NEX" /grant "NT AUTHORITY\\SYSTEM:(OI)(CI)RX"')
print("\nOption 2: Change service account")
print('  sc config "NEX-Automat-Loader" obj= ".\\Administrator" password= "***"')
print("\nOption 3: Run service as NetworkService")
print('  sc config "NEX-Automat-Loader" obj= "NT AUTHORITY\\NetworkService"')
print("=" * 70)