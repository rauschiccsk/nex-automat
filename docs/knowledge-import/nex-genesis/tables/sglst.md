# SGLST - Špecifikačné skupiny

## Kľúčové slová / Aliases

SGLST, SGLST.BTR, servisné skupiny, service groups, skupiny služieb

## Popis
Zoznam špecifikačných skupín. Doplnková kategorizácia tovaru podľa vlastností (napr. bio produkty, bezlepkové, vegánske).

## Btrieve súbor
`SGLST.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\SGLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SgCode | longint | 4 | Číselný kód špecifikačnej skupiny - **PRIMARY KEY** |
| SgName | Str50 | 51 | Názov špecifikačnej skupiny |
| _SgName | Str50 | 51 | Vyhľadávacie pole názvu |
| CrtUser | Str8 | 9 | Používateľ vytvorenia záznamu |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SgCode | SgCode | Unique |
| 1 | _SgName | SgName | Case-insensitive, Duplicit |

## Relácie

Používané v:
- GSCAT.SgCode - tovar môže patriť do špecifikačnej skupiny

## Príklady použitia

- BIO produkty
- Bezlepkové výrobky
- Vegánske produkty
- Lokálni výrobcovia
- Akciový tovar

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model
- [ ] API endpoint
