"""
Diagnose Btrieve path and open issues
Try different path formats and open modes
"""

from nexdata import BtrieveClient
from pathlib import Path


def test_path_format(client: BtrieveClient, path: str, description: str):
    """Test opening file with specific path format"""
    print(f"\n📝 Testing: {description}")
    print(f"   Path: {path}")

    # Try different open modes
    modes = [
        (-2, "Read-only (default)"),
        (0, "Normal"),
        (-1, "Accelerated"),
    ]

    for mode, mode_desc in modes:
        print(f"   Mode {mode:2d} ({mode_desc}): ", end="")
        status, pos_block = client.open_file(path, mode=mode)

        if status == 0:
            print("✅ SUCCESS!")
            client.close_file(pos_block)
            return True
        else:
            msg = client.get_status_message(status)
            print(f"❌ {status} ({msg})")

    return False


def diagnose():
    print("=" * 60)
    print("BTRIEVE PATH DIAGNOSIS")
    print("=" * 60)

    # Check if file exists
    gscat_path = Path(r"C:\NEX\GSCAT.BTR")
    print(f"\n📁 Checking file existence:")
    print(f"   Path: {gscat_path}")
    print(f"   Exists: {gscat_path.exists()}")
    if gscat_path.exists():
        print(f"   Size: {gscat_path.stat().st_size:,} bytes")

    # Initialize client
    print(f"\n📡 Initializing Btrieve client...")
    try:
        client = BtrieveClient(config_or_path={})
        print("✅ Client initialized")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

    # Test different path formats
    test_paths = [
        (r"C:\NEX\GSCAT.BTR", "Backslash (raw string)"),
        ("C:\\NEX\\GSCAT.BTR", "Backslash (escaped)"),
        ("C:/NEX/GSCAT.BTR", "Forward slash"),
        ("C:\\NEX\\GSCAT.BTR\x00", "Backslash + null terminator"),
    ]

    print("\n" + "=" * 60)
    print("TESTING PATH FORMATS")
    print("=" * 60)

    success = False
    for path, desc in test_paths:
        if test_path_format(client, path, desc):
            success = True
            print(f"\n🎉 WORKING PATH FORMAT FOUND!")
            print(f"   Use: {repr(path)}")
            break

    if not success:
        print("\n" + "=" * 60)
        print("❌ NO WORKING PATH FORMAT FOUND")
        print("=" * 60)
        print("\n🔍 Possible issues:")
        print("   1. Pervasive PSQL service not running")
        print("      Check: sc query psql")
        print("   2. File locked by another process")
        print("   3. Insufficient permissions")
        print("   4. Pervasive configuration issue")

    return success


if __name__ == "__main__":
    diagnose()