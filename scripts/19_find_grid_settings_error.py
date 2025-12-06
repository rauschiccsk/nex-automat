#!/usr/bin/env python3
"""
Script 19: Find grid settings error source
Nájde kde sa vypisuje chyba "Chyba pri ukladaní grid settings"
"""

from pathlib import Path
import os


def find_error_message():
    """Nájde súbor kde sa vypisuje chyba grid settings"""

    search_dirs = [
        Path("apps/supplier-invoice-editor"),
        Path("packages/nex-shared")
    ]

    search_text = "Chyba pri ukladaní grid settings"

    print("=" * 80)
    print(f"SEARCHING FOR: '{search_text}'")
    print("=" * 80)

    found_files = []

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if search_text in content:
                            found_files.append(file_path)

                            # Zobraz okolie chybovej správy
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if search_text in line:
                                    print(f"\n📄 {file_path}")
                                    print(f"   Line {i}:")
                                    # Zobraz ±5 riadkov okolo
                                    for j in range(max(0, i - 6), min(len(lines), i + 5)):
                                        marker = ">>>" if j == i - 1 else "   "
                                        print(f"{marker} {j + 1:4d}: {lines[j]}")
                    except:
                        pass

    if not found_files:
        print("❌ Error message not found in source files")
        print("\nSearching for 'grid settings' more broadly...")

        # Širšie hľadanie
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = Path(root) / file
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            if 'grid settings' in content.lower():
                                print(f"  Found in: {file_path}")
                        except:
                            pass

    return found_files


if __name__ == "__main__":
    files = find_error_message()

    if files:
        print("\n" + "=" * 80)
        print("FOUND IN FILES:")
        print("=" * 80)
        for f in files:
            print(f"  {f}")