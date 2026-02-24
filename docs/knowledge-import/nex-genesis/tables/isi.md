# ISI - Položky dodávateľských faktúr

## Kľúčové slová / Aliases

ISI, ISI.BTR, príjemky položky, goods receipt items, prijaté položky

## Popis

Položková tabuľka dodávateľských faktúr. Obsahuje jednotlivé tovarové položky faktúr s množstvami, cenami a väzbami na dodacie listy.

## Btrieve súbor

`ISIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISIyynnn.BTR`

## Štruktúra polí (47 polí)

### Identifikácia položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum dokladu |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Čiarový kód |
| StkCode | Str15 | 16 | Skladový kód |
| Notice | Str30 | 31 | Poznámka |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvo a sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzky |
| StkNum | word | 2 | Číslo skladu |
| GsQnt | double | 8 | Prijaté množstvo |
| VatPrc | byte | 1 | Sadzba DPH % |
| DscPrc | double | 8 | Zľava % |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDValue | double | 8 | NC pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcCValue | double | 8 | NC bez DPH |
| AcEValue | double | 8 | NC s DPH |
| AcAValue | double | 8 | PC bez DPH |
| AcBValue | double | 8 | PC s DPH |

### Hodnoty v mene faktúry (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDPrice | double | 8 | NC/MJ pred zľavou |
| FgCPrice | double | 8 | NC/MJ bez DPH |
| FgEPrice | double | 8 | NC/MJ s DPH |
| FgDValue | double | 8 | NC pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgCValue | double | 8 | NC bez DPH |
| FgEValue | double | 8 | NC s DPH |

### Párovanie s dodacím listom

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód dodávateľa |
| OsdNum | Str12 | 13 | Číslo objednávky |
| OsdItm | word | 2 | Riadok objednávky |
| TsdNum | Str12 | 13 | Číslo dodacieho listu |
| TsdItm | word | 2 | Riadok dodacieho listu |
| TsdDate | DateType | 4 | Dátum dodacieho listu |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str8 | 9 | Analytický účet |
| Status | Str1 | 2 | Stav položky |
| Cctvat | byte | 1 | Prenesená daňová povinnosť |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit (Composite PK) |
| 1 | DocNum | DocNum | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | BarCode | BarCode | Case-insensitive, Duplicit |
| 4 | StkCode | StkCode | Case-insensitive, Duplicit |
| 5 | Status | Status | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ISH.DocNum | Hlavička faktúry |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| StkNum | STKLST.StkNum | Sklad |
| PaCode | PAB.PaCode | Dodávateľ |
| TsdNum | TSH.DocNum | Dodávateľský dodací list |
| OsdNum | OSH.DocNum | Objednávka |

## Väzba na dodacie listy

```
ISI.TsdNum → TSH.DocNum (hlavička DDL)
ISI.TsdNum + ISI.TsdItm → TSI (položka DDL)
```

## Business pravidlá

- Položka môže byť pripojená k dodaciemu listu (TsdNum)
- Pri párovaní sa hodnoty kopírujú z DDL
- Účtovanie používa AccSnt + AccAnl ako protiúčet

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
