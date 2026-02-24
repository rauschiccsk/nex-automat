# RMBLST - Zoznam kníh medziskladových presunov

## Kľúčové slová / Aliases

RMBLST, RMBLST.BTR, zoznam, kníh, medziskladových, presunov

## Popis

Konfiguračná tabuľka kníh medziskladových presunov. Definuje základné nastavenia pre každú knihu vrátane predvolených skladov a pohybov pre výdaj aj príjem.

## Btrieve súbor

`RMBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\RMBLST.BTR`

## Štruktúra polí (39 polí)

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

### Zdrojový sklad (výdaj)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScStkNum | word | 2 | Predvolený zdrojový sklad |
| ScSmCode | word | 2 | Predvolený pohyb výdaja |

### Cieľový sklad (príjem)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TgStkNum | word | 2 | Predvolený cieľový sklad |
| TgSmCode | word | 2 | Predvolený pohyb príjmu |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Online | byte | 1 | Priebežný skladový presun (1=zapnutý) |
| AutoAcc | byte | 1 | Automatické rozúčtovanie |
| Shared | byte | 1 | Zdieľanie pre iné prevádzky |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
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
| ScStkNum | STKLST.StkNum | Zdrojový sklad |
| TgStkNum | STKLST.StkNum | Cieľový sklad |
| ScSmCode | SMLST.SmCode | Pohyb výdaja |
| TgSmCode | SMLST.SmCode | Pohyb príjmu |

## Použitie

- Konfigurácia kníh medziskladových presunov
- Definícia párov skladov (zdroj-cieľ)
- Nastavenie automatických operácií
- Správa zdieľania

## Business pravidlá

- Každá kniha má unikátne číslo (BookNum)
- Kniha definuje predvolené sklady a pohyby
- ScStkNum a TgStkNum by mali byť rôzne
- Online=1 znamená okamžitú realizáciu presunu

## Príklad konfigurácie

```
BookNum: 00001
BookName: Presuny SKLAD1 → SKLAD2
ScStkNum: 10 (Hlavný sklad)
TgStkNum: 20 (Predajňa)
ScSmCode: 5 (Výdaj presun)
TgSmCode: 6 (Príjem presun)
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
