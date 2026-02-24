# ISHOLE - Voľné poradové čísla DF

## Kľúčové slová / Aliases

ISHOLE, ISHOLE.BTR, prázdne čísla príjemiek, receipt number gaps

## Popis

Pomocná tabuľka pre evidenciu voľných (zmazaných) poradových čísel dodávateľských faktúr. Umožňuje znovupoužitie čísel po vymazaní dokladov.

## Btrieve súbor

`ISHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISHOLE.BTR`

## Polia (7)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy DF |
| SerNum | longint | 4 | Voľné poradové číslo |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum, SerNum | BnSn | Duplicit (Composite PK) |

## Použitie

Pri vytváraní nového dokladu systém:
1. Skontroluje ISHOLE pre danú knihu
2. Ak existuje voľné číslo, použije ho a vymaže z ISHOLE
3. Ak neexistuje, použije nasledujúce poradové číslo

Pri mazaní dokladu:
1. SerNum sa zapíše do ISHOLE
2. Číslo je k dispozícii pre nový doklad

## Business pravidlá

- Umožňuje zachovať súvislú číselnú radu
- Voľné čísla sa používajú prednostne
- FIFO princíp pri výbere voľného čísla

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model (nepotrebné - sekvencie)
