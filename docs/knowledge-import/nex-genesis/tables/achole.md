# ACHOLE - Voľné čísla dokladov akciových precenení

## Kľúčové slová / Aliases

ACHOLE, ACHOLE.BTR, voľné, čísla, dokladov, akciových, precenení

## Popis

Pomocná tabuľka pre evidenciu voľných poradových čísiel dokladov akciových precenení. Slúži na opätovné využitie čísel zmazaných dokladov.

## Btrieve súbor

`ACHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACHOLE.BTR`

## Štruktúra polí (7 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy ACP |
| SerNum | longint | 4 | Poradové číslo ACP |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum, SerNum | BnSn | Duplicit |

## Použitie

- Evidencia voľných čísel po zmazaní dokladu
- Opätovné prideľovanie čísel novým dokladom
- Zachovanie kontinuity číselného radu

## Business pravidlá

- Pri zmazaní dokladu sa SerNum pridá do ACHOLE
- Pri vytvorení nového dokladu sa najprv hľadá voľné číslo
- Ak nie je voľné číslo, použije sa nasledujúce v poradí

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
