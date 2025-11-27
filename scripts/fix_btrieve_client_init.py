"""
Fix BtrieveClient __init__ - handle empty dict correctly
Simple line-by-line replacement
"""

from pathlib import Path

BTRIEVE_CLIENT = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def fix_init():
    print("=" * 60)
    print("FIX: BtrieveClient __init__ method")
    print("=" * 60)

    if not BTRIEVE_CLIENT.exists():
        print(f"❌ File not found: {BTRIEVE_CLIENT}")
        return False

    print(f"\n📄 Reading: {BTRIEVE_CLIENT}")

    # Read file
    with open(BTRIEVE_CLIENT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find and replace
    modified = False
    for i, line in enumerate(lines):
        # Find the problematic line
        if "if config_or_path:" in line and "# Load config" in lines[i - 1] if i > 0 else False:
            old_line = line
            # Replace with correct check
            lines[i] = line.replace("if config_or_path:", "if config_or_path is not None:")
            print(f"\n✅ Line {i + 1} fixed:")
            print(f"   ❌ {old_line.strip()}")
            print(f"   ✅ {lines[i].strip()}")
            modified = True
            break

    if not modified:
        # Try simpler search
        for i, line in enumerate(lines):
            if "if config_or_path:" in line:
                old_line = line
                lines[i] = line.replace("if config_or_path:", "if config_or_path is not None:")
                print(f"\n✅ Line {i + 1} fixed:")
                print(f"   ❌ {old_line.strip()}")
                print(f"   ✅ {lines[i].strip()}")
                modified = True
                break

    if not modified:
        print("\n❌ Could not find line to replace")
        print("Looking for: 'if config_or_path:'")
        return False

    # Write back
    with open(BTRIEVE_CLIENT, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("\n📋 Changes:")
    print("   Now {} (empty dict) works correctly!")

    print("\n📝 Next step:")
    print("   pip install -e packages/nexdata")
    print("   python scripts/test_tsh_tsi_read.py")

    return True


if __name__ == "__main__":
    success = fix_init()
    exit(0 if success else 1)