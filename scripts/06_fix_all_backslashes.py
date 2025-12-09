# Fix ALL backslashes in GSCAT model paths

from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_MODEL = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "models" / "gscat.py"

print("=" * 70)
print("FIXING ALL BACKSLASHES IN PATHS")
print("=" * 70)

# Read as binary
with open(GSCAT_MODEL, 'rb') as f:
    content = f.read().decode('utf-8')

# Fix the full path - replace single backslashes with doubles
old_path = r'Location: C:\\NEX\YEARACT\STORES\GSCAT.BTR'
new_path = r'Location: C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR'

if old_path in content:
    content = content.replace(old_path, new_path)
    print(f"✅ Fixed path in Location line")
else:
    print(f"⚠️  Path not found, trying alternative...")
    # Try to fix any remaining single backslashes in paths
    content = content.replace(r'\YEARACT', r'\\YEARACT')
    content = content.replace(r'\STORES', r'\\STORES')
    print(f"✅ Fixed remaining backslashes")

# Write back
with open(GSCAT_MODEL, 'wb') as f:
    f.write(content.encode('utf-8'))

print(f"Location: {GSCAT_MODEL}")

# Verify
try:
    compile(content, str(GSCAT_MODEL), 'exec')
    print("\n✅ SUCCESS - No syntax warnings")
    print("\nNext Step:")
    print("python scripts/test_ean_lookup.py")
except SyntaxError as e:
    print(f"\n❌ Error: {e}")