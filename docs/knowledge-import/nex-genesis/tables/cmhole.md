# CMHOLE - Voľné poradové čísla kompletizácie

## Kľúčové slová / Aliases

CMHOLE, CMHOLE.BTR, voľné, poradové, čísla, kompletizácie

## Popis

Evidencia voľných (uvoľnených) poradových čísiel kompletizačných dokladov. Vznikajú pri mazaní dokladov a môžu byť znovu použité.

## Btrieve súbor

`CMHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\CMHOLE.BTR`

## Štruktúra polí (5 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | word | 2 | Číslo knihy - **FK** |
| SerNum | longint | 4 | Voľné poradové číslo |

### Doplňujúce

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Účtovný rok |
| DelDate | DateType | 4 | Dátum zmazania dokladu |
| DelUser | Str8 | 9 | Používateľ, ktorý zmazal doklad |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum, SerNum | BookSer | Unikátny |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BookNum | CMBLST.BookNum | Kniha dokladov |

## Použitie

- Evidencia uvoľnených čísel
- Opätovné použitie čísel (voliteľné)
- Audit zmazaných dokladov

## Business pravidlá

- Pri zmazaní dokladu sa číslo pridá do CMHOLE
- Pri vytvorení nového dokladu môže systém ponúknuť číslo z CMHOLE
- DelDate/DelUser slúžia pre audit

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
