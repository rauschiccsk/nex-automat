# KSH - Hlavičky dokladov konsignačného vyúčtovania

## Kľúčové slová / Aliases

KSH, KSH.BTR, hlavičky, dokladov, konsignačného, vyúčtovania

## Popis

Tabuľka hlavičiek dokladov konsignačného (komisionálneho) vyúčtovania. Obsahuje sumárne údaje o vyúčtovaní za obdobie vrátane partnera, skladu a finančných hodnôt. Každá kniha má vlastný súbor.

## Btrieve súbor

`KSHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\KSHyynnn.BTR`

## Štruktúra polí (29 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |
| Year | Str2 | 3 | Rok dokladu |

### Sklad a partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu - **FK STKLST** |
| PaCode | longint | 4 | Číselný kód firmy - **FK PAB** |
| PaName | Str60 | 61 | Pracovný názov firmy |
| _PaName | Str60 | 61 | Vyhľadávacie pole názvu |

### Obdobie vyúčtovania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Začiatok dátumového intervalu |
| EndDate | DateType | 4 | Koniec dátumového intervalu |

### DPH sadzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH daňovej skupiny č.1 |
| VatPrc2 | byte | 1 | Sadzba DPH daňovej skupiny č.2 |
| VatPrc3 | byte | 1 | Sadzba DPH daňovej skupiny č.3 |

### Finančné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue | double | 8 | Nákupná cena tovaru bez DPH |
| EValue | double | 8 | Nákupná cena tovaru s DPH |
| PrfPrc | double | 8 | Obchodná marža v % |
| PrfVal | double | 8 | Obchodná marža v EUR |
| AValue | double | 8 | Predajná cena bez DPH |
| BValue | double | 8 | Predajná cena s DPH |

### Väzba na DL

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsdNum | Str12 | 13 | Číslo vystavného dodávateľského DL |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrnCnt | byte | 1 | Počet vytlačených kópií dokladu |
| ItmQnt | word | 2 | Počet položiek dokladu |
| DstLck | byte | 1 | Príznak uzatvorenia (1=uzatvorený) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | DocNum | DocNum | Duplicit |
| 2 | DocDate | DocDate | Duplicit |
| 3 | StkNum | StkNum | Duplicit |
| 4 | PaCode | PaCode | Duplicit |
| 5 | _PaName | PaName | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| PaCode | PAB.PaCode | Dodávateľ |
| DocNum | KSI.DocNum | Položky dokladu |
| DocNum | KSN.DocNum | Poznámky |
| DocNum | KSO.DocNum | História pohybov |
| TsdNum | TSH.DocNum | Vygenerovaný dodací list |

## Použitie

- Evidencia dokladov konsignačného vyúčtovania
- Sumárne údaje za obdobie
- Väzba na vygenerované dodacie listy
- Sledovanie stavu vyúčtovania

## Business pravidlá

- TsdNum='' znamená otvorený doklad (môže sa upravovať)
- TsdNum<>'' znamená uzavretý doklad (vygenerovaný DL)
- Doklad možno zmazať len ak ItmQnt=0
- BegDate-EndDate definuje obdobie pre výber predajov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
