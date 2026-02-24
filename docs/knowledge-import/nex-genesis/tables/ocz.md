# OCZ - Zálohy k zákazkám

## Kľúčové slová / Aliases

OCZ, OCZ.BTR, objednávky zálohy, order deposits, zálohové platby

## Popis

Tabuľka zálohových platieb k odberateľským zákazkám. Sleduje prijaté zálohy a ich čerpanie.

## Btrieve súbor

`OCZyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCZyynnn.BTR`

## Štruktúra polí (12 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo zákazky - **FK → OCH.DocNum** |
| ItmNum | word | 2 | Poradové číslo zálohy |
| DepDate | DateType | 4 | Dátum prijatia zálohy |
| DepType | Str1 | 2 | Typ zálohy (C=cash, B=bank, K=card) |
| AcDvzName | Str3 | 4 | Účtovná mena |
| AcDepVal | double | 8 | Hodnota zálohy v účtovnej mene |
| FgDvzName | Str3 | 4 | Mena zálohy |
| FgDepVal | double | 8 | Hodnota zálohy v mene zálohy |
| FgCourse | double | 8 | Kurz |
| ConDoc | Str12 | 13 | Číslo príjmového dokladu |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unique |
| 1 | DepDate | DepDate | Duplicit |
| 2 | ConDoc | ConDoc | Case-insensitive, Duplicit |
| 3 | DepType | DepType | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCH.DocNum | Hlavička zákazky |
| ConDoc | CPH.DocNum | Príjmový pokladničný doklad |

## Typy zálohy

| Hodnota | Popis |
|---------|-------|
| C | Hotovosť (Cash) |
| B | Bankový prevod |
| K | Platobná karta |

## Workflow

```
1. Prijatie objednávky
   ↓
2. Výpočet požadovanej zálohy (DepPrc z OCH/OCBLST)
   ↓
3. Prijatie zálohy (A_DepRcv)
   ↓
4. Zápis do OCZ
   ↓
5. Aktualizácia OCH.AcDepVal/FgDepVal
   ↓
6. Generovanie zálohovej faktúry (PCD)
   ↓
7. Pri vyúčtovaní - odpočet zálohy od faktúry
```

## Business pravidlá

- Jedna zákazka môže mať viac zálohových platieb
- Zálohy sa sčítavajú do OCH.AcDepVal/FgDepVal
- Pri vystavení faktúry sa zálohy odpočítavajú
- Multi-mena podpora

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
