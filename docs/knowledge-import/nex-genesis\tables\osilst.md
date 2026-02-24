# OSILST - Položky dodávateľských objednávok LIST

## Kľúčové slová / Aliases

OSILST, OSILST.BTR, zoznam položiek nákupných objednávok, PO items list

## Popis

Agregovaná tabuľka položiek dodávateľských objednávok. Rozšírená verzia OSI s dodatočnými poliami pre sledovanie termínov, dodávok a stavu.

## Btrieve súbor

`OSILST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSILST.BTR`

## Štruktúra polí (64 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmAdr | longint | 4 | Fyzická adresa položky |
| BokNum | Str3 | 4 | Číslo knihy |
| PrjNum | Str12 | 13 | Číslo projektu |
| DocNum | Str12 | 13 | Číslo objednávky - **FK → OSHLST.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |

### Produkt

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzky |
| StkNum | word | 2 | Číslo skladu |
| ProNum | longint | 4 | Produktové číslo |
| ProNam | Str60 | 61 | Názov produktu |
| _ProNam | Str60 | 61 | Vyhľadávacie pole |
| PgrNum | word | 2 | Produktová skupina |
| FgrNum | word | 2 | Finančná skupina |
| SgrNum | word | 2 | Obchodná skupina |
| BarCod | Str15 | 16 | Čiarový kód |
| StkCod | Str15 | 16 | Skladový kód |
| ShpCod | Str30 | 31 | Eshop kód |
| OrdCod | Str30 | 31 | Objednávkový kód |
| ProVol | double | 8 | Objem (m3) |
| ProWgh | double | 8 | Váha (kg) |
| ProTyp | Str1 | 2 | Typ produktu (T/W/O/S) |
| MsuNam | Str10 | 11 | Merná jednotka |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH (%) |
| OrdPrq | double | 8 | Objednané množstvo |
| RocPrq | double | 8 | Rezervované na zákazkách |
| TsdPrq | double | 8 | Dodané množstvo |
| CncPrq | double | 8 | Stornované množstvo |
| UndPrq | double | 8 | Množstvo na dodanie |
| IsdPrq | double | 8 | Vyfakturované množstvo |

### Ceny a hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OrdApc | double | 8 | Jednotková cena bez DPH |
| OrdAva | double | 8 | Hodnota bez DPH |
| OrdBva | double | 8 | Hodnota s DPH |
| OrpSrc | Str2 | 3 | Zdroj ceny (OP/LP) |
| TrsBva | double | 8 | Dopravné náklady s DPH |
| EndBva | double | 8 | Konečná hodnota s DPH |
| DvzBva | double | 8 | Hodnota v cudzej mene |

### Termíny dodávky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ParNum | longint | 4 | Kód dodávateľa |
| DocDte | DateType | 4 | Dátum objednávky |
| RatDay | word | 2 | Počet dní dodávky |
| RatTyp | Str1 | 2 | Typ termínu (F/P/A/Z) |
| RatDte | DateType | 4 | Aktuálny termín |
| RatNot | Str50 | 51 | Poznámka k termínu |
| RatPrv | DateType | 4 | Predchádzajúci termín |
| RatChg | byte | 1 | Číslo zmeny termínu |

### Väzby na doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsdNum | Str13 | 14 | Číslo DDL |
| TsdItm | word | 2 | Riadok DDL |
| TsdDte | DateType | 4 | Dátum DDL |
| TsdDoq | byte | 1 | Počet DDL |
| IsdNum | Str13 | 14 | Číslo faktúry |
| IsdItm | word | 2 | Riadok faktúry |
| IsdDte | DateType | 4 | Dátum faktúry |
| IsdDoq | byte | 1 | Počet faktúr |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FreRes | byte | 1 | Voľné množstvo na rezerváciu |
| SndSta | Str1 | 2 | Príznak odoslania (O) |
| SndDte | DateType | 4 | Dátum odoslania |
| ItmSta | Str1 | 2 | Stav položky (O) |
| ItmFrm | Str10 | 11 | Formulár položky |
| SpcMrk | Str10 | 11 | Špeciálne označenie |
| Notice | Str50 | 51 | Poznámka |
| CctVat | byte | 1 | Prevod DPH podľa colného sadzobníka |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUsr | Str8 | 9 | Používateľ vytvorenia |
| CrtDte | DateType | 4 | Dátum vytvorenia |
| CrtTim | TimeType | 4 | Čas vytvorenia |

## Indexy (17)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | ItmAdr | ItmAdr | Duplicit |
| 2 | ItmNum | ItmNum | Duplicit |
| 3 | DocNum, ItmNum | DnIn | Duplicit |
| 4 | DocNum, ProNum | DnPn | Duplicit |
| 5 | StkNum, ProNum | SnPn | Duplicit |
| 6 | ProNum, FreRes | PnFr | Duplicit |
| 7 | _ProNam | ProNam | Duplicit, Case insensitive |
| 8 | ParNum | ParNum | Duplicit |
| 9 | ItmSta | ItmSta | Duplicit |
| 10 | ProNum, ItmSta | PnSt | Duplicit |
| 11 | ParNum, ItmSta | PaSt | Duplicit |
| 12 | ParNum, ProNum, ItmSta | PaPnSt | Duplicit |
| 13 | ProNum | ProNum | Duplicit |
| 14 | BarCod | BarCod | Duplicit |
| 15 | StkCod | StkCod | Duplicit |
| 16 | OrdCod | OrdCod | Duplicit |

## Typ termínu (RatTyp)

| Hodnota | Popis |
|---------|-------|
| F | Fixný termín |
| P | Požadovaný termín |
| A | Akceptovaný termín |
| Z | Zmenený termín |

## Typ produktu (ProTyp)

| Hodnota | Popis |
|---------|-------|
| T | Tovar |
| W | Váhový tovar |
| O | Obal |
| S | Služba |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
