# OSBLST - Zoznam kníh dodávateľských objednávok

## Kľúčové slová / Aliases

OSBLST, OSBLST.BTR, zoznam kníh nákupných objednávok, PO books list

## Popis

Konfiguračná tabuľka definujúca knihy (série) dodávateľských objednávok. Obsahuje nastavenia číslovania, skladov a prepojenia na iné moduly.

## Btrieve súbor

`OSBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSBLST.BTR`

## Štruktúra polí (27 polí)

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok založenia knihy |

### Mena a nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzBook | byte | 1 | Typ knihy (0=tuzemská, 1=valutová) |
| DvzName | Str3 | 4 | Skratka meny |
| SerNum | word | 2 | Posledné poradové číslo |
| ExnFrm | Str12 | 13 | Formát externého čísla |
| DocQnt | word | 2 | Počet dokladov v knihe |

### Väzby na iné moduly

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| StkNum | word | 2 | Základný sklad |
| PabBook | word | 2 | Číslo knihy partnerov (dodávatelia) |
| TsdBook | Str5 | 6 | Číslo knihy DDL |
| PaCode | longint | 4 | Kód dodávateľa (ak je kniha vyhradená) |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatRnd | byte | 1 | Typ zaokrúhlenia DPH |
| ValRnd | byte | 1 | Typ zaokrúhlenia PC s DPH |

### Výpočet objednávok

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AvgCalc | byte | 1 | Spôsob výpočtu priemerného množstva |
| AvgMth | byte | 1 | Počet mesiacov pre priemer |
| ExtPrc | double | 8 | Percento extrému |
| OrdCoef | double | 8 | Koeficient objednacieho množstva |

### Integrácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Zdieľaný sklad (1=áno) |
| SndType | byte | 1 | Typ elektronického prenosu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Predvolený sklad |
| TsdBook | TSBLST.BookNum | Kniha DDL |
| PaCode | PAB.PaCode | Vyhradený dodávateľ |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
