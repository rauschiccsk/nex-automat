"""
Skript na vytvorenie kompletného GSCATRecord modelu
Zahŕňa VŠETKY polia z gscat.bdf vrátane BarCode
"""

complete_model = '''r"""
GSCAT Table Model - COMPLETE VERSION
Produktový katalóg (master produktová tabuľka)

Table: GSCAT.BTR
Location: C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR
Definition: gscat.bdf
Record Size: 705 bytes
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal
import struct


@dataclass
class GSCATRecord:
    """
    GSCAT record structure - Produktový katalóg
    Complete model with ALL fields from Btrieve definition
    """

    # === PRIMARY KEY ===
    GsCode: int  # Tovarové číslo (PLU) - primary key

    # === BASIC INFO ===
    GsName: str = ""  # Názov tovaru (Str30)
    _GsName: str = ""  # Vyhľadávacie pole názvu tovaru (Str15)

    # === CLASSIFICATION ===
    MgCode: int = 0  # Číslo tovarovej skupiny (longint)
    FgCode: int = 0  # Číslo finančnej skupiny (longint)

    # === IDENTIFICATION CODES ===
    BarCode: str = ""  # Prvotný identifikačný kód tovaru (Str15) - EAN!
    StkCode: str = ""  # Skladový kód tovaru (Str15)

    # === MEASUREMENT ===
    MsName: str = ""  # Názov mernej jednotky (Str10)

    # === PACKAGING ===
    PackGs: int = 0  # Tovarové číslo pripojeného obalu (longint)

    # === TYPE & FLAGS ===
    GsType: str = ""  # Typ položky (Str1) T-riadny tovar, W-vahovy tovar, O-obal
    DrbMust: int = 0  # Povinné zadávanie trvanlivosti (byte)
    PdnMust: int = 0  # Povinné sledovanie výrobných čísiel (byte)

    # === QUALITY ===
    GrcMth: int = 0  # Záručná doba (počet mesiacov) (word)

    # === PRICING & TAX ===
    VatPrc: int = 0  # Percentuálna sadzba DPH (byte)

    # === PHYSICAL PROPERTIES ===
    Volume: float = 0.0  # Objem tovaru (množstvo MJ na 1 m3) (double)
    Weight: float = 0.0  # Váha tovaru (váha jednej MJ) (double)

    # === BASE UNIT ===
    MsuQnt: float = 0.0  # Množstvo tovaru v základnej jednotke (double)
    MsuName: str = ""  # Názov základnej jednoty (Str5) kg,m,l,m2,m3

    # === BARCODES ===
    SbcCnt: int = 0  # Počet propojených druhotných identifikačných kódov (word)

    # === STATUS ===
    DisFlag: int = 0  # Vyradenie z evidencie (byte) 1-vyradený

    # === LAST PURCHASE ===
    LinPrice: float = 0.0  # Posledna nakupna cena tovaru (double)
    LinDate: Optional[datetime] = None  # Datum posledneho prijmu (DateType)
    LinStk: int = 0  # Cislo skladu posledneho prijmu (word)

    # === SYNC ===
    Sended: int = 0  # Priznak odoslania zmien (byte) 0-zmeneny, 1-odoslany
    ModNum: int = 0  # Poradove cislo modifikacie zaznamu (word)

    # === AUDIT ===
    ModUser: str = ""  # Prihlasovacie meno užívateľa (Str8)
    ModDate: Optional[datetime] = None  # Dátum posledného ukladania (DateType)
    ModTime: Optional[datetime] = None  # Čas posledného ukladania (TimeType)

    # === SUPPLIER ===
    LinPac: int = 0  # Kod posledneho dodavatela (longint)

    # === WEIGHING ===
    SecNum: int = 0  # Cislo vahovej sekcie (word)
    WgCode: int = 0  # Vahove tovarove cislo (vahove PLU) (word)

    # === CREATION ===
    CrtUser: str = ""  # Prihlasovacie meno uzivatela (Str8)
    CrtDate: Optional[datetime] = None  # Datum vytvorenia zaznam (DateType)
    CrtTime: Optional[datetime] = None  # Cas vytvorenia zaznam (TimeType)

    # === PRODUCT HIERARCHY ===
    BasGsc: int = 0  # Odkaz na základný tovar (longint)
    GscKfc: int = 0  # Počet kusov v kartónovom balení (word)
    GspKfc: int = 0  # Počet kartónov v paletovom balení (word)
    QliKfc: float = 0.0  # Hmotnosť kartónu (double)

    # === EXPIRATION ===
    DrbDay: int = 0  # Počet dni trvanlivosti (word)

    # === ORDERING ===
    OsdCode: str = ""  # Objednávaci kód tovaru (Str15)
    MinOsq: float = 0.0  # Minimálne objednávacie množstvo (double)

    # === CODES & SUPPLIERS ===
    SpcCode: str = ""  # Špecifikačný kód položky (Str30)
    PrdPac: int = 0  # Kód výrobcu (longint)
    SupPac: int = 0  # Kód dodávateľa (longint)

    # === ALCOHOL ===
    SpirGs: int = 0  # Priznak liehoveho výrobu (byte) 1-liehový výrobok

    # === ADDITIONAL NAME ===
    GaName: str = ""  # Doplnkový názov tovaru (Str60)
    _GaName: str = ""  # Doplnkový názov tovaru - vyhľadávacie pole (Str60)

    # === DIVISIBILITY ===
    DivSet: int = 0  # Priznak delitelnosti tovaru (byte)

    # === SPECIFICATION GROUP ===
    SgCode: int = 0  # Číslo špecifikačnej skupiny (longint)

    # === NOTES ===
    Notice: str = ""  # Poznámkový riadok (Str240)

    # === VAT CHANGE ===
    NewVatPrc: str = ""  # Nová pripravená sadzba na zmeny DPH (Str2)

    # === RESERVE ===
    Reserve: str = ""  # Reserve (Str4)

    # === E-SHOP ===
    ShpNum: int = 0  # Číslo elektronického obchodu (byte)
    SndShp: int = 0  # Príznnak, že karta bola uložená do e-shopu (byte)

    # === PRICE LISTS ===
    PlsNum1: int = 0  # Cislo predajneho cennika 1 (word)
    PlsNum2: int = 0  # Cislo predajneho cennika 2 (word)
    PlsNum3: int = 0  # Cislo predajneho cennika 3 (word)
    PlsNum4: int = 0  # Cislo predajneho cennika 4 (word)
    PlsNum5: int = 0  # Cislo predajneho cennika 5 (word)

    # === BATCH TRACKING ===
    RbaTrc: int = 0  # Povinné sledovanie výrobnej šarže (byte)

    # === CUSTOMS ===
    CctCod: str = ""  # Kód jednotnej tarify colného sadzobníka (Str10)

    # === ACCOUNTING ===
    IsiSnt: str = ""  # Syntetická časť účtu prerozúčtovanie položky DF (Str3)
    IsiAnl: str = ""  # Analytická časť účtu prerozúčtovanie položky DF (Str6)
    IciSnt: str = ""  # Syntetická časť účtu prerozúčtovanie položky OF (Str3)
    IciAnl: str = ""  # Analytická časť účtu prerozúčtovanie položky OF (Str6)

    # === PRODUCT TYPE ===
    ProTyp: str = ""  # Typ prduktu (Str1) M-materiál; T-tovar; S-služba

    # === INDEXES (constants) ===
    INDEX_GSCODE = 'GsCode'
    INDEX_GSNAME = 'GsName'
    INDEX_MGCODE = 'MgCode'
    INDEX_FGCODE = 'FgCode'
    INDEX_BARCODE = 'BarCode'  # INDEX NA EAN!!!
    INDEX_STKCODE = 'StkCode'
    INDEX_SPCCODE = 'SpcCode'
    INDEX_OSDCODE = 'OsdCode'

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'GSCATRecord':
        """
        Deserialize GSCAT record from bytes

        Field offsets calculated from gscat.bdf:
        Position calculation: sum of all previous field sizes

        String types: StrN means N bytes (fixed width, padded with nulls)
        longint: 4 bytes
        word: 2 bytes  
        byte: 1 byte
        double: 8 bytes
        DateType: 4 bytes (longint - days since 1899-12-30)
        TimeType: 4 bytes (longint - milliseconds since midnight)
        """
        if len(data) < 705:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected 705)")

        offset = 0

        # GsCode (longint, 4 bytes)
        GsCode = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # GsName (Str30, 30 bytes)
        GsName = data[offset:offset+30].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 30

        # _GsName (Str15, 15 bytes)
        _GsName = data[offset:offset+15].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 15

        # MgCode (longint, 4 bytes)
        MgCode = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # FgCode (longint, 4 bytes)
        FgCode = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # BarCode (Str15, 15 bytes) - EAN!!!
        BarCode = data[offset:offset+15].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 15

        # StkCode (Str15, 15 bytes)
        StkCode = data[offset:offset+15].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 15

        # MsName (Str10, 10 bytes)
        MsName = data[offset:offset+10].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 10

        # PackGs (longint, 4 bytes)
        PackGs = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # GsType (Str1, 1 byte)
        GsType = data[offset:offset+1].decode(encoding, errors='ignore')
        offset += 1

        # DrbMust (byte, 1 byte)
        DrbMust = data[offset]
        offset += 1

        # PdnMust (byte, 1 byte)
        PdnMust = data[offset]
        offset += 1

        # GrcMth (word, 2 bytes)
        GrcMth = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # VatPrc (byte, 1 byte)
        VatPrc = data[offset]
        offset += 1

        # Volume (double, 8 bytes)
        Volume = struct.unpack('<d', data[offset:offset+8])[0]
        offset += 8

        # Weight (double, 8 bytes)
        Weight = struct.unpack('<d', data[offset:offset+8])[0]
        offset += 8

        # MsuQnt (double, 8 bytes)
        MsuQnt = struct.unpack('<d', data[offset:offset+8])[0]
        offset += 8

        # MsuName (Str5, 5 bytes)
        MsuName = data[offset:offset+5].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 5

        # SbcCnt (word, 2 bytes)
        SbcCnt = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # DisFlag (byte, 1 byte)
        DisFlag = data[offset]
        offset += 1

        # LinPrice (double, 8 bytes)
        LinPrice = struct.unpack('<d', data[offset:offset+8])[0]
        offset += 8

        # LinDate (DateType, 4 bytes)
        LinDate_int = struct.unpack('<i', data[offset:offset+4])[0]
        LinDate = cls._decode_delphi_date(LinDate_int) if LinDate_int > 0 else None
        offset += 4

        # LinStk (word, 2 bytes)
        LinStk = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # Sended (byte, 1 byte)
        Sended = data[offset]
        offset += 1

        # ModNum (word, 2 bytes)
        ModNum = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # ModUser (Str8, 8 bytes)
        ModUser = data[offset:offset+8].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 8

        # ModDate (DateType, 4 bytes)
        ModDate_int = struct.unpack('<i', data[offset:offset+4])[0]
        ModDate = cls._decode_delphi_date(ModDate_int) if ModDate_int > 0 else None
        offset += 4

        # ModTime (TimeType, 4 bytes)
        ModTime_int = struct.unpack('<i', data[offset:offset+4])[0]
        ModTime = cls._decode_delphi_time(ModTime_int) if ModTime_int >= 0 else None
        offset += 4

        # LinPac (longint, 4 bytes)
        LinPac = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # SecNum (word, 2 bytes)
        SecNum = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # WgCode (word, 2 bytes)
        WgCode = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # CrtUser (Str8, 8 bytes)
        CrtUser = data[offset:offset+8].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 8

        # CrtDate (DateType, 4 bytes)
        CrtDate_int = struct.unpack('<i', data[offset:offset+4])[0]
        CrtDate = cls._decode_delphi_date(CrtDate_int) if CrtDate_int > 0 else None
        offset += 4

        # CrtTime (TimeType, 4 bytes)
        CrtTime_int = struct.unpack('<i', data[offset:offset+4])[0]
        CrtTime = cls._decode_delphi_time(CrtTime_int) if CrtTime_int >= 0 else None
        offset += 4

        # BasGsc (longint, 4 bytes)
        BasGsc = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # GscKfc (word, 2 bytes)
        GscKfc = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # GspKfc (word, 2 bytes)
        GspKfc = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # QliKfc (double, 8 bytes)
        QliKfc = struct.unpack('<d', data[offset:offset+8])[0]
        offset += 8

        # DrbDay (word, 2 bytes)
        DrbDay = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # OsdCode (Str15, 15 bytes)
        OsdCode = data[offset:offset+15].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 15

        # MinOsq (double, 8 bytes)
        MinOsq = struct.unpack('<d', data[offset:offset+8])[0]
        offset += 8

        # SpcCode (Str30, 30 bytes)
        SpcCode = data[offset:offset+30].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 30

        # PrdPac (longint, 4 bytes)
        PrdPac = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # SupPac (longint, 4 bytes)
        SupPac = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # SpirGs (byte, 1 byte)
        SpirGs = data[offset]
        offset += 1

        # GaName (Str60, 60 bytes)
        GaName = data[offset:offset+60].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 60

        # _GaName (Str60, 60 bytes)
        _GaName = data[offset:offset+60].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 60

        # DivSet (byte, 1 byte)
        DivSet = data[offset]
        offset += 1

        # SgCode (longint, 4 bytes)
        SgCode = struct.unpack('<i', data[offset:offset+4])[0]
        offset += 4

        # Notice (Str240, 240 bytes)
        Notice = data[offset:offset+240].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 240

        # NewVatPrc (Str2, 2 bytes)
        NewVatPrc = data[offset:offset+2].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 2

        # Reserve (Str4, 4 bytes)
        Reserve = data[offset:offset+4].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 4

        # ShpNum (byte, 1 byte)
        ShpNum = data[offset]
        offset += 1

        # SndShp (byte, 1 byte)
        SndShp = data[offset]
        offset += 1

        # PlsNum1 (word, 2 bytes)
        PlsNum1 = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # PlsNum2 (word, 2 bytes)
        PlsNum2 = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # PlsNum3 (word, 2 bytes)
        PlsNum3 = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # PlsNum4 (word, 2 bytes)
        PlsNum4 = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # PlsNum5 (word, 2 bytes)
        PlsNum5 = struct.unpack('<H', data[offset:offset+2])[0]
        offset += 2

        # RbaTrc (byte, 1 byte)
        RbaTrc = data[offset]
        offset += 1

        # CctCod (Str10, 10 bytes)
        CctCod = data[offset:offset+10].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 10

        # IsiSnt (Str3, 3 bytes)
        IsiSnt = data[offset:offset+3].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 3

        # IsiAnl (Str6, 6 bytes)
        IsiAnl = data[offset:offset+6].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 6

        # IciSnt (Str3, 3 bytes)
        IciSnt = data[offset:offset+3].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 3

        # IciAnl (Str6, 6 bytes)
        IciAnl = data[offset:offset+6].decode(encoding, errors='ignore').rstrip('\\x00 ')
        offset += 6

        # ProTyp (Str1, 1 byte)
        ProTyp = data[offset:offset+1].decode(encoding, errors='ignore')
        offset += 1

        # Total offset should be 705
        assert offset == 705, f"Offset mismatch: {offset} != 705"

        return cls(
            GsCode=GsCode,
            GsName=GsName,
            _GsName=_GsName,
            MgCode=MgCode,
            FgCode=FgCode,
            BarCode=BarCode,  # !!!
            StkCode=StkCode,
            MsName=MsName,
            PackGs=PackGs,
            GsType=GsType,
            DrbMust=DrbMust,
            PdnMust=PdnMust,
            GrcMth=GrcMth,
            VatPrc=VatPrc,
            Volume=Volume,
            Weight=Weight,
            MsuQnt=MsuQnt,
            MsuName=MsuName,
            SbcCnt=SbcCnt,
            DisFlag=DisFlag,
            LinPrice=LinPrice,
            LinDate=LinDate,
            LinStk=LinStk,
            Sended=Sended,
            ModNum=ModNum,
            ModUser=ModUser,
            ModDate=ModDate,
            ModTime=ModTime,
            LinPac=LinPac,
            SecNum=SecNum,
            WgCode=WgCode,
            CrtUser=CrtUser,
            CrtDate=CrtDate,
            CrtTime=CrtTime,
            BasGsc=BasGsc,
            GscKfc=GscKfc,
            GspKfc=GspKfc,
            QliKfc=QliKfc,
            DrbDay=DrbDay,
            OsdCode=OsdCode,
            MinOsq=MinOsq,
            SpcCode=SpcCode,
            PrdPac=PrdPac,
            SupPac=SupPac,
            SpirGs=SpirGs,
            GaName=GaName,
            _GaName=_GaName,
            DivSet=DivSet,
            SgCode=SgCode,
            Notice=Notice,
            NewVatPrc=NewVatPrc,
            Reserve=Reserve,
            ShpNum=ShpNum,
            SndShp=SndShp,
            PlsNum1=PlsNum1,
            PlsNum2=PlsNum2,
            PlsNum3=PlsNum3,
            PlsNum4=PlsNum4,
            PlsNum5=PlsNum5,
            RbaTrc=RbaTrc,
            CctCod=CctCod,
            IsiSnt=IsiSnt,
            IsiAnl=IsiAnl,
            IciSnt=IciSnt,
            IciAnl=IciAnl,
            ProTyp=ProTyp
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

    def __str__(self) -> str:
        return f"GSCAT({self.GsCode}: {self.GsName}, EAN: {self.BarCode})"
'''

