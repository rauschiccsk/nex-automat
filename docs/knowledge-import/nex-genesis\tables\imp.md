# IMP - Výrobné čísla interných príjemok

## Kľúčové slová / Aliases

IMP, IMP.BTR, výrobné, čísla, interných, príjemok

## Popis

Tabuľka výrobných čísel (sériových čísel) prijatého tovaru. Umožňuje sledovať jednotlivé kusy tovaru s výrobnými číslami.

## Btrieve súbor

`IMPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMPyynnn.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo príjemky - **FK → IMH.DocNum** |
| ItmNum | word | 2 | Číslo položky príjemky |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| ProdNum | Str30 | 31 | Výrobné číslo tovaru |

### Príjem

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum príjmu tovaru |
| StkNum | word | 2 | Číslo skladu príjmu |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, ProdNum | DoItPn | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | ProdNum | ProdNum | Duplicit, Case insensitive |
| 5 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IMH.DocNum | Hlavička príjemky |
| GsCode | GSCAT.GsCode | Tovar |
| StkNum | STKLST.StkNum | Sklad |

## Použitie

- Sledovanie sériových/výrobných čísel
- Evidencia záručných listov
- Traceability (sledovateľnosť) tovaru
- Reklamačné konanie

## Business pravidlá

- Jedna položka príjemky môže mať viacero výrobných čísel
- Výrobné číslo je unikátne pre daný tovar
- Používa sa pre techniku, elektroniku a iný sériovo číslovaný tovar

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
