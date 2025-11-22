"""
Deploy to Deployment Environment
================================
Copies updated files from Development to Deployment after Git commit.

Prerequisites:
- Git commit done (all changes committed)
- Git push done (changes pushed to GitHub)

Usage:
    cd C:\Development\nex-automat
    python scripts\deploy_to_deployment.py
"""

import shutil
from pathlib import Path

def deploy():
    """Deploy to Deployment environment."""
    dev_root = Path("C:/Development/nex-automat")
    deploy_root = Path("C:/Deployment/nex-automat")

    if not dev_root.exists():
        print("❌ Development not found:", dev_root)
        return False

    if not deploy_root.exists():
        print("❌ Deployment not found:", deploy_root)
        return False

    print("Deploying to Deployment environment...")

    # Files to deploy
    files_to_deploy = [
        "scripts/day5_preflight_check.py",
        "scripts/fix_day5_preflight_issues.py",
        "apps/supplier-invoice-loader/requirements.txt"
    ]

    for file_path in files_to_deploy:
        src = dev_root / file_path
        dst = deploy_root / file_path

        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ Deployed: {file_path}")
        else:
            print(f"⚠️  Not found: {file_path}")

    print("\n✅ Deployment complete!")
    print("\nNext steps:")
    print("1. cd C:\\Deployment\\nex-automat")
    print("2. pip install pillow")
    print("3. python scripts\\day5_preflight_check.py")

    return True

if __name__ == "__main__":
    deploy()
