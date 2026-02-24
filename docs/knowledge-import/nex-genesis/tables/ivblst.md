# IVBLST - Zoznam kníh inventúrnych dokladov

## Kľúčové slová / Aliases

IVBLST, IVBLST.BTR, zoznam, kníh, inventúrnych, dokladov

## Popis

Konfiguračná tabuľka kníh inventúrnych dokladov. Definuje číselné rady, predvolené hodnoty a prepojenia na vyrovnávacie knihy.

## Btrieve súbor

`IVBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\IVBLST.BTR`

## Štruktúra polí (22 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | word | 2 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| Year | Str2 | 3 | Účtovný rok |

### Číselná rada

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Posledné použité poradové číslo |
| SerPfx | Str4 | 5 | Prefix poradového čísla |
| SerSfx | Str4 | 5 | Suffix poradového čísla |

### Nastavenie skladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Predvolený sklad |

### Prepojenie na vyrovnávacie knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OmbBook | word | 2 | Číslo knihy interných výdajok (pre manká) |
| OmbSmCode | word | 2 | Kód skladového pohybu (manko) |
| ImbBook | word | 2 | Číslo knihy interných príjemok (pre prebytky) |
| ImbSmCode | word | 2 | Kód skladového pohybu (prebytok) |

### Nastavenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Delete | byte | 1 | Povolenie zrušiť knihu (0/1) |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaná) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | longint | 4 | Počet dokladov v knihe |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Unikátny |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Predvolený sklad |
| OmbBook | OMBLST.BookNum | Kniha výdajok (manká) |
| OmbSmCode | STMLST.SmCode | Pohyb pre manká |
| ImbBook | IMBLST.BookNum | Kniha príjemok (prebytky) |
| ImbSmCode | STMLST.SmCode | Pohyb pre prebytky |

## Použitie

- Konfigurácia kníh inventúrnych dokladov
- Správa číselných radov
- Predvolené hodnoty pre nové inventúry
- Prepojenie na vyrovnávacie knihy

## Business pravidlá

- Jedna kniha = jeden rok
- SerNum sa automaticky inkrementuje
- Delete=1 je potrebné pre zmazanie knihy
- Shared=1 aktivuje FTP synchronizáciu
- OmbBook/ImbBook definujú kam sa generujú vyrovnávacie doklady
- OmbSmCode/ImbSmCode definujú skladové pohyby pre manká/prebytky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
