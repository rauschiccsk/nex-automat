# Check NSSM service configuration in detail

import subprocess
from pathlib import Path

SERVICE_NAME = "NEX-Automat-Loader"
NSSM_PATH = Path(r"C:\Deployment\nex-automat\tools\nssm\win64\nssm.exe")

print("=" * 70)
print("CHECK NSSM SERVICE CONFIGURATION")
print("=" * 70)

if not NSSM_PATH.exists():
    print(f"❌ NSSM not found: {NSSM_PATH}")
    exit(1)

print(f"✅ NSSM: {NSSM_PATH}\n")

# Get all NSSM parameters
nssm_params = [
    "Application",
    "AppDirectory",
    "AppParameters",
    "AppEnvironment",
    "AppEnvironmentExtra",
    "DisplayName",
    "Description",
    "Start",
    "Type",
    "ObjectName",
    "Path",
]

print("NSSM Configuration:")
print("=" * 70)

for param in nssm_params:
    result = subprocess.run(
        f'"{NSSM_PATH}" get "{SERVICE_NAME}" {param}',
        capture_output=True,
        text=True,
        shell=True
    )

    if result.returncode == 0:
        value = result.stdout.strip()
        if value:
            print(f"{param:20s}: {value}")
        else:
            print(f"{param:20s}: (not set)")
    else:
        print(f"{param:20s}: (error reading)")

# Check stdout/stderr configuration
print("\n" + "=" * 70)
print("LOGGING CONFIGURATION:")
print("=" * 70)

log_params = ["AppStdout", "AppStderr"]
for param in log_params:
    result = subprocess.run(
        f'"{NSSM_PATH}" get "{SERVICE_NAME}" {param}',
        capture_output=True,
        text=True,
        shell=True
    )
    if result.returncode == 0:
        print(f"{param:20s}: {result.stdout.strip()}")

# Suggest fixes
print("\n" + "=" * 70)
print("POTENTIAL ISSUES & FIXES:")
print("=" * 70)

print("\n1. Check if AppDirectory is set correctly:")
print(f'   "{NSSM_PATH}" get "{SERVICE_NAME}" AppDirectory')
print(f'   Expected: C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader')

print("\n2. Check if PATH environment variable includes Btrieve:")
print(f'   "{NSSM_PATH}" get "{SERVICE_NAME}" AppEnvironmentExtra')
print(f'   Should include: PATH=C:\\PVSW\\bin;...')

print("\n3. Set AppEnvironmentExtra to include Btrieve path:")
print(f'   "{NSSM_PATH}" set "{SERVICE_NAME}" AppEnvironmentExtra "PATH=C:\\PVSW\\bin;%PATH%"')

print("\n4. Set AppDirectory:")
print(
    f'   "{NSSM_PATH}" set "{SERVICE_NAME}" AppDirectory "C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader"')

print("\n5. After changes, restart service:")
print(f'   net stop "{SERVICE_NAME}"')
print(f'   net start "{SERVICE_NAME}"')

print("\n" + "=" * 70)