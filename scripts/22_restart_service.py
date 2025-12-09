# Restart NEX-Automat-Loader service

import subprocess
import time
from datetime import datetime

SERVICE_NAME = "NEX-Automat-Loader"

print("=" * 70)
print("RESTART NEX-AUTOMAT-LOADER SERVICE")
print("=" * 70)
print(f"Service: {SERVICE_NAME}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)


def run_command(command, description):
    """Run command and return success status"""
    print(f"\n{description}")
    print("-" * 70)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=False
        )

        if result.returncode == 0:
            print(f"✅ Success")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️  Return code: {result.returncode}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


# Check if service exists
print("\nSTEP 1: Check service status")
print("-" * 70)
result = subprocess.run(
    f'sc query "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if "The specified service does not exist" in result.stdout:
    print(f"❌ Service '{SERVICE_NAME}' does not exist!")
    print("\nService might be started manually or with different name.")
    print("Check Services.msc or use:")
    print(f'  sc query type= service state= all | findstr /i "nex"')
    exit(1)

print(f"✅ Service exists")
if "RUNNING" in result.stdout:
    print("   Current state: RUNNING")
elif "STOPPED" in result.stdout:
    print("   Current state: STOPPED")
else:
    print(f"   State: {result.stdout}")

# Stop service
print("\nSTEP 2: Stop service")
print("-" * 70)
print("Attempting to stop service...")
result = subprocess.run(
    f'net stop "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if result.returncode == 0:
    print("✅ Service stopped")
elif "service is not started" in result.stdout.lower():
    print("⚪ Service was not running")
else:
    print(f"⚠️  Stop result: {result.stdout.strip()}")

# Wait a moment
print("\nWaiting 3 seconds...")
time.sleep(3)

# Start service
print("\nSTEP 3: Start service")
print("-" * 70)
print("Attempting to start service...")
result = subprocess.run(
    f'net start "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if result.returncode == 0:
    print("✅ Service started successfully")
    if result.stdout.strip():
        print(f"   {result.stdout.strip()}")
else:
    print(f"❌ Failed to start service")
    print(f"   Error: {result.stderr.strip() if result.stderr else result.stdout.strip()}")
    print("\nTry starting manually:")
    print("1. Open Services.msc")
    print(f"2. Find '{SERVICE_NAME}'")
    print("3. Right-click → Start")
    print("\nOr check service configuration:")
    print(f'   sc qc "{SERVICE_NAME}"')
    exit(1)

# Wait for service to initialize
print("\nWaiting 5 seconds for service initialization...")
time.sleep(5)

# Verify service is running
print("\nSTEP 4: Verify service status")
print("-" * 70)
result = subprocess.run(
    f'sc query "{SERVICE_NAME}"',
    capture_output=True,
    text=True,
    shell=True
)

if "RUNNING" in result.stdout:
    print("✅ Service is RUNNING")
elif "STOPPED" in result.stdout:
    print("❌ Service is STOPPED")
    print("   Service failed to start. Check logs:")
    print("   C:\\Deployment\\nex-automat\\logs\\")
    exit(1)
else:
    print(f"⚠️  Unexpected status: {result.stdout}")

# Check if port 8001 is listening
print("\nSTEP 5: Check API endpoint")
print("-" * 70)
result = subprocess.run(
    'netstat -ano | findstr ":8001"',
    capture_output=True,
    text=True,
    shell=True
)

if result.stdout:
    print("✅ Port 8001 is listening")
    print(f"   {result.stdout.strip()}")
else:
    print("⚠️  Port 8001 not detected yet")
    print("   Service may still be initializing...")

print("\n" + "=" * 70)
print("✅ SERVICE RESTART COMPLETE")
print("=" * 70)
print("\nService Information:")
print(f"  Name: {SERVICE_NAME}")
print(f"  Status: RUNNING")
print(f"  Port: 8001")
print(f"  Path: C:\\Deployment\\nex-automat")
print("\nLog files:")
print("  C:\\Deployment\\nex-automat\\logs\\supplier-invoice-loader.log")
print("\n" + "=" * 70)
print("NEXT STEP: Mágerstav Verification")
print("=" * 70)
print("1. Process a test invoice")
print("2. Verify NEX enrichment (81.2% match rate expected)")
print("3. Check nex_gs_code, nex_name, matched_by fields")
print("=" * 70)