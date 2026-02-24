# CMBLST - Zoznam kníh kompletizačných dokladov

## Kľúčové slová / Aliases

CMBLST, CMBLST.BTR, zoznam, kníh, kompletizačných, dokladov

## Popis

Konfiguračná tabuľka kníh kompletizačných dokladov. Definuje číselné rady a vlastnosti pre jednotlivé knihy podľa rokov.

## Btrieve súbor

`CMBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\CMBLST.BTR`

## Štruktúra polí (20 polí)

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

### Nastavenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Predvolený sklad |
| PdSmCode | word | 2 | Kód skladového pohybu príjmu výrobku |
| CmSmCode | word | 2 | Kód skladového pohybu výdaja komponentov |
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
| PdSmCode | STMLST.SmCode | Skladový pohyb príjmu |
| CmSmCode | STMLST.SmCode | Skladový pohyb výdaja |

## Použitie

- Konfigurácia kníh kompletizačných dokladov
- Správa číselných radov
- Predvolené hodnoty pre nové doklady

## Business pravidlá

- Jedna kniha = jeden rok
- SerNum sa automaticky inkrementuje
- Delete=1 je potrebné pre zmazanie knihy
- Shared=1 aktivuje FTP synchronizáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
