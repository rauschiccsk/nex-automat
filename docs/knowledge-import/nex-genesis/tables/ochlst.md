# OCHLST - Hlavičky zákaziek (LIST štruktúra)

## Kľúčové slová / Aliases

OCHLST, OCHLST.BTR, zoznam hlavičiek objednávok, order headers list

## Popis

Zjednotená tabuľka hlavičiek odberateľských zákaziek zo všetkých kníh. Novšia štruktúra, ktorá agreguje dáta z jednotlivých OCHyynnn súborov do jedného súboru.

## Btrieve súbor

`OCHLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCHLST.BTR`

## Štruktúra polí (119 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BokNum | word | 2 | Číslo knihy |
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Externé číslo (číslo zákazníka) |
| DocDate | DateType | 4 | Dátum prijatia objednávky |
| Year | Str2 | 3 | Rok dokladu |
| StkNum | word | 2 | Číslo priradeného skladu |
| ItmQnt | word | 2 | Počet položiek |

### Termíny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ReqDate | DateType | 4 | Požadovaný termín dodania |
| ConfDate | DateType | 4 | Potvrdený termín dodania |
| ExpDate | DateType | 4 | Termín expedície |
| ShpDate | DateType | 4 | Dátum odoslania |

### Partner (odberateľ)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| PaName | Str30 | 31 | Pracovný názov odberateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu |
| RegName | Str60 | 61 | Registrovaný názov |
| RegIno | Str15 | 16 | IČO |
| RegTin | Str15 | 16 | DIČ |
| RegVin | Str15 | 16 | IČ DPH |
| RegAddr | Str30 | 31 | Adresa |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |

### Dodacia adresa (prevádzka)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WpaCode | word | 2 | Číslo prevádzky |
| WpaName | Str60 | 61 | Názov prevádzky |
| WpaAddr | Str30 | 31 | Adresa prevádzky |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Doprava

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TrsCod | Str1 | 2 | Kód dopravy (C/V/E/O) |
| TrsCode | Str3 | 4 | Kód spôsobu dopravy |
| TrsName | Str20 | 21 | Názov spôsobu dopravy |
| TrsLine | Str3 | 4 | Smer rozvozu |

### Platobné podmienky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCod | Str1 | 2 | Forma úhrady (H/K/B/D/O) |
| PayCode | Str3 | 4 | Kód formy úhrady |
| PayName | Str20 | 21 | Názov formy úhrady |
| PlsNum | word | 2 | Číslo cenníka |
| DscPrc | double | 8 | Zľava % |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Kód účtovnej meny (EUR) |
| AcDValue | double | 8 | PC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcRndVal | double | 8 | Zaokrúhlenie |
| AcCValue | double | 8 | PC bez DPH |
| AcVatVal | double | 8 | Hodnota DPH |
| AcEValue | double | 8 | PC s DPH |
| AcDepVal | double | 8 | Záloha v účtovnej mene |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Kód vyúčtovacej meny |
| FgCourse | double | 8 | Kurz |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgCValue | double | 8 | PC bez DPH |
| FgVatVal | double | 8 | Hodnota DPH |
| FgEValue | double | 8 | PC s DPH |
| FgDepVal | double | 8 | Záloha vo vyúčtovacej mene |

### Stavy dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | Str1 | 2 | Uzamknutie (L=locked, R=creating) |
| DstCls | Str1 | 2 | Ukončenosť (C=closed) |
| DstMod | Str1 | 2 | Modifikácia (M=modified) |
| DstExd | Str1 | 2 | Expedícia (E=expedícia) |
| DstPrn | byte | 1 | Vytlačené |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania |
| SndNum | word | 2 | Poradové číslo odoslania |
| SndStat | Str1 | 2 | Stav prenosu (S/O/E) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (18)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Unique |
| 1 | BokNum, Year, SerNum | BokYrSr | Unique |
| 2 | ExtNum | ExtNum | Case-insensitive, Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | StkNum | StkNum | Duplicit |
| 5 | PaCode | PaCode | Duplicit |
| 6 | _PaName | PaName | Case-insensitive, Duplicit |
| 7 | ReqDate | ReqDate | Duplicit |
| 8 | ConfDate | ConfDate | Duplicit |
| 9 | DstLck | DstLck | Duplicit |
| 10 | DstCls | DstCls | Duplicit |
| 11 | DstExd | DstExd | Duplicit |
| 12 | TrsCod | TrsCod | Duplicit |
| 13 | TrsLine | TrsLine | Duplicit |
| 14 | Sended | Sended | Duplicit |
| 15 | SndStat | SndStat | Duplicit |
| 16 | BokNum | BokNum | Duplicit |
| 17 | Year | Year | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BokNum | OCBLST.BokNum | Kniha zákaziek |
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |

## Rozdiel OCH vs OCHLST

| Aspekt | OCH | OCHLST |
|--------|-----|--------|
| Súbory | Viac súborov (OCHyynnn.BTR) | Jeden súbor (OCHLST.BTR) |
| Prístup | Treba vybrať knihu | Všetky knihy naraz |
| Pole BokNum | Nie (implicitne v názve) | Áno (explicitne) |
| Použitie | Staršie verzie NEX | Novšie verzie NEX |
| Výkon | Rýchlejší pre jednu knihu | Rýchlejší pre prehľady |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
