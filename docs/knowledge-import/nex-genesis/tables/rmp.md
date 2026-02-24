# RMP - Výrobné čísla medziskladových presunov

## Kľúčové slová / Aliases

RMP, RMP.BTR, výrobné, čísla, medziskladových, presunov

## Popis

Tabuľka výrobných (sériových) čísel presúvaného tovaru. Umožňuje sledovať jednotlivé kusy tovaru s výrobnými číslami pri presune medzi skladmi.

## Btrieve súbor

`RMPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\RMPyynnn.BTR`

## Štruktúra polí (13 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo presunu - **FK → RMH.DocNum** |
| ItmNum | word | 2 | Číslo položky presunu |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| ProdNum | Str30 | 31 | Výrobné číslo tovaru |

### Sklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScStkNum | word | 2 | Číslo zdrojového skladu |
| TgStkNum | word | 2 | Číslo cieľového skladu |
| DocDate | DateType | 4 | Dátum presunu |

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
| DocNum | RMH.DocNum | Hlavička presunu |
| GsCode | GSCAT.GsCode | Tovar |
| ScStkNum | STKLST.StkNum | Zdrojový sklad |
| TgStkNum | STKLST.StkNum | Cieľový sklad |

## Použitie

- Sledovanie sériových/výrobných čísel pri presune
- Traceability (sledovateľnosť) tovaru medzi skladmi
- Evidencia presunu konkrétnych kusov

## Business pravidlá

- Jedna položka presunu môže mať viacero výrobných čísel
- Výrobné číslo musí existovať v zdrojovom sklade
- Pri presune sa výrobné číslo "presunie" do cieľového skladu
- Uchováva informáciu o oboch skladoch (odkiaľ-kam)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
