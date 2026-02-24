# TCH - Hlavičky odberateľských dodacích listov

## Kľúčové slová / Aliases

TCH, TCH.BTR, dodacie listy hlavičky, delivery notes header, výdaj, expedícia

## Popis

Hlavičková tabuľka odberateľských dodacích listov (ODL). Obsahuje údaje o odberateľovi, hodnotách dokladu, stave vyskladnenia a párovania s faktúrami.

## Btrieve súbor

`TCHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCHyynnn.BTR`

## Štruktúra polí (125 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo (číslo odberateľa) |
| OcdNum | Str12 | 13 | Číslo odberateľskej objednávky |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |
| DlvDate | DateType | 4 | Dátum platnosti dodávky (vyskladnenie) |
| Year | Str2 | 3 | Rok dokladu |
| StkNum | word | 2 | Číslo priradeného skladu |

### Partner (odberateľ)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| PaName | Str30 | 31 | Pracovný názov odberateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu |
| RegName | Str60 | 61 | Registrovaný názov firmy |
| RegIno | Str15 | 16 | IČO |
| RegTin | Str15 | 16 | DIČ |
| RegVin | Str15 | 16 | IČ DPH |
| RegAddr | Str30 | 31 | Adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Príjemca tovaru (prevádzka)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpaCode | longint | 4 | Kód príjemcu tovaru |
| WpaCode | word | 2 | Číslo prevádzky partnera |
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
| PlsNum | word | 2 | Číslo predajného cenníka |
| DscPrc | double | 8 | Percentuálna zľava |
| HdsPrc | double | 8 | Hlavičková zľava % |

### Factoring

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcFacDay | word | 2 | Factoringová splatnosť - počet dní |
| IcFacPrc | double | 8 | Percentuálne zvýšenie cien pri factoringu |

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
| AcDvzName | Str3 | 4 | Kód účtovnej meny (EUR) |
| AcCValue | double | 8 | NC bez DPH |
| AcDValue | double | 8 | PC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcAValue | double | 8 | PC bez DPH po zľave |
| AcVatVal | double | 8 | DPH |
| AcBValue | double | 8 | PC s DPH |
| AcAValue1-5 | double | 8 | PC bez DPH podľa sadzby DPH |
| AcBValue1-5 | double | 8 | PC s DPH podľa sadzby DPH |
| AcRndVat | double | 8 | Zaokrúhlenie DPH |
| AcRndVal | double | 8 | Zaokrúhlenie dokladu |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Kód vyúčtovacej meny |
| FgCourse | double | 8 | Kurz |
| FgCValue | double | 8 | NC bez DPH |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgAValue | double | 8 | PC bez DPH po zľave |
| FgVatVal | double | 8 | DPH |
| FgBValue | double | 8 | PC s DPH |
| FgDBValue | double | 8 | PC s DPH pred zľavou |
| FgDscBVal | double | 8 | Hodnota zľavy z PC s DPH |
| FgAValue1-5 | double | 8 | PC bez DPH podľa sadzby DPH |
| FgBValue1-5 | double | 8 | PC s DPH podľa sadzby DPH |
| FgHdsVal | double | 8 | Hlavičková zľava |
| FgRndVat | double | 8 | Zaokrúhlenie DPH |
| FgRndVal | double | 8 | Zaokrúhlenie dokladu |

### Logistické údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Volume | double | 8 | Objem tovaru (m³) |
| Weight | double | 8 | Váha tovaru (kg) |
| RcvName | Str30 | 31 | Meno osoby, ktorá prevzala tovar |
| RcvCode | Str10 | 11 | ID kód osoby (COP) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek |
| CntOut | word | 2 | Počet vyskladnených položiek |
| CntExp | word | 2 | Počet expedovaných položiek |

### Stavy a príznaky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatDoc | byte | 1 | Daňový doklad (1=DPH) |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| DstPair | Str1 | 2 | Párovanie (N/Q) |
| DstLck | byte | 1 | Uzamknutie (0/1) |
| DstCls | byte | 1 | Ukončenie (0/1) |
| DstAcc | Str1 | 2 | Zaúčtovanie (A) |
| SmCode | word | 2 | Kód skladového pohybu |

### Párovanie s faktúrou

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcdNum | Str14 | 15 | Číslo odberateľskej faktúry |

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
| RspName | Str20 | 21 | Meno osoby, ktorá vystavila doklad |
| DlrCode | word | 2 | Kód obchodného zástupcu |
| CusCard | Str20 | 21 | Číslo zákazníckej karty |
| SteCode | word | 2 | Kód skladníka |
| SpMark | Str10 | 11 | Všeobecné označenie |
| BonNum | byte | 1 | Číslo bonusovej akcie |
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| PrjCode | Str12 | 13 | Kód projektu |
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania (0/1) |
| SndNum | word | 2 | Poradové číslo odoslania |
| SndStat | Str1 | 2 | Stav prenosu (S/O/E) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (20)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit |
| 3 | OcdNum | OcdNum | Duplicit |
| 4 | DocDate | DocDate | Duplicit |
| 5 | StkNum | StkNum | Duplicit |
| 6 | PaCode | PaCode | Duplicit |
| 7 | _PaName | PaName | Duplicit |
| 8 | AcDvzName | AcDvzName | Case-insensitive, Duplicit |
| 9 | FgDvzName | FgDvzName | Case-insensitive, Duplicit |
| 10 | AcBValue | AcBValue | Duplicit |
| 11 | FgBValue | FgBValue | Duplicit |
| 12 | DstPair, PaCode | DpPc | Duplicit |
| 13 | DstCls | DstCls | Duplicit |
| 14 | Sended | Sended | Duplicit |
| 15 | DstAcc | DstAcc | Duplicit |
| 16 | SpMark | SpMark | Duplicit |
| 17 | PrjCode | PrjCode | Duplicit |
| 18 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |
| SmCode | SMLST.SmCode | Typ pohybu |
| OcdNum | OCH.DocNum | Zákazka |
| IcdNum | ICH.DocNum | Faktúra |
| PlsNum | PLSLST.PlsNum | Cenník |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
