"""Python wrapper pre Pervasive Btrieve API (32-bit)"""

import ctypes
from pathlib import Path
from typing import Tuple


class BtrieveClient:
    """Python wrapper pre Pervasive Btrieve API (32-bit)"""
    
    # Operation codes
    B_OPEN = 0
    B_CLOSE = 1
    B_INSERT = 2
    B_UPDATE = 3
    B_DELETE = 4
    B_GET_EQUAL = 5
    B_GET_NEXT = 6
    B_GET_PREVIOUS = 7
    B_GET_FIRST = 12
    B_GET_LAST = 13
    
    # Status codes
    STATUS_SUCCESS = 0
    STATUS_INVALID_OPERATION = 1
    STATUS_IO_ERROR = 2
    STATUS_FILE_NOT_OPEN = 3
    STATUS_KEY_NOT_FOUND = 4
    STATUS_DUPLICATE_KEY = 5
    
    def __init__(self, config_or_path=None):
        """Inicializácia Btrieve klienta"""
        self.dll = None
        self.btrcall = None
        self._load_dll()
    
    def _load_dll(self) -> None:
        """Načítaj Btrieve DLL"""
        dll_names = ['w3btrv7.dll', 'wbtrv32.dll']
        search_paths = [
            Path(r"C:\Program Files (x86)\Pervasive Software\PSQL\bin"),
            Path(r"C:\PVSW\bin"),
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
                        ctypes.c_uint8
                    ]
                    self.btrcall.restype = ctypes.c_int16
                    print(f"✅ Loaded Btrieve DLL: {dll_name}")
                    return
                except Exception:
                    continue
        
        raise RuntimeError("Could not load Btrieve DLL")
    
    def open_file(self, filename: str, owner_name: str = "", mode: int = -2) -> Tuple[int, bytes]:
        """Otvor Btrieve súbor"""
        pos_block = ctypes.create_string_buffer(128)
        data_buffer = ctypes.create_string_buffer(256)
        data_len = ctypes.c_uint32(0)
        filename_bytes = filename.encode('ascii') + b'\x00'
        key_buffer = ctypes.create_string_buffer(filename_bytes)
        key_len = 255
        
        status = self.btrcall(
            self.B_OPEN,
            pos_block,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            key_len,
            mode & 0xFF
        )
        return status, pos_block.raw
    
    def close_file(self, pos_block: bytes) -> int:
        """Zavri Btrieve súbor"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(1)
        data_len = ctypes.c_uint32(0)
        key_buffer = ctypes.create_string_buffer(1)
        
        status = self.btrcall(
            self.B_CLOSE,
            pos_block_buf,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            0,
            0
        )
        return status
    
    def get_first(self, pos_block: bytes, key_num: int = 0) -> Tuple[int, bytes]:
        """Načítaj prvý záznam"""
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
            key_num & 0xFF
        )
        
        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[:data_len.value]
        else:
            return status, b''
    
    def get_next(self, pos_block: bytes) -> Tuple[int, bytes]:
        """Načítaj ďalší záznam"""
        pos_block_buf = ctypes.create_string_buffer(pos_block)
        data_buffer = ctypes.create_string_buffer(4096)
        data_len = ctypes.c_uint32(4096)
        key_buffer = ctypes.create_string_buffer(255)
        
        status = self.btrcall(
            self.B_GET_NEXT,
            pos_block_buf,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            255,
            0
        )
        
        if status == self.STATUS_SUCCESS:
            return status, data_buffer.raw[:data_len.value]
        else:
            return status, b''
    
    def get_status_message(self, status_code: int) -> str:
        """Konvertuj status code na správu"""
        messages = {
            0: "SUCCESS",
            1: "INVALID_OPERATION",
            2: "IO_ERROR",
            3: "FILE_NOT_OPEN",
            4: "KEY_NOT_FOUND",
            5: "DUPLICATE_KEY",
        }
        return messages.get(status_code, f"UNKNOWN_ERROR_{status_code}")
