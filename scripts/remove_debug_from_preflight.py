#!/usr/bin/env python3
"""
Remove DEBUG output from day5_preflight_check.py now that issue is fixed
"""

from pathlib import Path


def remove_debug():
    """Remove debug print statements"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the debug section
    old_debug = '''        
        # DEBUG: Show what we're working with
        print(f"DEBUG: stdout type = {type(stdout)}")
        print(f"DEBUG: stdout length = {len(stdout)}")
        print(f"DEBUG: stdout repr = {stdout!r}")
        print(f"DEBUG: 'running' in stdout.lower() = {'running' in stdout.lower()}")
        print(f"DEBUG: 'SERVICE_RUNNING' in stdout = {'SERVICE_RUNNING' in stdout}")
'''

    if old_debug in content:
        content = content.replace(old_debug, '\n')
        print("✅ Removed debug section")
    else:
        # Try line by line removal
        lines = content.split('\n')
        new_lines = []
        skip_next = False

        for line in lines:
            if 'DEBUG:' in line:
                continue  # Skip this line
            new_lines.append(line)

        content = '\n'.join(new_lines)
        print("✅ Removed debug lines")

    # Write back
    print(f"💾 Writing clean version...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print()
    print("✅ Debug output removed!")
    print()
    print("Deploy and verify:")
    print("  python scripts\\deploy_to_deployment.py")
    print("  cd C:\\Deployment\\nex-automat")
    print("  python scripts\\day5_preflight_check.py")
    print()
    print("Should see clean output: 5/6 checks passed ✅")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  REMOVE DEBUG OUTPUT")
    print("=" * 70)
    print()

    success = remove_debug()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")