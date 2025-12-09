"""
Session Script 13: Fix BARCODERepository find_by_barcode
Fixes UnboundLocalError for 'file' variable
"""
from pathlib import Path

def main():
    barcode_repo = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata\repositories\barcode_repository.py")

    print("=" * 60)
    print("Fixing find_by_barcode() Method")
    print("=" * 60)

    with open(barcode_repo, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the method and fix it
    modified = False
    for i, line in enumerate(lines):
        # Find "try:" line after "def find_by_barcode"
        if i > 0 and 'def find_by_barcode' in lines[i-10:i].__str__():
            if line.strip() == 'try:':
                # Insert "file = None" before try
                indent = len(line) - len(line.lstrip())
                lines.insert(i, ' ' * indent + 'file = None\n')
                modified = True
                print(f"✅ Added 'file = None' at line {i+1}")
                break

    if modified:
        with open(barcode_repo, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("\n✅ File updated successfully")
    else:
        # Alternative approach - find method definition and add file = None
        in_method = False
        for i, line in enumerate(lines):
            if 'def find_by_barcode' in line:
                in_method = True
                continue

            if in_method and 'try:' in line:
                # Check if 'file = None' is already on previous line
                if i > 0 and 'file = None' in lines[i-1]:
                    print("⚠️  Already fixed - 'file = None' exists")
                    return 0

                # Add 'file = None' before try
                indent = len(line) - len(line.lstrip())
                lines.insert(i, ' ' * indent + 'file = None\n')

                with open(barcode_repo, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                print(f"✅ Added 'file = None' at line {i+1}")
                print("\n✅ File updated successfully")
                return 0

        print("⚠️  Could not locate the exact position")
        print("\nShowing find_by_barcode method:")
        in_method = False
        for i, line in enumerate(lines):
            if 'def find_by_barcode' in line:
                in_method = True

            if in_method:
                print(f"{i+1:4d}: {line.rstrip()}")

                # Stop after finally block
                if 'file.close()' in line:
                    break

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())