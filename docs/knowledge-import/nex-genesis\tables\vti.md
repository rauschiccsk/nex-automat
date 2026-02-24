# VTI - Položky kontrolného výkazu

## Kľúčové slová / Aliases

VTI, VTI.BTR, položky, kontrolného, výkazu

## Popis

Položky kontrolného výkazu DPH (Kontrolný výkaz k dani z pridanej hodnoty). Každý záznam reprezentuje jeden riadok výkazu s detailmi o doklade a DPH hodnote.

## Btrieve súbor

`VTI.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VTI.BTR`

## Štruktúra polí (26 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok výkazu |
| ClsNum | word | 2 | Číslo uzávierky DPH - **FK VTRLST** |
| RowNum | longint | 4 | Poradové číslo riadku |
| RowTyp | Str2 | 3 | Typ riadku (A1/A2/B1/B2/B3/C1/C2/D1/D2) |

### Identifikácia partnera

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VIN | Str20 | 21 | IČ DPH odberateľa/dodávateľa |

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu |
| ExtNum | Str32 | 33 | Externé číslo dokladu (faktúry) |
| VatDate | DateType | 4 | Dátum dodania tovaru |

### Hodnoty DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue | double | 8 | Základ dane |
| VValue | double | 8 | Daň (DPH) |
| SValue | double | 8 | Výška odpočítateľnej dane |
| VatPrc | byte | 1 | Sadzba dane (%) |

### Tovar (pre colné účely)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SrbCode | Str4 | 5 | Kód Spoločného colného sadzobníka |
| SrtTyp | Str2 | 3 | Druh tovaru (MT/IO) |
| GsQnt | double | 8 | Množstvo tovaru |
| MsName | Str2 | 3 | Merná jednotka (m, ks, t, kg) |

### Opravy (dobropisy/ťarchopisy)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CorNum | Str1 | 2 | Kód opravy (1/2) |
| ODocNum | Str12 | 13 | Interné číslo zdrojového dokladu |
| OExtNum | Str32 | 33 | Externé číslo zdrojového dokladu |

### Hodnoty pre D1/D2 riadky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue1 | double | 8 | Základ dane - základná sadzba |
| VValue1 | double | 8 | Daň - základná sadzba |
| AValue2 | double | 8 | Základ dane - znížená sadzba |
| VValue2 | double | 8 | Daň - znížená sadzba |

### Príznak

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sumarize | byte | 1 | Súhrnný riadok (1=áno) |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, ClsNum, RowNum | YeCnRn | Duplicit |
| 1 | Year, ClsNum | YearClsNum | Duplicit |
| 2 | DocNum, VatPrc | DnVp | Duplicit |
| 3 | ExtNum, VatPrc | EnVp | Duplicit |
| 4 | Year, ClsNum, DocNum, VatPrc, RowTyp | YeCnDnVpRt | Duplicit |

## Typy riadkov (RowTyp)

### Sekcia A - Dodania

| Typ | Popis | VIN |
|-----|-------|-----|
| A1 | Dodanie tovaru/služby | Odberateľ |
| A2 | Oprava dodania (dobropis/ťarchopis) | Odberateľ |

### Sekcia B - Nadobudnutia

| Typ | Popis | VIN |
|-----|-------|-----|
| B1 | Nadobudnutie tovaru z EÚ | Dodávateľ |
| B2 | Prijatie služby z EÚ | Dodávateľ |
| B3 | Tuzemské samozdanenie | Dodávateľ |

### Sekcia C - Dovoz

| Typ | Popis |
|-----|-------|
| C1 | Dovoz tovaru - colný dlh |
| C2 | Dovoz tovaru - odložená platba |

### Sekcia D - Súhrnné riadky

| Typ | Popis |
|-----|-------|
| D1 | Súhrnný riadok |
| D2 | Oprava súhrnného riadku |

## Kódy opravy (CorNum)

| Hodnota | Popis |
|---------|-------|
| 1 | Dobropis |
| 2 | Ťarchopis |

## Druh tovaru (SrtTyp)

| Hodnota | Popis |
|---------|-------|
| MT | Minerálny tovar |
| IO | Iný tovar/služba |

## Použitie

- Generovanie kontrolného výkazu DPH
- XML export pre Finančnú správu SR
- Detail jednotlivých transakcií

## Business pravidlá

- Jeden doklad môže mať viac riadkov (podľa VatPrc)
- ExtNum bez medzier, pomlčky a lomky povolené
- Pre A2/D2 riadky sa vyplňuje ODocNum/OExtNum
- D1/D2 používajú AValue1/VValue1 a AValue2/VValue2
- Sumarize=1 pre súhrnné (agregované) riadky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
