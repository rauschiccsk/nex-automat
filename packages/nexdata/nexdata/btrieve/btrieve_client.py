# nex_shared/btrieve/btrieve_client.py
"""
Python wrapper pre Pervasive Btrieve API (32-bit)
FIXED: Correct BTRCALL signature based on Delphi btrapi32.pas
"""

import ctypes
import os
from pathlib import Path


class BtrieveClient:
    """
    Python wrapper pre Pervasive Btrieve API (32-bit)
    Používa w3btrv7.dll alebo wbtrv32.dll
    """

    # Btrieve operation codes
    B_OPEN = 0
    B_CLOSE = 1
    B_INSERT = 2
    B_UPDATE = 3
    B_DELETE = 4
    B_GET_EQUAL = 5
    B_GET_NEXT = 6
    B_GET_PREVIOUS = 7
    B_GET_GREATER = 8
    B_GET_GREATER_OR_EQUAL = 9
    B_GET_LESS = 10
    B_GET_LESS_OR_EQUAL = 11
    B_GET_FIRST = 12
    B_GET_LAST = 13
    B_STEP_NEXT = 24
    B_STEP_PREVIOUS = 35

    # Btrieve status codes
    STATUS_SUCCESS = 0
    STATUS_INVALID_OPERATION = 1
    STATUS_IO_ERROR = 2
    STATUS_FILE_NOT_OPEN = 3
    STATUS_KEY_NOT_FOUND = 4
    STATUS_DUPLICATE_KEY = 5
    STATUS_INVALID_KEY_NUMBER = 6
    STATUS_DIFFERENT_KEY_NUMBER = 7
    STATUS_INVALID_POSITIONING = 8

    def __init__(self, config_or_path=None):
        """
        Inicializácia Btrieve klienta

        Args:
            config_or_path: Dict s config dátami ALEBO string s cestou ku config súboru (YAML)
        """
        self.dll = None
        self.btrcall = None
        self.database_path = None
        self.config = None

        # Load config
        if config_or_path is not None:
            if isinstance(config_or_path, dict):
                # Config už je dict (z FastAPI dependencies)
                self.config = config_or_path
            elif isinstance(config_or_path, str):
                # Config je cesta k súboru
                from pathlib import Path

                import yaml

                config_path = Path(config_or_path)
                with open(config_path, encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
            else:
                raise TypeError("config_or_path must be dict or str")
        else:
            # Load default config
            from pathlib import Path

            import yaml

            config_path = Path("config/database.yaml")
            with open(config_path, encoding="utf-8") as f:
                self.config = yaml.safe_load(f)

        # Initialize DLL
        self._load_dll()

    def _resolve_table_path(self, table_name_or_path: str) -> str:
        """
        Resolve table name to filesystem path using config

        Args:
            table_name_or_path: Either table name (e.g. 'gscat', 'tsh-001') or direct path

        Returns:
            Filesystem path to .BTR file
        """
        # Check if config has table mapping
        if self.config and "nex_genesis" in self.config:
            tables = self.config.get("nex_genesis", {}).get("tables", {})

            # First try direct lookup
            if table_name_or_path in tables:
                return tables[table_name_or_path]

            # Try dynamic table lookup (e.g., 'tsh-001' -> 'tsh')
            if "-" in table_name_or_path:
                parts = table_name_or_path.split("-")
                if len(parts) == 2:
                    base_name = parts[0]  # 'tsh' from 'tsh-001'
                    book_id = parts[1]  # '001' from 'tsh-001'

                    if base_name in tables:
                        path_template = tables[base_name]
                        # Replace {book_id} placeholder
                        return path_template.replace("{book_id}", book_id)

        # Fallback: if we have database_path, construct path
        if self.config and "database_path" in self.config:
            db_path = self.config["database_path"]
            # table_name to uppercase + .BTR extension
            table_file = f"{table_name_or_path.upper()}.BTR"
            return os.path.join(db_path, table_file)

        # It's already a path, or no config - use as-is
        return table_name_or_path

    def _load_dll(self) -> None:
        """Načítaj Btrieve DLL a nastav BTRCALL funkciu - NO EMOJIS"""

        # DLL priority list
        dll_names = [
            "w3btrv7.dll",  # Primary - Windows Btrieve API
            "wbtrv32.dll",  # Fallback - 32-bit Btrieve API
        ]

        # FIRST: Try loading from PATH (no absolute path)
        # This allows DLL to be found when C:\PVSW\bin is in PATH
        print("[DEBUG] Attempting to load Btrieve DLL from PATH...")
        for dll_name in dll_names:
            try:
                print(f"[DEBUG] Trying {dll_name} from PATH...")
                # Load DLL from PATH
                self.dll = ctypes.WinDLL(dll_name)
                print(f"[DEBUG] DLL loaded: {dll_name}")

                # Get BTRCALL function
                try:
                    self.btrcall = self.dll.BTRCALL
                    print("[DEBUG] BTRCALL function found (uppercase)")
                except AttributeError:
                    # Try lowercase
                    try:
                        self.btrcall = self.dll.btrcall
                        print("[DEBUG] btrcall function found (lowercase)")
                    except AttributeError:
                        print(f"[DEBUG] No BTRCALL/btrcall function in {dll_name}")
                        continue

                # Configure BTRCALL signature
                self.btrcall.argtypes = [
                    ctypes.c_uint16,  # operation (WORD)
                    ctypes.POINTER(ctypes.c_char),  # posBlock (VAR)
                    ctypes.POINTER(ctypes.c_char),  # dataBuffer (VAR)
                    ctypes.POINTER(ctypes.c_uint32),  # dataLen (longInt = 4 bytes!)
                    ctypes.POINTER(ctypes.c_char),  # keyBuffer (VAR)
                    ctypes.c_uint8,  # keyLen (BYTE)
                    ctypes.c_uint8,  # keyNum (BYTE, unsigned!)
                ]
                self.btrcall.restype = ctypes.c_int16  # Status code (SMALLINT)

                print(f"[SUCCESS] Loaded Btrieve DLL from PATH: {dll_name}")
                return

            except Exception as e:
                print(f"[DEBUG] Failed to load {dll_name} from PATH: {e}")
                continue

        # FALLBACK: Try absolute paths
        print("[DEBUG] PATH loading failed, trying absolute paths...")

        search_paths = [
            # 1. Pervasive PSQL installation (v11.30)
            Path(r"C:\Program Files (x86)\Pervasive Software\PSQL\bin"),
            # 2. Old Pervasive installation
            Path(r"C:\PVSW\bin"),
            # 3. Local external-dlls directory
            Path(__file__).parent.parent.parent / "external-dlls",
            # 4. System directory (Windows\SysWOW64)
            Path(r"C:\Windows\SysWOW64"),
        ]

        # Try each path and DLL combination
        for search_path in search_paths:
            if not search_path.exists():
                print(f"[DEBUG] Skipping (not exists): {search_path}")
                continue

            print(f"[DEBUG] Checking: {search_path}")

            for dll_name in dll_names:
                dll_path = search_path / dll_name

                if not dll_path.exists():
                    continue

                try:
                    print(f"[DEBUG] Trying {dll_name}...")
                    # Load DLL
                    self.dll = ctypes.WinDLL(str(dll_path))
                    print(f"[DEBUG] DLL loaded: {dll_path}")

                    # Get BTRCALL function
                    try:
                        self.btrcall = self.dll.BTRCALL
                    except AttributeError:
                        # Try lowercase
                        try:
                            self.btrcall = self.dll.btrcall
                        except AttributeError:
                            print("[DEBUG] No BTRCALL function")
                            continue

                    # Configure BTRCALL signature
                    self.btrcall.argtypes = [
                        ctypes.c_uint16,  # operation (WORD)
                        ctypes.POINTER(ctypes.c_char),  # posBlock (VAR)
                        ctypes.POINTER(ctypes.c_char),  # dataBuffer (VAR)
                        ctypes.POINTER(ctypes.c_uint32),  # dataLen (longInt = 4 bytes!)
                        ctypes.POINTER(ctypes.c_char),  # keyBuffer (VAR)
                        ctypes.c_uint8,  # keyLen (BYTE)
                        ctypes.c_uint8,  # keyNum (BYTE, unsigned!)
                    ]
                    self.btrcall.restype = ctypes.c_int16  # Status code (SMALLINT)

                    print(
                        f"[SUCCESS] Loaded Btrieve DLL: {dll_name} from {search_path}"
                    )
                    return

                except Exception as e:
                    print(f"[DEBUG] Failed: {e}")
                    continue

        raise RuntimeError(
            "[ERROR] Could not load any Btrieve DLL from any location.\n"
            "Searched paths:\n"
            + "\n".join(f"  - {p}" for p in search_paths if p.exists())
        )

    def open_file(
        self, filename: str, owner_name: str = "", mode: int = -2
    ) -> tuple[int, bytes]:
        """
        Otvor Btrieve súbor - FIXED with owner name support

        CRITICAL: Owner name must be in data_buffer for files with owner security!

        Args:
            filename: Cesta k .dat/.BTR súboru
            owner_name: Owner name (required for secured files!)
            mode: Open mode
                  0 = Normal
                 -1 = Accelerated
                 -2 = Read-only (DEFAULT - safest)
                 -3 = Exclusive

        Returns:
            Tuple[status_code, position_block]
        """
        # Position block (128 bytes)
        pos_block = ctypes.create_string_buffer(128)

        # Data buffer with OWNER NAME (if provided)
        if owner_name:
            # Owner name goes into data_buffer (null-terminated, max 8 chars)
            owner_bytes = owner_name.encode("ascii")[:8].ljust(8, b"\x00")
            data_buffer = ctypes.create_string_buffer(owner_bytes, 256)
            data_len = ctypes.c_uint32(len(owner_bytes))
        else:
            # No owner name - empty data buffer
            data_buffer = ctypes.create_string_buffer(256)
            data_len = ctypes.c_uint32(0)

        # FILENAME goes into KEY_BUFFER!
        # Resolve table name to filepath using config
        filepath = self._resolve_table_path(filename)

        filename_bytes = filepath.encode("ascii") + b"\x00"
        key_buffer = ctypes.create_string_buffer(filename_bytes)

        # keyLen = 255 (max key length)
        key_len = 255

        # Call BTRCALL
        status = self.btrcall(
            self.B_OPEN,
            pos_block,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            key_len,
            mode & 0xFF,
        )

        return status, pos_block.raw

    def close_file(self, pos_block: bytes) -> int:
        """
        Zavri Btrieve súbor

        Args:
            pos_block: Position block z open_file()

        Returns:
            status_code
        """
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(1)
        data_len = ctypes.c_uint32(0)  # longInt (4 bytes)
        key_buffer = ctypes.create_string_buffer(1)

        status = self.btrcall(
            self.B_CLOSE,
            pos_block_buf,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            0,  # keyLen
            0,  # keyNum
        )

        return status

    def get_first(self, pos_block: bytes, key_num: int = 0) -> tuple[int, bytes]:
        """
        Načítaj prvý záznam

        Args:
            pos_block: Position block
            key_num: Index number (default: 0)

        Returns:
            Tuple[status_code, data]
        """
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(4096)  # Max record size
        data_len = ctypes.c_uint32(4096)  # longInt (4 bytes)
        key_buffer = ctypes.create_string_buffer(255)

        status = self.btrcall(
            self.B_GET_FIRST,
            pos_block_buf,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            255,  # keyLen
            key_num & 0xFF,
        )

        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[: data_len.value]
        else:
            return status, b""

    def get_next(self, pos_block: bytes) -> tuple[int, bytes]:
        """
        Načítaj ďalší záznam

        Args:
            pos_block: Position block

        Returns:
            Tuple[status_code, data]
        """
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(4096)
        data_len = ctypes.c_uint32(4096)  # longInt (4 bytes)
        key_buffer = ctypes.create_string_buffer(255)

        status = self.btrcall(
            self.B_GET_NEXT,
            pos_block_buf,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            255,  # keyLen
            0,
        )

        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[: data_len.value]
        else:
            return status, b""

    def get_status_message(self, status_code: int) -> str:
        """
        Konvertuj status code na human-readable správu

        Args:
            status_code: Btrieve status code

        Returns:
            Status message
        """
        messages = {
            0: "SUCCESS",
            1: "INVALID_OPERATION",
            2: "IO_ERROR",
            3: "FILE_NOT_OPEN",
            4: "KEY_NOT_FOUND",
            5: "DUPLICATE_KEY",
            6: "INVALID_KEY_NUMBER",
            7: "DIFFERENT_KEY_NUMBER",
            8: "INVALID_POSITIONING",
            11: "INVALID_FILENAME",
            12: "FILE_NOT_OPEN",
        }
        return messages.get(status_code, f"UNKNOWN_ERROR_{status_code}")


# Convenience functions
def open_btrieve_file(
    filename: str, config_path: str | None = None
) -> tuple[BtrieveClient, bytes]:
    """
    Helper funkcia na otvorenie Btrieve súboru

    Args:
        filename: Cesta k .BTR súboru
        config_path: Cesta ku config súboru

    Returns:
        Tuple[client, position_block]
    """
    client = BtrieveClient(config_path)
    status, pos_block = client.open_file(filename)

    if status != BtrieveClient.STATUS_SUCCESS:
        raise RuntimeError(
            f"Failed to open {filename}: {client.get_status_message(status)}"
        )

    return client, pos_block
