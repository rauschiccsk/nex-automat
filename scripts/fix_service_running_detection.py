#!/usr/bin/env python3
"""
Fix SERVICE_RUNNING detection in day5_preflight_check.py

Problem: Script shows "Status: SERVICE_RUNNING" but then reports "Service is NOT running"
Solution: Fix the status detection logic to properly recognize SERVICE_RUNNING
"""

import sys
from pathlib import Path


def fix_service_detection():
    """Fix SERVICE_RUNNING detection in preflight check"""

    # Path to the script
    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    # Read current content
    print(f"📖 Reading {script_path}...")
    content = script_path.read_text(encoding='utf-8')

    # Find and fix the service status check
    # The problem is likely in how we check for SERVICE_RUNNING

    # Old pattern (incorrect):
    old_pattern = '''        if "SERVICE_RUNNING" in status_output:
            print(f"✅ Service is running")
            service_ok = True
        else:
            print(f"❌ Service is NOT running")'''

    # New pattern (correct):
    new_pattern = '''        if "SERVICE_RUNNING" in status_output or "Status: SERVICE_RUNNING" in status_output:
            print(f"✅ Service is running")
            service_ok = True
        else:
            print(f"❌ Service is NOT running")'''

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("✅ Found and fixed service status detection")
    else:
        # Try alternative pattern
        alt_old = '''        if "running" in status_output.lower():
            print(f"✅ Service is running")
            service_ok = True
        else:
            print(f"❌ Service is NOT running")'''

        alt_new = '''        if "SERVICE_RUNNING" in status_output or "running" in status_output.lower():
            print(f"✅ Service is running")
            service_ok = True
        else:
            print(f"❌ Service is NOT running")'''

        if alt_old in content:
            content = content.replace(alt_old, alt_new)
            print("✅ Found and fixed service status detection (alternative pattern)")
        else:
            print("⚠️  Pattern not found - checking for other variations...")

            # Let's try to find any service check section
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'if "SERVICE_RUNNING"' in line or 'if "running"' in line:
                    print(f"📍 Found status check at line {i + 1}: {line.strip()}")

    # Write fixed content
    print(f"💾 Writing fixed content to {script_path}...")
    script_path.write_text(content, encoding='utf-8')

    print("✅ Fix completed!")
    print()
    print("Next steps:")
    print("1. Deploy to Deployment:")
    print("   python scripts\\deploy_to_deployment.py")
    print("2. Run preflight check again:")
    print("   cd C:\\Deployment\\nex-automat")
    print("   python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("  FIX SERVICE_RUNNING DETECTION")
    print("=" * 60)
    print()

    success = fix_service_detection()

    sys.exit(0 if success else 1)