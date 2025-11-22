#!/usr/bin/env python3
"""
Simple fix: Just strip ALL null bytes from NSSM output
NSSM returns mixed encoding - some lines ASCII, some UTF-16LE
"""

from pathlib import Path


def fix_null_bytes():
    """Fix by simply stripping all null bytes"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the decoding section and replace with simple null byte stripping
    old_code = '''        # Decode NSSM output (may be UTF-16LE with null bytes)
        try:
            # Try UTF-16LE decoding first
            stdout = result.stdout.decode("utf-16le").rstrip("\\x00")
        except:
            try:
                # Fallback to UTF-8
                stdout = result.stdout.decode("utf-8", errors="ignore")
            except:
                # Last resort - convert to string and strip nulls
                stdout = str(result.stdout).replace("\\x00", "")'''

    new_code = '''        # NSSM returns mixed encoding - just decode as UTF-8 and strip null bytes
        try:
            stdout = result.stdout.decode("utf-8", errors="ignore")
        except:
            stdout = str(result.stdout)

        # Strip all null bytes (NSSM returns UTF-16LE fragments with \\x00)
        stdout = stdout.replace("\\x00", "")'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Replaced decoding logic with simple null byte stripping")
    else:
        print("⚠️  Pattern not found, trying alternative...")

        # Alternative - just add .replace after any decode
        if 'stdout = result.stdout.decode' in content:
            lines = content.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                # If this is a decode line, add replace right after
                if 'stdout = result.stdout.decode' in line and 'replace' not in line:
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + 'stdout = stdout.replace("\\x00", "")  # Strip UTF-16 null bytes')
            content = '\n'.join(new_lines)
            print("✅ Added null byte stripping after decode")
        else:
            print("❌ Could not find decode to fix")
            return False

    # Write back
    print(f"💾 Writing fixed content...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print()
    print("✅ Fix completed!")
    print()
    print("This simple approach just strips ALL \\x00 bytes")
    print("which is exactly what we need for NSSM mixed output")
    print()
    print("Deploy and test:")
    print("  python scripts\\deploy_to_deployment.py")
    print("  cd C:\\Deployment\\nex-automat")
    print("  python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  FIX NULL BYTE STRIPPING")
    print("=" * 70)
    print()

    success = fix_null_bytes()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")