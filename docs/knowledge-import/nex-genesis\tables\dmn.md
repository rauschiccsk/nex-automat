# DMN - Poznámky ku dokladom rozobrania

## Kľúčové slová / Aliases

DMN, DMN.BTR, poznámky, dokladom, rozobrania

## Popis

Tabuľka poznámkových riadkov k dokladom rozobrania. Umožňuje pridávať textové poznámky k jednotlivým dokladom. Každá kniha má vlastný súbor.

## Btrieve súbor

`DMNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\DMNyynnn.BTR`

## Štruktúra polí (3 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK DMH** |
| LinNum | word | 2 | Poradové číslo poznámkového riadku |
| Notice | Str250 | 251 | Poznámkový riadok |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, LinNum | DoLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | DMH.DocNum | Hlavička dokladu |

## Použitie

- Textové poznámky k dokladu rozobrania
- Dôvod rozobrania
- Výsledky diagnostiky
- Informácie o reklamácii

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
