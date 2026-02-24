# MCH - Hlavičky odberateľských cenových ponúk

## Kľúčové slová / Aliases

MCH, MCH.BTR, hlavičky, odberateľských, cenových, ponúk

## Popis

Hlavičková tabuľka odberateľských cenových ponúk. Obsahuje komplexné údaje o ponuke vrátane odberateľa, duálnych mien, zliav, zodpovedných osôb a sledovania vybavenosti.

## Btrieve súbor

`MCHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\MCHyynnn.BTR`

## Štruktúra polí (126 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Poradové číslo ponuky |
| DocNum | Str12 | 13 | Interné číslo ponuky - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo ponuky |
| DocDate | DateType | 4 | Dátum vystavenia |
| ExpDate | DateType | 4 | Dátum platnosti ponuky |
| DlvDate | DateType | 4 | Dátum navrhovanej dodávky |

### Sklad a cenník

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo priradeného skladu |
| PlsNum | word | 2 | Číslo predajného cenníka |
| AplNum | word | 2 | Číslo akciového cenníka |

### Odberateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód odberateľa - **FK → PAB.PaCode** |
| PaName | Str30 | 31 | Názov odberateľa |
| _PaName | Str20 | 21 | Vyhľadávacie pole názvu |
| RegName | Str60 | 61 | Registrovaný názov firmy |
| RegIno | Str15 | 16 | IČO partnera |
| RegTin | Str15 | 16 | DIČ partnera |
| RegVin | Str15 | 16 | IČ pre DPH |
| RegAddr | Str30 | 31 | Registrovaná adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Miesto dodania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SpaCode | longint | 4 | Kód príjemcu tovaru |
| WpaCode | word | 2 | Číslo prevádzkovej jednotky |
| WpaName | Str60 | 61 | Názov prevádzky |
| WpaAddr | Str30 | 31 | Adresa prevádzky |
| WpaSta | Str2 | 3 | Kód štátu prevádzky |
| WpaCty | Str3 | 4 | Kód obce prevádzky |
| WpaCtn | Str30 | 31 | Názov mesta prevádzky |
| WpaZip | Str15 | 16 | PSČ prevádzky |

### Platba a doprava

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Skratka formy úhrady |
| PayName | Str20 | 21 | Názov formy úhrady |
| TrsCode | Str3 | 4 | Kód spôsobu dopravy |
| TrsName | Str20 | 21 | Názov spôsobu dopravy |
| MyConto | Str30 | 31 | Bankový účet dodávateľa |

### Zľavy a zálohy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscPrc | double | 8 | Percentuálna zľava |
| PrfPrc | double | 8 | Percentuálna záloha |
| IcFacDay | word | 2 | Factoringová splatnosť (dni) |
| IcFacPrc | double | 8 | Zvýšenie cien pri factoringu (%) |

### DPH skupiny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1-5 | byte | 1 | Sadzby DPH skupín 1-5 |
| VatDoc | byte | 1 | Daňový doklad (1=DPH) |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Názov účtovnej meny |
| AcCValue | double | 8 | NC bez DPH |
| AcDValue | double | 8 | PC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcAValue | double | 8 | PC bez DPH po zľave |
| AcBValue | double | 8 | PC s DPH po zľave |
| AcVatVal | double | 8 | DPH z PC |
| AcPValue | double | 8 | Hodnota zálohy |
| AcAValue1-5 | double | 8 | PC bez DPH podľa DPH skupín |
| AcBValue1-5 | double | 8 | PC s DPH podľa DPH skupín |
| AcPayVal | double | 8 | Uhradená čiastka |
| AcEndVal | double | 8 | Zostatok k úhrade |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Názov vyúčtovacej meny |
| FgCourse | double | 8 | Kurz meny |
| FgCValue | double | 8 | NC bez DPH |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgAValue | double | 8 | PC bez DPH po zľave |
| FgVatVal | double | 8 | DPH z PC |
| FgBValue | double | 8 | PC s DPH po zľave |
| FgPValue | double | 8 | Hodnota zálohy |
| FgAValue1-5 | double | 8 | PC bez DPH podľa DPH skupín |
| FgBValue1-5 | double | 8 | PC s DPH podľa DPH skupín |
| FgPayVal | double | 8 | Uhradená čiastka |
| FgEndVal | double | 8 | Zostatok k úhrade |

