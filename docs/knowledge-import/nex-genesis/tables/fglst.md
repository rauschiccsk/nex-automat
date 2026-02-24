# FGLST - Finančné skupiny

## Kľúčové slová / Aliases

FGLST, FGLST.BTR, finančné skupiny, financial groups, účtovné skupiny

## Popis
Zoznam finančných skupín. Slúži na kategorizáciu tovaru z pohľadu marže, zľavy a účtovania.

## Btrieve súbor
`FGLST.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\FGLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgCode | longint | 4 | Číselný kód finančnej skupiny - **PRIMARY KEY** |
| FgName | Str30 | 31 | Názov finančnej skupiny |
| _FgName | Str20 | 21 | Vyhľadávacie pole názvu |
| Describe | Str150 | 151 | Podrobný popis finančnej skupiny |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |
| MaxDsc | double | 8 | Maximálna hodnota zľavy (%) |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |
| MinPrf | double | 8 | Minimálna obchodná marža (%) |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | FgCode | FgCode | Duplicit |
| 1 | _FgName | FgName | Case-insensitive, Duplicit |
| 2 | Sended | Sended | Duplicit |

## Relácie

Používané v:
- GSCAT.FgCode - každý tovar patrí do finančnej skupiny

## Business pravidlá

- **MaxDsc**: Maximálna zľava, ktorú je možné poskytnúť na tovar v tejto skupine
- **MinPrf**: Minimálna marža, pod ktorú nesmie klesnúť predajná cena

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model
- [ ] API endpoint
