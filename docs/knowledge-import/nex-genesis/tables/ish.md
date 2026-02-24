# ISH - Hlavičky dodávateľských faktúr

## Kľúčové slová / Aliases

ISH, ISH.BTR, príjemky hlavičky, goods receipt header, príjem tovaru, bevételezés

## Popis

Hlavná tabuľka dodávateľských faktúr (záväzkov). Obsahuje všetky údaje o prijatých faktúrach vrátane partnera, hodnôt, úhrad a stavov spracovania.

## Btrieve súbor

`ISHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISHyynnn.BTR`

## Štruktúra polí (124 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo faktúry |
| DocNum | Str12 | 13 | Interné číslo faktúry |
| ExtNum | Str12 | 13 | Externé číslo faktúry (od dodávateľa) |
| IncNum | Str32 | 33 | Číslo faktúry od dodávateľa |
| Year | Str2 | 3 | Rok dokladu |

### Dátumy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum prijatia faktúry |
| SndDate | DateType | 4 | Dátum vystavenia faktúry |
| ExpDate | DateType | 4 | Dátum splatnosti |
| VatDate | DateType | 4 | Dátum DPH (strana príjemcu) |
| PayDate | DateType | 4 | Dátum poslednej úhrady |
| TaxDate | DateType | 4 | Dátum zdaniteľného plnenia |
| AccDate | DateType | 4 | Dátum zaúčtovania |
| PmqDate | DateType | 4 | Dátum prevodného príkazu |
| WrnDate | DateType | 4 | Dátum upomienky |

### Dodávateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód dodávateľa |
| PaName | Str30 | 31 | Pracovný názov dodávateľa |
| _PaName | Str30 | 31 | Vyhľadávací názov |
| RegName | Str60 | 61 | Registrovaný názov firmy |
| RegIno | Str15 | 16 | IČO partnera |
| RegTin | Str15 | 16 | DIČ partnera |
| RegVin | Str15 | 16 | IČ DPH |
| RegAddr | Str30 | 31 | Registrovaná adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Prevádzka partnera

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpaCode | longint | 4 | Číselný kód príjemcu tovaru |
| WpaCode | word | 2 | Číslo prevádzky partnera |
| WpaName | Str60 | 61 | Názov prevádzky |
| WpaAddr | Str30 | 31 | Adresa prevádzky |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Platobné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Skratka formy úhrady |
| PayName | Str20 | 21 | Názov formy úhrady |
| ContoNum | Str30 | 31 | Bankový účet partnera |
| BankCode | Str15 | 16 | Kód banky |
| BankSeat | Str30 | 31 | Sídlo banky |
| IbanCode | Str34 | 35 | IBAN kód |
| SwftCode | Str20 | 21 | SWIFT kód |
| CsyCode | Str4 | 5 | Konštantný symbol |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| StkNum | word | 2 | Číslo skladu |
| PlsNum | word | 2 | Číslo cenníka |
| TrsCode | Str3 | 4 | Kód dopravy |
| TrsName | Str20 | 21 | Názov dopravy |
| DscPrc | double | 8 | Zľava % |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH skupiny 1 |
| VatPrc2 | byte | 1 | Sadzba DPH skupiny 2 |
| VatPrc3 | byte | 1 | Sadzba DPH skupiny 3 |
| VatPrc4 | byte | 1 | Sadzba DPH skupiny 4 |
| VatPrc5 | byte | 1 | Sadzba DPH skupiny 5 |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Názov účtovnej meny |
| AcDValue | double | 8 | NC pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcCValue | double | 8 | NC bez DPH |
| AcVatVal | double | 8 | Hodnota DPH |
| AcEValue | double | 8 | NC s DPH |
| AcCValue1-5 | double | 8×5 | NC bez DPH podľa DPH skupín |
| AcEValue1-5 | double | 8×5 | NC s DPH podľa DPH skupín |
| AcAValue | double | 8 | PC bez DPH |
| AcBValue | double | 8 | PC s DPH |
| AcPrvPay | double | 8 | Úhrada z minulých rokov |
| AcPayVal | double | 8 | Uhradená čiastka |
| AcEndVal | double | 8 | Zostatok k úhrade |

### Hodnoty v mene faktúry (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Mena faktúry |
| FgCourse | double | 8 | Kurz meny |
| FgDValue | double | 8 | NC pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgCValue | double | 8 | NC bez DPH |
| FgVatVal | double | 8 | Hodnota DPH |
| FgEValue | double | 8 | NC s DPH |
| FgCValue1-5 | double | 8×5 | NC bez DPH podľa DPH skupín |
| FgEValue1-5 | double | 8×5 | NC s DPH podľa DPH skupín |
| FgPrvPay | double | 8 | Úhrada z minulých rokov |
| FgPayVal | double | 8 | Uhradená čiastka |
| FgEndVal | double | 8 | Zostatok k úhrade |

### Koncoročné prekurzovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| EyCourse | double | 8 | Koncoročný kurz |
| EyCrdVal | double | 8 | Kurzový rozdiel |
| CctVal | double | 8 | Prenesená daňová povinnosť |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocSnt | Str3 | 4 | Syntetický účet |
| DocAnl | Str6 | 7 | Analytický účet |

### Párovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsdNum | Str15 | 16 | Číslo vypárovaného DDL |
| IodNum | Str12 | 13 | Číslo pôvodnej FA (pre dobropis) |
| IoeNum | Str32 | 33 | Externé číslo pôvodnej FA |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatDoc | byte | 1 | Daňový doklad (1=áno) |
| VatCls | byte | 1 | Poradové číslo uzávierky DPH |
| DocSpc | byte | 1 | Špecifikácia dokladu |
| PrnCnt | byte | 1 | Počet tlačených kópií |
| ItmQnt | word | 2 | Počet položiek |
| DstPair | Str1 | 2 | Stav párovania (N/Q) |
| DstLck | byte | 1 | Uzamknutie (0/1) |
| DstCls | byte | 1 | Ukončenosť (0/1) |
| DstAcc | Str1 | 2 | Zaúčtovanie (A) |
| DstLiq | Str1 | 2 | Likvidácia (L) |
| Sended | byte | 1 | Odoslanie zmien |
| SndStat | Str1 | 2 | Stav prenosu |
| WrnNum | byte | 1 | Číslo upomienky |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (15)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Primary Key |
| 1 | DocNum | DocNum | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | ExpDate | ExpDate | Duplicit |
| 5 | _PaName | PaName | Case-insensitive, Duplicit |
| 6 | AcDvzName | AcDvzName | Case-insensitive, Duplicit |
| 7 | FgDvzName | FgDvzName | Case-insensitive, Duplicit |
| 8 | AcEValue | AcEValue | Duplicit |
| 9 | FgEValue | FgEValue | Duplicit |
| 10 | DstAcc | DstAcc | Duplicit |
| 11 | PaCode | PaCode | Duplicit |
| 12 | DstLiq | DstLiq | Duplicit |
| 13 | IodNum | IodNum | Duplicit |
| 14 | IncNum | IncNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Dodávateľ |
| StkNum | STKLST.StkNum | Sklad |
| PayCode | PAYLST.PayCode | Forma úhrady |
| TrsCode | TRSLST.TrsCode | Spôsob dopravy |
| IodNum | ISH.DocNum | Pôvodná faktúra (pre dobropis) |

## Business pravidlá

- FgEndVal <> 0 = faktúra nie je uhradená (červené zobrazenie)
- VatCls > 0 = faktúra je v DPH uzávierke (nelze editovať)
- DstLck = 1 = doklad je uzamknutý
- DstAcc = 'A' = doklad je zaúčtovaný

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
