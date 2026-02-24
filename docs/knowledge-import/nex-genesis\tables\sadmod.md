# SADMOD - Modifikované doklady na prepočet

## Kľúčové slová / Aliases

SADMOD, SADMOD.BTR, modifikované, doklady, prepočet

## Popis

Pomocná tabuľka evidujúca doklady MO predaja, ktoré boli modifikované a vyžadujú prepočet. Slúži pre optimalizáciu - prepočítavajú sa len zmenené doklady.

## Btrieve súbor

`SADMOD.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SADMOD.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → SAH.DocNum** |
| ModUser | Str8 | 9 | Používateľ modifikácie |
| ModDate | DateType | 4 | Dátum modifikácie |
| ModTime | TimeType | 4 | Čas modifikácie |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit, Case insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | SAH.DocNum | Hlavička dokladu |

## Použitie

- Fronta na prepočet
- Optimalizácia spracovania
- Audit zmien

## Business pravidlá

- Záznam sa vytvorí pri modifikácii dokladu
- Po prepočte sa záznam vymaže
- Batch procesy spracovávajú záznamy z tejto tabuľky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
