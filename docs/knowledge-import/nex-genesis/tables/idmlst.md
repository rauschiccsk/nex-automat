# IDMLST - Zoznam pohybov účtovných dokladov

## Kľúčové slová / Aliases

IDMLST, IDMLST.BTR, zoznam, pohybov, účtovných, dokladov

## Popis

Číselník pohybov (predkontácií) pre interné účtovné doklady. Definuje často používané účtovné operácie s preddefinovaným účtom a stranou.

## Btrieve súbor

`IDMLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IDMLST.BTR`

## Štruktúra polí (13 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IdmNum | word | 2 | Kód pohybu - **PRIMARY KEY** |
| IdmName | Str30 | 31 | Názov pohybu |
| _IdmName | Str30 | 31 | Vyhľadávacie pole názvu |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str6 | 7 | Analytický účet |
| AccSide | Str1 | 2 | Strana účtovania (C=Má dať, D=Dal) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | IdmNum | IdmNum | Duplicit |
| 1 | _IdmName | IdmName | Duplicit |
| 2 | AccSnt, AccAnl | SntAnl | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt+AccAnl | ACCLST | Účet |

## Strany účtovania (AccSide)

| Hodnota | Popis |
|---------|-------|
| C | Credit - Má dať (MD) |
| D | Debit - Dal |

## Použitie

- Predkontácie pre rýchle zadávanie
- Štandardizované účtovné operácie
- Zjednodušenie práce účtovníkov

## Príklady pohybov

| IdmNum | IdmName | AccSnt | AccAnl | AccSide |
|--------|---------|--------|--------|---------|
| 1 | Kurzový zisk | 663 | 001 | D |
| 2 | Kurzová strata | 563 | 001 | C |
| 3 | Odpis pohľadávky | 546 | 001 | C |
| 4 | Zápočet pohľadávok | 311 | xxx | D |
| 5 | Zápočet záväzkov | 321 | xxx | C |

## Business pravidlá

- Pohyb definuje účet a stranu účtovania
- Pri zadávaní položky stačí vybrať pohyb
- AccSide určuje či hodnota ide na stranu MD alebo Dal
- Umožňuje štandardizáciu účtovných operácií

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
