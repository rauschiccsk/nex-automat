# Fix NSSM environment variables with correct format

import subprocess
from pathlib import Path

SERVICE_NAME = "NEX-Automat-Loader"
NSSM_PATH = Path(r"C:\Deployment\nex-automat\tools\nssm\win64\nssm.exe")

print("=" * 70)
print("FIX NSSM ENVIRONMENT VARIABLES - CORRECT FORMAT")
print("=" * 70)

# Stop service
print("\nSTEP 1: Stop service")
print("-" * 70)
subprocess.run(f'net stop "{SERVICE_NAME}"', capture_output=True, shell=True)
print("✅ Service stopped")

# Clear old AppEnvironmentExtra first
print("\nSTEP 2: Clear old AppEnvironmentExtra")
print("-" * 70)
result = subprocess.run(
    f'"{NSSM_PATH}" set "{SERVICE_NAME}" AppEnvironmentExtra ""',
    capture_output=True,
    text=True,
    shell=True
)
print("✅ Cleared")

# Set PYTHONIOENCODING separately
print("\nSTEP 3: Set PYTHONIOENCODING")
print("-" * 70)
result = subprocess.run(
    f'"{NSSM_PATH}" set "{SERVICE_NAME}" AppEnvironment PYTHONIOENCODING=utf-8',
    capture_output=True,
    text=True,
    shell=True
)
if result.returncode == 0:
    print("✅ PYTHONIOENCODING=utf-8")
else:
    print(f"⚠️  {result.stderr}")

# Add PATH to AppEnvironmentExtra using proper syntax
print("\nSTEP 4: Set PATH in AppEnvironmentExtra")
print("-" * 70)

# NSSM needs PATH with + prefix to append to existing
result = subprocess.run(
    f'"{NSSM_PATH}" set "{SERVICE_NAME}" AppEnvironmentExtra +PATH="C:\\PVSW\\bin"',
    capture_output=True,
    text=True,
    shell=True
)

if result.returncode == 0:
    print("✅ PATH prepended with C:\\PVSW\\bin")
else:
    print(f"⚠️  {result.stderr if result.stderr else result.stdout}")

# Verify
print("\nSTEP 5: Verify configuration")
print("-" * 70)

result = subprocess.run(
    f'"{NSSM_PATH}" get "{SERVICE_NAME}" AppEnvironment',
    capture_output=True,
    text=True,
    shell=True
)
print(f"AppEnvironment: {result.stdout.strip()}")

result = subprocess.run(
    f'"{NSSM_PATH}" get "{SERVICE_NAME}" AppEnvironmentExtra',
    capture_output=True,
    text=True,
    shell=True
)
env_extra = result.stdout.strip()
print(f"AppEnvironmentExtra: {env_extra[:100]}...")

# Start service
print("\nSTEP 6: Start service")
print("-" * 70)
result = subprocess.run(
    f'net start "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if result.returncode == 0:
    print("✅ Service started")
else:
    print(f"❌ Start failed: {result.stdout}")

# Wait and check
import time

print("\nWaiting 8 seconds for initialization...")
time.sleep(8)

print("\nSTEP 7: Check service status")
print("-" * 70)
result = subprocess.run(
    f'sc query "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if "RUNNING" in result.stdout:
    print("✅ Service is RUNNING")

    # Check port
    time.sleep(2)
    result = subprocess.run(
        'netstat -ano | findstr ":8001"',
        capture_output=True,
        text=True,
        shell=True
    )

    if result.stdout:
        print("✅ Port 8001 is listening!")
    else:
        print("⚠️  Port 8001 not yet listening, waiting...")
        time.sleep(5)
        result = subprocess.run(
            'netstat -ano | findstr ":8001"',
            capture_output=True,
            text=True,
            shell=True
        )
        if result.stdout:
            print("✅ Port 8001 is NOW listening!")

elif "PAUSED" in result.stdout:
    print("⚠️  Service is PAUSED")
    print("\nCheck logs:")
    print("  python scripts/27_check_service_logs.py")
else:
    print(f"⚠️  Status: {result.stdout}")

print("\n" + "=" * 70)
print("ENVIRONMENT FIX COMPLETE")
print("=" * 70)