# ICPDEF - Definícia období splatnosti OF

## Kľúčové slová / Aliases

ICPDEF, ICPDEF.BTR, predvolby faktúr, invoice defaults, šablóny

## Popis

Číselník pre definíciu intervalov splatnosti odberateľských faktúr. Používa sa pri analýze pohľadávok podľa doby po splatnosti (Aging report).

## Btrieve súbor

`ICPDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICPDEF.BTR`

## Štruktúra polí (9 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | word | 2 | Poradové číslo intervalu - **PRIMARY KEY** |
| Describe | Str60 | 61 | Textový popis intervalu |
| BegDqt | longint | 4 | Začiatok obdobia (dni) |
| EndDqt | longint | 4 | Koniec obdobia (dni) |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SerNum | SerNum | Duplicit |

## Príklad definícií

| SerNum | Describe | BegDqt | EndDqt |
|--------|----------|--------|--------|
| 1 | Pred splatnosťou | -9999 | -1 |
| 2 | Splatné | 0 | 0 |
| 3 | Po splatnosti 1-30 dní | 1 | 30 |
| 4 | Po splatnosti 31-60 dní | 31 | 60 |
| 5 | Po splatnosti 61-90 dní | 61 | 90 |
| 6 | Po splatnosti nad 90 dní | 91 | 9999 |

## Použitie

- Analýza pohľadávok podľa splatnosti
- Výkaz Aging (veková štruktúra pohľadávok)
- Plánovanie cash-flow
- Určenie eskalácie upomienok

## Business pravidlá

- Intervaly sa definujú v dňoch od dátumu splatnosti
- Záporné hodnoty = pred splatnosťou
- Kladné hodnoty = po splatnosti
- Intervaly by mali pokrývať celý rozsah bez prekrytia
- Používa sa pre automatické priradenie upomienok

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
