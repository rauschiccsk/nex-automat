# ISRLST - Réžijné položky dodávateľských faktúr

## Kľúčové slová / Aliases

ISRLST, ISRLST.BTR, reklamácie príjemiek, receipt claims, vrátený tovar

## Popis

Číselník réžijných (netovarových) položiek pre dodávateľské faktúry. Definuje štandardné položky ako doprava, balenie, poistenie a pod.

## Btrieve súbor

`ISRLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISRLST.BTR`

## Polia (16)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | word | 2 | Poradové číslo položky - **PRIMARY KEY** |
| IsrName | Str30 | 31 | Názov réžijnej položky |
| _IsrName | Str30 | 31 | Vyhľadávacie pole |
| CPrice | double | 8 | Jednotková cena bez DPH |
| VatPrc | byte | 1 | Percentuálna sadzba DPH |
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str6 | 7 | Analytický účet |
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SerNum | SerNum | Duplicit |
| 1 | _IsrName | IsrName | Duplicit |
| 2 | AccSnt, AccAnl | SntAnl | Duplicit |

## Príklady položiek

| SerNum | IsrName | VatPrc | AccSnt | AccAnl |
|--------|---------|--------|--------|--------|
| 1 | Doprava | 20 | 518 | 001 |
| 2 | Balné | 20 | 518 | 002 |
| 3 | Poistenie | 0 | 548 | 001 |
| 4 | Manipulačný poplatok | 20 | 518 | 003 |
| 5 | Clo | 0 | 538 | 001 |
| 6 | Ekologický príspevok | 20 | 518 | 004 |

## Použitie

- Rýchle vkladanie štandardných réžijných položiek
- Jednotné účtovné predkontácie pre réžie
- Správne zatriedenie DPH sadzby

## Business pravidlá

- Réžijné položky nie sú viazané na tovar (GsCode)
- Majú vlastné účtovné predkontácie
- Pri vložení na faktúru sa použije AccSnt + AccAnl pre účtovanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
