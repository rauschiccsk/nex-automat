"""TSH Table Model - Dodacie listy Header"""

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
        doc_number = data[0:20].decode(encoding, errors='ignore').rstrip('\x00 ')
        
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
        pab_name = data[40:140].decode(encoding, errors='ignore').rstrip('\x00 ')
        pab_address = data[140:290].decode(encoding, errors='ignore').rstrip('\x00 ')
        pab_ico = data[290:310].decode(encoding, errors='ignore').rstrip('\x00 ')
        pab_dic = data[310:330].decode(encoding, errors='ignore').rstrip('\x00 ')
        pab_ic_dph = data[330:360].decode(encoding, errors='ignore').rstrip('\x00 ')
        
        # Financial
        currency = data[360:364].decode(encoding, errors='ignore').rstrip('\x00 ')
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
        invoice_number = data[457:487].decode(encoding, errors='ignore').rstrip('\x00 ')
        order_number = data[487:517].decode(encoding, errors='ignore').rstrip('\x00 ')
        
        # Notes (flexible)
        internal_note = ""
        public_note = ""
        if len(data) >= 717:
            internal_note = data[517:717].decode(encoding, errors='ignore').rstrip('\x00 ')
        if len(data) >= 917:
            public_note = data[717:917].decode(encoding, errors='ignore').rstrip('\x00 ')
        
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
