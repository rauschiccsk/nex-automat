"""
Script 05: Fix BtrieveClient._load_dll() Method
================================================

Purpose: Fix DLL loading to use PATH environment variable first

Changes:
1. Try loading from PATH first (no absolute path)
2. Then try absolute paths as fallback
3. This allows DLL to be found when C:\PVSW\bin is in PATH

Usage:
    python scripts/05_fix_btrieve_load_dll.py
"""

from pathlib import Path


def create_fixed_load_dll():
    """Generate fixed _load_dll() method"""
    return '''    def _load_dll(self) -> None:
        """Načítaj Btrieve DLL a nastav BTRCALL funkciu - FIXED WITH PATH SUPPORT"""

        # DLL priority list
        dll_names = [
            'w3btrv7.dll',  # Primary - Windows Btrieve API
            'wbtrv32.dll',  # Fallback - 32-bit Btrieve API
        ]

        # FIRST: Try loading from PATH (no absolute path)
        # This allows DLL to be found when C:\\PVSW\\bin is in PATH
        for dll_name in dll_names:
            try:
                # Load DLL from PATH
                self.dll = ctypes.WinDLL(dll_name)

                # Get BTRCALL function
                try:
                    self.btrcall = self.dll.BTRCALL
                except AttributeError:
                    # Try lowercase
                    try:
                        self.btrcall = self.dll.btrcall
                    except AttributeError:
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

            except Exception:
                # Silent fail, try next DLL
                continue

        # FALLBACK: Try absolute paths
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
                continue

            for dll_name in dll_names:
                dll_path = search_path / dll_name

                if not dll_path.exists():
                    continue

                try:
                    # Load DLL
                    self.dll = ctypes.WinDLL(str(dll_path))

                    # Get BTRCALL function
                    try:
                        self.btrcall = self.dll.BTRCALL
                    except AttributeError:
                        # Try lowercase
                        try:
                            self.btrcall = self.dll.btrcall
                        except AttributeError:
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
                    # Silent fail, try next DLL
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
    print("FIXING BTRIEVE CLIENT - _load_dll() METHOD")
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
    print(f"   Lines to replace: {end_idx - start_idx}")

    # Replace method
    new_lines = (
            lines[:start_idx] +
            create_fixed_load_dll().split('\n') +
            lines[end_idx:]
    )

    # Write back
    new_content = '\n'.join(new_lines)

    with open(btrieve_client_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)

    print(f"✅ File updated: {btrieve_client_path}")

    print("\n" + "=" * 70)
    print("CHANGES MADE")
    print("=" * 70)
    print("""
✅ Added PATH-based DLL loading as FIRST priority
✅ Absolute paths moved to FALLBACK
✅ When C:\\PVSW\\bin is in PATH, DLL loads immediately

This fixes the issue where:
- Console app works (PATH is set)
- Service fails (PATH not visible to Python at import time)
    """)

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Test in Development:
   python scripts/01_test_console_app.py

2. If works, commit and push:
   git add packages/nexdata/nexdata/btrieve/btrieve_client.py
   git commit -m "Fix BtrieveClient to use PATH for DLL loading"
   git push

3. Deploy to Production:
   cd C:\\Deployment\\nex-automat
   git pull

4. Test service startup
    """)


if __name__ == "__main__":
    main()