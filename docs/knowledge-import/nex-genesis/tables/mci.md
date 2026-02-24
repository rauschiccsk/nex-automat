# MCI - Položky odberateľských cenových ponúk

## Kľúčové slová / Aliases

MCI, MCI.BTR, položky, odberateľských, cenových, ponúk

## Popis

Položková tabuľka odberateľských cenových ponúk. Obsahuje detailné informácie o ponúkanom tovare vrátane cien v dvoch menách, zliav a stavu realizácie.

## Btrieve súbor

`MCIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\MCIyynnn.BTR`

## Štruktúra polí (61 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo ponuky - **FK → MCH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum vystavenia ponuky |
| ExpDate | DateType | 4 | Dodacia lehota |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Tovarová skupina |
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT.GsCode** |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| GsType | Str1 | 2 | Typ položky (T=tovar, W=váhový, O=obal) |
| MsName | Str10 | 11 | Merná jednotka |
| PackGs | longint | 4 | Tovarové číslo vratného obalu |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Množstvo tovaru |
| OfrQnt | Str20 | 21 | Množstvo pre platnosť ponuky |
| DlvQnt | double | 8 | Dodané množstvo (zákazka vytvorená) |
| Volume | double | 8 | Objem tovaru |
| Weight | double | 8 | Váha tovaru |

### Ceny a zľavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH (%) |
| DscPrc | double | 8 | Percentuálna zľava |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcCValue | double | 8 | NC bez DPH |
| AcDValue | double | 8 | PC bez DPH pred zľavou |
| AcDscVal | double | 8 | Hodnota zľavy |
| AcAValue | double | 8 | PC bez DPH po zľave |
| AcBValue | double | 8 | PC s DPH po zľave |

### Ceny vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgCPrice | double | 8 | NC/MJ bez DPH |
| FgDPrice | double | 8 | PC/MJ bez DPH pred zľavou |
| FgAPrice | double | 8 | PC/MJ bez DPH po zľave |
| FgBPrice | double | 8 | PC/MJ s DPH po zľave |

### Hodnoty vo vyúčtovacej mene (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgCValue | double | 8 | NC bez DPH |
| FgDValue | double | 8 | PC bez DPH pred zľavou |
| FgDscVal | double | 8 | Hodnota zľavy |
| FgAValue | double | 8 | PC bez DPH po zľave |
| FgBValue | double | 8 | PC s DPH po zľave |

### Alternatívne hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BciAvalue | double | 8 | Hodnota podľa obchodných podmienok |
| PrjAvalue | double | 8 | Hodnota v projektových cenách |
| SrcCPrice | Str1 | 2 | Zdroj NC (B=obch. podmienky, A=priem. NC) |

### Nadväznosti

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| StkNum | word | 2 | Číslo skladu rezervácie |
| SupPaCode | longint | 4 | Kód dodávateľa tovaru |

### Zákazka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo odberateľskej zákazky |
| OcdItm | word | 2 | Riadok odberateľskej zákazky |
| OcdDate | DateType | 4 | Dátum odberateľskej zákazky |

### Dodací list

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TcdNum | Str12 | 13 | Číslo dodacieho listu |
| TcdItm | word | 2 | Riadok dodacieho listu |
| TcdDate | DateType | 4 | Dátum dodacieho listu |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Stav položky (N/D/R/E) |
| Action | Str1 | 2 | Akciový tovar (A=akcia) |
| DcCode | byte | 1 | Kód dôvodu odmietnutia |
| Cctvat | byte | 1 | Prevod daňovej povinnosti DPH |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Notice | Str30 | 31 | Poznámka k položke |
| DlrCode | word | 2 | Kód obchodného zástupcu |
| SpMark | Str10 | 11 | Všeobecné označenie |
| ModNum | word | 2 | Poradové číslo modifikácie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | DocNum, GsCode | DoGs | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | PaCode | PaCode | Duplicit |
| 5 | Status | Status | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | MCH.DocNum | Hlavička ponuky |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |
| OcdNum | OCH.DocNum | Odberateľská zákazka |
| TcdNum | TCH.DocNum | Dodací list |

## Stavy položky (Status)

| Hodnota | Popis |
|---------|-------|
| N | Vystavená (nová) |
| D | Odmietnutá |
| R | Realizuje sa |
| E | Ukončená (vybavená) |

## Použitie

- Položky cenových ponúk
- Sledovanie realizácie
- Prepojenie na zákazky a DDL
- Multi-menové kalkulácie

## Business pravidlá

- FgAValue = FgAPrice × GsQnt
- FgBValue = FgBPrice × GsQnt
- Status='E' znamená ukončenú položku
- DlvQnt sleduje dodané množstvo

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
