"""
Script 04: Show BtrieveClient._load_dll() method
=================================================

Purpose: Display the current _load_dll() implementation

Usage:
    python scripts/04_show_btrieve_load_dll.py
"""

from pathlib import Path


def main():
    btrieve_client_path = Path("C:/Development/nex-automat/packages/nexdata/nexdata/btrieve/btrieve_client.py")

    if not btrieve_client_path.exists():
        print(f"❌ File not found: {btrieve_client_path}")
        return

    print("=" * 70)
    print("BTRIEVE CLIENT - _load_dll() METHOD")
    print("=" * 70)

    with open(btrieve_client_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find _load_dll method
    lines = content.split('\n')
    in_method = False
    indent_level = None
    method_lines = []

    for i, line in enumerate(lines, 1):
        if 'def _load_dll(' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            method_lines.append(f"{i:4d}: {line}")
            continue

        if in_method:
            current_indent = len(line) - len(line.lstrip())

            # Check if we're still in the method
            if line.strip() and current_indent <= indent_level:
                break

            method_lines.append(f"{i:4d}: {line}")

    if method_lines:
        print("\n".join(method_lines))
    else:
        print("❌ _load_dll() method not found")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()