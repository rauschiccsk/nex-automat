# ICH - Hlavičky odberateľských faktúr

## Kľúčové slová / Aliases

ICH, ICH.BTR, faktúry odberateľské hlavičky, customer invoices header, predajné faktúry, számlák

## Popis

Hlavičková tabuľka odberateľských faktúr (pohľadávok). Obsahuje údaje o odberateľovi, hodnotách dokladu, úhradách, splatnosti a stave spracovania.

## Btrieve súbor

`ICHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICHyynnn.BTR`

## Štruktúra polí (149 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo faktúry - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo (variabilný symbol) |
| OcdNum | Str12 | 13 | Číslo zákazky |
| Year | Str2 | 3 | Rok dokladu |

### Dátumy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum vystavenia faktúry |
| SndDate | DateType | 4 | Dátum odoslania faktúry |
| ExpDate | DateType | 4 | Dátum splatnosti |
| VatDate | DateType | 4 | Dátum dodania (zdaniteľného plnenia) |
| PayDate | DateType | 4 | Dátum poslednej úhrady |
| EmlDate | DateType | 4 | Dátum odoslania emailom |

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

### Príjemca (prevádzka)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpaCode | longint | 4 | Kód príjemcu tovaru |
| WpaCode | word | 2 | Číslo prevádzky |
| WpaName | Str60 | 61 | Názov prevádzky |
| WpaAddr | Str30 | 31 | Adresa prevádzky |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Platobné podmienky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Kód formy úhrady |
| PayName | Str19 | 20 | Názov formy úhrady |
| PayMode | byte | 1 | Spôsob úhrady faktúry |
| CsyCode | Str4 | 5 | Konštantný symbol |
| MyConto | Str30 | 31 | Bankový účet dodávateľa |

### Factoring

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcFacDay | word | 2 | Factoringová splatnosť (dni) |
| IcFacPrc | double | 8 | Percentuálne zvýšenie cien pri factoringu |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH 1 |
| VatPrc2 | byte | 1 | Sadzba DPH 2 |
| VatPrc3 | byte | 1 | Sadzba DPH 3 |
| VatPrc4 | byte | 1 | Sadzba DPH 4 |
| VatPrc5 | byte | 1 | Sadzba DPH 5 |
| VatDoc | byte | 1 | Daňový doklad (1=DPH) |
| VatCls | byte | 1 | Číslo uzávierky DPH |
| VatDis | byte | 1 | Vylúčiť z evidencie DPH (1=áno) |

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
| AcPValue | double | 8 | Záloha |
| AcPrvPay | double | 8 | Úhrada z minulých rokov |
| AcPayVal | double | 8 | Uhradená čiastka |
| AcEndVal | double | 8 | Zostatok k úhrade |
| AcAValue1-5 | double | 8 | PC bez DPH podľa sadzby |
| AcBValue1-5 | double | 8 | PC s DPH podľa sadzby |
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
| FgPValue | double | 8 | Záloha |
| FgPrvPay | double | 8 | Úhrada z minulých rokov |
| FgPayVal | double | 8 | Uhradená čiastka |
| FgEndVal | double | 8 | Zostatok k úhrade |
| FgDBValue | double | 8 | PC s DPH pred zľavou |
| FgDscBVal | double | 8 | Hodnota zľavy s DPH |
| FgHValue | double | 8 | PC s DPH pred zľavou |
| FgHdsVal | double | 8 | Hlavičková zľava |
| FgRndVat | double | 8 | Zaokrúhlenie DPH |
| FgRndVal | double | 8 | Zaokrúhlenie dokladu |
| FgAValue1-5 | double | 8 | PC bez DPH podľa sadzby |
| FgBValue1-5 | double | 8 | PC s DPH podľa sadzby |

### Koncoročné prekurzovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| EyCourse | double | 8 | Koncoročný kurz |
| EyCrdVal | double | 8 | Kurzový rozdiel |

