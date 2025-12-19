"""Fix new_chat.py to use sys.executable instead of 'python'."""
from pathlib import Path

FILE = Path(r"C:\Development\nex-automat\new_chat.py")

content = FILE.read_text(encoding="utf-8")

# Fix 1: Add sys import if missing
if "import sys" not in content:
    content = content.replace(
        "import subprocess",
        "import subprocess\nimport sys"
    )
    print("✅ Added: import sys")

# Fix 2: Replace "python" with sys.executable
if '["python",' in content:
    content = content.replace(
        '["python",',
        '[sys.executable,'
    )
    print("✅ Fixed: subprocess.run uses sys.executable")
else:
    print("ℹ️  Already using sys.executable or pattern not found")

FILE.write_text(content, encoding="utf-8")
print(f"\n✅ Updated: {FILE}")