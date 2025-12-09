# Check service configuration

import subprocess
from pathlib import Path

SERVICE_NAME = "NEX-Automat-Loader"
DEPLOY_ROOT = Path(r"C:\Deployment\nex-automat")

print("=" * 70)
print("CHECK SERVICE CONFIGURATION")
print("=" * 70)

# Get service config
print("\nSTEP 1: Query service configuration")
print("-" * 70)
result = subprocess.run(
    f'sc qc "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

print(result.stdout)

# Parse BINARY_PATH_NAME
binary_path = None
for line in result.stdout.split('\n'):
    if 'BINARY_PATH_NAME' in line:
        # Extract path after colon
        parts = line.split(':', 1)
        if len(parts) > 1:
            binary_path = parts[1].strip()
            print(f"\nConfigured binary path:")
            print(f"  {binary_path}")

if not binary_path:
    print("❌ Could not find BINARY_PATH_NAME in service config")
    exit(1)

# Check if path exists
print("\nSTEP 2: Verify binary path")
print("-" * 70)

# Clean up path (remove quotes if present)
clean_path = binary_path.strip('"')

# Check if it's a full path or needs to be resolved
if Path(clean_path).exists():
    print(f"✅ Binary exists: {clean_path}")
else:
    print(f"❌ Binary NOT FOUND: {clean_path}")

    # Suggest correct paths
    print("\nLooking for main.py in deployment...")
    main_py = DEPLOY_ROOT / "apps" / "supplier-invoice-loader" / "main.py"
    python_exe = DEPLOY_ROOT / "venv32" / "Scripts" / "python.exe"

    if main_py.exists():
        print(f"✅ Found main.py: {main_py}")
    else:
        print(f"❌ main.py not found: {main_py}")

    if python_exe.exists():
        print(f"✅ Found python.exe: {python_exe}")
    else:
        print(f"❌ python.exe not found: {python_exe}")

    print("\nCorrect service command should be:")
    print(f'  "{python_exe}" "{main_py}"')

    print("\nTo fix service, run as Administrator:")
    print(f'  sc config "{SERVICE_NAME}" binPath= "\\"{python_exe}\\" \\"{main_py}\\""')

# Check for nssm (if used)
print("\nSTEP 3: Check if NSSM is used")
print("-" * 70)
if 'nssm' in binary_path.lower():
    print("✅ Service uses NSSM (Non-Sucking Service Manager)")
    nssm_path = binary_path.split()[0].strip('"')

    if Path(nssm_path).exists():
        print(f"   NSSM exists: {nssm_path}")

        # Get NSSM configuration
        print("\n   Checking NSSM configuration...")
        result = subprocess.run(
            f'"{nssm_path}" get "{SERVICE_NAME}" Application',
            capture_output=True,
            text=True,
            shell=True
        )
        app_path = result.stdout.strip()
        print(f"   Application: {app_path}")

        if app_path and Path(app_path).exists():
            print(f"   ✅ Application exists")
        else:
            print(f"   ❌ Application NOT FOUND: {app_path}")
    else:
        print(f"   ❌ NSSM not found: {nssm_path}")
else:
    print("⚪ Service does not use NSSM")

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)