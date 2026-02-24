# OST - Väzby na dodacie listy

## Kľúčové slová / Aliases

OST, OST.BTR, objednávky termíny, order terms, dodacie termíny

## Popis

Tabuľka prepojení položiek dodávateľských objednávok s dodacími listami príjmu (DDL). Sleduje, ktoré položky objednávky boli dodané ktorým dodacím listom.

## Btrieve súbor

`OSTyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSTyynnn.BTR`

## Štruktúra polí (13 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo objednávky - **FK → OSH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky objednávky |
| TsdNum | Str12 | 13 | Číslo dodacieho listu - **FK → TSH.DocNum** |
| TsdItm | word | 2 | Riadok dodacieho listu |

### Údaje o dodávke

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsdDate | DateType | 4 | Dátum dodacieho listu |
| GsCode | longint | 4 | Tovarové číslo |
| DlvQnt | double | 8 | Dodané množstvo |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, TsdNum, TsdItm | DoItTdTi | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OSH.DocNum | Hlavička objednávky |
| TsdNum | TSH.DocNum | Dodací list príjmu |
| GsCode | GSCAT.GsCode | Tovar |

## Workflow

```
1. Položka objednávky (OSI)
   ↓
2. Príjem tovaru - vytvorenie DDL (TSH/TSI)
   ↓
3. Zápis väzby do OST
   ↓
4. Aktualizácia OSI.DlvQnt, OSI.StkStat
```

## Business pravidlá

- Jedna položka objednávky môže byť dodaná viacerými DDL (čiastočné dodávky)
- Jeden DDL môže obsahovať položky z viacerých objednávok
- DlvQnt v OST = množstvo dodané konkrétnym DDL pre danú položku

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
