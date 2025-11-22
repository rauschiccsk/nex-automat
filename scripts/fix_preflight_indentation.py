#!/usr/bin/env python3
"""
Fix indentation error in day5_preflight_check.py
"""

from pathlib import Path


def fix_indentation():
    """Fix the indentation issue in check_service_status"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    content = script_path.read_text(encoding='utf-8')

    # Find and fix the broken try block
    old_broken = '''        
        # Decode NSSM output (may be UTF-16LE with null bytes)
        try:
        stdout = result.stdout.decode('utf-16le').rstrip('\x00')
        except:
            try:
                stdout = result.stdout.decode('utf-8', errors='ignore')
            except:
                stdout = str(result.stdout).replace('\x00', '')'''

    new_fixed = '''        
        # Decode NSSM output (may be UTF-16LE with null bytes)
        try:
            stdout = result.stdout.decode('utf-16le').rstrip('\x00')
        except:
            try:
                stdout = result.stdout.decode('utf-8', errors='ignore')
            except:
                stdout = str(result.stdout).replace('\x00', '')'''

    if old_broken in content:
        content = content.replace(old_broken, new_fixed)
        print("✅ Fixed indentation in try block")
    else:
        # Try to find just the problem line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "stdout = result.stdout.decode('utf-16le')" in line and not line.strip().startswith('#'):
                # Check if this line is improperly indented (not inside try)
                if not lines[i].startswith('            '):  # Should have 12 spaces
                    print(f"Found problem at line {i + 1}: {line}")
                    # Fix this line and surrounding context
                    lines[i] = '            ' + line.lstrip()
                    print(f"Fixed to: {lines[i]}")

        content = '\n'.join(lines)
        print("✅ Fixed indentation")

    # Write fixed content
    print(f"💾 Writing fixed content...")
    script_path.write_text(content, encoding='utf-8')

    print()
    print("✅ Fix completed!")
    print()
    print("Deploy and test:")
    print("1. python scripts\\deploy_to_deployment.py")
    print("2. cd C:\\Deployment\\nex-automat")
    print("3. python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  FIX INDENTATION ERROR")
    print("=" * 70)
    print()

    success = fix_indentation()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")