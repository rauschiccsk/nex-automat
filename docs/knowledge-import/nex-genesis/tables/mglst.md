# MGLST - Tovarové skupiny

## Kľúčové slová / Aliases

MGLST, MGLST.BTR, tovarové skupiny, merchandise groups, produktové kategórie, kategorizácia

## Popis
Hierarchický zoznam tovarových skupín. Umožňuje kategorizáciu tovaru do stromovej štruktúry pomocou poľa Parent.

## Btrieve súbor
`MGLST.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\MGLST.BTR`

## Veľkosť záznamu
~134-200+ bytes (závisí od verzie)

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | longint | 4 | Číselný kód tovarovej skupiny - **PRIMARY KEY** |
| MgName | Str30 | 31 | Názov tovarovej skupiny |
| _MgName | Str15 | 16 | Vyhľadávacie pole názvu |
| Profit | double | 8 | Doporučený zisk predaja (%) |
| Parent | longint | 4 | Kód nadradenej skupiny (0 = hlavná skupina) |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |
| PrfPrc1 | double | 8 | Doporučený zisk pre cenu D1 |
| PrfPrc2 | double | 8 | Doporučený zisk pre cenu D2 |
| PrfPrc3 | double | 8 | Doporučený zisk pre cenu D3 |
| DscPrc1 | double | 8 | Percentuálna zľava pre cenu D1 |
| DscPrc2 | double | 8 | Percentuálna zľava pre cenu D2 |
| DscPrc3 | double | 8 | Percentuálna zľava pre cenu D3 |
| Eshop1 | byte | 1 | Internetový obchod č.1 |
| Eshop2 | byte | 1 | Internetový obchod č.2 |
| Eshop3 | byte | 1 | Internetový obchod č.3 |
| Eshop4 | byte | 1 | Internetový obchod č.4 |
| Eshop5 | byte | 1 | Internetový obchod č.5 |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | MgCode | MgCode | Duplicit |
| 1 | _MgName | MgName | Case-insensitive, Duplicit |
| 2 | Profit | Profit | Duplicit |
| 3 | Parent | Parent | Duplicit |
| 4 | Sended | Sended | Duplicit |
| 5 | Eshop1 | Eshop1 | Duplicit |
| 6 | Eshop2 | Eshop2 | Duplicit |
| 7 | Eshop3 | Eshop3 | Duplicit |
| 8 | Eshop4 | Eshop4 | Duplicit |
| 9 | Eshop5 | Eshop5 | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| Parent | MGLST.MgCode | Nadradená skupina (self-reference) |

## Hierarchická štruktúra

```
Parent = 0  → Hlavná (root) skupina
Parent > 0  → Podskupina (child)
```

Príklad:
```
MgCode=1, Parent=0, MgName="Potraviny"        # Root
MgCode=10, Parent=1, MgName="Mliečne výrobky" # Child of 1
MgCode=11, Parent=1, MgName="Pečivo"          # Child of 1
MgCode=100, Parent=10, MgName="Jogurty"       # Child of 10
```

## Stav migrácie

- [x] Model vytvorený (`packages/nexdata/nexdata/models/mglst.py`)
- [x] Kamenický dekódovanie
- [ ] PostgreSQL model
- [ ] API endpoint
- [ ] Stromové zobrazenie (PySide6)
