# CTYLST - Zoznam miest a obcí

## Kľúčové slová / Aliases

CTYLST, CTYLST.BTR, mestá, obce, cities, towns, zoznam miest, PSČ, ZIP codes

## Popis

Číselník miest a obcí. Obsahuje PSČ a telefónne predvoľby pre jednotlivé sídla v rámci štátov.

## Btrieve súbor

`CTYLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\CTYLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CtyCode | Str3 | 4 | Skratka obce - **PRIMARY KEY** |
| StaCode | Str2 | 3 | Kód štátu - **FK → STALST** |
| CtyName | Str30 | 31 | Názov obce |
| _CtyName | Str30 | 31 | Vyhľadávacie pole názvu |
| ZipCode | Str15 | 16 | PSČ |
| CtyTel | Str6 | 7 | Telefónna predvoľba obce |
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
| 0 | CtyCode | CtyCode | Case-insensitive, Duplicit |
| 1 | CtyCode, StaCode | CcSc | Case-insensitive, Duplicit |
| 2 | _CtyName | CtyName | Case-insensitive, Duplicit |
| 3 | ZipCode | ZipCode | Case-insensitive, Duplicit |
| 4 | CtyTel | CtyTel | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StaCode | STALST.StaCode | Štát |

## Príklady dát

| CtyCode | StaCode | CtyName | ZipCode | CtyTel |
|---------|---------|---------|---------|--------|
| BA | SK | Bratislava | 811 01 | 02 |
| KE | SK | Košice | 040 01 | 055 |
| ZA | SK | Žilina | 010 01 | 041 |
| BB | SK | Banská Bystrica | 974 01 | 048 |
| NR | SK | Nitra | 949 01 | 037 |

## Použitie

Mesto sa priraďuje na adresách partnerov:
- `PAB.RegCty` - mesto registrovanej adresy
- `PAB.CrpCty` - mesto korešpondenčnej adresy
- `PAB.IvcCty` - mesto fakturačnej adresy
- `PASUBC.WpaCty` - mesto prevádzky
- `PACNTC.RsdCtc` - mesto trvalého pobytu kontaktu

## Business pravidlá

- CtyCode je unikátny v rámci štátu
- Composite index CcSc umožňuje rovnaký CtyCode v rôznych štátoch
- ZipCode môže obsahovať medzery (formát SR: "XXX XX")
- _CtyName je uppercase pre case-insensitive vyhľadávanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
