# CSYLST - Zoznam konštantných symbolov

## Kľúčové slová / Aliases

CSYLST, CSYLST.BTR, zoznam, konštantných, symbolov

## Popis

Číselník konštantných symbolov používaných pri platobnom styku.

## Btrieve súbor

`CSYLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSYLST.BTR`

## Štruktúra polí (6 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CsyCode | Str4 | 5 | Konštantný symbol - **PRIMARY KEY** |
| CsyName | Str60 | 61 | Názov konštantného symbolu |
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CsyCode | CsyCode | Duplicit |

## Príklady konštantných symbolov

| CsyCode | CsyName |
|---------|---------|
| 0008 | Platba za tovar |
| 0108 | Platba za služby |
| 0308 | Platba za práce |
| 0558 | Záloha |
| 1148 | Úhrada faktúry |

## Použitie

- Identifikácia typu platby
- Štandardné bankové symboly SR
- Výber pri zadávaní platieb

## Business pravidlá

- 4-miestny kód podľa bankových štandardov
- Používa sa pri platobnom styku
- Povinný údaj pri niektorých typoch platieb

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
