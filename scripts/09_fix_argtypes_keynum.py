#!/usr/bin/env python3
"""
Manually fix argtypes keyNum parameter
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def fix_argtypes():
    """Fix keyNum parameter in argtypes"""

    print("=" * 70)
    print("Fix Argtypes KeyNum Parameter")
    print("=" * 70)
    print()

    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return False

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find argtypes definition
    found = False
    for i, line in enumerate(lines):
        if 'self.btrcall.argtypes = [' in line:
            print(f"✓ Found argtypes at line {i + 1}")

            # Look for keyNum parameter (should be ~6 lines after)
            for j in range(i, min(i + 10, len(lines))):
                if 'c_int8' in lines[j] and ('keyNum' in lines[j] or '# keyNum' in lines[j]):
                    print(f"✓ Found c_int8 at line {j + 1}")
                    print(f"  Old: {lines[j]}")

                    # Replace c_int8 with c_uint8
                    lines[j] = lines[j].replace('c_int8', 'c_uint8')
                    print(f"  New: {lines[j]}")

                    found = True
                    break

            if found:
                break

    if not found:
        print("❌ Could not find c_int8 in argtypes")

        # Show argtypes section for debugging
        print()
        print("Current argtypes section:")
        in_argtypes = False
        for i, line in enumerate(lines):
            if 'self.btrcall.argtypes = [' in line:
                in_argtypes = True

            if in_argtypes:
                print(f"{i + 1:3d}: {line}")

                if ']' in line and in_argtypes:
                    break

        return False

    # Write back
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print()
    print(f"✅ Fixed: {TARGET_FILE}")
    print()
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = fix_argtypes()

    if success:
        print("✅ KeyNum parameter fixed!")
        print()
        print("Next: Test again")
        print("  python scripts/test_direct_open.py")
    else:
        print("❌ Fix failed - manual intervention needed")

    print("=" * 70)