# OMN - Poznámky k interným výdajkám

## Kľúčové slová / Aliases

OMN, OMN.BTR, poznámky, interným, výdajkám

## Popis

Tabuľka poznámkových riadkov k interným skladovým výdajkám. Umožňuje pridávať viacriadkové poznámky k dokladom.

## Btrieve súbor

`OMNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OMNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo výdajky - **FK → OMH.DocNum** |
| NotType | Str1 | 2 | Typ poznámkového riadku (nepoužíva sa) |
| LinNum | word | 2 | Poradové číslo poznámkového riadku |
| Notice | Str250 | 251 | Poznámkový riadok |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NotType, LinNum | DoNtLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OMH.DocNum | Hlavička výdajky |

## Použitie

- Viacriadkové poznámky k výdajke
- Doplnkové informácie o výdaji
- Špeciálne inštrukcie

## Business pravidlá

- Jeden doklad môže mať neobmedzený počet poznámkových riadkov
- NotType je rezervované pre budúce použitie
- Poznámky sa tlačia na doklade

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
