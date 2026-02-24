# IMN - Poznámky k interným príjemkam

## Kľúčové slová / Aliases

IMN, IMN.BTR, poznámky, interným, príjemkam

## Popis

Tabuľka poznámok a textových príslušenstiev k interným príjemkam.

## Btrieve súbor

`IMNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo príjemky - **FK → IMH.DocNum** |
| NotType | Str1 | 2 | Typ poznámky (T=text, P=príloha) |
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
| DocNum | IMH.DocNum | Hlavička príjemky |

## Typy poznámok (NotType)

| Hodnota | Popis |
|---------|-------|
| T | Textová časť (tlačí sa na doklade) |
| P | Príloha (referencia na súbor) |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
