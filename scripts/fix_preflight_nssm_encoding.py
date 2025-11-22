#!/usr/bin/env python3
"""
Fix UTF-16 encoding issue in day5_preflight_check.py
Same issue as manage_service.py - NSSM returns UTF-16LE
"""

from pathlib import Path


def fix_preflight_check():
    """Fix encoding issue in preflight check"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    content = script_path.read_text(encoding='utf-8')

    # Find the subprocess.run call in check_service_status
    old_code = '''        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Print raw output
        print(result.stdout)

        # Debug: show what we're checking
        stdout_lower = result.stdout.lower()
        has_running = "running" in stdout_lower
        has_service_running = "service_running" in stdout_lower

        # Check if service is running - check for both patterns
        if has_running or has_service_running or "SERVICE_RUNNING" in result.stdout:'''

    new_code = '''        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=False,  # Get bytes to handle UTF-16
            timeout=10
        )

        # Decode NSSM output (may be UTF-16LE with null bytes)
        try:
            stdout = result.stdout.decode('utf-16le').rstrip('\x00')
        except:
            try:
                stdout = result.stdout.decode('utf-8', errors='ignore')
            except:
                stdout = str(result.stdout).replace('\x00', '')

        # Print decoded output
        print(stdout)

        # Check if service is running
        stdout_lower = stdout.lower()
        has_running = "running" in stdout_lower
        has_service_running = "service_running" in stdout_lower

        # Check if service is running - check for both patterns
        if has_running or has_service_running or "SERVICE_RUNNING" in stdout:'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Fixed encoding in check_service_status()")
    else:
        print("⚠️  Exact pattern not found")

        # Try simpler replacement - just the subprocess.run part
        old_simple = '''        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )'''

        new_simple = '''        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=False,  # Get bytes to handle UTF-16
            timeout=10
        )

        # Decode output (handle UTF-16LE from NSSM)
        try:
            stdout_decoded = result.stdout.decode('utf-16le').rstrip('\x00')
        except:
            stdout_decoded = result.stdout.decode('utf-8', errors='ignore').replace('\x00', '')

        # Replace result.stdout with decoded version
        class DecodedResult:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        result = DecodedResult(result.returncode, stdout_decoded, result.stderr)'''

        if old_simple in content:
            content = content.replace(old_simple, new_simple)
            print("✅ Fixed subprocess.run encoding")
        else:
            print("❌ Could not find subprocess.run to fix")
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
    print("2. Run preflight check:")
    print("   cd C:\\Deployment\\nex-automat")
    print("   python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  FIX PREFLIGHT CHECK ENCODING")
    print("=" * 70)
    print()

    success = fix_preflight_check()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")