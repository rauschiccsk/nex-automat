# ACDTMP - Dočasný doklad akciového precenenia

## Kľúčové slová / Aliases

ACDTMP, ACDTMP.BTR, dočasný, doklad, akciového, precenenia

## Popis

Pracovná tabuľka pre dočasné uloženie položiek pred ich zápisom do precenovacieho dokladu. Slúži ako medzipamäť pri hromadnom pridávaní položiek.

## Btrieve súbor

`ACDTMP.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACDTMP.BTR`

## Štruktúra polí (14 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **PK** |
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Identifikačný kód tovaru (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Názov mernej jednotky |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH v % |
| StkCPrice | double | 8 | Nákupná cena tovaru bez DPH |
| BefBPrice | double | 8 | Predajná cena s DPH pred precenením |
| NewBPrice | double | 8 | Akciová predajná cena s DPH |
| BefProfit | double | 8 | Zisk v % pred precenením |
| NewProfit | double | 8 | Zisk v % počas akciovej ceny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |

## Použitie

- Dočasné uloženie položiek pred zápisom do ACI
- Hromadný import akciových cien
- Príprava precenovacieho dokladu

## Business pravidlá

- Tabuľka sa vyprázdňuje pred každým použitím
- Po potvrdení sa položky presunú do ACI
- Neobsahuje AftBPrice (cena po akcii)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
