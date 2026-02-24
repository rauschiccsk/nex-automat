# ISN - Poznámky k dodávateľským faktúram

## Kľúčové slová / Aliases

ISN, ISN.BTR, príjemky poznámky, receipt notes, poznámky k príjmu

## Popis

Tabuľka poznámok k dodávateľským faktúram. Umožňuje ukladať dlhé texty a dodatočné informácie k dokladom.

## Btrieve súbor

`ISNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISNyynnn.BTR`

## Polia (5)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo DF - **FK → ISH** |
| LinNum | word | 2 | Poradové číslo riadku |
| Notice | Str250 | 251 | Text poznámky |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, LinNum | DoLn | Duplicit (Composite PK) |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ISH.DocNum | Hlavička dokladu |

## Použitie

- Poznámky k faktúre
- Dodacie podmienky
- Reklamačné informácie
- Špeciálne inštrukcie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
