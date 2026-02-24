# CASLST - Zoznam elektronických registračných pokladníc

## Kľúčové slová / Aliases

CASLST, CASLST.BTR, zoznam, elektronických, registračných, pokladníc

## Popis

Tabuľka zoznamu elektronických registračných pokladníc. Jednoduchý register pokladníc používaný pre základnú identifikáciu. Globálny súbor.

## Btrieve súbor

`CASLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CASLST.BTR`

## Štruktúra polí (6 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CasNum | word | 2 | Číslo pokladne |
| CasName | Str30 | 31 | Pomenovanie pokladne |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CasNum | CasNum | Duplicit |

## Príklad

```
CasNum  = 1
CasName = "Hlavná pokladňa"

CasNum  = 2
CasName = "Pokladňa - Bar"

CasNum  = 3
CasName = "Pokladňa - Terasa"
```

## Použitie

- Základný register pokladníc
- Identifikácia pokladníc v systéme
- Prepojenie s CABLST (rozšírená konfigurácia)

## Business pravidlá

- CasNum je unikátne číslo pokladne
- Táto tabuľka je jednoduchšia verzia, CABLST obsahuje rozšírenú konfiguráciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
