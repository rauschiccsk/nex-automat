# OSH - Hlavičky dodávateľských objednávok

## Kľúčové slová / Aliases

OSH, OSH.BTR, objednávky odoslané hlavičky, purchase orders header, nákupné objednávky

## Popis

Tabuľka hlavičiek dodávateľských objednávok. Obsahuje základné údaje o objednávke, dodávateľovi, termínoch a finančných sumách.

## Btrieve súbor

`OSHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSHyynnn.BTR`

## Štruktúra polí (79 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo objednávky |
| DocNum | Str12 | 13 | Interné číslo objednávky - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo objednávky (u dodávateľa) |
| Year | Str2 | 3 | Rok dokladu |

### Dátumy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum vystavenia objednávky |
| DlvDate | DateType | 4 | Termín dodávky tovaru |

### Dodávateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód dodávateľa |
| PaName | Str30 | 31 | Pracovný názov dodávateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu |
| RegName | Str60 | 61 | Registrovaný názov firmy |
| RegIno | Str15 | 16 | IČO partnera |
| RegTin | Str15 | 16 | DIČ partnera |
| RegVin | Str15 | 16 | IČ pre DPH |
| RegAddr | Str30 | 31 | Registrovaná adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Miesto dodania (prevádzka)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WpaCode | word | 2 | Číslo prevádzkovej jednotky príjemcu |
| WpaName | Str60 | 61 | Názov prevádzkovej jednotky |
| WpaAddr | Str30 | 31 | Adresa prevádzky |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Platba a doprava

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Skratka formy úhrady |
| PayName | Str20 | 21 | Názov formy úhrady |
| TrsCode | Str3 | 4 | Kód spôsobu dopravy |
| TrsName | Str20 | 21 | Názov spôsobu dopravy |

### Sklad a cenník

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo priradeného skladu |
| PlsNum | word | 2 | Číslo predajného cenníka |
| SmCode | word | 2 | Číslo skladového pohybu |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH skupiny č.1 |
| VatPrc2 | byte | 1 | Sadzba DPH skupiny č.2 |
| VatPrc3 | byte | 1 | Sadzba DPH skupiny č.3 |
| VatPrc4 | byte | 1 | Sadzba DPH skupiny č.4 |
| VatPrc5 | byte | 1 | Sadzba DPH skupiny č.5 |

### Účtovná mena (EUR)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Názov účtovnej meny |
| AcDValue | double | 8 | NC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcCValue | double | 8 | NC tovaru bez DPH |
| AcVatVal | double | 8 | Hodnota DPH |
| AcEValue | double | 8 | NC tovaru s DPH |
| AcAValue | double | 8 | Hodnota v PC bez DPH |
| AcBValue | double | 8 | Hodnota v PC s DPH |

### Vyúčtovacia mena (cudzia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Názov vyúčtovacej meny |
| FgCourse | double | 8 | Kurz meny |
| FgDValue | double | 8 | NC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgCValue | double | 8 | NC bez DPH |
| FgVatVal | double | 8 | Hodnota DPH |
| FgEValue | double | 8 | PC s DPH po zľave |

### Ostatné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Volume | double | 8 | Objem tovaru (m3) |
| Weight | double | 8 | Váha tovaru (kg) |
| DscPrc | double | 8 | Percentuálna zľava |
| VatDoc | byte | 1 | Príznak daňového dokladu |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| ItmQnt | word | 2 | Počet položiek |
| IsExpDay | word | 2 | Splatnosť faktúr (dni) |
| RspName | Str30 | 31 | Meno vystaviteľa |
| RspSig | Str5 | 6 | Iniciály vystaviteľa |
| VerSig | Str5 | 6 | Iniciály kontrolóra |
| AprSig | Str5 | 6 | Iniciály schvaľovateľa |

### Stav dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstStk | Str1 | 2 | Príznak príjmu na sklad (N/S) |
| DstLck | byte | 1 | Príznak uzatvorenia |
| DstCls | byte | 1 | Príznak ukončenosti |
| Sended | byte | 1 | Príznak odoslania zmien |
| SndStat | Str1 | 2 | Stav internetového prenosu |
| DstSnd | Str1 | 2 | Príznak odoslania dodávateľovi |
| CnfStat | Str1 | 2 | Stav potvrdenia termínu |

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

## Indexy (15)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | DlvDate | DlvDate | Duplicit |
| 5 | AcEValue | AcEValue | Duplicit |
| 6 | FgEValue | FgEValue | Duplicit |
| 7 | PaCode | PaCode | Duplicit |
| 8 | _PaName | PaName | Duplicit |
| 9 | AcDvzName | AcDvzName | Duplicit, Case insensitive |
| 10 | FgDvzName | FgDvzName | Duplicit, Case insensitive |
| 11 | DstStk | DstStk | Duplicit |
| 12 | DstCls | DstCls | Duplicit |
| 13 | PaCode, DstSnd | PaDs | Duplicit |
| 14 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Dodávateľ |
| StkNum | STKLST.StkNum | Sklad |
| SmCode | SMLST.SmCode | Skladový pohyb |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
