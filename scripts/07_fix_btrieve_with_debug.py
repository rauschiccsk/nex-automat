"""
Script 07: Fix BtrieveClient with Debug Output
===============================================

Purpose: Add debug output to see why PATH loading fails

Usage:
    python scripts/07_fix_btrieve_with_debug.py
"""

from pathlib import Path


def create_fixed_load_dll_with_debug():
    """Generate fixed _load_dll() method with debug output"""
    return '''    def _load_dll(self) -> None:
        """Načítaj Btrieve DLL a nastav BTRCALL funkciu - WITH DEBUG"""

        # DLL priority list
        dll_names = [
            'w3btrv7.dll',  # Primary - Windows Btrieve API
            'wbtrv32.dll',  # Fallback - 32-bit Btrieve API
        ]

        # FIRST: Try loading from PATH (no absolute path)
        # This allows DLL to be found when C:\\PVSW\\bin is in PATH
        print("🔍 Attempting to load Btrieve DLL from PATH...")
        for dll_name in dll_names:
            try:
                print(f"   Trying {dll_name} from PATH...")
                # Load DLL from PATH
                self.dll = ctypes.WinDLL(dll_name)
                print(f"   ✅ DLL loaded: {dll_name}")

                # Get BTRCALL function
                try:
                    self.btrcall = self.dll.BTRCALL
                    print(f"   ✅ BTRCALL function found (uppercase)")
                except AttributeError:
                    # Try lowercase
                    try:
                        self.btrcall = self.dll.btrcall
                        print(f"   ✅ btrcall function found (lowercase)")
                    except AttributeError:
                        print(f"   ❌ No BTRCALL/btrcall function in {dll_name}")
                        continue

                # Configure BTRCALL signature
                self.btrcall.argtypes = [
                    ctypes.c_uint16,  # operation (WORD)
                    ctypes.POINTER(ctypes.c_char),  # posBlock (VAR)
                    ctypes.POINTER(ctypes.c_char),  # dataBuffer (VAR)
                    ctypes.POINTER(ctypes.c_uint32),  # dataLen (longInt = 4 bytes!)
                    ctypes.POINTER(ctypes.c_char),  # keyBuffer (VAR)
                    ctypes.c_uint8,  # keyLen (BYTE)
                    ctypes.c_uint8  # keyNum (BYTE, unsigned!)
                ]
                self.btrcall.restype = ctypes.c_int16  # Status code (SMALLINT)

                print(f"✅ Loaded Btrieve DLL from PATH: {dll_name}")
                return

            except Exception as e:
                print(f"   ❌ Failed to load {dll_name} from PATH: {e}")
                continue

        # FALLBACK: Try absolute paths
        print("⚠️  PATH loading failed, trying absolute paths...")

        search_paths = [
            # 1. Pervasive PSQL installation (v11.30)
            Path(r"C:\\Program Files (x86)\\Pervasive Software\\PSQL\\bin"),

            # 2. Old Pervasive installation
            Path(r"C:\\PVSW\\bin"),

            # 3. Local external-dlls directory
            Path(__file__).parent.parent.parent / 'external-dlls',

            # 4. System directory (Windows\\SysWOW64)
            Path(r"C:\\Windows\\SysWOW64"),
        ]

        # Try each path and DLL combination
        for search_path in search_paths:
            if not search_path.exists():
                print(f"   ⏭️  Skipping (not exists): {search_path}")
                continue

            print(f"   Checking: {search_path}")

            for dll_name in dll_names:
                dll_path = search_path / dll_name

                if not dll_path.exists():
                    continue

                try:
                    print(f"      Trying {dll_name}...")
                    # Load DLL
                    self.dll = ctypes.WinDLL(str(dll_path))
                    print(f"      ✅ DLL loaded: {dll_path}")

                    # Get BTRCALL function
                    try:
                        self.btrcall = self.dll.BTRCALL
                    except AttributeError:
                        # Try lowercase
                        try:
                            self.btrcall = self.dll.btrcall
                        except AttributeError:
                            print(f"      ❌ No BTRCALL function")
                            continue

                    # Configure BTRCALL signature
                    self.btrcall.argtypes = [
                        ctypes.c_uint16,  # operation (WORD)
                        ctypes.POINTER(ctypes.c_char),  # posBlock (VAR)
                        ctypes.POINTER(ctypes.c_char),  # dataBuffer (VAR)
                        ctypes.POINTER(ctypes.c_uint32),  # dataLen (longInt = 4 bytes!)
                        ctypes.POINTER(ctypes.c_char),  # keyBuffer (VAR)
                        ctypes.c_uint8,  # keyLen (BYTE)
                        ctypes.c_uint8  # keyNum (BYTE, unsigned!)
                    ]
                    self.btrcall.restype = ctypes.c_int16  # Status code (SMALLINT)

                    print(f"✅ Loaded Btrieve DLL: {dll_name} from {search_path}")
                    return

                except Exception as e:
                    print(f"      ❌ Failed: {e}")
                    continue

        raise RuntimeError(
            "❌ Could not load any Btrieve DLL from any location.\\n"
            "Searched paths:\\n" +
            "\\n".join(f"  - {p}" for p in search_paths if p.exists())
        )
'''


def main():
    btrieve_client_path = Path("C:/Development/nex-automat/packages/nexdata/nexdata/btrieve/btrieve_client.py")

    if not btrieve_client_path.exists():
        print(f"❌ File not found: {btrieve_client_path}")
        return

    print("=" * 70)
    print("FIXING BTRIEVE CLIENT - ADD DEBUG OUTPUT")
    print("=" * 70)

    # Read current file
    with open(btrieve_client_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find _load_dll method
    lines = content.split('\n')

    # Find start and end of method
    start_idx = None
    end_idx = None
    indent_level = None

    for i, line in enumerate(lines):
        if 'def _load_dll(' in line:
            start_idx = i
            indent_level = len(line) - len(line.lstrip())
            continue

        if start_idx is not None and end_idx is None:
            current_indent = len(line) - len(line.lstrip())

            # Check if we're still in the method
            if line.strip() and current_indent <= indent_level and not line.strip().startswith('#'):
                end_idx = i
                break

    if start_idx is None:
        print("❌ _load_dll() method not found")
        return

    # If no end found, go to end of file
    if end_idx is None:
        end_idx = len(lines)

    print(f"\n✅ Found _load_dll() method at lines {start_idx + 1}-{end_idx + 1}")

    # Replace method
    new_lines = (
            lines[:start_idx] +
            create_fixed_load_dll_with_debug().split('\n') +
            lines[end_idx:]
    )

    # Write back
    new_content = '\n'.join(new_lines)

    with open(btrieve_client_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)

    print(f"✅ File updated: {btrieve_client_path}")
    print("\n✅ Added detailed debug output to see why PATH loading fails")
    print("\n📋 Next: Run test again to see debug output")


if __name__ == "__main__":
    main()