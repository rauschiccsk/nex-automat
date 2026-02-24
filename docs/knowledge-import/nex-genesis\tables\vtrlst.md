# VTRLST - Zoznam uzávierok DPH

## Kľúčové slová / Aliases

VTRLST, VTRLST.BTR, zoznam, uzávierok, dph

## Popis

Hlavná konfiguračná tabuľka uzávierok DPH. Obsahuje registračné údaje platiteľa, obdobie uzávierky a súhrnné hodnoty DPH.

## Btrieve súbor

`VTRLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VTRLST.BTR`

## Štruktúra polí (42 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ClsNum | word | 2 | Číslo uzávierky DPH (yynnn) - **PRIMARY KEY** |
| Year | Str2 | 3 | Rok výkazu |
| VtcNum | byte | 1 | Číslo kalkulačného obdobia |
| Notice | Str15 | 16 | Popis uzávierky |

### Obdobie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Počiatočný dátum uzávierky |
| EndDate | DateType | 4 | Konečný dátum uzávierky |
| VtrDate | DateType | 4 | Dátum výkazu |

### Typ výkazu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SttTyp | Str1 | 2 | Druh výkazu (R/O/D) |
| AddDate | DateType | 4 | Dátum zistenia dodatočného výkazu |
| OblEnt | byte | 1 | Nevznikla daňová povinnosť (0/1) |

### Hodnoty DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InVatVal | double | 8 | DPH - vstup |
| OuVatVal | double | 8 | DPH - výstup |
| DfVatVal | double | 8 | DPH - rozdiel (daňová povinnosť) |
| RndVal | double | 8 | Zaokrúhlenie podľa predpisov |
| VatVal | double | 8 | DPH k úhrade |
| PayVal | double | 8 | Uhradená suma |
| EndVal | double | 8 | Zostatok k úhrade |
| PayDate | DateType | 4 | Dátum úhrady |

### Registračné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VIN | Str20 | 21 | IČ DPH |
| TIN | Str20 | 21 | DIČ |
| VatPrs | Str1 | 2 | Osoba platiteľa (P/I/O/Z/D) |
| RegName | Str60 | 61 | Názov/meno platiteľa |
| PaAddr1 | Str60 | 61 | Adresa - ulica |
| PaAddr2 | Str10 | 11 | Adresa - číslo |
| RegStn | Str30 | 31 | Štát |
| RegCtn | Str30 | 31 | Mesto |
| RegZip | Str6 | 7 | PSČ |
| RegEml | Str60 | 61 | Email |
| RegTel | Str30 | 31 | Telefón |
| RegFax | Str30 | 31 | Fax |

### Oprávnená osoba

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AutNam | Str60 | 61 | Meno oprávnenej osoby |
| AutTel | Str30 | 31 | Telefón oprávnenej osoby |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | word | 2 | Počet daňových dokladov |
| PrnQnt | word | 2 | Počet vytlačených kópií |
| DocCls | byte | 1 | Uzatvorenie dokladov (1=zapnuté) |

### Väzba na zdrojový výkaz

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SrcYear | Str2 | 3 | Rok zdrojového výkazu |
| SrcNum | longint | 4 | Číslo zdrojového výkazu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, ClsNum | YearClsNum | Unikátny |
| 1 | ClsNum | ClsNum | Duplicit |
| 2 | SrcYear, SrcNum | SySn | Duplicit |

## Typy výkazu (SttTyp)

| Hodnota | Popis |
|---------|-------|
| R | Riadny výkaz |
| O | Opravný výkaz |
| D | Dodatočný výkaz |

## Osoby platiteľa (VatPrs)

| Hodnota | Popis |
|---------|-------|
| P | Právnická osoba |
| I | Individuálny podnikateľ (SZČO) |
| O | Ostatné osoby |
| Z | Zahraničná osoba |
| D | Dedič |

## Použitie

- Evidencia DPH uzávierok
- Registračné údaje pre XML export
- Sledovanie úhrad daňovej povinnosti

## Business pravidlá

- ClsNum formát: yynnn (yy=rok, nnn=poradové číslo)
- DfVatVal = OuVatVal - InVatVal
- VatVal = DfVatVal + RndVal
- EndVal = VatVal - PayVal
- DocCls=1 uzatvára započítané doklady
- Pri dodatočnom výkaze (SttTyp='D') sa nastaví SrcYear/SrcNum

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
