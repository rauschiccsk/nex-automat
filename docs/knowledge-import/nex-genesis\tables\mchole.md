# MCHOLE - Voľné poradové čísla cenových ponúk

## Kľúčové slová / Aliases

MCHOLE, MCHOLE.BTR, voľné, poradové, čísla, cenových, ponúk

## Popis

Tabuľka voľných (uvoľnených) poradových čísel odberateľských cenových ponúk. Vznikajú pri mazaní rozpracovaných dokladov a môžu byť znovu použité.

## Btrieve súbor

`MCHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\MCHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy ponúk |
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
| BookNum | MCBLST.BookNum | Kniha ponúk |

## Použitie

- Evidencia voľných čísel pre opätovné použitie
- Zachovanie kontinuity číslovania
- Audit mazania dokladov

## Business pravidlá

- Pri vytváraní novej ponuky sa najprv hľadá voľné číslo v MCHOLE
- Ak existuje voľné číslo, použije sa a odstráni z MCHOLE
- Ak neexistuje, vygeneruje sa nové poradové číslo
- Pri zmazaní neuzatvorenej ponuky sa jej číslo zapíše do MCHOLE

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
