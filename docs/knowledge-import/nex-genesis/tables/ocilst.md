# OCILST - Položky zákaziek (LIST štruktúra)

## Kľúčové slová / Aliases

OCILST, OCILST.BTR, zoznam položiek objednávok, order items list

## Popis

Zjednotená tabuľka položiek odberateľských zákaziek zo všetkých kníh. Novšia štruktúra s rozšírenými poľami pre sledovanie rezervácií a dodávok.

## Btrieve súbor

`OCILST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCILST.BTR`

## Štruktúra polí (95 polí)

### Identifikácia položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BokNum | word | 2 | Číslo knihy |
| DocNum | Str12 | 13 | Číslo dokladu - **FK → OCHLST.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| ItmTyp | Str1 | 2 | Typ položky (T=tovar, S=služba, N=text) |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | Str15 | 16 | Kód tovaru |
| GsName | Str40 | 41 | Názov tovaru |
| GsUnit | Str4 | 5 | Jednotka |
| GsPckg | Str15 | 16 | Balenie |
| MglNum | longint | 4 | Kód MGLST (výrobca) |
| BarCode | Str20 | 21 | Čiarový kód |

### Termíny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ReqDate | DateType | 4 | Požadovaný termín dodania |
| ConfDate | DateType | 4 | Potvrdený termín dodania |
| ExpDate | DateType | 4 | Termín expedície |
| ShpDate | DateType | 4 | Dátum expedície |

### Množstvá a rezervácie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SalPrq | double | 8 | Celkové objednané množstvo |
| ReqPrq | double | 8 | Množstvo požiadaviek na objednanie |
| RstPrq | double | 8 | Množstvo rezervované zo zásob |
| RosPrq | double | 8 | Množstvo rezervované z objednávok |
| ExdPrq | double | 8 | Pripravené na expedíciu |
| TcdPrq | double | 8 | Dodané množstvo |
| CncPrq | double | 8 | Stornované množstvo |
| UndPrq | double | 8 | Nedodané množstvo |
| IcdPrq | double | 8 | Vyfakturované množstvo |
| FrePrq | double | 8 | Voľné množstvo (nezarezervované) |

### Stavy položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Skladový stav (N/O/R/P/S) |
| FinStat | Str1 | 2 | Finančný stav (F/C) |
| PrcStat | Str1 | 2 | Stav spracovania |

### Ceny v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Kód účtovnej meny |
| AcNValue | double | 8 | Nákupná cena (NC) |
| AcDValue | double | 8 | Jednotková PC pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcDscPrc | double | 8 | Percento zľavy |
| AcCValue | double | 8 | Jednotková PC bez DPH |
| AcEValue | double | 8 | Jednotková PC s DPH |
| AcSValue | double | 8 | Celková hodnota |
| AcMargin | double | 8 | Marža |

### Ceny vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Kód vyúčtovacej meny |
| FgCourse | double | 8 | Kurz |
| FgDValue | double | 8 | Jednotková PC pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgCValue | double | 8 | Jednotková PC bez DPH |
| FgEValue | double | 8 | Jednotková PC s DPH |
| FgSValue | double | 8 | Celková hodnota |

### DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatNum | byte | 1 | Číslo sadzby DPH (1-5) |
| VatPrc | byte | 1 | Sadzba DPH % |

### Párovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OsdNum | Str12 | 13 | Číslo dodávateľskej objednávky |
| OsdItm | word | 2 | Číslo položky objednávky |
| TcdNum | Str12 | 13 | Číslo odberateľského DL |
| TcdItm | word | 2 | Číslo položky DL |
| IcdNum | Str12 | 13 | Číslo odberateľskej faktúry |
| IcdItm | word | 2 | Číslo položky faktúry |
| ExdNum | Str12 | 13 | Číslo expedičného príkazu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (19)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unique |
| 1 | BokNum, DocNum, ItmNum | BokDocItm | Unique |
| 2 | GsCode | GsCode | Case-insensitive, Duplicit |
| 3 | GsName | GsName | Case-insensitive, Duplicit |
| 4 | BarCode | BarCode | Case-insensitive, Duplicit |
| 5 | StkStat | StkStat | Duplicit |
| 6 | FinStat | FinStat | Duplicit |
| 7 | PrcStat | PrcStat | Duplicit |
| 8 | ReqDate | ReqDate | Duplicit |
| 9 | ConfDate | ConfDate | Duplicit |
| 10 | ExpDate | ExpDate | Duplicit |
| 11 | TcdNum | TcdNum | Case-insensitive, Duplicit |
| 12 | IcdNum | IcdNum | Case-insensitive, Duplicit |
| 13 | OsdNum | OsdNum | Case-insensitive, Duplicit |
| 14 | ExdNum | ExdNum | Case-insensitive, Duplicit |
| 15 | BokNum | BokNum | Duplicit |
| 16 | MglNum | MglNum | Duplicit |
| 17 | DocNum | DocNum | Case-insensitive, Duplicit |
| 18 | ShpDate | ShpDate | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCHLST.DocNum | Hlavička zákazky |
| BokNum | OCBLST.BokNum | Kniha zákaziek |
| GsCode | GSCAT.GsCode | Tovar |
| MglNum | MGLST.MglNum | Výrobca |
| BarCode | BARCODE.BarCode | Čiarový kód |

## Rozšírené polia oproti OCI

| Pole | Popis |
|------|-------|
| BokNum | Explicitné číslo knihy |
| BarCode | Čiarový kód pre skenovanie |
| FrePrq | Voľné množstvo |
| AcMargin | Výpočet marže |
| PrcStat | Stav spracovania |
| ShpDate | Dátum expedície |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
