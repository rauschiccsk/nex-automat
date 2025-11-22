#!/usr/bin/env python3
"""
Add DEBUG output to preflight check to see what's happening with decoding
"""

from pathlib import Path


def add_debug():
    """Add debug output to check_service_status"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the print(stdout) line and add debug output after it
    old_code = '''        # Print decoded output
        print(stdout)

        # Check if service is running'''

    new_code = '''        # Print decoded output
        print(stdout)

        # DEBUG: Show what we're working with
        print(f"DEBUG: stdout type = {type(stdout)}")
        print(f"DEBUG: stdout length = {len(stdout)}")
        print(f"DEBUG: stdout repr = {stdout!r}")
        print(f"DEBUG: 'running' in stdout.lower() = {'running' in stdout.lower()}")
        print(f"DEBUG: 'SERVICE_RUNNING' in stdout = {'SERVICE_RUNNING' in stdout}")

        # Check if service is running'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Added debug output")
    else:
        print("⚠️  Could not find exact pattern to replace")
        print("Looking for alternative...")

        # Try to add after print(stdout)
        if 'print(stdout)' in content:
            lines = content.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                if 'print(stdout)' in line and i < len(lines) - 1:
                    # Add debug lines after this
                    indent = ' ' * 8  # Assume 8 spaces indent
                    new_lines.append('')
                    new_lines.append(indent + '# DEBUG: Show what we\'re working with')
                    new_lines.append(indent + 'print(f"DEBUG: stdout type = {type(stdout)}")')
                    new_lines.append(indent + 'print(f"DEBUG: stdout length = {len(stdout)}")')
                    new_lines.append(indent + 'print(f"DEBUG: stdout repr = {stdout!r}")')
                    new_lines.append(
                        indent + 'print(f"DEBUG: \'running\' in stdout.lower() = {\'running\' in stdout.lower()}")')
                    new_lines.append(
                        indent + 'print(f"DEBUG: \'SERVICE_RUNNING\' in stdout = {\'SERVICE_RUNNING\' in stdout}")')
            content = '\n'.join(new_lines)
            print("✅ Added debug output (alternative method)")
        else:
            print("❌ Could not find place to add debug")
            return False

    # Write back
    print(f"💾 Writing with debug output...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print()
    print("✅ Debug output added!")
    print()
    print("Deploy and test:")
    print("  python scripts\\deploy_to_deployment.py")
    print("  cd C:\\Deployment\\nex-automat")
    print("  python scripts\\day5_preflight_check.py")
    print()
    print("This will show EXACTLY what stdout contains after decoding")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  ADD DEBUG OUTPUT")
    print("=" * 70)
    print()

    success = add_debug()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")