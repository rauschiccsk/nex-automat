# CSHOLE - Voľné poradové čísla hotovostných dokladov

## Kľúčové slová / Aliases

CSHOLE, CSHOLE.BTR, voľné, poradové, čísla, hotovostných, dokladov

## Popis

Tabuľka voľných (uvoľnených) poradových čísel hotovostných dokladov. Vznikajú pri mazaní rozpracovaných dokladov a môžu byť znovu použité.

## Btrieve súbor

`CSHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy HP |
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
| BookNum | CSBLST.BookNum | Kniha pokladne |

## Použitie

- Evidencia voľných čísel pre opätovné použitie
- Zachovanie kontinuity číslovania
- Audit mazania dokladov

## Business pravidlá

- Pri vytváraní nového dokladu sa najprv hľadá voľné číslo v CSHOLE
- Ak existuje voľné číslo, použije sa a odstráni z CSHOLE
- Ak neexistuje, vygeneruje sa nové poradové číslo
- Pri zmazaní neuzatvoreného dokladu sa jeho číslo zapíše do CSHOLE

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
