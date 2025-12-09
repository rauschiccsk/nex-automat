# Deploy changes from Development to Deployment (Production)

import shutil
import subprocess
from pathlib import Path
from datetime import datetime

DEV_ROOT = Path(r"C:\Development\nex-automat")
DEPLOY_ROOT = Path(r"C:\Deployment\nex-automat")

print("=" * 70)
print("PRODUCTION DEPLOYMENT - NEX AUTOMAT v2.4 Phase 4")
print("=" * 70)
print(f"Source:      {DEV_ROOT}")
print(f"Destination: {DEPLOY_ROOT}")
print(f"Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Files to deploy
files_to_deploy = [
    "packages/nexdata/nexdata/models/gscat.py",
    "packages/nexdata/nexdata/repositories/gscat_repository.py",
    "scripts/test_ean_lookup.py",
    "scripts/reprocess_nex_enrichment.py",
]

print("\nSTEP 1: Verify Deployment directory exists")
print("-" * 70)
if not DEPLOY_ROOT.exists():
    print(f"❌ ERROR: Deployment directory not found: {DEPLOY_ROOT}")
    exit(1)
print(f"✅ Deployment directory exists")

print("\nSTEP 2: Pull latest changes from Git")
print("-" * 70)
try:
    result = subprocess.run(
        ["git", "pull", "origin", "develop"],
        cwd=DEPLOY_ROOT,
        capture_output=True,
        text=True,
        check=True
    )
    print("✅ Git pull successful")
    if result.stdout:
        print(f"   Output: {result.stdout.strip()}")
except subprocess.CalledProcessError as e:
    print(f"❌ ERROR: Git pull failed")
    print(f"   Error: {e.stderr}")
    exit(1)

print("\nSTEP 3: Verify deployed files")
print("-" * 70)
all_ok = True
for file_path in files_to_deploy:
    deploy_file = DEPLOY_ROOT / file_path
    if deploy_file.exists():
        size = deploy_file.stat().st_size
        print(f"✅ {file_path} ({size} bytes)")
    else:
        print(f"❌ {file_path} - NOT FOUND!")
        all_ok = False

if not all_ok:
    print("\n❌ ERROR: Some files missing after deployment")
    exit(1)

print("\nSTEP 4: Compare key files")
print("-" * 70)
# Compare gscat.py to ensure it has correct offset
deploy_gscat = DEPLOY_ROOT / "packages/nexdata/nexdata/models/gscat.py"
content = deploy_gscat.read_text(encoding='utf-8')

checks = [
    ("BarCode field exists", "BarCode: str" in content),
    ("Correct offset comment", "Offset 60-74" in content or "offset 60" in content.lower()),
    ("from_bytes method", "def from_bytes" in content),
    ("Record size 705", "705 bytes" in content or "705" in content),
]

for check_name, result in checks:
    if result:
        print(f"✅ {check_name}")
    else:
        print(f"⚠️  {check_name} - NOT FOUND")

print("\n" + "=" * 70)
print("DEPLOYMENT SUMMARY")
print("=" * 70)
print(f"✅ Files deployed: {len(files_to_deploy)}")
print(f"✅ Git pull: successful")
print(f"✅ File verification: passed")
print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Restart NEX-Automat-Loader service")
print("2. Verify service is running on port 8001")
print("3. Run Mágerstav verification test")
print("\nService control:")
print("  - Service name: NEX-Automat-Loader")
print("  - Start manually from Services.msc or:")
print("  - net start NEX-Automat-Loader")
print("=" * 70)