### Platba kartou

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrcVal | double | 8 | Úhrada platobnou kartou |
| CrCard | Str20 | 21 | Číslo platobnej karty |

### Párovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TcdNum | Str15 | 16 | Číslo dodacieho listu |
| IodNum | Str12 | 13 | Interné číslo pôvodnej FA (opravný doklad) |
| IoeNum | Str12 | 13 | Externé číslo pôvodnej FA |

### Upomienky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WrnNum | byte | 1 | Číslo upomienky |
| WrnDate | DateType | 4 | Dátum vystavenia upomienky |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocSnt | Str3 | 4 | Syntetický účet faktúry |
| DocAnl | Str6 | 7 | Analytický účet faktúry |
| DstAcc | Str1 | 2 | Zaúčtovanie (A) |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstPair | Str1 | 2 | Párovanie (N/Q) |
| DstPay | byte | 1 | Úhrada (0/1) |
| DstLck | byte | 1 | Uzamknutie (0/1) |
| DstCls | byte | 1 | Ukončenie (0/1) |
| DocSpc | byte | 1 | Špecifikácia dokladu |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| ItmQnt | word | 2 | Počet položiek |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzky |
| StkNum | word | 2 | Číslo skladu |
| TrsCode | Str3 | 4 | Kód dopravy |
| TrsName | Str20 | 21 | Názov dopravy |
| RspName | Str20 | 21 | Meno vystaviteľa |
| PlsNum | word | 2 | Číslo cenníka |
| PrfPrc | double | 8 | Percento zálohy |
| DscPrc | double | 8 | Zľava % |
| HdsPrc | double | 8 | Hlavičková zľava % |
| RcvName | Str30 | 31 | Meno príjemcu |
| DlrCode | word | 2 | Kód obchodného zástupcu |
| CusCard | Str20 | 21 | Číslo zákazníckej karty |
| SteCode | word | 2 | Kód skladníka |
| SpMark | Str10 | 11 | Všeobecné označenie |
| BonNum | byte | 1 | Číslo bonusovej akcie |
| CsgNum | Str15 | 16 | Číslo zásielky |
| PrjCode | Str12 | 13 | Kód projektu |
| Volume | double | 8 | Objem (m³) |
| Weight | double | 8 | Váha (kg) |
| QntSum | double | 8 | Kumulatívne množstvo položiek |
| CctVal | double | 8 | Prenesená daňová povinnosť |

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
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (23)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | PaCode | PaCode | Duplicit |
| 5 | _PaName | PaName | Case-insensitive, Duplicit |
| 6 | AcDvzName | AcDvzName | Case-insensitive, Duplicit |
| 7 | FgDvzName | FgDvzName | Case-insensitive, Duplicit |
| 8 | OcdNum | OcdNum | Duplicit |
| 9 | SndDate | SndDate | Duplicit |
| 10 | ExpDate | ExpDate | Duplicit |
| 11 | DstPair | DstPair | Duplicit |
| 12 | PaCode, DstPay | PaDp | Duplicit |
| 13 | AcBValue | AcBValue | Duplicit |
| 14 | FgBValue | FgBValue | Duplicit |
| 15 | FgEndVal | FgEndVal | Duplicit |
| 16 | DlrCode | DlrCode | Duplicit |
| 17 | Sended | Sended | Duplicit |
| 18 | CrCard | CrCard | Duplicit |
| 19 | DstAcc | DstAcc | Duplicit |
| 20 | SpMark | SpMark | Duplicit |
| 21 | PrjCode | PrjCode | Duplicit |
| 22 | IodNum | IodNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |
| TcdNum | TCH.DocNum | Dodací list |
| OcdNum | OCH.DocNum | Zákazka |
| PlsNum | PLSLST.PlsNum | Cenník |
| IodNum | ICH.DocNum | Pôvodná faktúra (dobropis) |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
