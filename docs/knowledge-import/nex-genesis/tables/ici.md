# ICI - Položky odberateľských faktúr

## Kľúčové slová / Aliases

ICI, ICI.BTR, faktúry odberateľské položky, customer invoice items, fakturované položky

## Popis

Položková tabuľka odberateľských faktúr. Obsahuje jednotlivé položky tovaru s cenami, DPH a párovaniami na dodacie listy a zákazky.

## Btrieve súbor

`ICIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICIyynnn.BTR`

## Štruktúra polí (80 polí)

### Identifikácia položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo faktúry - **FK → ICH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| GsType | Str1 | 2 | Typ položky (T=tovar, W=váhový, O=obal) |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Tovarová skupina |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód (EAN) |
| StkCode | Str15 | 16 | Skladový kód |
| MsName | Str10 | 11 | Merná jednotka |
| PackGs | longint | 4 | Tovarové číslo vratného obalu |
| Notice | Str30 | 31 | Poznámka k riadku |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Fakturované množstvo |
| GscQnt | double | 8 | Počet kartónových balení |
| GspQnt | double | 8 | Počet paletových balení |
| Volume | double | 8 | Objem (m³) |
| Weight | double | 8 | Váha (kg) |

### Sklad a dátumy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu |
| DocDate | DateType | 4 | Dátum vystavenia |
| DrbDate | DateType | 4 | Dátum ukončenia trvanlivosti |

### Ceny v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcCValue | double | 8 | NC bez DPH |
| AcDValue | double | 8 | PC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcAValue | double | 8 | PC bez DPH po zľave |
| AcBValue | double | 8 | PC s DPH |
| AcRndVal | double | 8 | Zaokrúhlenie |
| AcRndVat | double | 8 | Zaokrúhlenie DPH |

### Ceny vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgCourse | double | 8 | Kurz |
| FgCPrice | double | 8 | NC/MJ bez DPH |
| FgDPrice | double | 8 | PC/MJ bez DPH pred zľavou |
| FgAPrice | double | 8 | PC/MJ bez DPH po zľave |
| FgBPrice | double | 8 | PC/MJ s DPH |
| FgCValue | double | 8 | NC bez DPH |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgAValue | double | 8 | PC bez DPH po zľave |
| FgBValue | double | 8 | PC s DPH |
| FgHValue | double | 8 | PC s DPH pred zľavou |
| FgHdsVal | double | 8 | Hlavičková zľava |
| FgRndVal | double | 8 | Zaokrúhlenie |
| FgRndVat | double | 8 | Zaokrúhlenie DPH |

### DPH a zľavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH % |
| DscPrc | double | 8 | Percentuálna zľava |
| DscType | Str1 | 2 | Typ zľavy |
| DscGrp | byte | 1 | Skupina zľavy |
| HdsPrc | double | 8 | Hlavičková zľava % |
| Action | Str1 | 2 | Cenová akcia (A=akciový) |
| BonNum | byte | 1 | Číslo bonusovej akcie |
| Cctvat | byte | 1 | Prenesená daňová povinnosť |

### Párovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| DlrCode | word | 2 | Kód obchodného zástupcu |
| McdNum | Str12 | 13 | Číslo cenovej ponuky |
| McdItm | word | 2 | Riadok cenovej ponuky |
| OcdNum | Str12 | 13 | Číslo zákazky |
| OcdItm | word | 2 | Riadok zákazky |
| TcdNum | Str12 | 13 | Číslo DL |
| TcdItm | word | 2 | Riadok DL |
| TcdDate | DateType | 4 | Dátum DL |
| IcdNum | Str12 | 13 | Odkaz na prepojenú FA |
| IcdItm | word | 2 | Riadok prepojenej FA |
| ScdNum | Str12 | 13 | Číslo zdrojového dokladu |
| ScdItm | word | 2 | Riadok zdrojového dokladu |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Stav položky (N/Q) |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str8 | 9 | Analytický účet |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpMark | Str10 | 11 | Všeobecné označenie |
| SteCode | word | 2 | Kód skladníka |
| WriNum | word | 2 | Číslo prevádzky |
| CasNum | word | 2 | Číslo pokladne |
| RspUser | Str8 | 9 | Používateľ vystavenia |
| RspDate | DateType | 4 | Dátum vystavenia |
| RspTime | TimeType | 4 | Čas vystavenia |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | DocNum | DocNum | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | BarCode | BarCode | Case-insensitive, Duplicit |
| 4 | DocDate | DocDate | Duplicit |
| 5 | TcdNum, TcdItm | TnTi | Duplicit |
| 6 | Status | Status | Case-insensitive, Duplicit |
| 7 | DlrCode | DlrCode | Duplicit |
| 8 | ScdNum, ScdItm | SnSi | Duplicit |
| 9 | PaCode | PaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ICH.DocNum | Hlavička faktúry |
| GsCode | GSCAT.GsCode | Tovar |
| PaCode | PAB.PaCode | Odberateľ |
| TcdNum, TcdItm | TCI.DocNum, TCI.ItmNum | Položka DL |
| OcdNum, OcdItm | OCI.DocNum, OCI.ItmNum | Položka zákazky |
| StkNum | STKLST.StkNum | Sklad |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
