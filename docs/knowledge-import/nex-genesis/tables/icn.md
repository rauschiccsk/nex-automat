# ICN - Poznámky odberateľských faktúr

## Kľúčové slová / Aliases

ICN, ICN.BTR, faktúry poznámky, invoice notes, poznámky k faktúram

## Popis

Tabuľka poznámok a textových príslušenstiev k odberateľským faktúram. Obsahuje textové časti dokladu, prílohy a interné poznámky.

## Btrieve súbor

`ICNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo faktúry - **FK → ICH.DocNum** |
| NotType | Str1 | 2 | Typ poznámky (T=text, P=príloha, I=interná) |
| LinNum | word | 2 | Poradové číslo riadku |
| Notice | Str250 | 251 | Text poznámky |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NotType, LinNum | DoNtLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ICH.DocNum | Hlavička faktúry |

## Typy poznámok (NotType)

| Hodnota | Popis |
|---------|-------|
| T | Textová časť (tlačí sa na faktúre) |
| P | Príloha (referencia na súbor) |
| I | Interná poznámka (netlačí sa) |

## Použitie

- Doplňujúce informácie na faktúre
- Platobné inštrukcie
- Zmluvné podmienky
- Interné poznámky pre spracovanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
