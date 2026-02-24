# TSH - Hlavičky dodávateľských dodacích listov

## Kľúčové slová / Aliases

TSH, TSH.BTR, pokladničné doklady hlavičky, cash register header, pokladňa, tržby, predaj, sales

## Popis

Hlavičková tabuľka dodávateľských dodacích listov (DDL). Obsahuje údaje o dodávateľovi, dodacej adrese, hodnotách dokladu a stave spracovania.

## Btrieve súbor

`TSHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TSHyynnn.BTR`

## Štruktúra polí (128 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo (číslo dodávateľa) |
| DocDate | DateType | 4 | Dátum vystavenia |
| Year | Str2 | 3 | Rok dokladu |
| StkNum | word | 2 | Číslo priradeného skladu |
| ItmQnt | word | 2 | Počet položiek |

### Partner (dodávateľ)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód dodávateľa |
| PaName | Str30 | 31 | Pracovný názov dodávateľa |
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

### Platobné a dopravné podmienky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Kód formy úhrady |
| PayName | Str20 | 21 | Názov formy úhrady |
| TrsCode | Str3 | 4 | Kód spôsobu dopravy |
| TrsName | Str20 | 21 | Názov spôsobu dopravy |
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
| AcZValue | double | 8 | Colné náklady |
| AcTValue | double | 8 | Dopravné náklady |
| AcOValue | double | 8 | Ostatné obstarávacie náklady |
| AcSValue | double | 8 | Obstarávacia cena (s NSO) |
| AcDValue | double | 8 | NC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcRndVal | double | 8 | Zaokrúhlenie |
| AcCValue | double | 8 | NC bez DPH (bez NSO) |
| AcVatVal | double | 8 | Hodnota DPH |
| AcEValue | double | 8 | NC s DPH |
| AcCValue1-5 | double | 8 | NC bez DPH podľa DPH sadzby |
| AcEValue1-5 | double | 8 | NC s DPH podľa DPH sadzby |
| AcAValue | double | 8 | PC bez DPH |
| AcBValue | double | 8 | PC s DPH |
| AcPrfVal | double | 8 | Obchodná marža |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Kód vyúčtovacej meny |
| FgCourse | double | 8 | Kurz |
| FgDValue | double | 8 | NC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgRndVal | double | 8 | Zaokrúhlenie |
| FgCValue | double | 8 | NC bez DPH |
| FgVatVal | double | 8 | Hodnota DPH |
| FgEValue | double | 8 | NC s DPH |
| FgCValue1-5 | double | 8 | NC bez DPH podľa DPH sadzby |
| FgEValue1-5 | double | 8 | NC s DPH podľa DPH sadzby |
| FgCsdVal1-5 | double | 8 | Hotovostná úhrada podľa DPH |

### Párovanie s inými dokladmi

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo odberateľskej zákazky |
| CsdNum | Str12 | 13 | Číslo pokladničného dokladu |
| IsdNum | Str15 | 16 | Číslo dodávateľskej faktúry |
| TcdNum | Str12 | 13 | Číslo ODL (refakturácia) |
| IcdNum | Str12 | 13 | Číslo OF (refakturácia) |
| PkdNum | Str12 | 13 | Číslo prebaľovacieho dokladu |

### Čísla súvisiacich faktúr

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ZIseNum | Str12 | 13 | VS faktúry za clo |
| TIseNum | Str12 | 13 | VS faktúry za dopravu |
| OIseNum | Str12 | 13 | VS faktúry za ostatné |
| GIseNum | Str12 | 13 | VS faktúry za tovar |
| ZIsdNum | Str12 | 13 | Interné číslo FA za clo |
| TIsdNum | Str12 | 13 | Interné číslo FA za dopravu |
| OIsdNum | Str12 | 13 | Interné číslo FA za ostatné |
| GIsdNum | Str12 | 13 | Interné číslo FA za tovar |

### Stavy a príznaky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatDoc | byte | 1 | Daňový doklad (1=áno) |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| SmCode | word | 2 | Kód skladového pohybu |
| DstStk | Str1 | 2 | Príjem na sklad (N/S) |
| DstPair | Str1 | 2 | Vypárovanie (N/Q/C) |
| DstLck | byte | 1 | Uzamknutie (0/1) |
| DstCls | byte | 1 | Ukončenie (0/1) |
| DstAcc | Str1 | 2 | Zaúčtovanie (A) |
| DstCor | Str1 | 2 | Potvrdenie správnosti |
| DstLiq | Str1 | 2 | Likvidácia (L) |
| Sended | byte | 1 | Odoslanie zmien (0/1) |
| SndNum | word | 2 | Poradové číslo odoslania |
| SndStat | Str1 | 2 | Stav prenosu (S/O/E) |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CAccSnt | Str3 | 4 | Syntetický účet MD |
| CAccAnl | Str8 | 9 | Analytický účet MD |
| DAccSnt | Str3 | 4 | Syntetický účet DAL |
| DAccAnl | Str8 | 9 | Analytický účet DAL |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SteCode | word | 2 | Kód skladníka |
| PrfPrc | double | 8 | Obchodná marža % |
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum šarže |

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
| 1 | DocNum | DocNum | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | StkNum | StkNum | Duplicit |
| 5 | PaCode | PaCode | Duplicit |
| 6 | _PaName | PaName | Case-insensitive, Duplicit |
| 7 | AcDvzName | AcDvzName | Case-insensitive, Duplicit |
| 8 | FgDvzName | FgDvzName | Case-insensitive, Duplicit |
| 9 | AcEValue | AcEValue | Duplicit |
| 10 | FgEValue | FgEValue | Duplicit |
| 11 | OcdNum | OcdNum | Duplicit |
| 12 | CsdNum | CsdNum | Duplicit |
| 13 | Sended | Sended | Duplicit |
| 14 | DstAcc | DstAcc | Duplicit |
| 15 | SndStat | SndStat | Duplicit |
| 16 | DstCor | DstCor | Duplicit |
| 17 | PaCode, DstPair | PcDp | Duplicit |
| 18 | DstLiq | DstLiq | Duplicit |
| 19 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Dodávateľ |
| StkNum | STKLST.StkNum | Sklad |
| SmCode | SMLST.SmCode | Typ pohybu |
| IsdNum | ISH.DocNum | Dodávateľská faktúra |
| OcdNum | OCH.DocNum | Zákazka |
| PlsNum | PLSLST.PlsNum | Cenník |

## Stav migrácie

- [x] BDF dokumentácia
- [x] Btrieve model (nexdata) - čiastočne
- [ ] PostgreSQL model
- [ ] API endpoint
