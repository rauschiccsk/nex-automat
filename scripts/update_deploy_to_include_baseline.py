#!/usr/bin/env python3
"""
Update deploy_to_deployment.py to include create_baseline.py
"""

from pathlib import Path


def update_deploy_script():
    """Add create_baseline.py to deployment list"""

    script_path = Path("scripts/deploy_to_deployment.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the files list and add create_baseline.py
    # Look for the scripts list
    if '"scripts/manage_service.py"' in content and '"scripts/create_baseline.py"' not in content:
        # Add after manage_service.py
        old_line = '        "scripts/manage_service.py",'
        new_lines = '''        "scripts/manage_service.py",
        "scripts/create_baseline.py",'''

        content = content.replace(old_line, new_lines)
        print("✅ Added create_baseline.py to deployment list")
    else:
        print("⚠️  Pattern not found or already added")
        return False

    # Write back
    print(f"💾 Writing updated deploy script...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print()
    print("✅ Deploy script updated!")
    print()
    print("Now run:")
    print("  python scripts\\deploy_to_deployment.py")
    print("  cd C:\\Deployment\\nex-automat")
    print("  python scripts\\create_baseline.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  UPDATE DEPLOY SCRIPT")
    print("=" * 70)
    print()

    success = update_deploy_script()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")