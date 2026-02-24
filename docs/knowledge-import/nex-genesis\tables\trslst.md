# TRSLST - Spôsoby dopravy

## Kľúčové slová / Aliases

TRSLST, TRSLST.BTR, dopravcovia, transporters, spôsoby dopravy, szállítók

## Popis

Číselník spôsobov dopravy. Definuje možnosti prepravy tovaru pri objednávkach a dodávkach.

## Btrieve súbor

`TRPLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\TRPLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TrsCode | Str3 | 4 | Kód spôsobu dopravy - **PRIMARY KEY** |
| TrsName | Str30 | 31 | Názov spôsobu dopravy |
| _TrsName | Str20 | 21 | Vyhľadávacie pole názvu |
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | TrsCode | TrsCode | Duplicit |
| 1 | _TrsName | TrsName | Case-insensitive, Duplicit |
| 2 | Sended | Sended | Duplicit |

## Príklady dát

| TrsCode | TrsName | Popis |
|---------|---------|-------|
| VLA | Vlastná doprava | Vlastné vozidlo zákazníka |
| KUR | Kuriér | Kuriérska služba |
| POS | Pošta | Slovenská pošta |
| DHL | DHL | DHL Express |
| GLS | GLS | GLS kuriér |
| PPL | PPL | PPL CZ |
| ZAS | Zásielkovňa | Zásielkovňa.sk |
| OSO | Osobný odber | Vyzdvihnutie na predajni |

## Použitie

Spôsob dopravy sa priraďuje:
- `PAB.IsTrsCode` - preferovaná doprava od dodávateľa
- `PAB.IcTrsCode` - preferovaná doprava pre odberateľa
- `PASUBC.TrsCode` - doprava na konkrétnu prevádzku
- Používa sa aj na objednávkach a dodacích listoch

## Business pravidlá

- TrsCode je krátka skratka (max 3 znaky)
- _TrsName je uppercase pre case-insensitive vyhľadávanie
- Sended slúži na synchronizáciu zmien cez FTP

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
