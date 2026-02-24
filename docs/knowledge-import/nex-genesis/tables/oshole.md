# OSHOLE - Voľné poradové čísla dodávateľských objednávok

## Kľúčové slová / Aliases

OSHOLE, OSHOLE.BTR, prázdne čísla nákupných objednávok, PO number gaps

## Popis

Tabuľka voľných (uvoľnených) poradových čísel dodávateľských objednávok. Vznikajú pri mazaní rozpracovaných objednávok a môžu byť znovu použité.

## Btrieve súbor

`OSHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy objednávok |
| SerNum | longint | 4 | Voľné poradové číslo |
| ModUser | Str8 | 9 | Používateľ uvoľnenia |
| ModDate | DateType | 4 | Dátum uvoľnenia |
| ModTime | TimeType | 4 | Čas uvoľnenia |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum, SerNum | BnSn | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BookNum | OSBLST.BookNum | Kniha objednávok |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
