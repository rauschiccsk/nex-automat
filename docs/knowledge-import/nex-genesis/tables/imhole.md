# IMHOLE - Voľné poradové čísla interných príjemok

## Kľúčové slová / Aliases

IMHOLE, IMHOLE.BTR, voľné, poradové, čísla, interných, príjemok

## Popis

Tabuľka voľných (uvoľnených) poradových čísel interných príjemok. Vznikajú pri mazaní rozpracovaných dokladov a môžu byť znovu použité.

## Btrieve súbor

`IMHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy príjemok |
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
| BookNum | IMBLST.BookNum | Kniha príjemok |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
