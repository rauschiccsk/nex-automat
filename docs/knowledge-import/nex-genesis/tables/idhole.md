# IDHOLE - Voľné poradové čísla interných dokladov

## Kľúčové slová / Aliases

IDHOLE, IDHOLE.BTR, voľné, poradové, čísla, interných, dokladov

## Popis

Tabuľka voľných (uvoľnených) poradových čísel interných účtovných dokladov. Vznikajú pri mazaní rozpracovaných dokladov a môžu byť znovu použité.

## Btrieve súbor

`IDHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IDHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy dokladov |
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
| BookNum | IDBLST.BookNum | Kniha dokladov |

## Použitie

- Evidencia voľných čísel pre opätovné použitie
- Zachovanie kontinuity číslovania
- Audit mazania dokladov

## Business pravidlá

- Pri vytváraní nového dokladu sa najprv hľadá voľné číslo v IDHOLE
- Ak existuje voľné číslo, použije sa a odstráni z IDHOLE
- Ak neexistuje, vygeneruje sa nové poradové číslo
- Pri zmazaní neuzatvoreného dokladu sa jeho číslo zapíše do IDHOLE

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
