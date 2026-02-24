# IDN - Poznámky k interným účtovným dokladom

## Kľúčové slová / Aliases

IDN, IDN.BTR, poznámky, interným, účtovným, dokladom

## Popis

Tabuľka poznámkových riadkov k interným účtovným dokladom.

## Btrieve súbor

`IDNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IDNyynnn.BTR`

## Štruktúra polí (3 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → IDH.DocNum** |
| LinNum | word | 2 | Poradové číslo riadku |
| Notice | Str250 | 251 | Poznámkový riadok |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, LinNum | DoLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IDH.DocNum | Hlavička dokladu |

## Použitie

- Viacriadkové poznámky k dokladu
- Doplňujúce informácie k účtovnému zápisu
- Audit trail

## Business pravidlá

- Jeden doklad môže mať neobmedzený počet poznámkových riadkov
- LinNum určuje poradie riadkov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
