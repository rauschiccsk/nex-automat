# OCD - Zrušené položky zákaziek

## Kľúčové slová / Aliases

OCD, OCD.BTR, objednávky doručenia, order deliveries, dodanie

## Popis

Archívna tabuľka stornovaných/zrušených položiek z odberateľských zákaziek. Uchováva históriu stornovaných položiek pre audit a analýzu.

## Btrieve súbor

`OCDyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCDyynnn.BTR`

## Štruktúra polí (68 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo zákazky - **FK → OCH.DocNum** |
| ItmNum | word | 2 | Pôvodné poradové číslo položky |
| CncNum | word | 2 | Poradové číslo storna |
| CncDate | DateType | 4 | Dátum storna |
| CncReason | Str1 | 2 | Dôvod storna |

### Tovar (kópia z OCI)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | Str15 | 16 | Kód tovaru |
| GsName | Str40 | 41 | Názov tovaru |
| GsUnit | Str4 | 5 | Jednotka |
| MglNum | longint | 4 | Kód výrobcu |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SalPrq | double | 8 | Pôvodné objednané množstvo |
| CncPrq | double | 8 | Stornované množstvo |
| RstPrq | double | 8 | Uvoľnené rezervované množstvo |
| RosPrq | double | 8 | Uvoľnené z objednávok |

### Ceny v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Kód účtovnej meny |
| AcNValue | double | 8 | Nákupná cena |
| AcCValue | double | 8 | Jednotková PC bez DPH |
| AcEValue | double | 8 | Jednotková PC s DPH |
| AcSValue | double | 8 | Celková hodnota storna |

### Ceny vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Kód vyúčtovacej meny |
| FgCourse | double | 8 | Kurz |
| FgCValue | double | 8 | Jednotková PC bez DPH |
| FgEValue | double | 8 | Jednotková PC s DPH |
| FgSValue | double | 8 | Celková hodnota storna |

### DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatNum | byte | 1 | Číslo sadzby DPH |
| VatPrc | byte | 1 | Sadzba DPH % |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ storna |
| CrtDate | DateType | 4 | Dátum storna |
| CrtTime | TimeType | 4 | Čas storna |
| Note | Str100 | 101 | Poznámka k stornu |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, CncNum | DocItmCnc | Unique |
| 1 | DocNum | DocNum | Case-insensitive, Duplicit |
| 2 | GsCode | GsCode | Case-insensitive, Duplicit |
| 3 | CncDate | CncDate | Duplicit |
| 4 | CncReason | CncReason | Duplicit |
| 5 | CrtUser | CrtUser | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCH.DocNum | Hlavička zákazky |
| GsCode | GSCAT.GsCode | Tovar |

## Dôvody storna (CncReason)

| Hodnota | Popis |
|---------|-------|
| C | Zrušené zákazníkom |
| N | Tovar nedostupný |
| P | Zmena ceny |
| D | Duplicita |
| E | Chyba zadania |
| O | Iný dôvod |

## Workflow

```
1. Položka v OCI
   ↓
2. Požiadavka na storno (A_OciCnc)
   ↓
3. Uvoľnenie rezervácií (STS)
   ↓
4. Kópia položky do OCD
   ↓
5. Aktualizácia OCI.CncPrq
   ↓
6. Prepočet OCH hodnôt
```

## Business pravidlá

- Stornované položky sa archivujú
- Rezervácie sa automaticky uvoľňujú
- Celková hodnota sa prepočíta
- História stornovaní pre analýzu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
