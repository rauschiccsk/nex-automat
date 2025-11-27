"""
Create NEX Shared Package Files
Vytvorí všetky chýbajúce súbory v packages/nex-shared
"""

from pathlib import Path


def create_file(path: Path, content: str):
    """Vytvor súbor s obsahom"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    size = len(content.encode('utf-8'))
    rel_path = str(path.relative_to(Path('C:/Development/nex-automat')))
    print(f"✅ {rel_path:<60} ({size:>6} bytes)")


def main():
    """Main execution"""

    print("=" * 80)
    print("CREATING NEX-SHARED PACKAGE FILES")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat/packages/nex-shared")

    # 1. Main __init__.py
    create_file(base / "nex_shared/__init__.py", '''"""
NEX Shared Package
Btrieve models, client and repositories for NEX Genesis ERP
"""

from nex_shared.btrieve.btrieve_client import BtrieveClient
from nex_shared.models.tsh import TSHRecord
from nex_shared.models.tsi import TSIRecord

__all__ = [
    'BtrieveClient',
    'TSHRecord',
    'TSIRecord',
]
''')

    # 2. Models __init__.py
    create_file(base / "nex_shared/models/__init__.py", '"""Models package"""\n')

    # 3. Btrieve __init__.py
    create_file(base / "nex_shared/btrieve/__init__.py", '"""Btrieve package"""\n')

    # 4. Repositories __init__.py
    create_file(base / "nex_shared/repositories/__init__.py", '"""Repositories package"""\n')

    # 5. Utils __init__.py
    create_file(base / "nex_shared/utils/__init__.py", '"""Utils package"""\n')

    # 6. TSH Model
    create_file(base / "nex_shared/models/tsh.py", '''"""TSH Table Model - Dodacie listy Header"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
import struct


