# CAPDEF - Definícia pokladničných platidiel

## Kľúčové slová / Aliases

CAPDEF, CAPDEF.BTR, definícia, pokladničných, platidiel

## Popis

Tabuľka definícií typov platobných prostriedkov. Jednoduchý číselník názvov platidiel. Globálny súbor.

## Btrieve súbor

`CAPDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CAPDEF.BTR`

## Štruktúra polí (2 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayNum | byte | 1 | Kód platidla (0-9) |
| PayName | Str30 | 31 | Názov platidla |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PayNum | PayNum | Duplicit |

## Typické hodnoty

| PayNum | PayName |
|--------|---------|
| 0 | Hotovosť |
| 1 | Platobná karta |
| 2 | Stravovacie lístky |
| 3 | Šek |
| 4 | Preddavok |
| 5 | Kredit |
| 6 | Cudzia mena |
| 7 | Darčekový poukaz |
| 8 | Vernostné body |
| 9 | Iné |

## Použitie

- Definícia názvov platidiel pre celý systém
- Zdieľaný číselník pre všetky pokladne
- Konzistentné pomenovanie v CAH, CAP

## Business pravidlá

- Maximálne 10 typov platidiel (0-9)
- Názvy sa prenášajú do CAH.PayNameX

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
