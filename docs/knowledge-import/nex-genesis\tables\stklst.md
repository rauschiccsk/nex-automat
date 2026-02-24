# STKLST - Zoznam skladov

## Kľúčové slová / Aliases

STKLST, STKLST.BTR, zoznam skladov, warehouse list, evidencia skladov, raktárak

## Popis

Číselník skladov. Definuje dostupné sklady v systéme a ich vlastnosti.

## Btrieve súbor

`STKLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STORES\STKLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu - **PRIMARY KEY** |
| StkName | Str30 | 31 | Názov skladu |
| _StkName | Str15 | 16 | Vyhľadávacie pole názvu |
| StkType | Str1 | 2 | Typ skladu (T=tovarový, M=materiálový, V=výrobný) |
| IvDate | DateType | 4 | Dátum poslednej uzatvorenej inventúry |
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| PlsNum | word | 2 | Číslo pripojeného cenníka |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StkNum | StkNum | Duplicit |
| 1 | _StkName | StkName | Duplicit |

## Typy skladov

| StkType | Popis |
|---------|-------|
| T | Tovarový sklad |
| M | Materiálový sklad |
| V | Výrobný sklad |

## Multi-warehouse architektúra

Číslo skladu (StkNum) určuje názvy súborov:
- `STKxxxxx.BTR` - skladové karty
- `STMxxxxx.BTR` - skladové pohyby
- `FIFxxxxx.BTR` - FIFO karty
- `STBxxxxx.BTR` - počiatočné stavy
- `STSxxxxx.BTR` - rezervácie predaja

## Príklad dát

| StkNum | StkName | StkType | WriNum | PlsNum |
|--------|---------|---------|--------|--------|
| 1 | Hlavný sklad | T | 1 | 1 |
| 2 | Predajňa BA | T | 2 | 1 |
| 3 | Materiálový sklad | M | 1 | 0 |
| 4 | Výroba | V | 1 | 0 |

## Business pravidlá

- StkNum musí byť unikátne
- WriNum prepája sklad s prevádzkou
- PlsNum prepája sklad s cenníkom
- Shared=1 synchronizuje zmeny na pobočky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
