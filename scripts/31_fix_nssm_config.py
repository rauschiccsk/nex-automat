# Fix NSSM service configuration

import subprocess
from pathlib import Path

SERVICE_NAME = "NEX-Automat-Loader"
NSSM_PATH = Path(r"C:\Deployment\nex-automat\tools\nssm\win64\nssm.exe")

print("=" * 70)
print("FIX NSSM SERVICE CONFIGURATION")
print("=" * 70)


def run_nssm_command(action, param, value=None):
    """Run NSSM command and return success status"""
    if value:
        cmd = f'"{NSSM_PATH}" {action} "{SERVICE_NAME}" {param} "{value}"'
    else:
        cmd = f'"{NSSM_PATH}" {action} "{SERVICE_NAME}" {param}'

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()


# Stop service first
print("\nSTEP 1: Stop service")
print("-" * 70)
result = subprocess.run(f'net stop "{SERVICE_NAME}"', capture_output=True, text=True, shell=True)
if result.returncode == 0 or "service is not started" in result.stdout.lower():
    print("✅ Service stopped")
else:
    print(f"⚠️  {result.stdout.strip()}")

# Fix AppDirectory
print("\nSTEP 2: Set correct AppDirectory")
print("-" * 70)
app_dir = r"C:\Deployment\nex-automat\apps\supplier-invoice-loader"
success, stdout, stderr = run_nssm_command("set", "AppDirectory", app_dir)

if success:
    print(f"✅ AppDirectory set to: {app_dir}")
else:
    print(f"❌ Failed: {stderr if stderr else stdout}")
    exit(1)

# Fix AppEnvironmentExtra with both PYTHONIOENCODING and PATH
print("\nSTEP 3: Set AppEnvironmentExtra (PATH + encoding)")
print("-" * 70)

# NSSM environment format: VAR1=value1\0VAR2=value2
# We need to preserve PYTHONIOENCODING and add PATH
env_value = r"PYTHONIOENCODING=utf-8 PATH=C:\PVSW\bin;%PATH%"

success, stdout, stderr = run_nssm_command("set", "AppEnvironmentExtra", env_value)

if success:
    print(f"✅ AppEnvironmentExtra set:")
    print(f"   PYTHONIOENCODING=utf-8")
    print(f"   PATH=C:\\PVSW\\bin;%PATH%")
else:
    print(f"❌ Failed: {stderr if stderr else stdout}")
    exit(1)

# Verify changes
print("\nSTEP 4: Verify configuration")
print("-" * 70)

success, app_dir_actual, _ = run_nssm_command("get", "AppDirectory")
if success:
    print(f"AppDirectory: {app_dir_actual}")
    if app_dir in app_dir_actual:
        print("  ✅ Correct")
    else:
        print("  ⚠️  Still incorrect")

success, env_actual, _ = run_nssm_command("get", "AppEnvironmentExtra")
if success:
    print(f"AppEnvironmentExtra: {env_actual}")
    if "PATH" in env_actual and "PVSW" in env_actual:
        print("  ✅ PATH includes Btrieve")
    else:
        print("  ⚠️  PATH not set correctly")

# Start service
print("\nSTEP 5: Start service")
print("-" * 70)
result = subprocess.run(f'net start "{SERVICE_NAME}"', capture_output=True, text=True, shell=True)

if result.returncode == 0:
    print("✅ Service started successfully")
    print(result.stdout.strip())
else:
    print(f"❌ Failed to start: {result.stderr if result.stderr else result.stdout}")
    print("\nCheck logs:")
    print("  C:\\Deployment\\nex-automat\\logs\\service-stderr.log")
    exit(1)

# Wait and check status
import time

print("\nWaiting 5 seconds for initialization...")
time.sleep(5)

print("\nSTEP 6: Verify service status")
print("-" * 70)
result = subprocess.run(f'sc query "{SERVICE_NAME}"', capture_output=True, text=True, shell=True)

if "RUNNING" in result.stdout:
    print("✅ Service is RUNNING")
elif "PAUSED" in result.stdout:
    print("⚠️  Service is PAUSED - check logs for errors")
else:
    print(f"⚠️  Unexpected status:")
    print(result.stdout)

# Check port
print("\nSTEP 7: Check port 8001")
print("-" * 70)
result = subprocess.run('netstat -ano | findstr ":8001"', capture_output=True, text=True, shell=True)

if result.stdout:
    print("✅ Port 8001 is listening")
else:
    print("⚠️  Port 8001 not listening yet")
    print("   Wait a moment and check logs")

print("\n" + "=" * 70)
print("✅ NSSM CONFIGURATION FIXED")
print("=" * 70)
print("\nIf service is still PAUSED or has errors:")
print("  python scripts/27_check_service_logs.py")
print("=" * 70)