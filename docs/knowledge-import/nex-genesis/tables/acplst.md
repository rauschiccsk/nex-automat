# ACPLST - Položky pre tlač akciových letákov

## Kľúčové slová / Aliases

ACPLST, ACPLST.BTR, položky, pre, tlač, akciových, letákov

## Popis

Pracovná tabuľka pre prípravu položiek na tlač akciových letákov. Obsahuje rozšírené údaje o tovare vrátane informácií o dodávateľovi, krajine pôvodu a popisu pre tlač.

## Btrieve súbor

`ACPLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACPLST.BTR`

## Štruktúra polí (19 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **PK** |
| MgCode | longint | 4 | Číslo tovarovej skupiny |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Identifikačný kód tovaru (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |

### Rozšírené údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaName | Str30 | 31 | Názov dodávateľa tovaru |
| StaName | Str30 | 31 | Krajina pôvodu |
| TpyName | Str30 | 31 | Odroda |
| Weight | Str15 | 16 | Váha |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MsuName | Str10 | 11 | Základná merná jednotka |
| MsuPrice | double | 8 | Cena za základnú jednotku |
| BefBPrice | double | 8 | Predajná cena s DPH pred precenením |
| NewBPrice | double | 8 | Akciová predajná cena s DPH |

### Popis pre tlač

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe1 | Str30 | 31 | Popis 1 |
| Describe2 | Str30 | 31 | Popis 2 |
| Describe3 | Str30 | 31 | Popis 3 |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | _GsName | GsName | Duplicit, Case-insensitive |
| 2 | BarCode | BarCode | Duplicit |
| 3 | StkCode | StkCode | Duplicit, Case-insensitive |

## Použitie

- Príprava údajov pre tlač akciových letákov
- Rozšírené informácie o tovare pre marketing
- Tlač cien za základnú jednotku (MsuPrice)

## Business pravidlá

- Tabuľka sa plní z ACI s doplnením údajov z GSCAT, PAB
- MsuPrice = cena prepočítaná na základnú jednotku (kg, l, ks)
- Describe1-3 pre doplňujúce marketingové texty

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
