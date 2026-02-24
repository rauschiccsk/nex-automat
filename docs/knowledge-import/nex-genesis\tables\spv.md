# SPV - Daňové doklady zálohových platieb

## Kľúčové slová / Aliases

SPV, SPV.BTR, daňové, doklady, zálohových, platieb

## Popis

Daňové doklady k zálohovým platbám. Každý záznam reprezentuje jeden daňový doklad s detailom DPH podľa 3 skupín sadzieb. Tabuľka používa ročné knihy.

## Btrieve súbor

`SPVyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\DOCS\SPVyynnn.BTR`

## Štruktúra polí (35 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | word | 2 | Poradové číslo všetkých dokladov |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| Year | Str2 | 3 | Rok dokladu |
| DocDate | DateType | 4 | Dátum zaplatenia alebo čerpania zálohy |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa - **FK PAB** |
| PaName | Str30 | 31 | Názov odberateľa |
| _PaName | Str20 | 21 | Vyhľadávacie pole názvu |

### Sadzby DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH - skupina 1 (0%) |
| VatPrc2 | byte | 1 | Sadzba DPH - skupina 2 (základná) |
| VatPrc3 | byte | 1 | Sadzba DPH - skupina 3 (znížená) |

### Hodnoty bez DPH (AValue)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue | double | 8 | Celková hodnota dokladu bez DPH |
| AValue1 | double | 8 | Hodnota bez DPH - skupina 1 |
| AValue2 | double | 8 | Hodnota bez DPH - skupina 2 |
| AValue3 | double | 8 | Hodnota bez DPH - skupina 3 |

### Hodnoty DPH (VatVal)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal | double | 8 | Celková hodnota DPH |
| VatVal1 | double | 8 | Hodnota DPH - skupina 1 |
| VatVal2 | double | 8 | Hodnota DPH - skupina 2 |
| VatVal3 | double | 8 | Hodnota DPH - skupina 3 |

### Hodnoty s DPH (BValue)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BValue | double | 8 | Celková hodnota dokladu s DPH |
| BValue1 | double | 8 | Hodnota s DPH - skupina 1 |
| BValue2 | double | 8 | Hodnota s DPH - skupina 2 |
| BValue3 | double | 8 | Hodnota s DPH - skupina 3 |

### Prepojenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConDoc | Str12 | 13 | Číslo dokladu prijatia zálohy (SPD) |
| OcdNum | Str12 | 13 | Číslo zákazkového dokladu |

### Forma platby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayMode | Str1 | 2 | Forma zaplatenia (H/K/B) |
| RspName | Str30 | 31 | Meno používateľa, ktorý vystavil doklad |

### DPH uzávierka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatCls | byte | 1 | Číslo uzávierky DPH |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | DocNum | DocNum | Duplicit |
| 2 | DocDate | DocDate | Duplicit |
| 3 | PaCode | PaCode | Duplicit |
| 4 | _PaName | PaName | Duplicit, Case-insensitive |
| 5 | PayMode | PayMode | Duplicit |
| 6 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner katalóg |
| ConDoc | SPD.DocNum | Doklad prijatia zálohy |
| VatCls | VTRLST.ClsNum | Uzávierka DPH |

## Výpočtové pravidlá

DPH zo zálohy sa počíta metódou "zhora":
```
VatVal = BValue - BValue / (1 + VatPrc/100)
AValue = BValue - VatVal
```

Pre každú skupinu:
```
VatValN = BValueN - BValueN / (1 + VatPrcN/100)
AValueN = BValueN - VatValN
```

## Použitie

- Daňové doklady k prijatým zálohovým platbám
- Podklad pre uzávierku DPH
- Účtovanie DPH zo záloh

## Business pravidlá

- Jeden daňový doklad na jednu zálohovú platbu
- ConDoc prepája na SPD záznam
- OcdNum prepája na zákazku (OCH)
- VatCls sa vyplní pri uzávierke DPH
- Automatické účtovanie cez DocAccount

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
