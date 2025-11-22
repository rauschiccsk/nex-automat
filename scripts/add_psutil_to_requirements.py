#!/usr/bin/env python3
"""
Add psutil to scripts/requirements.txt
"""

from pathlib import Path


def add_psutil():
    """Add psutil to requirements if not present"""

    req_path = Path("scripts/requirements.txt")

    if not req_path.exists():
        print(f"Creating {req_path}...")
        req_path.write_text("psutil\n", encoding='utf-8')
        print("✅ Created scripts/requirements.txt with psutil")
        return True

    print(f"📖 Reading {req_path}...")
    content = req_path.read_text(encoding='utf-8')

    if 'psutil' in content:
        print("✅ psutil already in requirements.txt")
        return True

    # Add psutil
    content = content.rstrip() + '\npsutil\n'

    print(f"💾 Writing updated requirements...")
    req_path.write_text(content, encoding='utf-8')

    print("✅ Added psutil to scripts/requirements.txt")
    print()
    print("Next steps:")
    print("1. Deploy:")
    print("   python scripts\\deploy_to_deployment.py")
    print("2. Install in Deployment:")
    print("   cd C:\\Deployment\\nex-automat")
    print("   pip install -r scripts\\requirements.txt")
    print("3. Create baseline:")
    print("   python scripts\\create_baseline.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  ADD PSUTIL TO REQUIREMENTS")
    print("=" * 70)
    print()

    success = add_psutil()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")