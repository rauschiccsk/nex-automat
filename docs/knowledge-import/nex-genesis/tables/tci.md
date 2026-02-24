# TCI - Položky odberateľských dodacích listov

## Kľúčové slová / Aliases

TCI, TCI.BTR, dodacie listy položky, delivery notes items, vydané položky

## Popis

Položková tabuľka odberateľských dodacích listov (ODL). Obsahuje jednotlivé položky tovaru s cenami, stavmi vyskladnenia a párovaniami na zákazky a faktúry.

## Btrieve súbor

`TCIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCIyynnn.BTR`

## Štruktúra polí (79 polí)

### Identifikácia položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo dokladu - **FK → TCH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| GsType | Str1 | 2 | Typ položky (T=tovar, W=váhový, O=obal) |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Tovarová skupina |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |
| PackGs | longint | 4 | Tovarové číslo vratného obalu |
| Notice | Str30 | 31 | Poznámka k riadku |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Predané množstvo |
| GscQnt | double | 8 | Počet kartónových balení |
| GspQnt | double | 8 | Počet paletových balení |
| ExpQnt | double | 8 | Množstvo pripravené na expedíciu |
| Volume | double | 8 | Objem tovaru (m³) |
| Weight | double | 8 | Váha tovaru (kg) |

### Sklad a dátumy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu výdaja |
| DocDate | DateType | 4 | Dátum vystavenia |
| DlvDate | DateType | 4 | Dátum vyskladnenia |
| DrbDate | DateType | 4 | Dátum ukončenia trvanlivosti |
| DlvUser | Str8 | 9 | Meno skladníka |

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
| FgCPrice | double | 8 | NC/MJ bez DPH |
| FgDPrice | double | 8 | PC/MJ bez DPH pred zľavou |
| FgAPrice | double | 8 | PC/MJ bez DPH po zľave |
| FgBPrice | double | 8 | PC/MJ s DPH |
| FgCValue | double | 8 | NC bez DPH |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgAValue | double | 8 | PC bez DPH po zľave |
| FgBValue | double | 8 | PC s DPH |
| FgHdsVal | double | 8 | Hlavičková zľava |
| FgRndVal | double | 8 | Zaokrúhlenie |
| FgRndVat | double | 8 | Zaokrúhlenie DPH |

### DPH a zľavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH % |
| DscPrc | double | 8 | Percentuálna zľava |
| HdsPrc | double | 8 | Hlavičková zľava % |
| DscType | Str1 | 2 | Typ zľavy |
| Action | Str1 | 2 | Cenová akcia (A=akciový) |
| BonNum | byte | 1 | Číslo bonusovej akcie |
| Cctvat | byte | 1 | Prevod DPH podľa colného sadzobníka |

### Stavy položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Skladový stav (N/O/R/P/S/E) |
| FinStat | Str1 | 2 | Finančný stav (F/C) |

### Párovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| DlrCode | word | 2 | Kód obchodného zástupcu |
| McdNum | Str12 | 13 | Číslo cenovej ponuky |
| McdItm | word | 2 | Riadok cenovej ponuky |
| OcdNum | Str12 | 13 | Číslo zákazky |
| OcdItm | word | 2 | Riadok zákazky |
| IcdNum | Str12 | 13 | Číslo faktúry |
| IcdItm | word | 2 | Riadok faktúry |
| IcdDate | DateType | 4 | Dátum vystavenia faktúry |
| ScdNum | Str12 | 13 | Číslo zdrojového dokladu |
| ScdItm | word | 2 | Riadok zdrojového dokladu |

### Výrobné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpMark | Str10 | 11 | Všeobecné označenie |
| SteCode | word | 2 | Kód skladníka |
| WriNum | word | 2 | Číslo prevádzky |
| CasNum | word | 2 | Číslo pokladne |
| RspUser | Str8 | 9 | Používateľ vystavenia položky |
| RspDate | DateType | 4 | Dátum vystavenia položky |
| RspTime | TimeType | 4 | Čas vystavenia položky |

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
| 3 | DocNum, GsCode | DnGc | Duplicit |
| 4 | PaCode | PaCode | Duplicit |
| 5 | StkStat | StkStat | Duplicit |
| 6 | FinStat | FinStat | Duplicit |
| 7 | GsType | GsType | Duplicit |
| 8 | ScdNum, ScdItm | SnSi | Duplicit |
| 9 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | TCH.DocNum | Hlavička DL |
| GsCode | GSCAT.GsCode | Tovar |
| PaCode | PAB.PaCode | Odberateľ |
| OcdNum, OcdItm | OCI.DocNum, OCI.ItmNum | Položka zákazky |
| IcdNum, IcdItm | ICI.DocNum, ICI.ItmNum | Položka faktúry |
| StkNum | STKLST.StkNum | Sklad |

## Typy položiek (GsType)

| Hodnota | Popis |
|---------|-------|
| T | Riadny tovar |
| W | Váhový tovar |
| O | Obal |

## Skladové stavy (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Nerealizované |
| O | Objednané |
| R | Rezervované |
| P | Pripravené |
| S | Vyskladnené |
| E | Expedované |

## Finančné stavy (FinStat)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nevyfakturované |
| F | Vyfakturované |
| C | Vyúčtované cez ERP |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
