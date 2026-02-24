# IMH - Hlavičky interných príjemok

## Kľúčové slová / Aliases

IMH, IMH.BTR, interné príjmy hlavičky, internal receipt header, medzikladové presuny

## Popis

Tabuľka hlavičiek interných skladových príjemok. Obsahuje základné údaje o príjemke, finančných sumách a stave spracovania.

## Btrieve súbor

`IMHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMHyynnn.BTR`

## Štruktúra polí (76 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo príjemky |
| DocNum | Str12 | 13 | Interné číslo príjemky - **PRIMARY KEY** |
| Year | Str2 | 3 | Rok dokladu |
| DocDate | DateType | 4 | Dátum vystavenia príjemky |

### Sklad a pohyb

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo priradeného skladu |
| SmCode | word | 2 | Číslo skladového pohybu |
| SmName | Str17 | 18 | Názov skladového pohybu |
| PlsNum | word | 2 | Číslo cenníka |
| ConStk | word | 2 | Číslo protiskladu (medziskladový presun) |

### Väzby na iné doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo zdrojovej zákazky |
| OmdNum | Str20 | 21 | Číslo zdrojovej výdajky |

### Šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | double | 8 | Sadzba DPH skupiny č.1 |
| VatPrc2 | double | 8 | Sadzba DPH skupiny č.2 |
| VatPrc3 | double | 8 | Sadzba DPH skupiny č.3 |
| VatPrc4 | double | 8 | Sadzba DPH skupiny č.4 |
| VatPrc5 | double | 8 | Sadzba DPH skupiny č.5 |

### Hodnoty v NC bez DPH (podľa skupín DPH)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue1 | double | 8 | NC bez DPH - skupina 1 |
| CValue2 | double | 8 | NC bez DPH - skupina 2 |
| CValue3 | double | 8 | NC bez DPH - skupina 3 |
| CValue4 | double | 8 | NC bez DPH - skupina 4 |
| CValue5 | double | 8 | NC bez DPH - skupina 5 |
| CValue | double | 8 | NC bez DPH - celkom |

### Hodnoty DPH (podľa skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal1 | double | 8 | DPH - skupina 1 |
| VatVal2 | double | 8 | DPH - skupina 2 |
| VatVal3 | double | 8 | DPH - skupina 3 |
| VatVal | double | 8 | DPH - celkom |

### Hodnoty v NC s DPH (podľa skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| EValue1 | double | 8 | NC s DPH - skupina 1 |
| EValue2 | double | 8 | NC s DPH - skupina 2 |
| EValue3 | double | 8 | NC s DPH - skupina 3 |
| EValue4 | double | 8 | NC s DPH - skupina 4 |
| EValue5 | double | 8 | NC s DPH - skupina 5 |
| EValue | double | 8 | NC s DPH - celkom |

### Hodnoty v PC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue | double | 8 | PC bez DPH |
| BValue | double | 8 | PC s DPH |
| RndVal | double | 8 | Hodnota zaokrúhlenia |

### Ostatné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek |
| Describe | Str30 | 31 | Textový popis dokladu |
| PrnCnt | byte | 1 | Počet vytlačených kópií |

### Stavy dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstStk | Str1 | 2 | Stav skladu (N/S) |
| DstLck | byte | 1 | Uzamknutie dokladu |
| DstAcc | Str1 | 2 | Stav zaúčtovania |
| SndStat | Str1 | 2 | Stav internetového prenosu |
| Sended | byte | 1 | Príznak odoslania zmien |
| AwdSta | byte | 1 | Tovar na ceste |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccUser | Str8 | 9 | Používateľ zaúčtovania |
| AccDate | DateType | 4 | Dátum zaúčtovania |
| CAccSnt | Str3 | 4 | Účet MD - syntetická časť |
| CAccAnl | Str6 | 7 | Účet MD - analytická časť |
| DAccSnt | Str3 | 4 | Účet DAL - syntetická časť |
| DAccAnl | Str6 | 7 | Účet DAL - analytická časť |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (15)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | DocDate | DoDate | Duplicit |
| 3 | SmCode | SmCode | Duplicit |
| 4 | EValue | EValue | Duplicit |
| 5 | BValue | BValue | Duplicit |
| 6 | CValue | CValue | Duplicit |
| 7 | AValue | AValue | Duplicit |
| 8 | OmdNum | OmdNum | Duplicit |
| 9 | OcdNum | OcdNum | Duplicit |
| 10 | Describe | Describe | Duplicit, Case insensitive |
| 11 | DstAcc | DstAcc | Duplicit |
| 12 | DstStk | DstStk | Duplicit |
| 13 | Sended | Sended | Duplicit |
| 14 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Cieľový sklad |
| SmCode | SMLST.SmCode | Typ skladového pohybu |
| OcdNum | OCH.DocNum | Zdrojová zákazka |
| ConStk | STKLST.StkNum | Protisklad |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
