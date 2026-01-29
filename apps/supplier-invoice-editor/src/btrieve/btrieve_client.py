# src/btrieve/btrieve_client.py
"""
Python wrapper pre Pervasive Btrieve API (32-bit)
Adapted for supplier-invoice-editor Qt5 application
"""

import ctypes
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class BtrieveClient:
    """Python wrapper pre Pervasive Btrieve API (32-bit)"""

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

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Btrieve client"""
        self.dll = None
        self.btrcall = None
        self.config = config or {}
        self._load_dll()

    def _load_dll(self) -> None:
        """Load Btrieve DLL"""
        dll_names = ["w3btrv7.dll", "wbtrv32.dll"]
        search_paths = [
            Path(r"C:\Program Files (x86)\Pervasive Software\PSQL\bin"),
            Path(r"C:\PVSW\bin"),
            Path(__file__).parent.parent.parent / "external-dlls",
            Path(r"C:\Windows\SysWOW64"),
        ]

        for search_path in search_paths:
            if not search_path.exists():
                continue
            for dll_name in dll_names:
                dll_path = search_path / dll_name
                if not dll_path.exists():
                    continue
                try:
                    self.dll = ctypes.WinDLL(str(dll_path))
                    try:
                        self.btrcall = self.dll.BTRCALL
                    except AttributeError:
                        try:
                            self.btrcall = self.dll.btrcall
                        except AttributeError:
                            continue

                    self.btrcall.argtypes = [
                        ctypes.c_uint16,
                        ctypes.POINTER(ctypes.c_char),
                        ctypes.POINTER(ctypes.c_char),
                        ctypes.POINTER(ctypes.c_uint32),
                        ctypes.POINTER(ctypes.c_char),
                        ctypes.c_uint8,
                        ctypes.c_uint8,
                    ]
                    self.btrcall.restype = ctypes.c_int16
                    print(f"✅ Loaded Btrieve DLL: {dll_name} from {search_path}")
                    return
                except Exception:
                    continue

        raise RuntimeError("❌ Could not load any Btrieve DLL")

    def open_file(self, filename: str, owner_name: str = "", mode: int = -2) -> tuple[int, bytes]:
        """Open Btrieve file"""
        pos_block = ctypes.create_string_buffer(128)
        data_buffer = ctypes.create_string_buffer(256)
        data_len = ctypes.c_uint32(0)
        filename_bytes = filename.encode("ascii") + b"\x00"
        key_buffer = ctypes.create_string_buffer(filename_bytes)
        key_len = 255

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
        """Close Btrieve file"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(1)
        data_len = ctypes.c_uint32(0)
        key_buffer = ctypes.create_string_buffer(1)

        status = self.btrcall(self.B_CLOSE, pos_block_buf, data_buffer, ctypes.byref(data_len), key_buffer, 0, 0)
        return status

    def get_first(self, pos_block: bytes, key_num: int = 0) -> tuple[int, bytes]:
        """Get first record"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(4096)
        data_len = ctypes.c_uint32(4096)
        key_buffer = ctypes.create_string_buffer(255)

        status = self.btrcall(
            self.B_GET_FIRST,
            pos_block_buf,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            255,
            key_num & 0xFF,
        )

        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[: data_len.value]
        return status, b""

    def get_next(self, pos_block: bytes) -> tuple[int, bytes]:
        """Get next record"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(4096)
        data_len = ctypes.c_uint32(4096)
        key_buffer = ctypes.create_string_buffer(255)

        status = self.btrcall(self.B_GET_NEXT, pos_block_buf, data_buffer, ctypes.byref(data_len), key_buffer, 255, 0)

        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[: data_len.value]
        return status, b""

    def insert(self, pos_block: bytes, data: bytes) -> int:
        """Insert new record"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(data)
        data_len = ctypes.c_uint32(len(data))
        key_buffer = ctypes.create_string_buffer(255)

        status = self.btrcall(self.B_INSERT, pos_block_buf, data_buffer, ctypes.byref(data_len), key_buffer, 255, 0)
        return status

    def update(self, pos_block: bytes, data: bytes) -> int:
        """Update current record"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(data)
        data_len = ctypes.c_uint32(len(data))
        key_buffer = ctypes.create_string_buffer(255)

        status = self.btrcall(self.B_UPDATE, pos_block_buf, data_buffer, ctypes.byref(data_len), key_buffer, 255, 0)
        return status

    def get_status_message(self, status_code: int) -> str:
        """Convert status code to message"""
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


def open_btrieve_file(filename: str, config: dict[str, Any] | None = None) -> tuple[BtrieveClient, bytes]:
    """Helper function to open Btrieve file"""
    client = BtrieveClient(config)
    status, pos_block = client.open_file(filename)

    if status != BtrieveClient.STATUS_SUCCESS:
        raise RuntimeError(f"Failed to open {filename}: {client.get_status_message(status)}")

    return client, pos_block