### Zisk

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ProPrc | double | 8 | Zisk percentuálne |
| ProVal | double | 8 | Hodnota zisku |

### Vybavenosť

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| EquVal | double | 8 | Kumulatívna hodnota vybavených položiek |
| EquPrc | byte | 1 | Úspešnosť vybavenosti (%) |
| NeqNum | word | 2 | Dôvod nevybavenosti |

### Zodpovedné osoby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DlrCode | word | 2 | Kód obchodného zástupcu |
| Reserve | Str20 | 21 | Meno vystaviteľa |
| RspNum | word | 2 | Kód zodpovednej osoby |
| RspName | Str30 | 31 | Meno zodpovednej osoby |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | byte | 1 | Uzatvorenie (1=uzatvorený) |
| Accept | byte | 1 | Akceptovaná zákazníkom (1=áno) |
| DcCode | byte | 1 | Kód dôvodu odmietnutia |
| DstSpi | byte | 1 | Zálohová platba (1=áno) |
| DstPay | byte | 1 | Uhradená (1=áno) |
| PayDate | DateType | 4 | Dátum poslednej úhrady |

### Schvaľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SigUid1 | Str3 | 4 | Schválenie Level-1 |
| SigUid2 | Str3 | 4 | Schválenie Level-2 |
| SigUid3 | Str3 | 4 | Schválenie Level-3 |

### Projekt

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrjCode | Str12 | 13 | Kód projektu |
| PrjSub | word | 2 | Číslo podprojektu |

### Zákazník

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CusCard | Str20 | 21 | Číslo zákazníckej karty |
| CusReq | Str20 | 21 | Zákaznícke číslo požiadavky |
| CusTel | Str20 | 21 | Telefónny kontakt |
| CumEml | Str30 | 31 | Emailový kontakt |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| DocDes | Str50 | 51 | Popis dokladu |
| _DocDes | Str50 | 51 | Popis pre vyhľadávanie |
| SpMark | Str10 | 11 | Všeobecné označenie |
| IddQnt | word | 2 | Odložená splatnosť (dni) |
| DlvDay | word | 2 | Termín dodávky (dni) |
| TrmNum | word | 2 | Číslo mobilného zariadenia |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (14)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unique |
| 1 | DocNum | DocNum | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | ExpDate | ExpDate | Duplicit |
| 5 | PaCode | PaCode | Duplicit |
| 6 | _PaName | PaName | Duplicit |
| 7 | AcDvzName | AcDvzName | Duplicit, Case insensitive |
| 8 | FgDvzName | FgDvzName | Duplicit, Case insensitive |
| 9 | AcBValue | AcBValue | Duplicit |
| 10 | FgBValue | FgBValue | Duplicit |
| 11 | Accept | Accept | Duplicit |
| 12 | PrjCode | PrjCode | Duplicit |
| 13 | _DocDes | DocDes | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |
| PlsNum | PLSLST.PlsNum | Cenník |
| AplNum | APLLST.AplNum | Akciový cenník |
| DlrCode | DLRLST.DlrCode | Obchodný zástupca |

## Použitie

- Vytváranie cenových ponúk
- Sledovanie platnosti a akceptácie
- Multi-menové ponuky
- Sledovanie vybavenosti

## Business pravidlá

- ExpDate definuje platnosť ponuky
- Accept=1 znamená akceptáciu zákazníkom
- EquPrc=100 znamená plnú vybavenosť
- DstLck=1 znemožňuje ďalšie úpravy

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
