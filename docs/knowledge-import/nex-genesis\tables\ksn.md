# KSN - Poznámky k dokladom konsignačného vyúčtovania

## Kľúčové slová / Aliases

KSN, KSN.BTR, poznámky, dokladom, konsignačného, vyúčtovania

## Popis

Tabuľka poznámkových riadkov k dokladom konsignačného vyúčtovania. Umožňuje pridávať textové poznámky a prílohy k jednotlivým dokladom. Každá kniha má vlastný súbor.

## Btrieve súbor

`KSNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\KSNyynnn.BTR`

## Štruktúra polí (6 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK KSH** |
| NotType | Str1 | 2 | Typ poznámkového riadku (T=text, P=príloha) |
| LinNum | word | 2 | Poradové číslo poznámkového riadku |

### Obsah

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Notice | Str250 | 251 | Poznámkový riadok |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NotType, LinNum | DoNtLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | KSH.DocNum | Hlavička dokladu |

## Typy poznámok (NotType)

| Hodnota | Typ | Popis |
|---------|-----|-------|
| T | Text | Textová časť dokladu |
| P | Príloha | Odkaz na prílohu |

## Použitie

- Textové poznámky k dokladu vyúčtovania
- Prílohy a doplňujúce dokumenty
- Tlač poznámok na doklad

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
