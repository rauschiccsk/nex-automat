"""
Session Script 14: Fix GSCATRepository search_by_name Signature
Adds limit parameter to existing method
"""
from pathlib import Path

def main():
    gscat_repo = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata\repositories\gscat_repository.py")

    print("=" * 60)
    print("Fixing search_by_name() Signature")
    print("=" * 60)

    with open(gscat_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace signature
    old_sig = 'def search_by_name(self, search_term: str) -> List[GSCATRecord]:'
    new_sig = 'def search_by_name(self, search_term: str, limit: int = 20) -> List[GSCATRecord]:'

    if old_sig in content:
        content = content.replace(old_sig, new_sig)

        with open(gscat_repo, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Updated signature")
        print(f"\n  FROM: {old_sig}")
        print(f"  TO:   {new_sig}")
    else:
        print("⚠️  Signature already updated or not found")

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())