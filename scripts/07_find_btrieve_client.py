# Find BtrieveClient location in nexdata package

from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
NEXDATA = DEV_ROOT / "packages" / "nexdata" / "nexdata"

print("=" * 70)
print("SEARCHING FOR BTRIEVE CLIENT")
print("=" * 70)

# Search for files containing "BtrieveClient"
for py_file in NEXDATA.rglob("*.py"):
    try:
        content = py_file.read_text(encoding='utf-8')
        if 'class BtrieveClient' in content:
            print(f"\n✅ FOUND: {py_file.relative_to(DEV_ROOT)}")

            # Show class definition
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'class BtrieveClient' in line:
                    print(f"\nLine {i + 1}: {line}")
                    # Show next 5 lines
                    for j in range(1, 6):
                        if i + j < len(lines):
                            print(f"Line {i + j + 1}: {lines[i + j]}")
                    break
    except:
        pass

# List all Python files in nexdata
print("\n" + "=" * 70)
print("ALL PYTHON FILES IN NEXDATA:")
print("=" * 70)

py_files = sorted(NEXDATA.rglob("*.py"))
for f in py_files:
    rel_path = f.relative_to(NEXDATA)
    print(f"  {rel_path}")

print(f"\nTotal: {len(py_files)} files")