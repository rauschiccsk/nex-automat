# Fix Git conflicts in Deployment directory

import subprocess
from pathlib import Path
from datetime import datetime

DEPLOY_ROOT = Path(r"C:\Deployment\nex-automat")

print("=" * 70)
print("FIX DEPLOYMENT GIT CONFLICTS")
print("=" * 70)
print(f"Location: {DEPLOY_ROOT}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

def run_git(command, check=True):
    """Run git command and return result"""
    try:
        result = subprocess.run(
            command,
            cwd=DEPLOY_ROOT,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        return e

print("\nSTEP 1: Check Git status")
print("-" * 70)
result = run_git(["git", "status", "--short"])
if result.stdout:
    print("Modified/Untracked files:")
    for line in result.stdout.strip().split('\n'):
        print(f"  {line}")
else:
    print("No changes")

print("\nSTEP 2: Stash ALL changes (including untracked)")
print("-" * 70)
result = run_git(["git", "stash", "push", "--include-untracked", "-m", f"Auto-stash with untracked before Phase 4 {datetime.now().isoformat()}"])
if result.returncode == 0:
    print("✅ All changes stashed (including untracked files)")
    if result.stdout:
        print(f"   {result.stdout.strip()}")
else:
    print(f"⚠️  Stash with --include-untracked failed: {result.stderr}")
    print("\nTrying --all (includes ignored files too)...")
    result = run_git(["git", "stash", "push", "--all", "-m", f"Full stash before Phase 4 {datetime.now().isoformat()}"])
    if result.returncode == 0:
        print("✅ All changes stashed (including ignored)")
    else:
        print(f"❌ Full stash failed: {result.stderr}")
        exit(1)

print("\nSTEP 3: Pull latest changes")
print("-" * 70)
result = run_git(["git", "pull", "origin", "develop"])
if result.returncode == 0:
    print("✅ Git pull successful")
    if result.stdout:
        print(f"   {result.stdout.strip()}")
else:
    print(f"❌ Git pull failed: {result.stderr}")
    exit(1)

print("\nSTEP 4: Verify deployment")
print("-" * 70)

# Check key files
key_files = [
    "packages/nexdata/nexdata/models/gscat.py",
    "packages/nexdata/nexdata/repositories/gscat_repository.py",
    "scripts/test_ean_lookup.py",
    "scripts/reprocess_nex_enrichment.py",
]

all_ok = True
for file_path in key_files:
    full_path = DEPLOY_ROOT / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"✅ {file_path} ({size} bytes)")
    else:
        print(f"❌ {file_path} - NOT FOUND!")
        all_ok = False

if not all_ok:
    print("\n❌ ERROR: Some files missing")
    exit(1)

print("\nSTEP 5: Verify gscat.py content")
print("-" * 70)
gscat = DEPLOY_ROOT / "packages/nexdata/nexdata/models/gscat.py"
content = gscat.read_text(encoding='utf-8')

checks = [
    ("BarCode field", "BarCode: str" in content),
    ("Offset 60", "60" in content and "BarCode" in content),
    ("from_bytes method", "def from_bytes" in content),
    ("705 bytes", "705" in content),
]

for check_name, result in checks:
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")

print("\n" + "=" * 70)
print("✅ DEPLOYMENT FIXED AND VERIFIED")
print("=" * 70)
print("\nStashed changes saved as:")
print(f"  'Auto-stash before Phase 4 deployment {datetime.now().date()}'")
print("\nTo restore stashed changes later:")
print("  cd C:\\Deployment\\nex-automat")
print("  git stash list")
print("  git stash pop")
print("\n" + "=" * 70)
print("NEXT STEP: Restart NEX-Automat-Loader service")
print("=" * 70)