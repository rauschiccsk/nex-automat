# OMP - Výrobné čísla interných výdajok

## Kľúčové slová / Aliases

OMP, OMP.BTR, výrobné, čísla, interných, výdajok

## Popis

Tabuľka výrobných (sériových) čísel vydávaného tovaru. Umožňuje sledovať jednotlivé kusy tovaru s výrobnými číslami pri výdaji zo skladu.

## Btrieve súbor

`OMPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OMPyynnn.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo výdajky - **FK → OMH.DocNum** |
| ItmNum | word | 2 | Číslo položky výdajky |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| ProdNum | Str30 | 31 | Výrobné číslo tovaru |

### Výdaj

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum výdaja tovaru |
| StkNum | word | 2 | Číslo skladu výdaja |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

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
| DocNum | OMH.DocNum | Hlavička výdajky |
| GsCode | GSCAT.GsCode | Tovar |
| StkNum | STKLST.StkNum | Sklad |

## Použitie

- Sledovanie sériových/výrobných čísel pri výdaji
- Evidencia záručných výdajov
- Traceability (sledovateľnosť) tovaru
- Reklamačné konanie

## Business pravidlá

- Jedna položka výdajky môže mať viacero výrobných čísel
- Výrobné číslo musí existovať v skladových zásobách (IMP)
- Používa sa pre techniku, elektroniku a iný sériovo číslovaný tovar
- Pri výdaji sa výrobné číslo "spotrebuje" zo skladu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
