# OMHOLE - Voľné poradové čísla interných výdajok

## Kľúčové slová / Aliases

OMHOLE, OMHOLE.BTR, voľné, poradové, čísla, interných, výdajok

## Popis

Tabuľka voľných (uvoľnených) poradových čísel interných výdajok. Vznikajú pri mazaní rozpracovaných dokladov a môžu byť znovu použité.

## Btrieve súbor

`OMHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OMHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy výdajok |
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
| BookNum | OMBLST.BookNum | Kniha výdajok |

## Použitie

- Evidencia voľných čísel pre opätovné použitie
- Zachovanie kontinuity číslovania
- Audit mazania dokladov

## Business pravidlá

- Pri vytváraní novej výdajky sa najprv hľadá voľné číslo v OMHOLE
- Ak existuje voľné číslo, použije sa a odstráni z OMHOLE
- Ak neexistuje, vygeneruje sa nové poradové číslo
- Pri zmazaní neuzatvorenej výdajky sa jej číslo zapíše do OMHOLE

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
