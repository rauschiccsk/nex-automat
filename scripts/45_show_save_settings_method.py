#!/usr/bin/env python3
"""
Script 45: Show _save_settings implementation
Check how window dimensions are being saved
"""

from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BASE_WINDOW = PROJECT_ROOT / "packages" / "nex-shared" / "ui" / "base_window.py"


def main():
    """Show _save_settings implementation"""
    print("=" * 60)
    print("Showing BaseWindow _save_settings")
    print("=" * 60)

    if not BASE_WINDOW.exists():
        print(f"❌ File not found: {BASE_WINDOW}")
        return False

    content = BASE_WINDOW.read_text(encoding='utf-8')

    # Find _save_settings method
    pattern = r'def _save_settings\(self.*?\n(?=\n    def |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("\n📋 _save_settings implementation:\n")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines, 1):
            print(f"   {i:3d}: {line}")
    else:
        print("\n⚠️  _save_settings not found")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()