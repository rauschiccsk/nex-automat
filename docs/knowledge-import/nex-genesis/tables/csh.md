# CSH - Hlavičky hotovostných pokladničných dokladov

## Kľúčové slová / Aliases

CSH, CSH.BTR, hlavičky, hotovostných, pokladničných, dokladov

## Popis

Hlavičková tabuľka hotovostných pokladničných dokladov. Obsahuje údaje o príjmových a výdajových dokladoch vrátane duálnych mien (účtovná a pokladničná), DPH členenia, zostatkov a stavu pokladne.

## Btrieve súbor

`CSHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSHyynnn.BTR`

## Štruktúra polí (82 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Chronologické poradové číslo |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| DocCnt | word | 2 | Typové poradové číslo |
| DocType | Str1 | 2 | Typ dokladu (I=príjem, E=výdaj) |
| DocDate | DateType | 4 | Dátum zaúčtovania |

### Prevádzkové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| OcdNum | Str12 | 13 | Číslo odberateľskej objednávky |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód partnera - **FK → PAB.PaCode** |
| PaName | Str30 | 31 | Pracovný názov partnera |
| _PaName | Str30 | 31 | Vyhľadávacie pole |
| RegName | Str60 | 61 | Registrovaný názov firmy |
| RegIno | Str15 | 16 | IČO partnera |
| RegTin | Str15 | 16 | DIČ partnera |
| RegVin | Str15 | 16 | IČ pre DPH |
| RegAddr | Str30 | 31 | Registrovaná adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Vodič

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DrvCode | word | 2 | Kód vodiča |
| DrvName | Str30 | 31 | Meno a priezvisko vodiča |
| CarMark | Str10 | 11 | ŠPZ vozidla |

### Poznámka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Notice | Str30 | 31 | Poznámka k dokladu |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH skupiny 1 (%) |
| VatPrc2 | byte | 1 | Sadzba DPH skupiny 2 (%) |
| VatPrc3 | byte | 1 | Sadzba DPH skupiny 3 (%) |
| VatPrc4 | byte | 1 | Sadzba DPH skupiny 4 (%) |
| VatPrc5 | byte | 1 | Sadzba DPH skupiny 5 (%) |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Názov účtovnej meny |
| AcAValue | double | 8 | Hodnota bez DPH |
| AcVatVal | double | 8 | Hodnota DPH |
| AcBValue | double | 8 | Hodnota s DPH |
| AcAValue1-5 | double | 8 | Hodnota bez DPH podľa DPH skupín |
| AcBValue1-5 | double | 8 | Hodnota s DPH podľa DPH skupín |

### Hodnoty v pokladničnej mene (Py*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PyDvzName | Str3 | 4 | Názov pokladničnej meny |
| PyCourse | double | 8 | Kurz meny |
| PyAValue | double | 8 | Hodnota bez DPH |
| PyVatVal | double | 8 | Hodnota DPH |
| PyBValue | double | 8 | Hodnota s DPH |
| PyBegVal | double | 8 | Počiatočný stav pred dokladom |
| PyIncVal | double | 8 | Hodnota príjmu |
| PyExpVal | double | 8 | Hodnota výdaja |
| PyEndVal | double | 8 | Zostatok po zaúčtovaní |
| PyAValue1-5 | double | 8 | Hodnota bez DPH podľa DPH skupín |
| PyBValue1-5 | double | 8 | Hodnota s DPH podľa DPH skupín |

### Vylúčené hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExcCosVal | double | 8 | Vylúčená čiastka z nákladov |
| ExcVatVal | double | 8 | Vylúčená čiastka z DPH |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| DocSpc | byte | 1 | Špecifikácia dokladu |
| VatCls | byte | 1 | Číslo uzávierky DPH |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstAcc | Str1 | 2 | Zaúčtovaný (A=zaúčtovaný) |
| DstLck | byte | 1 | Uzatvorený (1=uzatvorený) |
| DstLiq | Str1 | 2 | Likvidovaný (L=likvidovaný) |
| Sended | byte | 1 | Odoslané zmeny (0=zmenený, 1=odoslaný) |
| SndStat | Str1 | 2 | Stav prenosu (.-odoslaný, O-potvrdený, E-chyba) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (13)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | DocType, DocCnt | DtDc | Duplicit |
| 3 | PaCode | PaCode | Duplicit |
| 4 | _PaName | PaName | Duplicit |
| 5 | PyIncVal | PyIncVal | Duplicit |
| 6 | PyExpVal | PyExpVal | Duplicit |
| 7 | DocDate | DocDate | Duplicit |
| 8 | DrvCode | DrvCode | Duplicit |
| 9 | CarMark | CarMark | Duplicit |
| 10 | Sended | Sended | Duplicit |
| 11 | DstAcc | DstAcc | Duplicit |
| 12 | DstLiq | DstLiq | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Obchodný partner |
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| DrvCode | DRVLST.DrvCode | Vodič |

## Typy dokladov (DocType)

| Hodnota | Popis |
|---------|-------|
| I | Príjmový pokladničný doklad |
| E | Výdajový pokladničný doklad |

## Použitie

- Príjmové a výdajové pokladničné doklady
- Úhrady faktúr
- Evidencia stavu pokladne
- Pokladničná kniha

## Business pravidlá

- DocType='I' - príjem (PyIncVal)
- DocType='E' - výdaj (PyExpVal)
- PyEndVal = PyBegVal + PyIncVal - PyExpVal
- DstAcc='A' po zaúčtovaní
- DstLiq='L' pre likvidované doklady

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
