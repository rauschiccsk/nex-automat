# IMBLST - Zoznam kníh interných príjemok

## Kľúčové slová / Aliases

IMBLST, IMBLST.BTR, zoznam, kníh, interných, príjemok

## Popis

Konfiguračná tabuľka definujúca knihy (série) interných skladových príjemok. Obsahuje nastavenia skladu, pohybu a spôsobu spracovania.

## Btrieve súbor

`IMBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMBLST.BTR`

## Štruktúra polí (36 polí)

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| _BookName | Str30 | 31 | Vyhľadávacie pole |
| BookYear | Str4 | 5 | Rok založenia knihy |

### Číslovanie a štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | word | 2 | Posledné poradové číslo |
| DocQnt | longint | 4 | Počet dokladov v knihe |

### Predvolené hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Základný sklad |
| SmCode | word | 2 | Základný skladový pohyb |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatRnd | byte | 1 | Typ zaokrúhlenia DPH |
| ValRnd | byte | 1 | Typ zaokrúhlenia NC s DPH |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AutoAcc | byte | 1 | Automatické zaúčtovanie |
| Online | byte | 1 | Priamy odpočet zo skladu (1=zapnutý) |
| FtpRcv | byte | 1 | Povoliť príjem cez internet |
| Shared | byte | 1 | Zdieľaný sklad (1=áno) |

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

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | _BookName | BookName | Duplicit, Case insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Predvolený sklad |
| SmCode | SMLST.SmCode | Predvolený skladový pohyb |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