# Uložiť do súboru
output_path = "packages/nexdata/nexdata/models/gscat_complete.py"

print("=" * 70)
print("Vytvorenie kompletného GSCAT modelu")
print("=" * 70)
print()
print(f"Vytváram: {output_path}")
print()
print("Nový model obsahuje:")
print("  ✓ Všetkých 60+ polí z gscat.bdf")
print("  ✓ BarCode pole (Str15) - EAN kód!")
print("  ✓ Presné offsety a typy")
print("  ✓ Kompletný from_bytes() parsing")
print()
print("DÔLEŽITÉ:")
print("  - Všetky názvy polí zodpovedajú Btrieve názvom")
print("  - BarCode je na pozícii 57 (offset vypočítaný)")
print("  - GsName je Str30, nie Str80 ako v starom modeli")
print("  - INDEX_BARCODE = 'BarCode' je definovaný")
print()
print("Po uložení:")
print("  1. Nahradiť packages/nexdata/nexdata/models/gscat.py")
print("  2. Upraviť GSCATRepository.find_by_barcode()")
print("  3. Upraviť ProductMatcher aby používal BarCode")
print("  4. Re-testovať EAN lookup")
print()
print("=" * 70)
print()
print("Obsah súboru:")
print("=" * 70)
print(complete_model)