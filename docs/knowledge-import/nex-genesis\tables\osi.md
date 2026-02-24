# OSI - Položky dodávateľských objednávok

## Kľúčové slová / Aliases

OSI, OSI.BTR, objednávky odoslané položky, purchase order items, objednané položky

## Popis

Tabuľka položiek dodávateľských objednávok. Obsahuje údaje o objednanom tovare, množstvách, cenách a stave dodávky.

## Btrieve súbor

`OSIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSIyynnn.BTR`

## Štruktúra polí (56 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo objednávky - **FK → OSH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Tovarová skupina |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Čiarový kód |
| StkCode | Str15 | 16 | Skladový kód |
| Notice | Str30 | 31 | Poznámka k položke |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OrdQnt | double | 8 | Objednané množstvo |
| DlvQnt | double | 8 | Dodané množstvo |

### Fyzické vlastnosti

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Volume | double | 8 | Objem tovaru (m3) |
| Weight | double | 8 | Váha tovaru (kg) |

### Ceny a hodnoty - účtovná mena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH (%) |
| DscPrc | double | 8 | Zľava (%) |
| AcDValue | double | 8 | NC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcCValue | double | 8 | NC tovaru bez DPH |
| AcEValue | double | 8 | NC tovaru s DPH |
| AcAPrice | double | 8 | PC bez DPH |
| AcBPrice | double | 8 | PC s DPH |
| AcAValue | double | 8 | Hodnota v PC bez DPH |
| AcBValue | double | 8 | Hodnota v PC s DPH |

### Ceny a hodnoty - vyúčtovacia mena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDPrice | double | 8 | NC/MJ bez DPH pred zľavou |
| FgCPrice | double | 8 | NC/MJ bez DPH |
| FgEPrice | double | 8 | NC/MJ s DPH |
| FgDValue | double | 8 | NC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgRndVal | double | 8 | Hodnota zaokrúhlenia |
| FgCValue | double | 8 | NC bez DPH |
| FgEValue | double | 8 | PC s DPH po zľave |

### Termíny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum vystavenia objednávky |
| DlvDate | DateType | 4 | Termín dodávky |
| DlvNoti | Str30 | 31 | Poznámka k dodávke |
| FixDate | DateType | 4 | Fixný termín dodávky |
| CnfDate | DateType | 4 | Potvrdený termín dodávky |
| ChgDate | DateType | 4 | Zmenený termín dodávky |
| SupDate | DateType | 4 | Dodávateľom potvrdený termín |
| RatDay | longint | 4 | Počet dní dodávky |

### Väzby na iné doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód dodávateľa |
| StkNum | word | 2 | Číslo skladu |
| TsdNum | Str12 | 13 | Číslo DDL |
| TsdItm | word | 2 | Riadok DDL |
| TsdDate | DateType | 4 | Dátum DDL |
| OcdNum | Str12 | 13 | Číslo zákazky |
| OcdItm | word | 2 | Riadok zákazky |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Príznak vybavenosti (O/S) |

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

## Indexy (9)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | DocNum | DocNum | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | PaCode | PaCode | Duplicit |
| 4 | StkStat | StkStat | Duplicit |
| 5 | PaCode, GsCode, StkStat | PaGsSt | Duplicit |
| 6 | GsCode, StkStat | GsSt | Duplicit |
| 7 | PaCode, StkStat | PaSt | Duplicit |
| 8 | TsdNum, TsdItm | TdTi | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OSH.DocNum | Hlavička objednávky |
| GsCode | GSCAT.GsCode | Tovar |
| PaCode | PAB.PaCode | Dodávateľ |
| StkNum | STKLST.StkNum | Sklad |
| TsdNum | TSH.DocNum | Dodací list príjmu |
| OcdNum | OCH.DocNum | Odberateľská zákazka |

## Stav položky (StkStat)

| Hodnota | Popis |
|---------|-------|
| O | Objednaný (čaká na dodanie) |
| S | Dodaný na sklad |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
