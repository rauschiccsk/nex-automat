# IMPLST - Zoznam vykonaných importov

## Kľúčové slová / Aliases

IMPLST, IMPLST.BTR, zoznam, vykonaných, importov

## Popis

Tabuľka evidencie vykonaných importov do interných príjemok. Sleduje históriu importovaných súborov pre auditné účely.

## Btrieve súbor

`IMPLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMPLST.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ImpNum | word | 2 | Poradové číslo importu - **PRIMARY KEY** |
| ImpNam | Str30 | 31 | Názov importovaného súboru |
| ImpUsr | Str8 | 9 | Používateľ importu |
| ImpDat | DateType | 4 | Dátum importu |
| ImpTim | TimeType | 4 | Čas importu |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | ImpNum | ImpNum | Unique |
| 1 | ImpNam | ImpNam | Duplicit, Case insensitive |
| 2 | ImpDat | ImpDat | Duplicit |

## Použitie

- Evidencia importovaných súborov
- Prevencia duplicitného importu
- Auditný záznam importov
- Sledovanie histórie importov

## Business pravidlá

- Každý import sa zaznamenáva
- Umožňuje kontrolu či súbor už bol importovaný
- Používa sa pre importy z elektronických váh, CSV, EDI

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
