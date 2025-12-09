# Fix GSCAT Model Unicode Error - Safe Version
# Reads as binary to avoid unicode issues

from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_MODEL = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "models" / "gscat.py"

print("=" * 70)
print("FIXING GSCAT MODEL UNICODE ERROR")
print("=" * 70)

# Read as binary
with open(GSCAT_MODEL, 'rb') as f:
    content_bytes = f.read()

# Decode to string
content = content_bytes.decode('utf-8')

# Count problematic backslashes
count_before = content.count(r'C:\NEX')

# Fix: Escape all backslashes in NEX paths
content_fixed = content.replace(r'C:\NEX', r'C:\\NEX')

# Count after fix
count_after = content_fixed.count(r'C:\\NEX')

# Write back
with open(GSCAT_MODEL, 'wb') as f:
    f.write(content_fixed.encode('utf-8'))

print(f"Fixed {count_before} occurrence(s)")
print(f"Changed: C:\\NEX → C:\\\\NEX")
print(f"Location: {GSCAT_MODEL}")

# Verify by trying to compile
try:
    compile(content_fixed, str(GSCAT_MODEL), 'exec')
    print("\n✅ FIX SUCCESSFUL - File compiles")
    print("\nNext Step:")
    print("python scripts/test_ean_lookup.py")
except SyntaxError as e:
    print(f"\n❌ FAILED - Syntax error: {e}")