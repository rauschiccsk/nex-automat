# STALST - Zoznam štátov

## Kľúčové slová / Aliases

STALST, STALST.BTR, štáty, krajiny, countries, states, zoznam krajín, országok

## Popis

Číselník štátov/krajín. Obsahuje medzinárodné kódy, telefónne predvoľby a údaje o menách.

## Btrieve súbor

`STALST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\STALST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StaCode | Str2 | 3 | Medzinárodný kód štátu (ISO 3166-1 alpha-2) - **PRIMARY KEY** |
| StaName | Str30 | 31 | Názov štátu |
| _StaName | Str30 | 31 | Vyhľadávacie pole názvu |
| StaTel | Str6 | 7 | Medzinárodná telefónna predvoľba |
| DvzName | Str3 | 4 | Kód meny (ISO 4217) |
| CryName | Str30 | 31 | Celý názov meny |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StaCode | StaCode | Case-insensitive, Duplicit |
| 1 | _StaName | StaName | Case-insensitive, Duplicit |
| 2 | StaTel | StaTel | Duplicit |
| 3 | DvzName | DvzName | Case-insensitive, Duplicit |

## Príklady dát

| StaCode | StaName | StaTel | DvzName | CryName |
|---------|---------|--------|---------|---------|
| SK | Slovensko | +421 | EUR | Euro |
| CZ | Česká republika | +420 | CZK | Česká koruna |
| AT | Rakúsko | +43 | EUR | Euro |
| HU | Maďarsko | +36 | HUF | Maďarský forint |
| PL | Poľsko | +48 | PLN | Poľský zlotý |
| DE | Nemecko | +49 | EUR | Euro |

## Použitie

Štát sa priraďuje na adresách partnerov:
- `PAB.RegSta` - štát registrovanej adresy
- `PAB.CrpSta` - štát korešpondenčnej adresy
- `PAB.IvcSta` - štát fakturačnej adresy
- `PASUBC.WpaSta` - štát prevádzky
- `PACNTC.RsdStc` - štát trvalého pobytu kontaktu

## Business pravidlá

- StaCode je ISO 3166-1 alpha-2 (2-písmenový kód)
- StaTel obsahuje medzinárodnú predvoľbu vrátane "+"
- DvzName je ISO 4217 kód meny
- _StaName je uppercase pre case-insensitive vyhľadávanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
