# nex_shared/btrieve/btrieve_client.py
"""
Python wrapper pre Pervasive Btrieve API (32-bit)
FIXED: Correct BTRCALL signature based on Delphi btrapi32.pas
"""
import ctypes
import os
import struct
from pathlib import Path
from typing import Optional, Tuple


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
                import yaml
                from pathlib import Path
                config_path = Path(config_or_path)
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
            else:
                raise TypeError("config_or_path must be dict or str")
        else:
            # Load default config
            import yaml
            from pathlib import Path
            config_path = Path("config/database.yaml")
            with open(config_path, 'r', encoding='utf-8') as f:
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
        if self.config and 'nex_genesis' in self.config:
            tables = self.config.get('nex_genesis', {}).get('tables', {})

            # First try direct lookup
            if table_name_or_path in tables:
                return tables[table_name_or_path]

            # Try dynamic table lookup (e.g., 'tsh-001' -> 'tsh')
            if '-' in table_name_or_path:
                parts = table_name_or_path.split('-')
                if len(parts) == 2:
                    base_name = parts[0]  # 'tsh' from 'tsh-001'
                    book_id = parts[1]     # '001' from 'tsh-001'

                    if base_name in tables:
                        path_template = tables[base_name]
                        # Replace {book_id} placeholder
                        return path_template.replace('{book_id}', book_id)

        # It's already a path, or no config - use as-is
        return table_name_or_path

    def _load_dll(self) -> None:
        """Načítaj Btrieve DLL a nastav BTRCALL funkciu - FIXED SIGNATURE"""

        # DLL priority list
        dll_names = [
            'w3btrv7.dll',  # Primary - Windows Btrieve API
            'wbtrv32.dll',  # Fallback - 32-bit Btrieve API
        ]

        # Search paths (in priority order)
        search_paths = [
            # 1. Pervasive PSQL installation (v11.30)
            Path(r"C:\Program Files (x86)\Pervasive Software\PSQL\bin"),

            # 2. Old Pervasive installation
            Path(r"C:\PVSW\bin"),

            # 3. Local external-dlls directory
            Path(__file__).parent.parent.parent / 'external-dlls',

            # 4. System directory (Windows\SysWOW64)
            Path(r"C:\Windows\SysWOW64"),
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

                    # Configure BTRCALL signature - FIXED according to btrapi32.pas!
                    self.btrcall.argtypes = [
                        ctypes.c_uint16,  # operation (WORD)
                        ctypes.POINTER(ctypes.c_char),  # posBlock (VAR)
                        ctypes.POINTER(ctypes.c_char),  # dataBuffer (VAR)
                        ctypes.POINTER(ctypes.c_uint32),  # dataLen (longInt = 4 bytes!) ← FIXED!
                        ctypes.POINTER(ctypes.c_char),  # keyBuffer (VAR)
                        ctypes.c_uint8,  # keyLen (BYTE)
                        ctypes.c_uint8  # keyNum (BYTE, unsigned!) ← FIXED!
                    ]
                    self.btrcall.restype = ctypes.c_int16  # Status code (SMALLINT)

                    print(f"✅ Loaded Btrieve DLL: {dll_name} from {search_path}")
                    return

                except Exception as e:
                    # Silent fail, try next DLL
                    continue

        raise RuntimeError(
            "❌ Could not load any Btrieve DLL from any location.\n"
            "Searched paths:\n" +
            "\n".join(f"  - {p}" for p in search_paths if p.exists())
        )

    def open_file(self, filename: str, owner_name: str = "", mode: int = -2) -> Tuple[int, bytes]:
        """
        Otvor Btrieve súbor - FIXED syntax podľa Delphi BtrOpen

        IMPORTANT: Based on Delphi BtrOpen (BtrHand.pas):
        - Filename goes in KEY_BUFFER (not data_buffer!)
        - Data_buffer is EMPTY (dataLen = 0!)
        - keyLen = 255 (max key length)

        Args:
            filename: Cesta k .dat/.BTR súboru
            owner_name: Owner name (optional, not used)
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

        # Data buffer is EMPTY for OPEN! (according to Delphi BtrOpen)
        data_buffer = ctypes.create_string_buffer(256)
        data_len = ctypes.c_uint32(0)  # ZERO! (and longInt = 4 bytes)

        # FILENAME goes into KEY_BUFFER! (not data_buffer!)
        # Resolve table name to filepath using config
        filepath = self._resolve_table_path(filename)

        filename_bytes = filepath.encode('ascii') + b'\x00'
        key_buffer = ctypes.create_string_buffer(filename_bytes)

        # keyLen = 255 (max key length, as in BTRV wrapper)
        key_len = 255

        # Call BTRCALL with CORRECT parameters
        status = self.btrcall(
            self.B_OPEN,
            pos_block,
            data_buffer,  # EMPTY!
            ctypes.byref(data_len),  # 0!
            key_buffer,  # FILENAME!
            key_len,  # 255!
            mode & 0xFF  # mode as unsigned BYTE
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
            0  # keyNum
        )

        return status

    def get_first(self, pos_block: bytes, key_num: int = 0) -> Tuple[int, bytes]:
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
            key_num & 0xFF
        )

        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[:data_len.value]
        else:
            return status, b''

    def get_next(self, pos_block: bytes) -> Tuple[int, bytes]:
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
            0
        )

        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[:data_len.value]
        else:
            return status, b''

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
def open_btrieve_file(filename: str, config_path: Optional[str] = None) -> Tuple[BtrieveClient, bytes]:
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
