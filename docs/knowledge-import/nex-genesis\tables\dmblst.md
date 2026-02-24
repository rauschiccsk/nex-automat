# DMBLST - Zoznam kníh dokladov rozobrania

## Kľúčové slová / Aliases

DMBLST, DMBLST.BTR, zoznam, kníh, dokladov, rozobrania

## Popis

Tabuľka zoznamu kníh dokladov rozobrania. Obsahuje konfiguráciu jednotlivých kníh vrátane nastavenia skladov a pohybov pre výdaj a príjem. Globálny súbor.

## Btrieve súbor

`DMBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\DMBLST.BTR`

## Štruktúra polí (17 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy dokladov rozobrania |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok, na ktorý je založená kniha |
| SerNum | word | 2 | Poradové číslo knihy |

### Konfigurácia skladov

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PlsNum | word | 2 | Číslo prioritného predajného cenníka |
| OuStkNum | word | 2 | Číslo skladu výdaja (výrobok) - **FK STKLST** |
| InStkNum | word | 2 | Číslo skladu príjmu (komponenty) - **FK STKLST** |
| OuSmCode | word | 2 | Základné nastavenie skladového pohybu výdaja - **FK SMLST** |
| InSmCode | word | 2 | Základné nastavenie skladového pohybu príjmu - **FK SMLST** |

### Štatistika

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | longint | 4 | Počet dokladov v danej knihe |

### Zdieľanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Príznak zdieľania (1=zdieľaný cez FTP) |

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

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| OuStkNum | STKLST.StkNum | Sklad výdaja výrobku |
| InStkNum | STKLST.StkNum | Sklad príjmu komponentov |
| OuSmCode | SMLST.SmCode | Typ pohybu výdaja |
| InSmCode | SMLST.SmCode | Typ pohybu príjmu |

## Použitie

- Definícia kníh dokladov rozobrania
- Nastavenie predvolených skladov a pohybov
- Štatistika počtu dokladov

## Business pravidlá

- OuStkNum = sklad hotových výrobkov (výdaj)
- InStkNum = sklad materiálu/polotovarov (príjem komponentov)
- Knihu možno zmazať len ak DocQnt=0

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
