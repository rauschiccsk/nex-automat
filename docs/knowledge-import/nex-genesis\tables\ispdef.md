# ISPDEF - Definícia období splatnosti DF

## Kľúčové slová / Aliases

ISPDEF, ISPDEF.BTR, predvolby príjemiek, receipt defaults, šablóny príjmu

## Popis

Číselník pre definíciu intervalov splatnosti dodávateľských faktúr. Používa sa pri analýze záväzkov podľa doby po splatnosti.

## Btrieve súbor

`ISPDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISPDEF.BTR`

## Polia (9)

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

- Analýza záväzkov podľa splatnosti
- Výkaz Aging (veková štruktúra záväzkov)
- Plánovanie cash-flow
- Upomienanie dodávateľov

## Business pravidlá

- Intervaly sa definujú v dňoch od dátumu splatnosti
- Záporné hodnoty = pred splatnosťou
- Kladné hodnoty = po splatnosti
- Intervaly by mali pokrývať celý rozsah bez prekrytia

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
