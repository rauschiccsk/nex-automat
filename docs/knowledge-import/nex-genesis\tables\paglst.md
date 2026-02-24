# PAGLST - Skupiny partnerov

## Kľúčové slová / Aliases

PAGLST, PAGLST.BTR, skupiny partnerov, partner groups, kategórie partnerov

## Popis

Číselník triediacich skupín partnerov. Umožňuje kategorizovať partnerov do skupín pre reporting a filtre.

## Btrieve súbor

`PAGLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PAGLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PagCode | word | 2 | Číslo skupiny - **PRIMARY KEY** |
| PagName | Str30 | 31 | Názov skupiny |
| _PagName | Str20 | 21 | Vyhľadávacie pole názvu |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PagCode | PagCode | Duplicit |
| 1 | _PagName | PagName | Case-insensitive, Duplicit |

## Použitie

Skupina sa priraďuje partnerom cez polia:
- `PAB.PagCode` - skupina dodávateľov
- `PAB.PgcCode` - skupina odberateľov

## Príklady skupín

| PagCode | PagName | Popis |
|---------|---------|-------|
| 1 | Veľkoobchod | Veľkoobchodní dodávatelia |
| 2 | Maloobchod | Maloobchodní partneri |
| 3 | Výrobcovia | Priami výrobcovia |
| 4 | Distribútori | Distribučné spoločnosti |
| 5 | Reťazce | Obchodné reťazce |

## Business pravidlá

- Jeden partner môže patriť do jednej skupiny dodávateľov a jednej skupiny odberateľov
- Používa sa pre agregované výkazy a filtre
- _PagName je uppercase verzia pre case-insensitive vyhľadávanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
