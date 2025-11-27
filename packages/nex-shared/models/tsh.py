r"""
TSH Table Model
Dodacie listy - Header (hlavičky dokladov)

Table: TSHA-001.BTR (actual year, book 001)
Location: C:\NEX\YEARACT\STORES\TSHA-001.BTR
Definition: tsh.bdf
Record Size: ~800 bytes
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
import struct


@dataclass
class TSHRecord:
    """
    TSH record structure - Dodacie listy Header

    Obsahuje hlavičku dodacieho listu (zákazník, dátumy, sumy).
    Položky sú v TSI tabuľke (TSI records s rovnakým DocNumber).
    """

    # Primary key
    doc_number: str  # Číslo dokladu (napr. "DL2025001") - primary key

    # Document info
    doc_type: int = 1  # Typ dokladu (1=príjem, 2=výdaj, 3=transfer)
    doc_date: Optional[date] = None  # Dátum vystavenia
    delivery_date: Optional[date] = None  # Dátum dodania
    due_date: Optional[date] = None  # Dátum splatnosti

    # Partner
    pab_code: int = 0  # Kód partnera (foreign key to PAB)
    pab_name: str = ""  # Názov partnera (cache)
    pab_address: str = ""  # Adresa partnera (cache)
    pab_ico: str = ""  # IČO partnera (cache)
    pab_dic: str = ""  # DIČ partnera (cache)
    pab_ic_dph: str = ""  # IČ DPH partnera (cache)

    # Financial
    currency: str = "EUR"  # Mena (EUR, USD, CZK, etc.)
    exchange_rate: Decimal = Decimal("1.0")  # Výmenný kurz

    # Amounts (in document currency)
    amount_base: Decimal = Decimal("0.00")  # Základ dane
    amount_vat: Decimal = Decimal("0.00")  # DPH
    amount_total: Decimal = Decimal("0.00")  # Celkom s DPH

    # VAT breakdown
    vat_20_base: Decimal = Decimal("0.00")  # Základ DPH 20%
    vat_20_amount: Decimal = Decimal("0.00")  # DPH 20%
    vat_10_base: Decimal = Decimal("0.00")  # Základ DPH 10%
    vat_10_amount: Decimal = Decimal("0.00")  # DPH 10%
    vat_0_base: Decimal = Decimal("0.00")  # Základ DPH 0%

    # Payment
    payment_method: int = 1  # Spôsob platby (1=hotovosť, 2=prevodom, 3=karta)
    payment_terms: int = 14  # Platobné podmienky (dni)
    paid: bool = False  # Zaplatené
    paid_date: Optional[date] = None  # Dátum platby
    paid_amount: Decimal = Decimal("0.00")  # Zaplatená suma

    # References
    invoice_number: str = ""  # Číslo faktúry (ak relevantné)
    order_number: str = ""  # Číslo objednávky
    internal_note: str = ""  # Interná poznámka
    public_note: str = ""  # Verejná poznámka (pre zákazníka)

    # Status
    status: int = 1  # Stav (1=draft, 2=confirmed, 3=shipped, 4=cancelled)
    locked: bool = False  # Uzamknutý (nemožno upravovať)
    posted: bool = False  # Zaúčtovaný

    # Warehouse
    warehouse_code: int = 1  # Kód skladu

    # Audit fields
    mod_user: str = ""  # Užívateľ poslednej zmeny
    mod_date: Optional[datetime] = None  # Dátum poslednej zmeny
    mod_time: Optional[datetime] = None  # Čas poslednej zmeny
    created_date: Optional[datetime] = None  # Dátum vytvorenia
    created_user: str = ""  # Užívateľ vytvorenia

    # Indexes (constants)
    INDEX_DOCNUMBER = 'DocNumber'  # Primary index
    INDEX_PABCODE = 'PabCode'  # Index podľa partnera
    INDEX_DOCDATE = 'DocDate'  # Index podľa dátumu
    INDEX_STATUS = 'Status'  # Index podľa stavu

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'TSHRecord':
        """
        Deserialize TSH record from bytes

        Field Layout (approximate, ~800 bytes):
        - DocNumber: 20 bytes (0-19) - string
        - DocType: 4 bytes (20-23) - longint
        - DocDate: 4 bytes (24-27) - longint (Delphi date)
        - DeliveryDate: 4 bytes (28-31) - longint
        - DueDate: 4 bytes (32-35) - longint
        - PabCode: 4 bytes (36-39) - longint
        - PabName: 100 bytes (40-139) - string
        - PabAddress: 150 bytes (140-289) - string
        - PabICO: 20 bytes (290-309) - string
        - PabDIC: 20 bytes (310-329) - string
        - PabICDPH: 30 bytes (330-359) - string
        - Currency: 4 bytes (360-363) - string
        - ExchangeRate: 8 bytes (364-371) - double
        - AmountBase: 8 bytes (372-379) - double
        - AmountVat: 8 bytes (380-387) - double
        - AmountTotal: 8 bytes (388-395) - double
        - Vat20Base: 8 bytes (396-403) - double
        - Vat20Amount: 8 bytes (404-411) - double
        - Vat10Base: 8 bytes (412-419) - double
        - Vat10Amount: 8 bytes (420-427) - double
        - Vat0Base: 8 bytes (428-435) - double
        - PaymentMethod: 4 bytes (436-439) - longint
        - PaymentTerms: 4 bytes (440-443) - longint
        - Paid: 1 byte (444) - boolean
        - PaidDate: 4 bytes (445-448) - longint
        - PaidAmount: 8 bytes (449-456) - double
        - InvoiceNumber: 30 bytes (457-486) - string
        - OrderNumber: 30 bytes (487-516) - string
        - InternalNote: 200 bytes (517-716) - string
        - PublicNote: 200 bytes (717-916) - string (may be shorter)

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding

        Returns:
            TSHRecord instance
        """
        if len(data) < 500:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= 500)")

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

        # Check VAT calculation
        expected_total = self.amount_base + self.amount_vat
        if abs(expected_total - self.amount_total) > Decimal("0.01"):
            errors.append(f"Invalid total: {self.amount_total} != {expected_total}")

        return errors

    def __str__(self) -> str:
        return f"TSH({self.doc_number}: {self.pab_name}, {self.amount_total} {self.currency})"
