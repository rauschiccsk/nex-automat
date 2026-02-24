# OCN - Poznámky odberateľských zákaziek

## Kľúčové slová / Aliases

OCN, OCN.BTR, objednávky poznámky, order notes, poznámky k objednávkam

## Popis

Tabuľka poznámok a textových informácií k odberateľským zákazkám. Používa sa pre interné aj externé poznámky.

## Btrieve súbor

`OCNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCNyynnn.BTR`

## Štruktúra polí (6 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo dokladu - **FK → OCH.DocNum** |
| ItmNum | word | 2 | Poradové číslo poznámky |
| NoteType | Str1 | 2 | Typ poznámky (I=interná, E=externá) |
| NoteText | Str255 | 256 | Text poznámky |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unique |
| 1 | DocNum | DocNum | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCH.DocNum | Hlavička zákazky |

## Typy poznámok

| Hodnota | Popis |
|---------|-------|
| I | Interná poznámka (len pre pracovníkov) |
| E | Externá poznámka (pre zákazníka) |

## Použitie

- Interné poznámky pre spracovanie objednávky
- Externé poznámky tlačené na dokladoch
- Špeciálne inštrukcie pre expedíciu
- Komunikácia so zákazníkom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