@dataclass
class TSHRecord:
    """TSH record structure - Dodacie listy Header"""
    
    # Primary key
    doc_number: str
    
    # Document info
    doc_type: int = 1
    doc_date: Optional[date] = None
    delivery_date: Optional[date] = None
    due_date: Optional[date] = None
    
    # Partner
    pab_code: int = 0
    pab_name: str = ""
    pab_address: str = ""
    pab_ico: str = ""
    pab_dic: str = ""
    pab_ic_dph: str = ""
    
    # Financial
    currency: str = "EUR"
    exchange_rate: Decimal = Decimal("1.0")
    amount_base: Decimal = Decimal("0.00")
    amount_vat: Decimal = Decimal("0.00")
    amount_total: Decimal = Decimal("0.00")
    
    # VAT breakdown
    vat_20_base: Decimal = Decimal("0.00")
    vat_20_amount: Decimal = Decimal("0.00")
    vat_10_base: Decimal = Decimal("0.00")
    vat_10_amount: Decimal = Decimal("0.00")
    vat_0_base: Decimal = Decimal("0.00")
    
    # Payment
    payment_method: int = 1
    payment_terms: int = 14
    paid: bool = False
    paid_date: Optional[date] = None
    paid_amount: Decimal = Decimal("0.00")
    
    # References
    invoice_number: str = ""
    order_number: str = ""
    internal_note: str = ""
    public_note: str = ""
    
    # Status
    status: int = 1
    locked: bool = False
    posted: bool = False
    warehouse_code: int = 1
    
    # Audit
    mod_user: str = ""
    mod_date: Optional[datetime] = None
    mod_time: Optional[datetime] = None
    created_date: Optional[datetime] = None
    created_user: str = ""
    
    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'TSHRecord':
        """Deserialize TSH record from bytes"""
        if len(data) < 500:
            raise ValueError(f"Invalid record size: {len(data)} bytes")
        
        # Primary key
        doc_number = data[0:20].decode(encoding, errors='ignore').rstrip('\\x00 ')
        
        # Document info
        doc_type = struct.unpack('<i', data[20:24])[0]
        doc_date_int = struct.unpack('<i', data[24:28])[0]
        doc_date = cls._decode_delphi_date(doc_date_int) if doc_date_int > 0 else None
        delivery_date_int = struct.unpack('<i', data[28:32])[0]
        delivery_date = cls._decode_delphi_date(delivery_date_int) if delivery_date_int > 0 else None
        due_date_int = struct.unpack('<i', data[32:36])[0]
        due_date = cls._decode_delphi_date(due_date_int) if due_date_int > 0 else None
        
        # Partner
        pab_code = struct.unpack('<i', data[36:40])[0]
        pab_name = data[40:140].decode(encoding, errors='ignore').rstrip('\\x00 ')
        pab_address = data[140:290].decode(encoding, errors='ignore').rstrip('\\x00 ')
        pab_ico = data[290:310].decode(encoding, errors='ignore').rstrip('\\x00 ')
        pab_dic = data[310:330].decode(encoding, errors='ignore').rstrip('\\x00 ')
        pab_ic_dph = data[330:360].decode(encoding, errors='ignore').rstrip('\\x00 ')
        
        # Financial
        currency = data[360:364].decode(encoding, errors='ignore').rstrip('\\x00 ')
        exchange_rate = Decimal(str(struct.unpack('<d', data[364:372])[0]))
        amount_base = Decimal(str(round(struct.unpack('<d', data[372:380])[0], 2)))
        amount_vat = Decimal(str(round(struct.unpack('<d', data[380:388])[0], 2)))
        amount_total = Decimal(str(round(struct.unpack('<d', data[388:396])[0], 2)))
        
        # VAT breakdown
        vat_20_base = Decimal(str(round(struct.unpack('<d', data[396:404])[0], 2)))
        vat_20_amount = Decimal(str(round(struct.unpack('<d', data[404:412])[0], 2)))
        vat_10_base = Decimal(str(round(struct.unpack('<d', data[412:420])[0], 2)))
        vat_10_amount = Decimal(str(round(struct.unpack('<d', data[420:428])[0], 2)))
        vat_0_base = Decimal(str(round(struct.unpack('<d', data[428:436])[0], 2)))
        
        # Payment
        payment_method = struct.unpack('<i', data[436:440])[0]
        payment_terms = struct.unpack('<i', data[440:444])[0]
        paid = bool(data[444])
        paid_date_int = struct.unpack('<i', data[445:449])[0]
        paid_date = cls._decode_delphi_date(paid_date_int) if paid_date_int > 0 else None
        paid_amount = Decimal(str(round(struct.unpack('<d', data[449:457])[0], 2)))
        
        # References
        invoice_number = data[457:487].decode(encoding, errors='ignore').rstrip('\\x00 ')
        order_number = data[487:517].decode(encoding, errors='ignore').rstrip('\\x00 ')
        
        # Notes (flexible)
        internal_note = ""
        public_note = ""
        if len(data) >= 717:
            internal_note = data[517:717].decode(encoding, errors='ignore').rstrip('\\x00 ')
        if len(data) >= 917:
            public_note = data[717:917].decode(encoding, errors='ignore').rstrip('\\x00 ')
        
        return cls(
            doc_number=doc_number,
            doc_type=doc_type,
            doc_date=doc_date,
            delivery_date=delivery_date,
            due_date=due_date,
            pab_code=pab_code,
            pab_name=pab_name,
            pab_address=pab_address,
            pab_ico=pab_ico,
            pab_dic=pab_dic,
            pab_ic_dph=pab_ic_dph,
            currency=currency,
            exchange_rate=exchange_rate,
            amount_base=amount_base,
            amount_vat=amount_vat,
            amount_total=amount_total,
            vat_20_base=vat_20_base,
            vat_20_amount=vat_20_amount,
            vat_10_base=vat_10_base,
            vat_10_amount=vat_10_amount,
            vat_0_base=vat_0_base,
            payment_method=payment_method,
            payment_terms=payment_terms,
            paid=paid,
            paid_date=paid_date,
            paid_amount=paid_amount,
            invoice_number=invoice_number,
            order_number=order_number,
            internal_note=internal_note,
            public_note=public_note
        )
    
    @staticmethod
    def _decode_delphi_date(days: int) -> date:
        """Convert Delphi date to Python date"""
        from datetime import timedelta
        base_date = datetime(1899, 12, 30)
        return (base_date + timedelta(days=days)).date()
    
    def validate(self) -> list[str]:
        """Validate record"""
        errors = []
        if not self.doc_number.strip():
            errors.append("DocNumber cannot be empty")
        if self.pab_code <= 0:
            errors.append("PabCode must be positive")
        if self.amount_total < 0:
            errors.append("AmountTotal cannot be negative")
        expected_total = self.amount_base + self.amount_vat
        if abs(expected_total - self.amount_total) > Decimal("0.01"):
            errors.append(f"Invalid total: {self.amount_total} != {expected_total}")
        return errors
    
    def __str__(self) -> str:
        return f"TSH({self.doc_number}: {self.pab_name}, {self.amount_total} {self.currency})"
