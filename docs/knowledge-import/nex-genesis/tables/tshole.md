# TSHOLE - Voľné poradové čísla DDL

## Kľúčové slová / Aliases

TSHOLE, TSHOLE.BTR, prázdne čísla pokladní, cash number gaps, chýbajúce čísla

## Popis

Pomocná tabuľka pre evidenciu voľných (zmazaných) poradových čísel dodávateľských dodacích listov. Umožňuje znovupoužitie čísel po vymazaní dokladov.

## Btrieve súbor

`TSHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TSHOLE.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy DDL |
| SerNum | longint | 4 | Voľné poradové číslo |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum, SerNum | BnSn | Duplicit (Composite PK) |

## Použitie

Pri vytváraní nového dokladu systém:
1. Skontroluje TSHOLE pre danú knihu
2. Ak existuje voľné číslo, použije ho a vymaže z TSHOLE
3. Ak neexistuje, použije nasledujúce poradové číslo

Pri mazaní dokladu:
1. SerNum sa zapíše do TSHOLE
2. Číslo je k dispozícii pre nový doklad

## Business pravidlá

- Umožňuje zachovať súvislú číselnú radu
- Voľné čísla sa používajú prednostne
- FIFO princíp pri výbere voľného čísla

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model (nepotrebné - sekvencie)
