# GSNOTI - Poznámky k tovaru

## Kľúčové slová / Aliases

GSNOTI, GSNOTI.BTR, poznámky k tovaru, product notes, tovarové poznámky

## Popis
Tabuľka rozšírených poznámok k tovarovým položkám. Umožňuje ukladať dlhšie texty než pole Notice v GSCAT.

## Btrieve súbor
`GSNOTI.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSNOTI.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT** |
| Notice | Str160 | 161 | Poznámkový riadok |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |

## Business pravidlá

- Jeden tovar môže mať **viacero** poznámkových riadkov
- Používa sa pre:
  - Rozšírené popisy
  - Skladovacie pokyny
  - Alergény
  - Výživové hodnoty

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model
- [ ] API endpoint
