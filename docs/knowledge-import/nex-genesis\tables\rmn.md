# RMN - Poznámky k medziskladovým presunom

## Kľúčové slová / Aliases

RMN, RMN.BTR, poznámky, medziskladovým, presunom

## Popis

Tabuľka poznámkových riadkov k medziskladovým presunom. Umožňuje pridávať viacriadkové poznámky k dokladom.

## Btrieve súbor

`RMNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\RMNyynnn.BTR`

## Štruktúra polí (3 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo presunu - **FK → RMH.DocNum** |
| LinNum | word | 2 | Poradové číslo poznámkového riadku |
| Notice | Str250 | 251 | Poznámkový riadok |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, LinNum | DoNtLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | RMH.DocNum | Hlavička presunu |

## Použitie

- Viacriadkové poznámky k presunu
- Doplnkové informácie o presune
- Špeciálne inštrukcie pre sklad

## Business pravidlá

- Jeden doklad môže mať neobmedzený počet poznámkových riadkov
- Poznámky sa tlačia na doklade
- Zjednodušená štruktúra (bez NotType ako v IMN/OMN)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
