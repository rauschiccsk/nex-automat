# Restore NSSM from stash

import subprocess
from pathlib import Path

DEPLOY_ROOT = Path(r"C:\Deployment\nex-automat")
NSSM_PATH = DEPLOY_ROOT / "tools" / "nssm" / "win64" / "nssm.exe"

print("=" * 70)
print("RESTORE NSSM FROM STASH")
print("=" * 70)

# Check stash list
print("\nSTEP 1: List stashed changes")
print("-" * 70)
result = subprocess.run(
    ["git", "stash", "list"],
    cwd=DEPLOY_ROOT,
    capture_output=True,
    text=True
)

if result.stdout:
    print("Available stashes:")
    for line in result.stdout.strip().split('\n'):
        print(f"  {line}")
else:
    print("⚪ No stashes found")
    exit(1)

# Show what's in the latest stash
print("\nSTEP 2: Check if tools/nssm is in stash")
print("-" * 70)
result = subprocess.run(
    ["git", "stash", "show", "--name-only", "stash@{0}"],
    cwd=DEPLOY_ROOT,
    capture_output=True,
    text=True
)

has_nssm = False
if result.stdout:
    for line in result.stdout.strip().split('\n'):
        if 'tools/nssm' in line:
            has_nssm = True
            print(f"  ✅ Found: {line}")

if not has_nssm:
    print("  ❌ tools/nssm not found in stash")
    print("\n  Checking older stashes...")

    # Check stash@{1} if exists
    result = subprocess.run(
        ["git", "stash", "show", "--name-only", "stash@{1}"],
        cwd=DEPLOY_ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout and 'tools/nssm' in result.stdout:
        print("  ✅ Found in stash@{1}")
        has_nssm = True

if not has_nssm:
    print("\n❌ NSSM not found in any stash")
    print("\nAlternative: Download NSSM manually")
    print("  1. Download from: https://nssm.cc/download")
    print("  2. Extract to: C:\\Deployment\\nex-automat\\tools\\nssm\\")
    print("  3. Or copy from Development:")
    print(f"     xcopy C:\\Development\\nex-automat\\tools\\nssm C:\\Deployment\\nex-automat\\tools\\nssm /E /I")
    exit(1)

# Restore only tools/nssm from stash
print("\nSTEP 3: Restore tools/nssm from stash")
print("-" * 70)
print("Restoring tools/nssm directory...")

result = subprocess.run(
    ["git", "checkout", "stash@{0}", "--", "tools/nssm"],
    cwd=DEPLOY_ROOT,
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ Successfully restored tools/nssm")
else:
    print(f"❌ Failed to restore: {result.stderr}")
    exit(1)

# Verify NSSM exists now
print("\nSTEP 4: Verify NSSM")
print("-" * 70)
if NSSM_PATH.exists():
    print(f"✅ NSSM exists: {NSSM_PATH}")
    print(f"   Size: {NSSM_PATH.stat().st_size} bytes")

    # Test NSSM
    result = subprocess.run(
        [str(NSSM_PATH), "version"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"   Version: {result.stdout.strip()}")

else:
    print(f"❌ NSSM still not found: {NSSM_PATH}")
    exit(1)

print("\n" + "=" * 70)
print("✅ NSSM RESTORED SUCCESSFULLY")
print("=" * 70)
print("\nNext step: Restart service")
print("  python scripts/22_restart_service.py")
print("=" * 70)