# KSI - Položky dokladov konsignačného vyúčtovania

## Kľúčové slová / Aliases

KSI, KSI.BTR, položky, dokladov, konsignačného, vyúčtovania

## Popis

Tabuľka položiek dokladov konsignačného (komisionálneho) vyúčtovania. Obsahuje detaily o jednotlivých tovaroch vrátane väzby na pôvodný konsignačný príjem a vygenerovaný dodací list. Každá kniha má vlastný súbor.

## Btrieve súbor

`KSIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\KSIyynnn.BTR`

## Štruktúra polí (36 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK KSH** |
| ItmNum | word | 2 | Poradové číslo položky dokladu |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK GSCAT** |
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód tovaru (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka tovaru |
| Notice | Str30 | 31 | Poznámka k tovarovej položke |

### Množstvo a ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Vyúčtované množstvo |
| VatPrc | double | 8 | Sadzba DPH v % |
| CPrice | double | 8 | Nákupná cena/MJ bez DPH |
| CValue | double | 8 | Nákupná cena tovaru bez DPH |
| EValue | double | 8 | Nákupná cena tovaru s DPH |
| PrfPrc | double | 8 | Obchodná marža v % |
| PrfVal | double | 8 | Obchodná marža v EUR |
| AValue | double | 8 | Predajná cena bez DPH |
| BValue | double | 8 | Predajná cena s DPH |

### Väzba na partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód dodávateľa |

### Väzba na konsignačný príjem

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FifNum | longint | 4 | Číslo FIFO karty konsignačného príjmu |
| KidNum | Str12 | 13 | Interné číslo dokladu konsignačného príjmu |
| KidItm | word | 2 | Poradové číslo položky konsignačného príjmu |
| KidDate | DateType | 4 | Dátum konsignačného príjmu |

### Väzba na vygenerovaný DL

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsdNum | Str12 | 13 | Interné číslo riadneho príjmu (vyúčtovanie) |
| TsdItm | word | 2 | Poradové číslo položky riadneho príjmu |
| TsdDate | DateType | 4 | Dátum riadneho príjmu |

### DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CctVat | byte | 1 | Prevod daňovej povinnosti DPH podľa colného sadzobníka |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | DocNum | DocNum | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | BarCode | BarCode | Duplicit, Case-insensitive |
| 4 | StkCode | StkCode | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | KSH.DocNum | Hlavička dokladu |
| GsCode | GSCAT.GsCode | Katalógová karta produktu |
| PaCode | PAB.PaCode | Dodávateľ |
| FifNum | FIF.FifNum | FIFO karta konsignačného príjmu |
| KidNum | TSH.DocNum | Doklad konsignačného príjmu |
| TsdNum | TSH.DocNum | Doklad vyúčtovacieho príjmu |

## Použitie

- Evidencia položiek konsignačného vyúčtovania
- Sledovanie pôvodu tovaru (KidNum, FifNum)
- Väzba na vygenerované DL (TsdNum)
- Podklad pre fakturáciu

## Business pravidlá

- FifNum odkazuje na FIFO kartu s AcqStat='K' (konsignácia)
- Po vyúčtovaní sa TsdNum vyplní číslom vygenerovaného DL
- GsQnt sa sumarizuje z predajov v období BegDate-EndDate
- CctVat pre prenesenie daňovej povinnosti

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
