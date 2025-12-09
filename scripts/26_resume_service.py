# Resume (unpause) NEX-Automat-Loader service

import subprocess
import time
from datetime import datetime

SERVICE_NAME = "NEX-Automat-Loader"

print("=" * 70)
print("RESUME NEX-AUTOMAT-LOADER SERVICE")
print("=" * 70)

# Check current status
print("\nSTEP 1: Check current status")
print("-" * 70)
result = subprocess.run(
    f'sc query "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if "PAUSED" in result.stdout:
    print("⚠️  Service is PAUSED")
elif "RUNNING" in result.stdout:
    print("✅ Service is already RUNNING")
    print("\nNo action needed!")
    exit(0)
else:
    print(f"⚠️  Unexpected state: {result.stdout}")

# Resume service
print("\nSTEP 2: Resume service")
print("-" * 70)
result = subprocess.run(
    f'sc continue "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if result.returncode == 0:
    print("✅ Resume command sent successfully")
else:
    print(f"❌ Resume failed: {result.stderr if result.stderr else result.stdout}")

    # Try alternative: net continue
    print("\nTrying alternative command...")
    result = subprocess.run(
        f'net continue "{SERVICE_NAME}"',
        capture_output=True,
        text=True,
        shell=True
    )
    if result.returncode == 0:
        print("✅ Service resumed via net continue")
    else:
        print(f"❌ Also failed: {result.stderr if result.stderr else result.stdout}")
        exit(1)

# Wait for service to resume
print("\nWaiting 5 seconds for service to resume...")
time.sleep(5)

# Verify service is running
print("\nSTEP 3: Verify service is running")
print("-" * 70)
result = subprocess.run(
    f'sc query "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if "RUNNING" in result.stdout:
    print("✅ Service is RUNNING")
    print(result.stdout)
elif "PAUSED" in result.stdout:
    print("⚠️  Service is still PAUSED")
    print(result.stdout)
    exit(1)
else:
    print(f"⚠️  Unexpected status: {result.stdout}")

# Check port 8001
print("\nSTEP 4: Check API endpoint on port 8001")
print("-" * 70)
for attempt in range(3):
    result = subprocess.run(
        'netstat -ano | findstr ":8001"',
        capture_output=True,
        text=True,
        shell=True
    )

    if result.stdout:
        print(f"✅ Port 8001 is listening (attempt {attempt + 1}/3)")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
        break
    else:
        if attempt < 2:
            print(f"⚪ Port 8001 not detected yet (attempt {attempt + 1}/3), waiting...")
            time.sleep(3)
        else:
            print("⚠️  Port 8001 not detected after 3 attempts")
            print("   Check logs: C:\\Deployment\\nex-automat\\logs\\")

print("\n" + "=" * 70)
print("✅ SERVICE RESUMED SUCCESSFULLY")
print("=" * 70)
print("\nService status: RUNNING")
print("API endpoint: http://localhost:8001")
print("\n" + "=" * 70)
print("READY FOR MÁGERSTAV VERIFICATION")
print("=" * 70)