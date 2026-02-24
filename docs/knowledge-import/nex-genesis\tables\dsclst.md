# DSCLST - Zoznam typov zliav

## Kľúčové slová / Aliases

DSCLST, DSCLST.BTR, zoznam, typov, zliav

## Popis

Číselník typov zliav používaných pri predaji. Definuje možné zľavy, ktoré sa môžu aplikovať na položky alebo doklady.

## Btrieve súbor

`DSCLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\DSCLST.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscType | Str1 | 2 | Typové označenie zľavy - **PRIMARY KEY** |
| DscName | Str30 | 31 | Názov zľavy |
| _DscName | Str30 | 31 | Názov zľavy - vyhľadávacie pole |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DscType | DscType | Unikátny |
| 1 | _DscName | DscName | Duplicit |

## Príklady typov zliav

| DscType | DscName |
|---------|---------|
| A | Akciová zľava |
| M | Množstevná zľava |
| V | Vernostná zľava |
| Z | Zamestnanecká zľava |
| S | Sezónna zľava |

## Použitie

- Číselník zliav pre predajné doklady
- Kategorizácia zliav
- Výber zľavy pri zadávaní dokladu

## Business pravidlá

- DscType je jednoznakový kód pre rýchle zadávanie
- Zľavy sa aplikujú na položky alebo celé doklady
- Používa sa pri tvorbe odberateľských dokladov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
