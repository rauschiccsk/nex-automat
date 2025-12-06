#!/usr/bin/env python3
"""
Script 44: Show BaseWindow closeEvent implementation
Check how window state is being saved
"""

from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BASE_WINDOW = PROJECT_ROOT / "packages" / "nex-shared" / "ui" / "base_window.py"


def main():
    """Show closeEvent implementation"""
    print("=" * 60)
    print("Showing BaseWindow closeEvent")
    print("=" * 60)

    if not BASE_WINDOW.exists():
        print(f"❌ File not found: {BASE_WINDOW}")
        return False

    content = BASE_WINDOW.read_text(encoding='utf-8')

    # Find closeEvent method
    pattern = r'def closeEvent\(self.*?\n(?=\n    def |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("\n📋 closeEvent implementation:\n")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines, 1):
            print(f"   {i:3d}: {line}")
    else:
        print("\n⚠️  closeEvent not found")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()