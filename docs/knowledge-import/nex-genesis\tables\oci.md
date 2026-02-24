# OCI - Položky odberateľských zákaziek

## Kľúčové slová / Aliases

OCI, OCI.BTR, objednávky prijaté položky, orders received items, objednané položky

## Popis

Položková tabuľka odberateľských objednávok (zákaziek). Obsahuje jednotlivé položky tovaru s rezerváciami, množstvami a cenami.

## Btrieve súbor

`OCIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCIyynnn.BTR`

## Štruktúra polí (80 polí)

### Identifikácia položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo dokladu - **FK → OCH.DocNum** |
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

### Termíny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ReqDate | DateType | 4 | Požadovaný termín dodania |
| ConfDate | DateType | 4 | Potvrdený termín dodania |
| ExpDate | DateType | 4 | Termín expedície |

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

### Stavy položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Skladový stav (N/O/R/P/S) |
| FinStat | Str1 | 2 | Finančný stav (F/C) |

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
| TcdNum | Str12 | 13 | Číslo odberateľského DL |
| IcdNum | Str12 | 13 | Číslo odberateľskej faktúry |
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

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unique |
| 1 | GsCode | GsCode | Case-insensitive, Duplicit |
| 2 | GsName | GsName | Case-insensitive, Duplicit |
| 3 | StkStat | StkStat | Duplicit |
| 4 | FinStat | FinStat | Duplicit |
| 5 | ReqDate | ReqDate | Duplicit |
| 6 | ConfDate | ConfDate | Duplicit |
| 7 | TcdNum | TcdNum | Duplicit |
| 8 | IcdNum | IcdNum | Duplicit |
| 9 | OsdNum | OsdNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCH.DocNum | Hlavička zákazky |
| GsCode | GSCAT.GsCode | Tovar |
| MglNum | MGLST.MglNum | Výrobca |
| OsdNum | OSI.DocNum | Položka dodávateľskej objednávky |
| TcdNum | TCH.DocNum | Odberateľský DL |
| IcdNum | ICH.DocNum | Odberateľská faktúra |

## Skladové stavy (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Nerezervované |
| O | Objednané u dodávateľa |
| R | Rezervované zo zásob |
| P | Pripravené na expedíciu |
| S | Vyskladnené |

## Finančné stavy (FinStat)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Bez spracovania |
| F | Vyfakturované |
| C | Vyúčtované cez ERP |

## Kumulatívne množstvá - vzťahy

```
SalPrq = RstPrq + RosPrq + ReqPrq + UndPrq + CncPrq
       = TcdPrq + UndPrq + CncPrq (po expedícii)

Workflow:
SalPrq (objednané) → RstPrq/RosPrq (rezervované) → ExdPrq (expedícia) → TcdPrq (dodané) → IcdPrq (fakturované)
                                                                      → CncPrq (storno)
                                                                      → UndPrq (nedodané)
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
