# RMHOLE - Voľné poradové čísla medziskladových presunov

## Kľúčové slová / Aliases

RMHOLE, RMHOLE.BTR, voľné, poradové, čísla, medziskladových, presunov

## Popis

Tabuľka voľných (uvoľnených) poradových čísel medziskladových presunov. Vznikajú pri mazaní rozpracovaných dokladov a môžu byť znovu použité.

## Btrieve súbor

`RMHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\RMHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy presunov |
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
| BookNum | RMBLST.BookNum | Kniha presunov |

## Použitie

- Evidencia voľných čísel pre opätovné použitie
- Zachovanie kontinuity číslovania
- Audit mazania dokladov

## Business pravidlá

- Pri vytváraní nového presunu sa najprv hľadá voľné číslo v RMHOLE
- Ak existuje voľné číslo, použije sa a odstráni z RMHOLE
- Ak neexistuje, vygeneruje sa nové poradové číslo
- Pri zmazaní nezrealizovaného presunu sa jeho číslo zapíše do RMHOLE

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
