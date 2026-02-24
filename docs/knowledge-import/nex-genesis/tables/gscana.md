# GSCANA - Doplnkové názvy tovaru

## Kľúčové slová / Aliases

GSCANA, GSCANA.BTR, analytické údaje, analytics data, štatistiky tovaru

## Popis
Tabuľka rozšírených/doplnkových názvov tovaru. Umožňuje ukladať dlhšie alternatívne názvy pre vyhľadávanie.

## Btrieve súbor
`GSCANA.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSCANA.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **PRIMARY KEY** |
| GaName | Str200 | 201 | Doplnkový názov tovaru |
| _GaName | Str200 | 201 | Vyhľadávacie pole doplnkového názvu |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Unique |
| 1 | _GaName | GaName | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |

## Použitie

- Rozšírené popisy produktov
- Alternatívne názvy pre vyhľadávanie
- Značky a obchodné názvy
- Kľúčové slová pre e-shop

## Poznámka

Pole `_GaName` je automaticky generované pre case-insensitive vyhľadávanie (uppercase verzia `GaName`).

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model
- [ ] API endpoint
