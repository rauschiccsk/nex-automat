#!/usr/bin/env python3
"""
Fix service status check in day5_preflight_check.py with debug output
"""

from pathlib import Path


def fix_service_check():
    """Fix the service status check with proper debugging"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    content = script_path.read_text(encoding='utf-8')

    # Find the problematic section
    old_code = '''        print(result.stdout)

        # Check if service is running
        if "running" in result.stdout.lower():
            print("✅ Service is RUNNING")
            return True
        else:
            print("❌ Service is NOT running")
            print("   Run: python scripts/manage_service.py start")
            return False'''

    # New code with proper checks and debug
    new_code = '''        # Print raw output
        print(result.stdout)

        # Debug: show what we're checking
        stdout_lower = result.stdout.lower()
        has_running = "running" in stdout_lower
        has_service_running = "service_running" in stdout_lower

        # Check if service is running - check for both patterns
        if has_running or has_service_running or "SERVICE_RUNNING" in result.stdout:
            print("✅ Service is RUNNING")
            return True
        else:
            print("❌ Service is NOT running")
            print("   Run: python scripts/manage_service.py start")
            return False'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Found and replaced service check code")
    else:
        print("⚠️  Exact pattern not found, trying alternative fix...")

        # Alternative: just replace the if statement
        old_if = '''        if "running" in result.stdout.lower():'''
        new_if = '''        if "running" in result.stdout.lower() or "SERVICE_RUNNING" in result.stdout:'''

        if old_if in content:
            content = content.replace(old_if, new_if)
            print("✅ Fixed service check condition")
        else:
            print("❌ Could not find service check to fix!")
            return False

    # Write fixed content
    print(f"💾 Writing fixed content...")
    script_path.write_text(content, encoding='utf-8')

    print()
    print("✅ Fix completed!")
    print()
    print("Next steps:")
    print("1. Deploy to Deployment:")
    print("   python scripts\\deploy_to_deployment.py")
    print("2. Test in Deployment:")
    print("   cd C:\\Deployment\\nex-automat")
    print("   python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  FIX SERVICE STATUS CHECK")
    print("=" * 70)
    print()

    success = fix_service_check()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")