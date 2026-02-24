# ICHOLE - Voľné poradové čísla OF

## Kľúčové slová / Aliases

ICHOLE, ICHOLE.BTR, prázdne čísla faktúr, invoice number gaps

## Popis

Tabuľka voľných (uvoľnených) poradových čísel odberateľských faktúr. Vznikajú pri mazaní rozpracovaných faktúr a môžu byť znovu použité.

## Btrieve súbor

`ICHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy OF |
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
| BookNum | ICBLST.BookNum | Kniha faktúr |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
