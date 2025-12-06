#!/usr/bin/env python3
"""
Script 24: Find all save_grid_settings() calls
Nájde kde sa volá save_grid_settings a s akými parametrami
"""

from pathlib import Path
import os


def find_calls():
    """Nájde všetky volania save_grid_settings()"""

    search_dir = Path("apps/supplier-invoice-editor")

    print("=" * 80)
    print("SEARCHING FOR save_grid_settings() CALLS")
    print("=" * 80)

    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines = content.split('\n')

                    for i, line in enumerate(lines, 1):
                        if 'save_grid_settings(' in line and 'def save_grid_settings' not in line:
                            print(f"\n📄 {file_path.relative_to(search_dir)}")
                            print(f"   Line {i}:")

                            # Zobraz okolie
                            for j in range(max(0, i - 5), min(len(lines), i + 5)):
                                marker = ">>>" if j == i - 1 else "   "
                                print(f"{marker} {j + 1:4d}: {lines[j]}")

                except:
                    pass


if __name__ == "__main__":
    find_calls()