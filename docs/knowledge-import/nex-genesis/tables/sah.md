# SAH - Hlavičky výdajok MO predaja

## Kľúčové slová / Aliases

SAH, SAH.BTR, hlavičky, výdajok, predaja

## Popis

Hlavičková tabuľka skladových výdajok z maloobchodného predaja (ERP pokladne). Obsahuje súhrnné hodnoty tržby, DPH členenie a referencie na súvisiace pokladničné doklady.

## Btrieve súbor

`SAH$$.BTR` ($$ = číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SAH$$.BTR`

## Štruktúra polí (65 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Účtovné číslo dokladu - **PRIMARY KEY** |
| DocDate | DateType | 4 | Dátum predaja |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Celkový počet položiek |
| NsiCnt | word | 2 | Počet nevysporiadaných položiek |
| PrnCnt | byte | 1 | Počet vytlačených kópií |

### DPH skupiny - sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | double | 8 | Sadzba DPH - skupina 1 |
| VatPrc2 | double | 8 | Sadzba DPH - skupina 2 |
| VatPrc3 | double | 8 | Sadzba DPH - skupina 3 |
| VatPrc4 | double | 8 | Sadzba DPH - skupina 4 |
| VatPrc5 | double | 8 | Sadzba DPH - skupina 5 |

### DPH skupiny - hodnoty bez DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue1 | double | 8 | Hodnota predaja bez DPH - skupina 1 |
| AValue2 | double | 8 | Hodnota predaja bez DPH - skupina 2 |
| AValue3 | double | 8 | Hodnota predaja bez DPH - skupina 3 |
| AValue4 | double | 8 | Hodnota predaja bez DPH - skupina 4 |
| AValue5 | double | 8 | Hodnota predaja bez DPH - skupina 5 |

### DPH skupiny - hodnoty DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal1 | double | 8 | Hodnota DPH - skupina 1 |
| VatVal2 | double | 8 | Hodnota DPH - skupina 2 |
| VatVal3 | double | 8 | Hodnota DPH - skupina 3 |
| VatVal4 | double | 8 | Hodnota DPH - skupina 4 |
| VatVal5 | double | 8 | Hodnota DPH - skupina 5 |

### DPH skupiny - hodnoty s DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BValue1 | double | 8 | Hodnota predaja s DPH - skupina 1 |
| BValue2 | double | 8 | Hodnota predaja s DPH - skupina 2 |
| BValue3 | double | 8 | Hodnota predaja s DPH - skupina 3 |
| BValue4 | double | 8 | Hodnota predaja s DPH - skupina 4 |
| BValue5 | double | 8 | Hodnota predaja s DPH - skupina 5 |

### Celkové hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue | double | 8 | Celková hodnota v NC |
| AValue | double | 8 | Celková hodnota bez DPH |
| VatVal | double | 8 | Celková hodnota DPH |
| BValue | double | 8 | Celková hodnota s DPH |
| DscVal | double | 8 | Hodnota zliav |
| IValue | double | 8 | Hodnota v predpokladanej NC (informatívna) |

### Členenie tržby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GscVal | double | 8 | Hodnota predaného tovaru bez DPH |
| SecVal | double | 8 | Hodnota predaných služieb bez DPH |
| CrcVal | double | 8 | Hodnota tržby cez platobné karty |

### Zálohy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpiVal | double | 8 | Hodnota prijatých záloh |
| SpeVal | double | 8 | Hodnota použitých záloh |
| SpiVat | double | 8 | DPH z prijatých záloh |
| SpeVat | double | 8 | DPH z použitých záloh |

### Hotovosť

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CseVal | double | 8 | Hodnota vydanej (odvedenej) hotovosti |
| IncVal | double | 8 | Príjem hotovosti do pokladne |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CAccSnt | Str3 | 4 | Syntetický účet MD |
| CAccAnl | Str8 | 9 | Analytický účet MD |
| DAccSnt | Str3 | 4 | Syntetický účet Dal |
| DAccAnl | Str8 | 9 | Analytický účet Dal |
| DstAcc | Str1 | 2 | Zaúčtovaný (A=zaúčtovaný) |

### Súvisiace doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BvlDoc | Str12 | 13 | Príjmový PD - príjem dennej tržby |
| CseDoc | Str12 | 13 | Výdajový PD - odvod hotovosti do HP |
| CsiDoc | Str12 | 13 | Príjmový PD - príjem do HP |
| SpiDoc | Str12 | 13 | Príjmový PD - príjem zálohy |
| SpeDoc | Str12 | 13 | Výdajový PD - výdaj použitej zálohy |
| SpvDoc | Str12 | 13 | Interný ÚD - DPH záloh |
| CrcDoc | Str12 | 13 | Výdajový PD - výdaj platobných kariet |
| IncCse | Str12 | 13 | Výdajový PD - výdaj z HP do ERP |
| IncCsi | Str12 | 13 | Príjmový PD - príjem z HP do ERP |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Odoslané zmeny (0=zmenený, 1=odoslaný) |
| SndStat | Str1 | 2 | Stav prenosu (.-odoslaný, O-potvrdený, E-chyba) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocDate | DocDate | Duplicit |
| 2 | AValue | AValue | Duplicit |
| 3 | BValue | BValue | Duplicit |
| 4 | Sended | Sended | Duplicit |
| 5 | DstAcc | DstAcc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BvlDoc | CSD.DocNum | Pokladničný doklad |
| CseDoc | CSD.DocNum | Pokladničný doklad |
| CsiDoc | CSD.DocNum | Pokladničný doklad |

## Použitie

- Denné uzávierky ERP pokladní
- Evidencia tržieb
- Sledovanie DPH
- Podklad pre účtovanie

## Business pravidlá

- NsiCnt > 0 znamená nevysporiadané položky (červené)
- DstAcc='A' znamená zaúčtovaný doklad
- Sended=1 po synchronizácii s centrálou

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
