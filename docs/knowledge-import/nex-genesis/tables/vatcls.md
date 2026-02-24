# VATCLS - Súhrn uzávierok DPH

## Kľúčové slová / Aliases

VATCLS, VATCLS.BTR, súhrn, uzávierok, dph

## Popis

Súhrnná tabuľka uzávierok DPH s detailným rozpisom hodnôt podľa smeru (vstup/výstup), pôvodu (tuzemsko/zahraničie) a 6 skupín sadzieb DPH.

## Btrieve súbor

`VATCLS.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VATCLS.BTR`

## Štruktúra polí (57 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ClsNum | Str5 | 6 | Číslo uzávierky DPH (yynnn) - **PRIMARY KEY** |
| BegDate | DateType | 4 | Počiatočný dátum uzávierky |
| EndDate | DateType | 4 | Konečný dátum uzávierky |
| Notice | Str15 | 16 | Popis uzávierky |

### Sadzby DPH (6 skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH % - skupina 1 |
| VatPrc2 | byte | 1 | Sadzba DPH % - skupina 2 |
| VatPrc3 | byte | 1 | Sadzba DPH % - skupina 3 |
| VatPrc4 | byte | 1 | Sadzba DPH % - skupina 4 |
| VatPrc5 | byte | 1 | Sadzba DPH % - skupina 5 |
| VatPrc6 | byte | 1 | Sadzba DPH % - skupina 6 |

### Vstup - Tuzemsko (Ii = Input internal)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IiAValue1 | double | 8 | Základ DPH - vstup/tuzemsko - skupina 1 |
| IiAValue2 | double | 8 | Základ DPH - vstup/tuzemsko - skupina 2 |
| IiAValue3 | double | 8 | Základ DPH - vstup/tuzemsko - skupina 3 |
| IiAValue4 | double | 8 | Základ DPH - vstup/tuzemsko - skupina 4 |
| IiAValue5 | double | 8 | Základ DPH - vstup/tuzemsko - skupina 5 |
| IiAValue6 | double | 8 | Základ DPH - vstup/tuzemsko - skupina 6 |
| IiVatVal1 | double | 8 | Hodnota DPH - vstup/tuzemsko - skupina 1 |
| IiVatVal2 | double | 8 | Hodnota DPH - vstup/tuzemsko - skupina 2 |
| IiVatVal3 | double | 8 | Hodnota DPH - vstup/tuzemsko - skupina 3 |
| IiVatVal4 | double | 8 | Hodnota DPH - vstup/tuzemsko - skupina 4 |
| IiVatVal5 | double | 8 | Hodnota DPH - vstup/tuzemsko - skupina 5 |
| IiVatVal6 | double | 8 | Hodnota DPH - vstup/tuzemsko - skupina 6 |

### Vstup - Zahraničie (If = Input foreign)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IfAValue1 | double | 8 | Základ DPH - vstup/zahraničie - skupina 1 |
| IfAValue2 | double | 8 | Základ DPH - vstup/zahraničie - skupina 2 |
| IfAValue3 | double | 8 | Základ DPH - vstup/zahraničie - skupina 3 |
| IfAValue4 | double | 8 | Základ DPH - vstup/zahraničie - skupina 4 |
| IfAValue5 | double | 8 | Základ DPH - vstup/zahraničie - skupina 5 |
| IfAValue6 | double | 8 | Základ DPH - vstup/zahraničie - skupina 6 |
| IfVatVal1 | double | 8 | Hodnota DPH - vstup/zahraničie - skupina 1 |
| IfVatVal2 | double | 8 | Hodnota DPH - vstup/zahraničie - skupina 2 |
| IfVatVal3 | double | 8 | Hodnota DPH - vstup/zahraničie - skupina 3 |
| IfVatVal4 | double | 8 | Hodnota DPH - vstup/zahraničie - skupina 4 |
| IfVatVal5 | double | 8 | Hodnota DPH - vstup/zahraničie - skupina 5 |
| IfVatVal6 | double | 8 | Hodnota DPH - vstup/zahraničie - skupina 6 |

### Výstup (O = Output)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OAValue1 | double | 8 | Základ DPH - výstup - skupina 1 |
| OAValue2 | double | 8 | Základ DPH - výstup - skupina 2 |
| OAValue3 | double | 8 | Základ DPH - výstup - skupina 3 |
| OAValue4 | double | 8 | Základ DPH - výstup - skupina 4 |
| OAValue5 | double | 8 | Základ DPH - výstup - skupina 5 |
| OAValue6 | double | 8 | Základ DPH - výstup - skupina 6 |
| OVatVal1 | double | 8 | Hodnota DPH - výstup - skupina 1 |
| OVatVal2 | double | 8 | Hodnota DPH - výstup - skupina 2 |
| OVatVal3 | double | 8 | Hodnota DPH - výstup - skupina 3 |
| OVatVal4 | double | 8 | Hodnota DPH - výstup - skupina 4 |
| OVatVal5 | double | 8 | Hodnota DPH - výstup - skupina 5 |
| OVatVal6 | double | 8 | Hodnota DPH - výstup - skupina 6 |

### Súhrnné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IVatVal | double | 8 | Celková hodnota DPH - vstup |
| OVatVal | double | 8 | Celková hodnota DPH - výstup |
| DVatVal | double | 8 | Hodnota DPH - rozdiel (daňová povinnosť) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IDocQnt | word | 2 | Počet dokladov na vstupe |
| ODocQnt | word | 2 | Počet dokladov na výstupe |
| PrnQnt | word | 2 | Počet vytlačených kópií |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | ClsNum | ClsNum | Duplicit |

## Konvencia názvov polí

| Prefix | Význam |
|--------|--------|
| Ii | Input internal (vstup tuzemsko) |
| If | Input foreign (vstup zahraničie) |
| O | Output (výstup) |
| A | Amount (základ dane) |
| Vat | DPH hodnota |
| 1-6 | Číslo skupiny DPH |

## Výpočtové pravidlá

```
IVatVal = SUM(IiVatVal1..6) + SUM(IfVatVal1..6)
OVatVal = SUM(OVatVal1..6)
DVatVal = OVatVal - IVatVal
```

## Použitie

- Súhrnný prehľad uzávierky DPH
- Podklad pre tlač a export
- Archivácia hodnôt uzávierky

## Business pravidlá

- Jeden záznam na uzávierku
- Rozlíšenie tuzemských a zahraničných vstupov
- DVatVal > 0 = daňová povinnosť
- DVatVal < 0 = nadmerný odpočet

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
