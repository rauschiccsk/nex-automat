# OCNLST - Poznámky zákaziek (LIST štruktúra)

## Kľúčové slová / Aliases

OCNLST, OCNLST.BTR, zoznam poznámok objednávok, order notes list

## Popis

Zjednotená tabuľka poznámok k odberateľským zákazkám zo všetkých kníh. Rozšírená verzia OCN s dodatočnými poľami pre audit.

## Btrieve súbor

`OCNLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCNLST.BTR`

## Štruktúra polí (7 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BokNum | word | 2 | Číslo knihy |
| DocNum | Str12 | 13 | Číslo dokladu - **FK → OCHLST.DocNum** |
| ItmNum | word | 2 | Poradové číslo poznámky |
| NoteType | Str1 | 2 | Typ poznámky (I=interná, E=externá) |
| NoteText | Str255 | 256 | Text poznámky |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unique |
| 1 | BokNum, DocNum, ItmNum | BokDocItm | Unique |
| 2 | DocNum | DocNum | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCHLST.DocNum | Hlavička zákazky |
| BokNum | OCBLST.BokNum | Kniha zákaziek |

## Typy poznámok

| Hodnota | Popis |
|---------|-------|
| I | Interná poznámka (len pre pracovníkov) |
| E | Externá poznámka (pre zákazníka) |

## Rozdiel OCN vs OCNLST

| Aspekt | OCN | OCNLST |
|--------|-----|--------|
| Súbory | Viac súborov (OCNyynnn.BTR) | Jeden súbor (OCNLST.BTR) |
| Pole BokNum | Nie | Áno |
| Indexy | 2 | 3 (vrátane BokNum) |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
