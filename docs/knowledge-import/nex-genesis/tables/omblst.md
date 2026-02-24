# OMBLST - Zoznam kníh interných výdajok

## Kľúčové slová / Aliases

OMBLST, OMBLST.BTR, zoznam, kníh, interných, výdajok

## Popis

Konfiguračná tabuľka kníh interných skladových výdajok. Definuje základné nastavenia pre každú knihu vrátane prepojenia na príjemky pri medziskladových presunoch.

## Btrieve súbor

`OMBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OMBLST.BTR`

## Štruktúra polí (36 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| _BookName | Str30 | 31 | Názov pre vyhľadávanie |
| BookYear | Str4 | 5 | Rok založenia knihy |
| SerNum | word | 2 | Poradové číslo knihy |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | longint | 4 | Počet dokladov v knihe |

### Základné nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Základný sklad |
| SmCode | word | 2 | Základný skladový pohyb |

### Medziskladový presun

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ImdBook | Str5 | 6 | Číslo knihy príjemok pre medziskladový presun |
| ImdStk | word | 2 | Sklad medziprevádzkového príjmu |
| ImdSmc | word | 2 | Skladový pohyb medziprevádzkového príjmu |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Online | byte | 1 | Priamy odpočet zo skladu (1=zapnutý) |
| AutoAcc | byte | 1 | Automatické rozúčtovanie |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatRnd | byte | 1 | Typ zaokrúhľovania DPH z NC |
| ValRnd | byte | 1 | Typ zaokrúhľovania NC s DPH |

### Modifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Poradové číslo modifikácie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | _BookName | _BookName | Duplicit, Case insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Základný sklad |
| SmCode | SMLST.SmCode | Základný skladový pohyb |
| ImdBook | IMBLST.BookNum | Kniha príjemok |
| ImdStk | STKLST.StkNum | Sklad príjmu |
| ImdSmc | SMLST.SmCode | Pohyb príjmu |

## Použitie

- Konfigurácia kníh výdajok
- Nastavenie medziskladových presunov
- Definícia automatických operácií
- Správa zaokrúhľovania

## Business pravidlá

- Každá kniha má unikátne číslo (BookNum)
- ImdBook definuje prepojenie na knihu príjemok
- Online=1 znamená okamžité odpočítanie zo skladu
- Shared=1 aktivuje FTP synchronizáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
