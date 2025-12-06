#!/usr/bin/env python3
"""
Script 13: Analyze how MainWindow uses config
Find all references to self.config in MainWindow
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def find_config_usages(content: str) -> list:
    """Find all self.config usages"""
    # Find patterns like self.config.xxx
    pattern = r'self\.config\.[a-zA-Z_][a-zA-Z0-9_]*'
    matches = re.findall(pattern, content)
    return sorted(set(matches))


def main():
    """Analyze config usage in MainWindow"""
    print("=" * 60)
    print("Analyzing config usage in MainWindow")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    # Read content
    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Find config usages
    usages = find_config_usages(content)

    if not usages:
        print("\n⚠️  No self.config.xxx usages found")
        print("   Config might be stored but not used")
    else:
        print(f"\n📝 Found {len(usages)} config attribute usages:")
        for usage in usages:
            print(f"   - {usage}")

    # Check if config is stored
    if 'self.config = config' in content:
        print("\n✅ Config is stored: self.config = config")

    # Find __init__ method
    init_start = content.find('def __init__')
    if init_start != -1:
        init_end = content.find('\n    def ', init_start + 1)
        if init_end == -1:
            init_end = len(content)

        init_method = content[init_start:init_end]
        print("\n📋 __init__ method (first 30 lines):")
        lines = init_method.split('\n')[:30]
        for line in lines:
            print(f"   {line}")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)