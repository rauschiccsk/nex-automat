# TCN - Poznámky odberateľských dodacích listov

## Kľúčové slová / Aliases

TCN, TCN.BTR, dodacie listy poznámky, delivery notes, poznámky k výdaju

## Popis

Tabuľka poznámok a textových príslušenstiev k odberateľským dodacím listom. Obsahuje textové časti dokladu a prílohy.

## Btrieve súbor

`TCNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo DL - **FK → TCH.DocNum** |
| NotType | Str1 | 2 | Typ poznámkového riadku (T=text, P=príloha) |
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
| DocNum | TCH.DocNum | Hlavička DL |

## Typy poznámok (NotType)

| Hodnota | Popis |
|---------|-------|
| T | Textová časť dokladu (tlačí sa) |
| P | Príloha (interná poznámka) |

## Použitie

- Doplňujúce informácie na dodacom liste
- Špeciálne pokyny pre expedíciu
- Interné poznámky pre spracovanie
- Textové prílohy k dokladu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
