# Check BtrieveClient __init__ signature

from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
BTRIEVE_CLIENT = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "btrieve" / "btrieve_client.py"

print("=" * 70)
print("BTRIEVE CLIENT __INIT__ SIGNATURE")
print("=" * 70)

content = BTRIEVE_CLIENT.read_text(encoding='utf-8')
lines = content.split('\n')

# Find __init__ method
in_init = False
indent_level = 0

for i, line in enumerate(lines):
    if 'def __init__' in line and 'BtrieveClient' in content[:content.index(line)].split('\n')[-20:]:
        in_init = True
        indent_level = len(line) - len(line.lstrip())
        print(f"Line {i+1}: {line}")
    elif in_init:
        current_indent = len(line) - len(line.lstrip())
        # End when we hit another method at same level
        if line.strip().startswith('def ') and current_indent <= indent_level:
            break
        print(f"Line {i+1}: {line}")
        # Stop after first 20 lines of method
        if i > (lines.index(next(l for l in lines if 'def __init__' in l)) + 20):
            break

print("\n" + "=" * 70)