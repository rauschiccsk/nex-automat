# OSPLST - Zoznam dodávateľov pre objednávky

## Kľúčové slová / Aliases

OSPLST, OSPLST.BTR, zoznam partnerov objednávok, PO partners list

## Popis

Pomocná tabuľka zoznamu dodávateľov pre objednávkový systém. Obsahuje agregované údaje o dodávateľoch a ich dodávkach.

## Btrieve súbor

`OSPLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSPLST.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód dodávateľa - **PRIMARY KEY** |
| PaName | Str60 | 61 | Názov dodávateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole |
| GstCnt | longint | 4 | Počet dodávaných tovarov |
| OrdCoef | double | 8 | Koeficient výpočtu objednacieho množstva |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode | PaCode | Duplicit |
| 1 | _PaName | PaName | Duplicit, Case insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner (dodávateľ) |

## Použitie

- Rýchly výber dodávateľa pri objednávkach
- Štatistiky dodávateľov
- Nastavenie koeficientov objednávania

## Business pravidlá

- GstCnt sa aktualizuje pri evidencii nových produktov od dodávateľa
- OrdCoef ovplyvňuje automatický výpočet objednacieho množstva

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
