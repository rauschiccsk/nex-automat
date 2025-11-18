r"""
BARCODE Table Model
Druhotné identifikačné kódy (čiarové kódy) produktov

Table: BARCODE.BTR
Location: C:\NEX\YEARACT\STORES\BARCODE.BTR
Definition: barcode.bdf
Record Size: ~50 bytes
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import struct


@dataclass
class BarcodeRecord:
    """
    BARCODE record structure

    Jeden produkt môže mať viacero čiarových kódov.
    Composite index GsBc zabezpečuje unique constraint (GsCode + BarCode).
    """

    # Primary fields
    gs_code: int  # Tovarové číslo (PLU) - foreign key to GSCAT
    bar_code: str  # Čiarový kód (EAN, Code128, QR, custom)

    # Audit fields
    mod_user: str = ""  # Užívateľ, ktorý urobil poslednú zmenu
    mod_date: Optional[datetime] = None  # Dátum poslednej zmeny
    mod_time: Optional[datetime] = None  # Čas poslednej zmeny

    # Indexes (constants)
    INDEX_GSCODE = 'GsCode'  # Index podľa tovarového čísla
    INDEX_BARCODE = 'BarCode'  # Index podľa čiarového kódu
    INDEX_GSBC = 'GsBc'  # Composite index (unique)

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'BarcodeRecord':
        """
        Deserialize Btrieve record from bytes

        Field Layout (approximate):
        - GsCode: 4 bytes (0-3) - longint
        - BarCode: 15 bytes (4-18) - string
        - ModUser: 8 bytes (19-26) - string
        - ModDate: 4 bytes (27-30) - longint (days since 1899-12-30)
        - ModTime: 4 bytes (31-34) - longint (milliseconds since midnight)

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            BarcodeRecord instance
        """
        if len(data) < 35:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= 35)")

        # GsCode (longint, 4 bytes)
        gs_code = struct.unpack('<i', data[0:4])[0]

        # BarCode (string, 15 bytes)
        bar_code = data[4:19].decode(encoding, errors='ignore').rstrip('\x00 ')

        # ModUser (string, 8 bytes)
        mod_user = data[19:27].decode(encoding, errors='ignore').rstrip('\x00 ')

        # ModDate (longint, 4 bytes) - days since 1899-12-30
        mod_date_int = struct.unpack('<i', data[27:31])[0]
        mod_date = cls._decode_delphi_date(mod_date_int) if mod_date_int > 0 else None

        # ModTime (longint, 4 bytes) - milliseconds since midnight
        mod_time_int = struct.unpack('<i', data[31:35])[0]
        mod_time = cls._decode_delphi_time(mod_time_int) if mod_time_int >= 0 else None

        return cls(
            gs_code=gs_code,
            bar_code=bar_code,
            mod_user=mod_user,
            mod_date=mod_date,
            mod_time=mod_time
        )

    def to_bytes(self, encoding: str = 'cp852') -> bytes:
        """
        Serialize record to bytes for Btrieve

        Args:
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            Raw bytes for Btrieve
        """
        result = bytearray(50)  # Fixed size record

        # GsCode
        struct.pack_into('<i', result, 0, self.gs_code)

        # BarCode (pad to 15 bytes)
        bar_code_bytes = self.bar_code.encode(encoding)[:15]
        result[4:4 + len(bar_code_bytes)] = bar_code_bytes

        # ModUser (pad to 8 bytes)
        mod_user_bytes = self.mod_user.encode(encoding)[:8]
        result[19:19 + len(mod_user_bytes)] = mod_user_bytes

        # ModDate
        if self.mod_date:
            mod_date_int = self._encode_delphi_date(self.mod_date)
            struct.pack_into('<i', result, 27, mod_date_int)

        # ModTime
        if self.mod_time:
            mod_time_int = self._encode_delphi_time(self.mod_time)
            struct.pack_into('<i', result, 31, mod_time_int)

        return bytes(result)

    @staticmethod
    def _decode_delphi_date(days: int) -> datetime:
        """
        Convert Delphi TDateTime date part to Python datetime

        Delphi date: days since 1899-12-30
        """
        from datetime import timedelta
        base_date = datetime(1899, 12, 30)
        return base_date + timedelta(days=days)

    @staticmethod
    def _encode_delphi_date(dt: datetime) -> int:
        """Convert Python datetime to Delphi date (days since 1899-12-30)"""
        base_date = datetime(1899, 12, 30)
        delta = dt - base_date
        return delta.days

    @staticmethod
    def _decode_delphi_time(milliseconds: int) -> datetime:
        """
        Convert Delphi TDateTime time part to Python datetime

        Delphi time: milliseconds since midnight
        """
        from datetime import timedelta
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return base_time + timedelta(milliseconds=milliseconds)

    @staticmethod
    def _encode_delphi_time(dt: datetime) -> int:
        """Convert Python datetime to Delphi time (milliseconds since midnight)"""
        midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = dt - midnight
        return int(delta.total_seconds() * 1000)

    def validate(self) -> list[str]:
        """
        Validate record fields

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if self.gs_code <= 0:
            errors.append("GsCode must be positive")

        if not self.bar_code or len(self.bar_code.strip()) == 0:
            errors.append("BarCode cannot be empty")

        if len(self.bar_code) > 15:
            errors.append(f"BarCode too long: {len(self.bar_code)} (max 15)")

        if len(self.bar_code.strip()) < 8:
            errors.append(f"BarCode too short: {len(self.bar_code.strip())} (min 8)")

        if len(self.mod_user) > 8:
            errors.append(f"ModUser too long: {len(self.mod_user)} (max 8)")

        return errors

    def __str__(self) -> str:
        """String representation"""
        return f"BarcodeRecord(gs_code={self.gs_code}, bar_code='{self.bar_code}')"

    def __repr__(self) -> str:
        """Debug representation"""
        return (f"BarcodeRecord(gs_code={self.gs_code}, bar_code='{self.bar_code}', "
                f"mod_user='{self.mod_user}', mod_date={self.mod_date}, mod_time={self.mod_time})")


# Example usage
if __name__ == "__main__":
    # Create new record
    record = BarcodeRecord(
        gs_code=12345,
        bar_code="8594000123456",
        mod_user="API",
        mod_date=datetime.now(),
        mod_time=datetime.now()
    )

    print("Created:", record)
    print("Valid:", len(record.validate()) == 0)

    # Serialize/Deserialize test
    raw_bytes = record.to_bytes()
    print(f"Serialized: {len(raw_bytes)} bytes")

    restored = BarcodeRecord.from_bytes(raw_bytes)
    print("Restored:", restored)
    print("Match:", record.gs_code == restored.gs_code and record.bar_code == restored.bar_code)