#!/usr/bin/env python3
"""
Remove psutil from scripts/requirements.txt since we don't use it
"""

from pathlib import Path


def remove_psutil():
    """Remove psutil line from requirements.txt"""

    req_path = Path("scripts/requirements.txt")

    if not req_path.exists():
        print(f"✅ {req_path} doesn't exist - nothing to do")
        return True

    print(f"📖 Reading {req_path}...")
    content = req_path.read_text(encoding='utf-8')

    if 'psutil' not in content:
        print("✅ psutil not in requirements.txt - already clean")
        return True

    # Remove psutil line
    lines = content.split('\n')
    new_lines = [line for line in lines if 'psutil' not in line.lower()]

    new_content = '\n'.join(new_lines)

    print(f"💾 Writing cleaned requirements...")
    req_path.write_text(new_content, encoding='utf-8')

    print("✅ Removed psutil from scripts/requirements.txt")
    print()
    print("Reason: create_baseline.py uses only Python built-ins")
    print("        psutil cannot be installed on Windows 32-bit Python 3.13")
    print()
    print("Next: Deploy to sync")
    print("   python scripts\\deploy_to_deployment.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  REMOVE PSUTIL FROM REQUIREMENTS")
    print("=" * 70)
    print()

    success = remove_psutil()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")