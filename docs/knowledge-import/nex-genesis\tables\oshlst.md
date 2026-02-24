# OSHLST - Hlavičky dodávateľských objednávok LIST

## Kľúčové slová / Aliases

OSHLST, OSHLST.BTR, zoznam hlavičiek nákupných objednávok, PO headers list

## Popis

Agregovaná tabuľka hlavičiek dodávateľských objednávok. Rozšírená verzia OSH s dodatočnými poliami pre sledovanie stavu, zálohovými faktúrami a projektovými údajmi.

## Btrieve súbor

`OSHLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSHLST.BTR`

## Štruktúra polí (119 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BokNum | Str3 | 4 | Číslo knihy |
| DocYer | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Poradové číslo |
| DocNum | Str12 | 13 | Interné číslo - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo |
| PrjNum | Str12 | 13 | Číslo projektu |
| PrjCod | Str30 | 31 | Kódové označenie projektu |

### Dátumy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDte | DateType | 4 | Dátum vystavenia |
| ExpDte | DateType | 4 | Dátum platnosti (expirácie) |
| ReqDte | DateType | 4 | Požadovaný termín dodávky |
| SndDte | DateType | 4 | Dátum odoslania |
| ReqTyp | Str1 | 2 | Typ termínu (!-požadovaný) |

### Dodávateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ParNum | longint | 4 | Číselný kód dodávateľa |
| ParNam | Str60 | 61 | Názov dodávateľa |
| _ParNam | Str60 | 61 | Vyhľadávacie pole |
| RegIno | Str15 | 16 | IČO |
| RegTin | Str15 | 16 | DIČ |
| RegVin | Str15 | 16 | IČ pre DPH |
| RegAdr | Str30 | 31 | Adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Kontaktná osoba

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CtpNum | longint | 4 | ID kontaktnej osoby |
| CtpNam | Str30 | 31 | Meno kontaktnej osoby |
| CtpTel | Str20 | 21 | Telefón |
| CtpFax | Str20 | 21 | Fax |
| CtpEml | Str30 | 31 | Email |

### Miesto dodania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpaNum | longint | 4 | Kód príjemcu |
| WpaNum | word | 2 | Číslo prevádzky príjemcu |
| WpaNam | Str60 | 61 | Názov prevádzky |
| WpaAdr | Str30 | 31 | Adresa |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Platba a doprava

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCod | Str1 | 2 | Kód formy úhrady |
| PayNam | Str20 | 21 | Názov formy úhrady |
| TrsCod | Str5 | 6 | Kód dopravy |
| TrsNam | Str20 | 21 | Názov dopravy |
| ComDlv | byte | 1 | Dodať kompletnú objednávku |
| RcvTyp | Str1 | 2 | Spôsob prevzatia (O/E/V) |

### Sumy a hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek |
| ProVol | double | 8 | Objem tovaru (m3) |
| ProWgh | double | 8 | Váha tovaru (kg) |
| ProAva | double | 8 | Hodnota tovaru bez DPH |
| SrvAva | double | 8 | Hodnota služieb bez DPH |
| OrdAva | double | 8 | Hodnota dokladu bez DPH |
| VatVal | double | 8 | Hodnota DPH |
| OrdBva | double | 8 | Hodnota dokladu s DPH |
| TrsBva | double | 8 | Dopravné náklady s DPH |
| EndBva | double | 8 | Konečná hodnota s DPH |

### Cudzia mena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzNam | Str3 | 4 | Názov meny |
| DvzCrs | double | 8 | Kurz meny |
| DvzBva | double | 8 | Hodnota s DPH v cudzej mene |

### Záloha

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DepPrc | double | 8 | Percento zálohy |
| DepBva | double | 8 | Hodnota zálohy s DPH |
| DepDte | DateType | 4 | Dátum prijatia zálohy |
| DepPay | Str1 | 2 | Platobný prostriedok zálohy |

### Sledovanie množstiev

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OrdPrq | double | 8 | Objednané množstvo |
| RocPrq | double | 8 | Rezervované na zákazkách |
| TsdPrq | double | 8 | Dodané množstvo |
| CncPrq | double | 8 | Stornované množstvo |
| UndPrq | double | 8 | Množstvo na dodanie |
| IsdPrq | double | 8 | Vyfakturované množstvo |

