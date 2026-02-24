# ISDSPC - Špecifikácie dodávateľských faktúr

## Kľúčové slová / Aliases

ISDSPC, ISDSPC.BTR, príjemky dispečing, receipt dispatch, expedícia

## Popis

Číselník špecifikácií dodávateľských faktúr. Definuje typy dokladov pre účely DPH evidencie a vykazovania.

## Btrieve súbor

`ISDSPC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISDSPC.BTR`

## Polia (12)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocSpc | word | 2 | Kód špecifikácie - **PRIMARY KEY** |
| SpcName | Str60 | 61 | Pomenovanie špecifikácie |
| VatSpc | byte | 1 | Špecifikácia pre evidenciu DPH |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocSpc | DocSpc | Unique |

## Príklady špecifikácií

| DocSpc | SpcName | VatSpc |
|--------|---------|--------|
| 0 | Bežná faktúra | 1 |
| 1 | Splátkový kalendár | 0 |
| 2 | JCD (colný doklad) | 1 |
| 3 | Preddavková faktúra | 0 |
| 4 | Interný doklad | 0 |

## Použitie

- Filtrovanie dokladov podľa typu
- Správne zaradenie do DPH evidencie
- Výkazy a prehľady podľa typu dokladu

## Business pravidlá

- VatSpc = 1 znamená, že doklad vstupuje do DPH evidencie
- VatSpc = 0 pre doklady, ktoré nie sú daňové doklady

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
