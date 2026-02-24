# STKPDN - Výrobné čísla skladových položiek

## Kľúčové slová / Aliases

STKPDN, STKPDN.BTR, výrobné čísla, serial numbers, sériové čísla, šarže

## Popis

Tabuľka evidencie výrobných čísel (sériových čísel) tovarov. Umožňuje sledovať individuálne kusy tovaru od príjmu po výdaj.

## Btrieve súbor

`STKPDN.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STORES\STKPDN.BTR`

## Polia

### Výrobné číslo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrdNum | Str30 | 31 | Výrobné číslo tovaru - **PRIMARY KEY** |
| Status | Str1 | 2 | Stav (N=prijatý, S=vyskladnený) |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| StkNum | word | 2 | Číslo skladu |

### Príjem

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InpDoc | Str12 | 13 | Číslo príjmového dokladu |
| InpItm | word | 2 | Číslo položky príjmu |
| InpDat | DateType | 4 | Dátum príjmu |
| InpFif | longint | 4 | Číslo FIFO karty |

### Výdaj

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OutDoc | Str12 | 13 | Číslo výdajového dokladu |
| OutItm | word | 2 | Číslo položky výdaja |
| OutDat | DateType | 4 | Dátum výdaja |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUsr | Str8 | 9 | Používateľ vytvorenia |
| CrtDat | DateType | 4 | Dátum vytvorenia |
| CrtTim | TimeType | 4 | Čas vytvorenia |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PrdNum | PrdNum | Duplicit |
| 1 | PrdNum, Status | PnSt | Duplicit |
| 2 | PrdNum, Status, GsCode | PnStGc | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | OutDoc, OutItm | OdOi | Duplicit |

## Stavy výrobného čísla

| Status | Popis |
|--------|-------|
| N | Prijatý - na sklade |
| S | Vyskladnený - vydaný |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | STK.GsCode | Skladová karta |
| StkNum | STKLST.StkNum | Sklad |
| InpFif | FIF.FifNum | FIFO karta príjmu |

## Použitie

- Evidencia sériových čísel elektroniky
- Sledovanie záručných opráv
- Reklamačné konania
- Inventúra podľa výrobných čísel

## Business pravidlá

- STK.PdnMust=1 → povinné zadanie výrobného čísla
- Počet PrdNum so Status=N = STK.ActSnQnt
- Každé výrobné číslo je unikátne v rámci GsCode

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