''')

    # 7. TSI Model
    create_file(base / "nex_shared/models/tsi.py", '''"""TSI Table Model - Dodacie listy Items"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal
import struct


@dataclass
class TSIRecord:
    """TSI record structure - Dodacie listy Items"""
    
    # Composite primary key
    doc_number: str
    line_number: int
    
    # Product
    gs_code: int = 0
    gs_name: str = ""
    bar_code: str = ""
    
    # Quantity
    quantity: Decimal = Decimal("1.0")
    unit: str = "ks"
    unit_coef: Decimal = Decimal("1.0")
    
    # Pricing
    price_unit: Decimal = Decimal("0.00")
    price_unit_vat: Decimal = Decimal("0.00")
    vat_rate: Decimal = Decimal("20.0")
    discount_percent: Decimal = Decimal("0.0")
    
    # Line totals
    line_base: Decimal = Decimal("0.00")
    line_vat: Decimal = Decimal("0.00")
    line_total: Decimal = Decimal("0.00")
    
    # Stock
    warehouse_code: int = 1
    batch_number: str = ""
    serial_number: str = ""
    
    # Additional
    note: str = ""
    supplier_item_code: str = ""
    status: int = 1
    
    # Audit
    mod_user: str = ""
    mod_date: Optional[datetime] = None
    mod_time: Optional[datetime] = None
    
    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'TSIRecord':
        """Deserialize TSI record from bytes"""
        if len(data) < 400:
            raise ValueError(f"Invalid record size: {len(data)} bytes")
        
        # Primary key
        doc_number = data[0:20].decode(encoding, errors='ignore').rstrip('\\x00 ')
        line_number = struct.unpack('<i', data[20:24])[0]
        
        # Product
        gs_code = struct.unpack('<i', data[24:28])[0]
        gs_name = data[28:108].decode(encoding, errors='ignore').rstrip('\\x00 ')
        bar_code = data[108:123].decode(encoding, errors='ignore').rstrip('\\x00 ')
        
        # Quantity
        quantity = Decimal(str(round(struct.unpack('<d', data[123:131])[0], 3)))
        unit = data[131:141].decode(encoding, errors='ignore').rstrip('\\x00 ')
        unit_coef = Decimal(str(struct.unpack('<d', data[141:149])[0]))
        
        # Pricing
        price_unit = Decimal(str(round(struct.unpack('<d', data[149:157])[0], 2)))
        price_unit_vat = Decimal(str(round(struct.unpack('<d', data[157:165])[0], 2)))
        vat_rate = Decimal(str(round(struct.unpack('<d', data[165:173])[0], 1)))
        discount_percent = Decimal(str(round(struct.unpack('<d', data[173:181])[0], 2)))
        
        # Line totals
        line_base = Decimal(str(round(struct.unpack('<d', data[181:189])[0], 2)))
        line_vat = Decimal(str(round(struct.unpack('<d', data[189:197])[0], 2)))
        line_total = Decimal(str(round(struct.unpack('<d', data[197:205])[0], 2)))
        
        # Stock
        warehouse_code = struct.unpack('<i', data[205:209])[0]
        batch_number = data[209:239].decode(encoding, errors='ignore').rstrip('\\x00 ')
        serial_number = data[239:269].decode(encoding, errors='ignore').rstrip('\\x00 ')
        
        # Additional
        note = data[269:369].decode(encoding, errors='ignore').rstrip('\\x00 ')
        supplier_item_code = data[369:399].decode(encoding, errors='ignore').rstrip('\\x00 ')
        status = struct.unpack('<i', data[399:403])[0]
        
        # Audit
        mod_user = ""
        mod_date = None
        mod_time = None
        if len(data) >= 419:
            mod_user = data[403:411].decode(encoding, errors='ignore').rstrip('\\x00 ')
            mod_date_int = struct.unpack('<i', data[411:415])[0]
            mod_date = cls._decode_delphi_date(mod_date_int) if mod_date_int > 0 else None
            mod_time_int = struct.unpack('<i', data[415:419])[0]
            mod_time = cls._decode_delphi_time(mod_time_int) if mod_time_int >= 0 else None
        
        return cls(
            doc_number=doc_number,
            line_number=line_number,
            gs_code=gs_code,
            gs_name=gs_name,
            bar_code=bar_code,
            quantity=quantity,
            unit=unit,
            unit_coef=unit_coef,
            price_unit=price_unit,
            price_unit_vat=price_unit_vat,
            vat_rate=vat_rate,
            discount_percent=discount_percent,
            line_base=line_base,
            line_vat=line_vat,
            line_total=line_total,
            warehouse_code=warehouse_code,
            batch_number=batch_number,
            serial_number=serial_number,
            note=note,
            supplier_item_code=supplier_item_code,
            status=status,
            mod_user=mod_user,
            mod_date=mod_date,
            mod_time=mod_time
        )
    
    @staticmethod
    def _decode_delphi_date(days: int) -> datetime:
        """Convert Delphi date to Python datetime"""
        from datetime import timedelta
        base_date = datetime(1899, 12, 30)
        return base_date + timedelta(days=days)
    
    @staticmethod
    def _decode_delphi_time(milliseconds: int) -> datetime:
        """Convert Delphi time to Python datetime"""
        from datetime import timedelta
        base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return base + timedelta(milliseconds=milliseconds)
    
    def calculate_line_totals(self) -> None:
        """Calculate line totals"""
        subtotal = self.quantity * self.price_unit
        discount_amount = subtotal * (self.discount_percent / Decimal("100"))
        self.line_base = subtotal - discount_amount
        self.line_vat = self.line_base * (self.vat_rate / Decimal("100"))
        self.line_total = self.line_base + self.line_vat
        self.line_base = round(self.line_base, 2)
        self.line_vat = round(self.line_vat, 2)
        self.line_total = round(self.line_total, 2)
    
    def validate(self) -> list[str]:
        """Validate record"""
        errors = []
        if not self.doc_number.strip():
            errors.append("DocNumber cannot be empty")
        if self.line_number <= 0:
            errors.append("LineNumber must be positive")
        if self.gs_code <= 0:
            errors.append("GsCode must be positive")
        if self.quantity <= 0:
            errors.append("Quantity must be positive")
        if self.price_unit < 0:
            errors.append("PriceUnit cannot be negative")
        if self.discount_percent < 0 or self.discount_percent > 100:
            errors.append(f"Invalid discount: {self.discount_percent}%")
        expected_total = self.line_base + self.line_vat
        if abs(expected_total - self.line_total) > Decimal("0.01"):
            errors.append(f"Invalid line total: {self.line_total} != {expected_total}")
        return errors
    
    def __str__(self) -> str:
        return f"TSI({self.doc_number}/{self.line_number}: {self.gs_name}, {self.quantity} {self.unit})"
''')

    # 8. BtrieveClient (skrátená verzia pre základnú funkcionalitu)
    create_file(base / "nex_shared/btrieve/btrieve_client.py", '''"""Python wrapper pre Pervasive Btrieve API (32-bit)"""

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
            Path(r"C:\\Program Files (x86)\\Pervasive Software\\PSQL\\bin"),
            Path(r"C:\\PVSW\\bin"),
            Path(r"C:\\Windows\\SysWOW64"),
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
        filename_bytes = filename.encode('ascii') + b'\\x00'
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
''')

    # 9. Base Repository
    create_file(base / "nex_shared/repositories/base_repository.py", '''"""Base Repository Pattern"""

from typing import Generic, TypeVar, Optional, List, Callable
from abc import ABC, abstractmethod
from nex_shared.btrieve.btrieve_client import BtrieveClient
import logging

logger = logging.getLogger(__name__)
T = TypeVar('T')


class BaseRepository(Generic[T], ABC):
    """Base repository providing common CRUD operations"""
    
    def __init__(self, btrieve_client: BtrieveClient):
        """Initialize repository with Btrieve client"""
        self.client = btrieve_client
        self._is_open = False
    
    @property
    @abstractmethod
    def table_name(self) -> str:
        """Table name for BtrieveClient"""
        pass
    
    @abstractmethod
    def from_bytes(self, data: bytes) -> T:
        """Convert raw Btrieve bytes to model instance"""
        pass
    
    def open(self) -> bool:
        """Open Btrieve table"""
        if self._is_open:
            return True
        status, pos_block = self.client.open_file(self.table_name)
        if status == BtrieveClient.STATUS_SUCCESS:
            self._is_open = True
            self._pos_block = pos_block
            return True
        return False
    
    def close(self):
        """Close Btrieve table"""
        if self._is_open and hasattr(self, '_pos_block'):
            self.client.close_file(self._pos_block)
            self._is_open = False
    
    def get_first(self) -> Optional[T]:
        """Get first record"""
        if not self._is_open:
            if not self.open():
                return None
        status, data = self.client.get_first(self._pos_block)
        if status == BtrieveClient.STATUS_SUCCESS:
            try:
                return self.from_bytes(data)
            except Exception as e:
                logger.error(f"Failed to deserialize: {e}")
                return None
        return None
    
    def get_next(self) -> Optional[T]:
        """Get next record"""
        if not self._is_open:
            return None
        status, data = self.client.get_next(self._pos_block)
        if status == BtrieveClient.STATUS_SUCCESS:
            try:
                return self.from_bytes(data)
            except Exception as e:
                logger.error(f"Failed to deserialize: {e}")
                return None
        return None
    
    def get_all(self, max_records: int = 10000) -> List[T]:
        """Get all records"""
        records = []
        if not self._is_open:
            if not self.open():
                return records
        record = self.get_first()
        if record:
            records.append(record)
        else:
            return records
        while len(records) < max_records:
            record = self.get_next()
            if record is None:
                break
            records.append(record)
        return records
''')

    print()
    print("=" * 80)
    print("✅ ALL FILES CREATED")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. python scripts\\reinstall_nex_shared.py")
    print("2. python scripts\\test_nex_shared_import.py")


if __name__ == "__main__":
    main()