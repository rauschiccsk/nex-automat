# Copy NSSM from Development to Deployment

import shutil
from pathlib import Path

SOURCE_NSSM = Path(r"C:\Tools\nssm")
DEPLOY_NSSM = Path(r"C:\Deployment\nex-automat\tools\nssm")
NSSM_EXE = DEPLOY_NSSM / "win64" / "nssm.exe"

print("=" * 70)
print("COPY NSSM TO DEPLOYMENT")
print("=" * 70)
print(f"Source:      {SOURCE_NSSM}")
print(f"Destination: {DEPLOY_NSSM}")
print("=" * 70)

# Check source exists
print("\nSTEP 1: Check source")
print("-" * 70)
if not SOURCE_NSSM.exists():
    print(f"❌ NSSM not found: {SOURCE_NSSM}")
    print("\nDownload NSSM from: https://nssm.cc/download")
    print("Extract to: C:\\Tools\\nssm\\")
    exit(1)

print(f"✅ Source exists: {SOURCE_NSSM}")

# List what will be copied
source_files = list(SOURCE_NSSM.rglob("*"))
print(f"   Files to copy: {len([f for f in source_files if f.is_file()])}")

# Create destination directory
print("\nSTEP 2: Prepare destination")
print("-" * 70)
DEPLOY_NSSM.parent.mkdir(parents=True, exist_ok=True)
print(f"✅ Directory ready: {DEPLOY_NSSM.parent}")

# Copy directory
print("\nSTEP 3: Copy files")
print("-" * 70)
try:
    if DEPLOY_NSSM.exists():
        print(f"⚠️  Destination exists, removing old version...")
        shutil.rmtree(DEPLOY_NSSM)

    shutil.copytree(SOURCE_NSSM, DEPLOY_NSSM)
    print(f"✅ Copied successfully")
except Exception as e:
    print(f"❌ Copy failed: {e}")
    exit(1)

# Verify
print("\nSTEP 4: Verify")
print("-" * 70)
if NSSM_EXE.exists():
    print(f"✅ NSSM executable: {NSSM_EXE}")
    print(f"   Size: {NSSM_EXE.stat().st_size:,} bytes")

    # List all files
    copied_files = list(DEPLOY_NSSM.rglob("*"))
    file_count = len([f for f in copied_files if f.is_file()])
    print(f"   Total files: {file_count}")

    # Show structure
    print("\n   Directory structure:")
    for item in sorted(DEPLOY_NSSM.rglob("*.exe")):
        rel_path = item.relative_to(DEPLOY_NSSM)
        print(f"     {rel_path}")
else:
    print(f"❌ NSSM executable not found: {NSSM_EXE}")
    exit(1)

print("\n" + "=" * 70)
print("✅ NSSM COPY SUCCESSFUL")
print("=" * 70)
print("\nNext step: Restart service")
print("  python scripts/22_restart_service.py")
print("=" * 70)