# ISBLST - Zoznam kníh dodávateľských faktúr

## Kľúčové slová / Aliases

ISBLST, ISBLST.BTR, zoznam kníh príjemiek, receipt books list

## Popis

Číselník kníh dodávateľských faktúr. Definuje nastavenia pre jednotlivé knihy - prepojenie na cenník, sklad, účtovné predkontácie.

## Btrieve súbor

`ISBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISBLST.BTR`

## Štruktúra polí (41 polí)

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok knihy |
| SerNum | word | 2 | Poradové číslo |
| DocQnt | word | 2 | Počet dokladov |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzBook | byte | 1 | Typ knihy (0=tuzemská, 1=valutová) |
| DvzName | Str3 | 4 | Mena knihy |
| CsyCode | Str4 | 5 | Prednastavený konštantný symbol |
| WriNum | word | 2 | Predvolená prevádzka |
| StkNum | word | 2 | Predvolený sklad |
| PlsNum | word | 2 | Predvolený cenník |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatRnd | byte | 1 | Typ zaokrúhlenia DPH |
| ValRnd | byte | 1 | Typ zaokrúhlenia NC s DPH |

### Účtovné predkontácie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocSnt | Str3 | 4 | Syntetický účet dodávateľa |
| DocAnl | Str6 | 7 | Analytický účet dodávateľa |
| VatSnt | Str3 | 4 | Syntetický účet uplatnenej DPH |
| VatAnl | Str6 | 7 | Analytický účet uplatnenej DPH |
| NVatSnt | Str3 | 4 | Syntetický účet neuplatnenej DPH |
| NVatAnl | Str6 | 7 | Analytický účet neuplatnenej DPH |
| GscSnt | Str3 | 4 | Syntetický účet tovarových položiek |
| GscAnl | Str6 | 7 | Analytický účet tovarových položiek |
| SecSnt | Str3 | 4 | Syntetický účet služieb |
| SecAnl | Str6 | 7 | Analytický účet služieb |

### Prepojenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PabBook | word | 2 | Číslo knihy partnerov |
| TsdBook | Str5 | 6 | Číslo knihy dodacích listov |
| CsdBook | Str5 | 6 | Číslo knihy pokladničných dokladov |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AutoAcc | byte | 1 | Automatické účtovanie (1=zapnuté) |
| AccTsd | byte | 1 | Automatické účtovanie pripojených DDL |
| SumAcc | byte | 1 | Kumulatívne účtovanie |
| VatCls | byte | 1 | Započítať do evidencie DPH |
| DocSpc | byte | 1 | Špecifikácia dokladu (0=FA, 1=Splátkový kalendár, 2=JCD) |
| Shared | byte | 1 | Zdieľanie cez FTP |

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

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Multi-kniha architektúra

Číslo knihy určuje názvy dátových súborov:
- `ISH` + BookNum → ISHyynnn.BTR
- `ISI` + BookNum → ISIyynnn.BTR
- `ISN` + BookNum → ISNyynnn.BTR
- `ISW` + BookNum → ISWbbbbb.BTR

## Príklad použitia

| BookNum | BookName | DvzBook | DvzName |
|---------|----------|---------|---------|
| 24001 | Tuzemské faktúry 2024 | 0 | EUR |
| 24002 | Zahraničné faktúry 2024 | 1 | USD |

## Typy dokladov (DocSpc)

| Hodnota | Popis |
|---------|-------|
| 0 | Bežná faktúra |
| 1 | Splátkový kalendár |
| 2 | JCD (colné doklady) |

## Business pravidlá

- Jedna kniha = jeden účtovný rok
- DvzBook=0 pre tuzemské doklady (EUR)
- DvzBook=1 pre zahraničné doklady (cudzia mena)
- AutoAcc=1 automaticky účtuje po vytlačení
- AccTsd=1 účtuje aj pripojené dodacie listy

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
