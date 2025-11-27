"""
Fix GSCAT repository path
"""

from pathlib import Path

GSCAT_REPO = Path("packages/nexdata/nexdata/repositories/gscat_repository.py")


def fix_path():
    print("=" * 60)
    print("FIX: GSCAT Repository path")
    print("=" * 60)

    if not GSCAT_REPO.exists():
        print(f"❌ File not found: {GSCAT_REPO}")
        return False

    print(f"\n📄 Reading: {GSCAT_REPO}")

    # Read file
    with open(GSCAT_REPO, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace path
    old_path = 'return "C:/NEX/GSCAT.BTR"'
    new_path = 'return "C:/NEX/YEARACT/STORES/GSCAT.BTR"'

    if old_path not in content:
        print("⚠️  Old path not found - already fixed?")
        return False

    content = content.replace(old_path, new_path)

    # Write back
    with open(GSCAT_REPO, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Path fixed")
    print(f"\n   ❌ Old: C:/NEX/GSCAT.BTR")
    print(f"   ✅ New: C:/NEX/YEARACT/STORES/GSCAT.BTR")

    print("\n📝 Next step:")
    print("   python scripts/test_gscat_read.py")

    return True


if __name__ == "__main__":
    success = fix_path()
    exit(0 if success else 1)