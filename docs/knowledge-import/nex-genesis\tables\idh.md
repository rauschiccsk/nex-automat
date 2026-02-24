# IDH - Hlavičky interných účtovných dokladov

## Kľúčové slová / Aliases

IDH, IDH.BTR, hlavičky, interných, účtovných, dokladov

## Popis

Hlavičková tabuľka interných účtovných dokladov. Obsahuje súhrnné údaje o doklade vrátane účtov MD/Dal, hodnôt a DPH členenia.

## Btrieve súbor

`IDHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IDHyynnn.BTR`

## Štruktúra polí (49 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo dokladu |
| DocDate | DateType | 4 | Dátum založenia dokladu |

### Prevádzkové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| DocType | byte | 1 | Typ dokladu (0=bežný, 1=otvorenie, 2=uzatvorenie) |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód firmy - **FK → PAB.PaCode** |
| PaName | Str30 | 31 | Názov firmy |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu firmy |

### Popis

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Textový popis dokladu |
| _Describe | Str30 | 31 | Vyhľadávacie pole popisu |
| ConDoc | Str12 | 13 | Odkaz na iný doklad |

### Účtovanie - hlavné účty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CAccSnt | Str3 | 4 | Syntetický účet MD (Má dať) |
| CAccAnl | Str6 | 7 | Analytický účet MD |
| DAccSnt | Str3 | 4 | Syntetický účet Dal |
| DAccAnl | Str6 | 7 | Analytický účet Dal |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocVal | double | 8 | Hodnota dokladu |
| CredVal | double | 8 | Hodnota strany MD |
| DebVal | double | 8 | Hodnota strany Dal |
| ItmQnt | longint | 4 | Počet položiek dokladu |

### DPH členenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VtcSpc | byte | 1 | Špecifikácia DPH |
| VatCls | byte | 1 | Číslo uzávierky DPH |
| VatPrc1 | byte | 1 | Sadzba DPH skupiny 1 (%) |
| VatPrc2 | byte | 1 | Sadzba DPH skupiny 2 (%) |
| VatPrc3 | byte | 1 | Sadzba DPH skupiny 3 (%) |
| VatPrc4 | byte | 1 | Sadzba DPH skupiny 4 (%) |
| VatPrc5 | byte | 1 | Sadzba DPH skupiny 5 (%) |

### Hodnoty podľa DPH skupín

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcAValue1 | double | 8 | Hodnota bez DPH - skupina 1 |
| AcAValue2 | double | 8 | Hodnota bez DPH - skupina 2 |
| AcAValue3 | double | 8 | Hodnota bez DPH - skupina 3 |
| AcAValue4 | double | 8 | Hodnota bez DPH - skupina 4 |
| AcAValue5 | double | 8 | Hodnota bez DPH - skupina 5 |
| AcVatVal1 | double | 8 | DPH - skupina 1 |
| AcVatVal2 | double | 8 | DPH - skupina 2 |
| AcVatVal3 | double | 8 | DPH - skupina 3 |
| AcVatVal4 | double | 8 | DPH - skupina 4 |
| AcVatVal5 | double | 8 | DPH - skupina 5 |

### Celkové hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcAValue | double | 8 | Celková hodnota bez DPH |
| AcVatVal | double | 8 | Celková hodnota DPH |
| AcBValue | double | 8 | Celková hodnota s DPH |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | byte | 1 | Uzatvorenie (1=uzatvorený) |
| DstAcc | Str1 | 2 | Zaúčtovaný (A=zaúčtovaný) |
| DstDif | Str1 | 2 | Rozdiel MD/Dal (!=existuje rozdiel) |
| SndStat | Str1 | 2 | Stav prenosu (.-odoslaný, O-potvrdený, E-chyba) |

### Účtovanie - audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccUser | Str8 | 9 | Používateľ zaúčtovania |
| AccDate | DateType | 4 | Dátum zaúčtovania |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrnCnt | word | 2 | Počet vytlačených dokladov |
| ModNum | word | 2 | Počítadlo modifikácií |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Unique, Case insensitive |
| 1 | ExtNum | ExtNum | Duplicit, Case insensitive |
| 2 | _Describe | Describe | Duplicit |
| 3 | DocVal | DocVal | Duplicit |
| 4 | PaCode | PaCode | Duplicit |
| 5 | _PaName | PaName | Duplicit |
| 6 | ConDoc | ConDoc | Duplicit |
| 7 | Year, SerNum | YearSerNum | Unique |
| 8 | DocDate | DocDate | Duplicit |
| 9 | DstAcc | DstAcc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Obchodný partner |
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| CAccSnt+CAccAnl | ACCLST | Účet MD |
| DAccSnt+DAccAnl | ACCLST | Účet Dal |

## Typy dokladov (DocType)

| Hodnota | Popis |
|---------|-------|
| 0 | Bežný účtovný doklad |
| 1 | Otvorenie účtov (počiatočné stavy) |
| 2 | Uzatvorenie účtov (záverečné stavy) |

## Použitie

- Interné účtovné doklady
- Kurzové rozdiely
- Otváranie/zatváranie účtovného obdobia
- Zápočty pohľadávok a záväzkov

## Business pravidlá

- CredVal musí rovnať DebVal (bilančná rovnováha)
- DstDif='!' signalizuje nerovnováhu MD/Dal
- DstAcc='A' znamená zaúčtovaný doklad
- DstLck=1 blokuje úpravy
- DocType rozlišuje bežné doklady od otváracích/zatváracích

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
