# TSI - Položky dodávateľských dodacích listov

## Kľúčové slová / Aliases

TSI, TSI.BTR, pokladničné položky, cash register items, predané položky, účtenky

## Popis

Položková tabuľka dodávateľských dodacích listov. Obsahuje jednotlivé tovarové položky s množstvami, cenami a stavom spracovania.

## Btrieve súbor

`TSIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TSIyynnn.BTR`

## Štruktúra polí (64 polí)

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
| GsType | Str1 | 2 | Typ položky (T/W/O) |
| MsName | Str10 | 11 | Merná jednotka |
| PackGs | longint | 4 | Číslo vratného obalu |
| Notice | Str30 | 31 | Poznámka |

### Množstvo a sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu |
| GsQnt | double | 8 | Prijaté množstvo |
| VatPrc | double | 8 | Sadzba DPH % |
| DscPrc | double | 8 | Zľava % |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcSPrice | double | 8 | NC/MJ bez DPH (s NSO) - sklad |
| AcDValue | double | 8 | NC pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcCValue | double | 8 | NC bez DPH (bez NSO) - FA |
| AcEValue | double | 8 | NC s DPH |
| AcZValue | double | 8 | Colné náklady |
| AcTValue | double | 8 | Dopravné náklady |
| AcOValue | double | 8 | Ostatné NSO |
| AcSValue | double | 8 | Obstarávacia cena (s NSO) |
| AcRndVal | double | 8 | Zaokrúhlenie |
| AcAValue | double | 8 | PC bez DPH |
| AcBValue | double | 8 | PC s DPH |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDPrice | double | 8 | NC/MJ pred zľavou |
| FgCPrice | double | 8 | NC/MJ bez DPH |
| FgEPrice | double | 8 | NC/MJ s DPH |
| FgDValue | double | 8 | NC pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgRndVal | double | 8 | Zaokrúhlenie |
| FgCValue | double | 8 | NC bez DPH |
| FgEValue | double | 8 | NC s DPH |

### Trvanlivosť a šarža

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DrbDate | DateType | 4 | Dátum expirácie |
| RbaCode | Str30 | 31 | Kód šarže |
| RbaDate | DateType | 4 | Dátum šarže |

### Partner a párovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód dodávateľa |
| OsdNum | Str12 | 13 | Číslo objednávky |
| OsdItm | word | 2 | Riadok objednávky |
| IsdNum | Str12 | 13 | Číslo faktúry |
| IsdItm | word | 2 | Riadok faktúry |
| IsdDate | DateType | 4 | Dátum faktúry |
| OcdNum | Str12 | 13 | Číslo zákazky |
| OcdItm | longint | 4 | Riadok zákazky |
| OmdNum | Str12 | 13 | Číslo internej výdajky |
| PkdNum | Str12 | 13 | Číslo prebaľovacieho dokladu |
| PkdItm | word | 2 | Riadok prebaľovania |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav skladu (N=evidované, S=naskladnené) |
| FinStat | Str1 | 2 | Finančný stav (F=fakturované, C=uhradené HP) |
| AcqStat | Str1 | 2 | Obstaranie (R=riadny, K=komisionálny) |
| SteCode | word | 2 | Kód skladníka |
| Cctvat | byte | 1 | Prevod DPH povinnosti |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (9)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit (Composite PK) |
| 1 | DocNum | DocNum | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | BarCode | BarCode | Case-insensitive, Duplicit |
| 4 | StkCode | StkCode | Case-insensitive, Duplicit |
| 5 | StkStat | StkStat | Case-insensitive, Duplicit |
| 6 | FinStat | FinStat | Case-insensitive, Duplicit |
| 7 | PaCode | PaCode | Duplicit |
| 8 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | TSH.DocNum | Hlavička dokladu |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| StkNum | STKLST.StkNum | Sklad |
| PaCode | PAB.PaCode | Dodávateľ |
| IsdNum | ISH.DocNum | Faktúra |
| OsdNum | OSH.DocNum | Objednávka |

## Typy položiek

| GsType | Popis |
|--------|-------|
| T | Riadny tovar |
| W | Vážený tovar |
| O | Obal |

## Stavy položky

### StkStat (skladový stav)
| Hodnota | Popis |
|---------|-------|
| N | Zaevidované (nie na sklade) |
| S | Naskladnené |

### FinStat (finančný stav)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Bez spracovania |
| F | Vyfakturované |
| C | Vyúčtované cez HP |

## Stav migrácie

- [x] BDF dokumentácia
- [x] Btrieve model (nexdata) - čiastočne
- [ ] PostgreSQL model
- [ ] API endpoint
