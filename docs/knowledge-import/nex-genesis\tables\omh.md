# OMH - Hlavičky interných skladových výdajok

## Kľúčové slová / Aliases

OMH, OMH.BTR, interné výdaje hlavičky, internal issue header, výdajky, interný pohyb

## Popis

Hlavičková tabuľka interných skladových výdajok. Obsahuje základné údaje o doklade, súčty hodnôt a stavy spracovania.

## Btrieve súbor

`OMHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OMHyynnn.BTR`

## Štruktúra polí (76 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Poradové číslo skladovej výdajky |
| DocNum | Str12 | 13 | Interné číslo skladovej výdajky - **PRIMARY KEY** |
| DocDate | DateType | 4 | Dátum vystavenia |
| StkNum | word | 2 | Číslo priradeného skladu |
| SmCode | word | 2 | Číslo skladového pohybu |
| SmName | Str17 | 18 | Názov skladového pohybu |

### Nadväznosti

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Interné číslo zákazky |
| ImdNum | Str20 | 21 | Číslo automaticky vystavenej príjemky |
| TrgStk | longint | 4 | Cieľový sklad (0=definitívny výdaj) |
| ConStk | word | 2 | Číslo protiskladu príjmu/výdaja |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek dokladu |
| PlsNum | word | 2 | Číslo predajného cenníka |

### DPH skupiny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | double | 8 | Sadzba DPH skupiny č.1 |
| VatPrc2 | double | 8 | Sadzba DPH skupiny č.2 |
| VatPrc3 | double | 8 | Sadzba DPH skupiny č.3 |
| VatPrc4 | double | 8 | Sadzba DPH skupiny č.4 |
| VatPrc5 | double | 8 | Sadzba DPH skupiny č.5 |

### Hodnoty v NC bez DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue1 | double | 8 | Hodnota v NC bez DPH - skupina 1 |
| CValue2 | double | 8 | Hodnota v NC bez DPH - skupina 2 |
| CValue3 | double | 8 | Hodnota v NC bez DPH - skupina 3 |
| CValue4 | double | 8 | Hodnota v NC bez DPH - skupina 4 |
| CValue5 | double | 8 | Hodnota v NC bez DPH - skupina 5 |
| CValue | double | 8 | Hodnota v NC bez DPH - spolu |

### DPH z NC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal1 | double | 8 | DPH z NC - skupina 1 |
| VatVal2 | double | 8 | DPH z NC - skupina 2 |
| VatVal3 | double | 8 | DPH z NC - skupina 3 |
| VatVal | double | 8 | DPH z NC - spolu |

### Hodnoty v NC s DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| EValue1 | double | 8 | Hodnota v NC s DPH - skupina 1 |
| EValue2 | double | 8 | Hodnota v NC s DPH - skupina 2 |
| EValue3 | double | 8 | Hodnota v NC s DPH - skupina 3 |
| EValue4 | double | 8 | Hodnota v NC s DPH - skupina 4 |
| EValue5 | double | 8 | Hodnota v NC s DPH - skupina 5 |
| EValue | double | 8 | Hodnota v NC s DPH - spolu |

### Hodnoty v PC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CAccSnt | Str3 | 4 | Syntetický účet MD |
| CAccAnl | Str6 | 7 | Analytický účet MD |
| DAccSnt | Str3 | 4 | Syntetický účet DAL |
| DAccAnl | Str6 | 7 | Analytický účet DAL |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | byte | 1 | Uzatvorenie (1=uzatvorený) |
| DstAcc | Str1 | 2 | Zaúčtovanie (A=zaúčtovaný) |
| DstStk | Str1 | 2 | Stav skladu |
| ImdSnd | Str1 | 2 | Medziprevádzkové odoslanie (O=odoslaný) |
| SndStat | Str1 | 2 | Stav internetového prenosu (S/O/E) |
| Sended | byte | 1 | Príznak odoslania zmien |

### Šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis dokladu |
| PrnCnt | byte | 1 | Počet vytlačených kópií |

### Účtovanie audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccUser | Str8 | 9 | Používateľ zaúčtovania |
| AccDate | DateType | 4 | Dátum zaúčtovania |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (13)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | DocDate | DocDate | Duplicit |
| 3 | SmCode | SmCode | Duplicit |
| 4 | EValue | EValue | Duplicit |
| 5 | BValue | BValue | Duplicit |
| 6 | CValue | CValue | Duplicit |
| 7 | AValue | AValue | Duplicit |
| 8 | ImdNum | ImdNum | Duplicit |
| 9 | Describe | Describe | Duplicit, Case insensitive |
| 10 | OcdNum | OcdNum | Duplicit |
| 11 | Sended | Sended | Duplicit |
| 12 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| SmCode | SMLST.SmCode | Skladový pohyb |
| OcdNum | OCH.DocNum | Zákazka |
| TrgStk | STKLST.StkNum | Cieľový sklad |
| ImdNum | IMH.DocNum | Vytvorená príjemka |

## Použitie

- Evidencia interných výdajov
- Likvidácie a spotreby
- Medziskladové presuny
- Inventúrne manká

## Business pravidlá

- TrgStk=0 znamená definitívny výdaj (tovar opúšťa systém)
- TrgStk>0 znamená medziskladový presun (automatická príjemka)
- DstLck=1 znemožňuje ďalšie úpravy
- Pri mazaní sa položky vracajú na sklad

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
