# TSBLST - Zoznam kníh dodávateľských DL

## Kľúčové slová / Aliases

TSBLST, TSBLST.BTR, zoznam kníh pokladní, cash register books, pokladne

## Popis

Číselník kníh dodávateľských dodacích listov. Definuje nastavenia pre jednotlivé knihy - prepojenie na cenník, sklad, spôsob spracovania.

## Btrieve súbor

`TSBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TSBLST.BTR`

## Polia

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok knihy |
| SerNum | word | 2 | Poradové číslo |
| DocQnt | word | 2 | Počet dokladov |

### Nastavenia spracovania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Predvolený dodávateľ |
| StkNum | word | 2 | Predvolený sklad |
| PlsNum | word | 2 | Predvolený cenník |
| WriNum | word | 2 | Číslo prevádzky |
| PabBook | word | 2 | Kniha partnerov |
| SmCode | word | 2 | Predvolený skladový pohyb |
| DvzName | Str3 | 4 | Mena knihy |
| DvzBook | word | 2 | Typ knihy (0=tuzemská, 1=valutová) |
| IsdBook | Str5 | 6 | Číslo knihy faktúr |

### Elektronický prenos

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsdRcv | byte | 1 | Typ prenosu (0=všeobecný, 1=špeciálny) |
| RcvType | byte | 1 | Typ špeciálneho prenosu |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RevCalc | byte | 1 | Výpočet NC z PC |
| AutoAcc | byte | 1 | Automatické účtovanie (1=zapnuté) |
| BcsVer | byte | 1 | Kontrola obchodných podmienok |
| Online | byte | 1 | Okamžitý príjem na sklad |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatRnd | byte | 1 | Typ zaokrúhlenia DPH |
| ValRnd | byte | 1 | Typ zaokrúhlenia PC s DPH |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |

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

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Multi-kniha architektúra

Číslo knihy určuje názvy dátových súborov:
- `TSH` + BookNum → TSHyynnn.BTR
- `TSI` + BookNum → TSIyynnn.BTR
- `TSN` + BookNum → TSNyynnn.BTR
- `TSP` + BookNum → TSPyynnn.BTR

## Príklad použitia

| BookNum | BookName | DvzBook | StkNum |
|---------|----------|---------|--------|
| 24001 | Tuzemské DDL 2024 | 0 | 1 |
| 24002 | Importné DDL 2024 | 1 | 1 |
| 24003 | Centrálny sklad | 0 | 2 |

## Business pravidlá

- Jedna kniha = jeden účtovný rok
- DvzBook=0 pre tuzemské doklady (EUR)
- DvzBook=1 pre zahraničné doklady (cudzia mena)
- AutoAcc=1 automaticky účtuje po vytlačení

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
