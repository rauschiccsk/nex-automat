# OSN - Poznámky k dodávateľským objednávkam

## Kľúčové slová / Aliases

OSN, OSN.BTR, objednávky odoslané poznámky, purchase order notes

## Popis

Tabuľka poznámok a textových príslušenstiev k dodávateľským objednávkam. Obsahuje textové časti dokladu a prílohy.

## Btrieve súbor

`OSNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo objednávky - **FK → OSH.DocNum** |
| NotType | Str1 | 2 | Typ poznámky (T=text, P=príloha, I=interná) |
| LinNum | word | 2 | Poradové číslo riadku |
| Notice | Str80 | 81 | Text poznámky |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NotType, LinNum | DoNtLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OSH.DocNum | Hlavička objednávky |

## Typy poznámok (NotType)

| Hodnota | Popis |
|---------|-------|
| T | Textová časť (tlačí sa na objednávke) |
| P | Príloha (referencia na súbor) |
| I | Interná poznámka (netlačí sa) |

## Použitie

- Doplňujúce informácie na objednávke
- Špeciálne požiadavky na dodávku
- Interné poznámky pre spracovanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