### Zálohová faktúra

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PsdYer | Str2 | 3 | Rok zálohovej faktúry |
| PsdSer | longint | 4 | Poradové číslo |
| PsdNum | Str12 | 13 | Interné číslo |
| PseNum | Str12 | 13 | Dodávateľské číslo |
| PsvNum | Str10 | 11 | Variabilný symbol |
| PsdDte | DateType | 4 | Dátum vystavenia |
| PseDte | DateType | 4 | Dátum splatnosti |
| PsdVal | double | 8 | Hodnota zálohovej faktúry |
| PspVal | double | 8 | Zaplatená záloha |
| PspCur | double | 8 | Kurz uhradenej zálohy |
| PsdIba | Str30 | 31 | IBAN pre platbu |
| PsdUsr | Str10 | 11 | Používateľ evidencie |
| PsdUsn | Str30 | 31 | Meno používateľa |

### Faktúra za zálohu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DsdNum | Str12 | 13 | Interné číslo faktúry |
| DseNum | Str12 | 13 | Dodávateľské číslo |
| DsvNum | Str10 | 11 | Variabilný symbol |
| DsdDte | DateType | 4 | Dátum vystavenia |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstRat | Str1 | 2 | Zmenený termín (R) |
| DstLck | Str1 | 2 | Uzamknutie (L/R) |
| DstCls | Str1 | 2 | Ukončenie (C) |
| SpcMrk | Str10 | 11 | Špeciálne označenie |

### Väzby na doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AtcDoq | byte | 1 | Počet príloh |
| SrdNum | Str13 | 14 | Číslo zdrojového dokladu |
| SrdDoq | byte | 1 | Počet zdrojových dokladov |
| TsdNum | Str13 | 14 | Číslo DDL |
| TsdDoq | byte | 1 | Počet DDL |
| TsdPrc | byte | 1 | Percento dodávky |
| IsdNum | Str13 | 14 | Číslo faktúry |
| IsdDoq | byte | 1 | Počet faktúr |
| IsdPrc | byte | 1 | Percento fakturácie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUsr | Str8 | 9 | Používateľ vytvorenia |
| CrtUsn | Str30 | 31 | Meno používateľa |
| CrtDte | DateType | 4 | Dátum vytvorenia |
| CrtTim | TimeType | 4 | Čas vytvorenia |
| MngUsr | Str8 | 9 | Zodpovedná osoba |
| MngUsn | Str30 | 31 | Meno zodpovednej osoby |
| MngDte | DateType | 4 | Dátum zodpovednosti |
| EdiUsr | Str8 | 9 | Editujúci používateľ |
| EdiDte | DateType | 4 | Dátum editácie |
| EdiTim | TimeType | 4 | Čas editácie |
| PrnCnt | byte | 1 | Počet tlačí |
| PrnUsr | word | 2 | Používateľ tlače |
| PrnDte | DateType | 4 | Dátum tlače |

## Indexy (24)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Unique |
| 1 | BokNum | BokNum | Duplicit |
| 2 | DocYer, SerNum | DySn | Duplicit |
| 3 | DocYer, BokNum, SerNum | DyBnSn | Duplicit |
| 4 | ExtNum | ExtNum | Duplicit |
| 5 | DocDte | DocDte | Duplicit |
| 6 | ReqDte | ReqDte | Duplicit |
| 7 | ParNum | ParNum | Duplicit |
| 8 | RegIno | RegIno | Duplicit |
| 9 | SpaNum, WpaNum | SnWn | Duplicit |
| 10 | _ParNam | ParNam | Duplicit |
| 11 | EndBva | EndBva | Duplicit |
| 12 | DepBva | DepBva | Duplicit |
| 13 | PrjNum | PrjNum | Duplicit |
| 14 | PrjCod | PrjCod | Duplicit |
| 15 | DstRat | DstRat | Duplicit |
| 16 | PsdYer, PsdSer | PyPs | Duplicit |
| 17 | PsdNum | PsdNum | Duplicit |
| 18 | PseNum | PseNum | Duplicit |
| 19 | PsvNum | PsvNum | Duplicit |
| 20 | DsdNum | DsdNum | Duplicit |
| 21 | DseNum | DseNum | Duplicit |
| 22 | DsvNum | DsvNum | Duplicit |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
