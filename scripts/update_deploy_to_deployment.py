"""
Update Deploy Script
====================
Aktualizuje deploy_to_deployment.py o všetky nové scripty.

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\update_deploy_to_deployment.py
"""

from pathlib import Path


def update_deploy_script():
    """Update deploy_to_deployment.py with all new scripts."""

    deploy_script = Path("scripts/deploy_to_deployment.py")

    if not deploy_script.exists():
        print(f"❌ Deploy script not found: {deploy_script}")
        return False

    new_content = '''"""
Deploy to Deployment Environment
================================
Copies updated files from Development to Deployment after Git commit.

Prerequisites:
- Running from Development environment
- All changes tested locally

Usage:
    cd C:\\\\Development\\\\nex-automat
    python scripts\\\\deploy_to_deployment.py
"""

import shutil
from pathlib import Path
from datetime import datetime

def print_section(title: str):
    """Print formatted section header."""
    print(f"\\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def backup_file(file_path: Path) -> bool:
    """Create backup before overwriting."""
    if not file_path.exists():
        return True

    try:
        backup = file_path.with_suffix(f'.backup_{datetime.now():%Y%m%d_%H%M%S}')
        shutil.copy2(file_path, backup)
        return True
    except Exception as e:
        print(f"  ⚠️  Backup failed: {e}")
        return False

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

    print_section("DEPLOYMENT: Development → Deployment")
    print(f"From: {dev_root}")
    print(f"To:   {deploy_root}")

    # Files to deploy (všetky DAY 5 scripty)
    files_to_deploy = [
        # Core preflight scripts
        "scripts/day5_preflight_check.py",
        "scripts/fix_day5_preflight_issues.py",

        # Diagnostic scripts
        "scripts/diagnose_deployment_issues.py",
        "scripts/analyze_config_location.py",
        "scripts/diagnose_pillow_import.py",

        # Fix scripts
        "scripts/create_day5_preflight_check.py",
        "scripts/fix_preflight_config_path.py",
        "scripts/fix_sqlite_check_final.py",
        "scripts/fix_pillow_import_name.py",
        "scripts/fix_escape_sequence_warning.py",

        # Test scripts
        "scripts/test_preflight_in_development.py",

        # Requirements
        "apps/supplier-invoice-loader/requirements.txt",
        "scripts/requirements.txt",

        # This deployment script itself
        "scripts/deploy_to_deployment.py"
    ]

    print_section("COPYING FILES")

    copied = []
    skipped = []
    failed = []

    for file_path in files_to_deploy:
        src = dev_root / file_path
        dst = deploy_root / file_path

        if not src.exists():
            print(f"⚠️  Skip (not in Dev): {file_path}")
            skipped.append(file_path)
            continue

        try:
            # Backup existing file
            if dst.exists():
                backup_file(dst)

            # Create parent directory
            dst.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(src, dst)

            size_kb = src.stat().st_size / 1024
            print(f"✅ {file_path} ({size_kb:.1f} KB)")
            copied.append(file_path)

        except Exception as e:
            print(f"❌ {file_path} - {e}")
            failed.append(file_path)

    # Summary
    print_section("DEPLOYMENT SUMMARY")

    print(f"\\n✅ Copied: {len(copied)} files")
    if skipped:
        print(f"⚠️  Skipped: {len(skipped)} files")
    if failed:
        print(f"❌ Failed: {len(failed)} files")

    if failed:
        print("\\nFailed files:")
        for f in failed:
            print(f"  - {f}")
        return False

    # Next steps
    print_section("NEXT STEPS")

    print("\\n1. Switch to Deployment:")
    print("   cd C:\\\\Deployment\\\\nex-automat")

    print("\\n2. Install/update dependencies:")
    print("   pip install -r scripts\\\\requirements.txt")
    print("   pip install -r apps\\\\supplier-invoice-loader\\\\requirements.txt")

    print("\\n3. Run preflight check:")
    print("   python scripts\\\\day5_preflight_check.py")

    print("\\n4. If service not running:")
    print("   python scripts\\\\manage_service.py start")

    print("\\n5. Verify all systems:")
    print("   python scripts\\\\day5_preflight_check.py")

    print("="*70)

    return True

if __name__ == "__main__":
    success = deploy()
    exit(0 if success else 1)
'''

    try:
        deploy_script.write_text(new_content, encoding='utf-8')
        print("=" * 70)
        print("  DEPLOY SCRIPT UPDATED")
        print("=" * 70)
        print(f"\\n✅ Updated: {deploy_script}")
        print(f"   Files to deploy: 14 scripts + 2 requirements.txt")
        print("\\nReady to deploy:")
        print("  python scripts\\\\deploy_to_deployment.py")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    update_deploy_script()