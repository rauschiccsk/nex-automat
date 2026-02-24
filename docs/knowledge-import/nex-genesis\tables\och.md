# OCH - Hlavičky odberateľských zákaziek

## Kľúčové slová / Aliases

OCH, OCH.BTR, objednávky prijaté hlavičky, orders received header, zákaznícke objednávky

## Popis

Hlavičková tabuľka odberateľských objednávok (zákaziek). Obsahuje údaje o odberateľovi, termínoch, hodnotách dokladu a stave spracovania.

## Btrieve súbor

`OCHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCHyynnn.BTR`

## Štruktúra polí (117 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo (číslo zákazníka) |
| DocDate | DateType | 4 | Dátum prijatia objednávky |
| Year | Str2 | 3 | Rok dokladu |
| StkNum | word | 2 | Číslo priradeného skladu |
| ItmQnt | word | 2 | Počet položiek |

### Termíny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ReqDate | DateType | 4 | Požadovaný termín dodania |
| ConfDate | DateType | 4 | Potvrdený termín dodania |
| ExpDate | DateType | 4 | Termín expedície |
| ShpDate | DateType | 4 | Dátum odoslania |

### Partner (odberateľ)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| PaName | Str30 | 31 | Pracovný názov odberateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu |
| RegName | Str60 | 61 | Registrovaný názov |
| RegIno | Str15 | 16 | IČO |
| RegTin | Str15 | 16 | DIČ |
| RegVin | Str15 | 16 | IČ DPH |
| RegAddr | Str30 | 31 | Adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Dodacia adresa (prevádzka)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WpaCode | word | 2 | Číslo prevádzky |
| WpaName | Str60 | 61 | Názov prevádzky |
| WpaAddr | Str30 | 31 | Adresa prevádzky |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Doprava

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TrsCod | Str1 | 2 | Kód dopravy (C/V/E/O) |
| TrsCode | Str3 | 4 | Kód spôsobu dopravy |
| TrsName | Str20 | 21 | Názov spôsobu dopravy |
| TrsLine | Str3 | 4 | Smer rozvozu |

### Platobné podmienky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCod | Str1 | 2 | Forma úhrady (H/K/B/D/O) |
| PayCode | Str3 | 4 | Kód formy úhrady |
| PayName | Str20 | 21 | Názov formy úhrady |
| PlsNum | word | 2 | Číslo cenníka |
| DscPrc | double | 8 | Zľava % |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH 1 |
| VatPrc2 | byte | 1 | Sadzba DPH 2 |
| VatPrc3 | byte | 1 | Sadzba DPH 3 |
| VatPrc4 | byte | 1 | Sadzba DPH 4 |
| VatPrc5 | byte | 1 | Sadzba DPH 5 |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Kód účtovnej meny |
| AcDValue | double | 8 | PC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcRndVal | double | 8 | Zaokrúhlenie |
| AcCValue | double | 8 | PC bez DPH |
| AcVatVal | double | 8 | Hodnota DPH |
| AcEValue | double | 8 | PC s DPH |
| AcCValue1-5 | double | 8 | PC bez DPH podľa DPH sadzby |
| AcEValue1-5 | double | 8 | PC s DPH podľa DPH sadzby |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Kód vyúčtovacej meny |
| FgCourse | double | 8 | Kurz |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgRndVal | double | 8 | Zaokrúhlenie |
| FgCValue | double | 8 | PC bez DPH |
| FgVatVal | double | 8 | Hodnota DPH |
| FgEValue | double | 8 | PC s DPH |
| FgCValue1-5 | double | 8 | PC bez DPH podľa DPH sadzby |
| FgEValue1-5 | double | 8 | PC s DPH podľa DPH sadzby |

### Zálohy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDepVal | double | 8 | Záloha v účtovnej mene |
| FgDepVal | double | 8 | Záloha vo vyúčtovacej mene |
| DepPrc | double | 8 | Percento zálohy |

### Stavy dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | Str1 | 2 | Uzamknutie (L=locked, R=creating) |
| DstCls | Str1 | 2 | Ukončenosť (C=closed) |
| DstMod | Str1 | 2 | Modifikácia (M=modified) |
| DstExd | Str1 | 2 | Expedícia (E=expedícia) |
| DstPrn | byte | 1 | Vytlačené |
| PrnCnt | byte | 1 | Počet vytlačených kópií |

### Párovanie s inými dokladmi

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OsdNum | Str12 | 13 | Číslo dodávateľskej objednávky |
| TcdNum | Str12 | 13 | Číslo odberateľského DL |
| IcdNum | Str12 | 13 | Číslo odberateľskej faktúry |
| PcdNum | Str12 | 13 | Číslo zálohovej faktúry |
| CpdNum | Str12 | 13 | Číslo pokladničného dokladu |
| ExdNum | Str12 | 13 | Číslo expedičného príkazu |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania |
| SndNum | word | 2 | Poradové číslo odoslania |
| SndStat | Str1 | 2 | Stav prenosu (S/O/E) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (20)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Case-insensitive, Duplicit |
| 2 | ExtNum | ExtNum | Case-insensitive, Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | StkNum | StkNum | Duplicit |
| 5 | PaCode | PaCode | Duplicit |
| 6 | _PaName | PaName | Case-insensitive, Duplicit |
| 7 | ReqDate | ReqDate | Duplicit |
| 8 | ConfDate | ConfDate | Duplicit |
| 9 | DstLck | DstLck | Duplicit |
| 10 | DstCls | DstCls | Duplicit |
| 11 | DstExd | DstExd | Duplicit |
| 12 | TrsCod | TrsCod | Duplicit |
| 13 | TrsLine | TrsLine | Duplicit |
| 14 | Sended | Sended | Duplicit |
| 15 | SndStat | SndStat | Duplicit |
| 16 | OsdNum | OsdNum | Duplicit |
| 17 | TcdNum | TcdNum | Duplicit |
| 18 | IcdNum | IcdNum | Duplicit |
| 19 | ExdNum | ExdNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |
| PlsNum | PLSLST.PlsNum | Cenník |
| TrsLine | TRSLST.TrsCode | Smer rozvozu |
| TcdNum | TCH.DocNum | Odberateľský DL |
| IcdNum | ICH.DocNum | Odberateľská faktúra |
| OsdNum | OSH.DocNum | Dodávateľská objednávka |

## Stavy zákazky

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Odomknutý |
| L | Uzamknutý |
| R | Práve sa vytvára |

### DstCls (Ukončenosť)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Aktívna |
| C | Ukončená |

### DstMod (Modifikácia)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Bez zmien |
| M | Modifikovaná - treba informovať zákazníka |

### DstExd (Expedícia)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nepripravuje sa |
| E | Prebieha expedícia |

## Doprava (TrsCod)

| Hodnota | Popis |
|---------|-------|
| C | Osobný odber (Customer) |
| V | Vlastný rozvoz |
| E | Externý prepravca |
| O | Iná forma dodávky |

## Forma úhrady (PayCod)

| Hodnota | Popis |
|---------|-------|
| H | Hotovosť |
| K | Platobná karta |
| B | Bankový prevod |
| D | Dobierka |
| O | Kompenzácia |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
