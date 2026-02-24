# SABLST - Zoznam kníh ERP predaja

## Kľúčové slová / Aliases

SABLST, SABLST.BTR, zoznam, kníh, erp, predaja

## Popis

Konfiguračná tabuľka kníh skladových výdajok maloobchodného predaja. Definuje prepojenia na sklady, pokladne a kalkulácie výrobkov.

## Btrieve súbor

`SABLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SABLST.BTR`

## Štruktúra polí (18 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Pomenovanie oddelenia/pokladne |

### Prevádzka a sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| StkNum | word | 2 | Číslo prednastaveného skladu |
| StkDet | byte | 1 | Spôsob určenia skladu výdaja |

### Prepojené knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CsdBook | Str5 | 6 | Kniha HP - zaúčtovanie tržby |
| IdpBook | Str5 | 6 | Kniha ID - preúčtovanie platobných kariet |
| CpiBook | Str5 | 6 | Kniha kalkulácií výrobkov (receptúr) |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| StkNum | STKLST.StkNum | Sklad |
| CsdBook | CSDLST.BookNum | Kniha hotovostnej pokladne |
| IdpBook | IDBLST.BookNum | Kniha interných dokladov |
| CpiBook | CPILST.BookNum | Kniha kalkulácií |

## Použitie

- Konfigurácia ERP pokladní
- Mapovanie pokladňa → sklad
- Prepojenie na účtovné knihy
- Nastavenie zdieľania údajov

## Business pravidlá

- Jedna kniha = jedna ERP pokladňa/oddelenie
- CsdBook určuje kam sa účtuje tržba
- CpiBook určuje odkiaľ sa berú receptúry
- Shared=1 pre synchronizáciu s centrálou

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
