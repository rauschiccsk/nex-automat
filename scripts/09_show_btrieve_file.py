# Show BtrieveClient file content

from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
BTRIEVE_CLIENT = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "btrieve" / "btrieve_client.py"

print("=" * 70)
print("BTRIEVE CLIENT - FIRST 100 LINES")
print("=" * 70)

content = BTRIEVE_CLIENT.read_text(encoding='utf-8')
lines = content.split('\n')

for i, line in enumerate(lines[:100], 1):
    print(f"{i:3d}: {line}")

print(f"\n... (showing first 100 of {len(lines)} total lines)")