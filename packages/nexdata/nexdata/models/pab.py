r"""
PAB Table Model
Katalóg obchodných partnerov (dodávatelia, odberatelia)

Table: PAB00000.BTR
Location: C:\NEX\YEARACT\DIALS\PAB00000.BTR
Definition: pab.bdf
Record Size: 1269 bytes
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import struct


@dataclass
class PABRecord:
    """
    PAB record structure - Obchodní partneri

    Evidencia všetkých obchodných partnerov (dodávatelia, odberatelia, ostatní).
    """

    # Primary key
    pab_code: int  # Kód partnera - primary key

    # Basic info
    name1: str = ""  # Názov firmy (riadok 1)
    name2: str = ""  # Názov firmy (riadok 2)
    short_name: str = ""  # Skrátený názov

    # Address
    street: str = ""  # Ulica a číslo
    city: str = ""  # Mesto
    zip_code: str = ""  # PSČ
    country: str = ""  # Krajina

    # Contact
    phone: str = ""  # Telefón
    fax: str = ""  # Fax
    email: str = ""  # Email
    web: str = ""  # Web stránka
    contact_person: str = ""  # Kontaktná osoba

    # Tax info
    ico: str = ""  # IČO (identifikačné číslo organizácie)
    dic: str = ""  # DIČ (daňové identifikačné číslo)
    ic_dph: str = ""  # IČ DPH (identifikačné číslo pre DPH)

    # Bank info
    bank_account: str = ""  # Číslo účtu
    bank_code: str = ""  # Kód banky
    bank_name: str = ""  # Názov banky
    iban: str = ""  # IBAN
    swift: str = ""  # SWIFT/BIC

    # Business info
    partner_type: int = 0  # Typ partnera (1=dodávateľ, 2=odberateľ, 3=oboje)
    payment_terms: int = 14  # Platobné podmienky (dni)
    credit_limit: float = 0.0  # Kreditný limit
    discount_percent: float = 0.0  # Zľava v percentách

    # Status
    active: bool = True  # Aktívny partner
    vat_payer: bool = True  # Platiteľ DPH

    # Notes
    note: str = ""  # Poznámka
    note2: str = ""  # Poznámka 2
    internal_note: str = ""  # Interná poznámka

    # Audit fields
    mod_user: str = ""  # Užívateľ poslednej zmeny
    mod_date: Optional[datetime] = None  # Dátum poslednej zmeny
    mod_time: Optional[datetime] = None  # Čas poslednej zmeny
    created_date: Optional[datetime] = None  # Dátum vytvorenia
    created_user: str = ""  # Užívateľ vytvorenia

    # Indexes (constants)
    INDEX_PABCODE = 'PabCode'  # Primary index
    INDEX_NAME = 'Name1'  # Index podľa názvu
    INDEX_ICO = 'ICO'  # Index podľa IČO
    INDEX_TYPE = 'PartnerType'  # Index podľa typu partnera

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'PABRecord':
        """
        Deserialize PAB record from bytes

        Field Layout (approximate, based on 1269 bytes record):
        - PabCode: 4 bytes (0-3) - longint
        - Name1: 100 bytes (4-103) - string
        - Name2: 100 bytes (104-203) - string
        - ShortName: 40 bytes (204-243) - string
        - Street: 80 bytes (244-323) - string
        - City: 50 bytes (324-373) - string
        - ZipCode: 10 bytes (374-383) - string
        - Country: 50 bytes (384-433) - string
        - Phone: 30 bytes (434-463) - string
        - Fax: 30 bytes (464-493) - string
        - Email: 60 bytes (494-553) - string
        - Web: 60 bytes (554-613) - string
        - ContactPerson: 50 bytes (614-663) - string
        - ICO: 20 bytes (664-683) - string
        - DIC: 20 bytes (684-703) - string
        - ICDPH: 30 bytes (704-733) - string
        - BankAccount: 30 bytes (734-763) - string
        - BankCode: 10 bytes (764-773) - string
        - BankName: 60 bytes (774-833) - string
        - IBAN: 40 bytes (834-873) - string
        - SWIFT: 20 bytes (874-893) - string
        - PartnerType: 4 bytes (894-897) - longint
        - PaymentTerms: 4 bytes (898-901) - longint
        - CreditLimit: 8 bytes (902-909) - double
        - DiscountPercent: 8 bytes (910-917) - double
        - Active: 1 byte (918) - boolean
        - VatPayer: 1 byte (919) - boolean
        - Note: 200 bytes (920-1119) - string
        - Note2: 100 bytes (1120-1219) - string
        - InternalNote: 100 bytes (1220-1319) - string (may overflow)

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            PABRecord instance
        """
        if len(data) < 1269:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected 1269)")

        # Primary key
        pab_code = struct.unpack('<i', data[0:4])[0]

        # Basic info
        name1 = data[4:104].decode(encoding, errors='ignore').rstrip('\x00 ')
        name2 = data[104:204].decode(encoding, errors='ignore').rstrip('\x00 ')
        short_name = data[204:244].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Address
        street = data[244:324].decode(encoding, errors='ignore').rstrip('\x00 ')
        city = data[324:374].decode(encoding, errors='ignore').rstrip('\x00 ')
        zip_code = data[374:384].decode(encoding, errors='ignore').rstrip('\x00 ')
        country = data[384:434].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Contact
        phone = data[434:464].decode(encoding, errors='ignore').rstrip('\x00 ')
        fax = data[464:494].decode(encoding, errors='ignore').rstrip('\x00 ')
        email = data[494:554].decode(encoding, errors='ignore').rstrip('\x00 ')
        web = data[554:614].decode(encoding, errors='ignore').rstrip('\x00 ')
        contact_person = data[614:664].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Tax info
        ico = data[664:684].decode(encoding, errors='ignore').rstrip('\x00 ')
        dic = data[684:704].decode(encoding, errors='ignore').rstrip('\x00 ')
        ic_dph = data[704:734].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Bank info
        bank_account = data[734:764].decode(encoding, errors='ignore').rstrip('\x00 ')
        bank_code = data[764:774].decode(encoding, errors='ignore').rstrip('\x00 ')
        bank_name = data[774:834].decode(encoding, errors='ignore').rstrip('\x00 ')
        iban = data[834:874].decode(encoding, errors='ignore').rstrip('\x00 ')
        swift = data[874:894].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Business info
        partner_type = struct.unpack('<i', data[894:898])[0]
        payment_terms = struct.unpack('<i', data[898:902])[0]
        credit_limit = struct.unpack('<d', data[902:910])[0]
        discount_percent = struct.unpack('<d', data[910:918])[0]

        # Status
        active = bool(data[918])
        vat_payer = bool(data[919])

        # Notes
        note = data[920:1120].decode(encoding, errors='ignore').rstrip('\x00 ')
        note2 = data[1120:1220].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Internal note (may be at different offset)
        internal_note = ""
        if len(data) >= 1269:
            # Try to extract from remaining bytes
            internal_note = data[1220:1269].decode(encoding, errors='ignore').rstrip('\x00 ')

        return cls(
            pab_code=pab_code,
            name1=name1,
            name2=name2,
            short_name=short_name,
            street=street,
            city=city,
            zip_code=zip_code,
            country=country,
            phone=phone,
            fax=fax,
            email=email,
            web=web,
            contact_person=contact_person,
            ico=ico,
            dic=dic,
            ic_dph=ic_dph,
            bank_account=bank_account,
            bank_code=bank_code,
            bank_name=bank_name,
            iban=iban,
            swift=swift,
            partner_type=partner_type,
            payment_terms=payment_terms,
            credit_limit=credit_limit,
            discount_percent=discount_percent,
            active=active,
            vat_payer=vat_payer,
            note=note,
            note2=note2,
            internal_note=internal_note
        )

    def validate(self) -> list[str]:
        """Validate record"""
        errors = []

        if self.pab_code <= 0:
            errors.append("PabCode must be positive")
        if not self.name1.strip():
            errors.append("Name1 cannot be empty")
        if self.ico and len(self.ico) not in [8, 10, 12]:
            errors.append(f"Invalid ICO length: {len(self.ico)} (expected 8, 10 or 12)")
        if self.payment_terms < 0:
            errors.append("PaymentTerms cannot be negative")
        if self.credit_limit < 0:
            errors.append("CreditLimit cannot be negative")

        return errors

    def get_full_name(self) -> str:
        """Get full company name (Name1 + Name2)"""
        if self.name2:
            return f"{self.name1} {self.name2}".strip()
        return self.name1

    def get_full_address(self) -> str:
        """Get full address as single line"""
        parts = [self.street, self.city, self.zip_code, self.country]
        return ", ".join([p for p in parts if p])

    def is_supplier(self) -> bool:
        """Check if partner is supplier"""
        return self.partner_type in [1, 3]  # 1=supplier, 3=both

    def is_customer(self) -> bool:
        """Check if partner is customer"""
        return self.partner_type in [2, 3]  # 2=customer, 3=both

    def __str__(self) -> str:
        return f"PAB({self.pab_code}: {self.name1})"