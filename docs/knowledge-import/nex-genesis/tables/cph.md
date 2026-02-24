# CPH - Hlavičky kalkulácií (Výrobky)

## Kľúčové slová / Aliases

CPH, CPH.BTR, hlavičky, kalkulácií, výrobky

## Popis

Tabuľka hlavičiek kalkulácií výrobkov. Obsahuje definíciu výrobku, jeho nákladovú a predajnú cenu, maržu a sumarizáciu nákladov podľa typu (materiál/réžia). Každá kniha má vlastný súbor.

## Btrieve súbor

`CPHnnnnn.BTR` (nnnnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DATA\CPHnnnnn.BTR`

## Štruktúra polí (30 polí)

### Identifikácia výrobku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdCode | longint | 4 | Tovarové číslo výrobku - **FK GSCAT** |
| PdName | Str30 | 31 | Názov výrobku |
| _PdName | Str30 | 31 | Názov výrobku - vyhľadávacie pole |
| BarCode | Str15 | 16 | Identifikačný kód výrobku |
| VatPrc | byte | 1 | Sadzba DPH výrobku v % |
| PdGsQnt | double | 8 | Množstvo vyrobeného výrobku (dávka) |
| MsName | Str10 | 11 | Merná jednotka výrobku |
| ItmQnt | word | 2 | Počet komponentov výrobku |

### Nákladové ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CpiVal | double | 8 | Hodnota komponentov (materiál, NC bez DPH) |
| CpsVal | double | 8 | Hodnota réžie (služby, NC bez DPH) |
| CValue | double | 8 | Úplné náklady (CpiVal + CpsVal) |
| CPrice | double | 8 | Nákladová cena/MJ (CValue / PdGsQnt) |

### Predajné ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| APrice | double | 8 | Predajná cena/MJ bez DPH |
| BPrice | double | 8 | Predajná cena/MJ s DPH |
| AValue | double | 8 | Predajná hodnota bez DPH (po zľave) |
| BValue | double | 8 | Predajná hodnota s DPH (po zľave) |
| DValue | double | 8 | Cenníková hodnota bez DPH (pred zľavou) |
| HValue | double | 8 | Cenníková hodnota s DPH (pred zľavou) |
| PrfPrc | double | 8 | Obchodná marža v % |

### Zľavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscPrc | double | 8 | Percentuálna zľava |
| DscAvl | double | 8 | Hodnota zľavy (bez DPH) |
| DscBvl | double | 8 | Hodnota zľavy (s DPH) |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

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

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PdCode | PdCode | Duplicit |
| 1 | _PdName | PdName | Duplicit, Case-insensitive |
| 2 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PdCode | GSCAT.GsCode | Katalógová karta výrobku |

## Kalkulačný vzorec

```
┌─────────────────────────────────────────────────────────────────┐
│ MATERIÁL (komponenty kde MgCode < SecMgc)                       │
│ CpiVal = Σ(CPI.CValue)                                          │
├─────────────────────────────────────────────────────────────────┤
│ RÉŽIA (služby kde MgCode >= SecMgc)                             │
│ CpsVal = Σ(CPI.CValue)                                          │
├─────────────────────────────────────────────────────────────────┤
│ ÚPLNÉ NÁKLADY                                                   │
│ CValue = CpiVal + CpsVal                                        │
│ CPrice = CValue / PdGsQnt                                       │
├─────────────────────────────────────────────────────────────────┤
│ PREDAJNÁ CENA                                                   │
│ AValue = Σ(CPI.APrice × CPI.CpGsQnt)                            │
│ BValue = Σ(CPI.BPrice × CPI.CpGsQnt)                            │
├─────────────────────────────────────────────────────────────────┤
│ MARŽA                                                           │
│ PrfPrc = (AValue - CValue) / CValue × 100                       │
└─────────────────────────────────────────────────────────────────┘
```

## Príklad

```
Výrobok: Sendvič (PdGsQnt=10 ks)
─────────────────────────────────────────────────────────────────
CpiVal = 7.80 EUR (materiál: chlieb, šunka, syr)
CpsVal = 4.20 EUR (réžia: práca, energia)
─────────────────────────────────────────────────────────────────
CValue = 12.00 EUR (úplné náklady na 10 ks)
CPrice = 1.20 EUR/ks (nákladová cena)
BPrice = 2.00 EUR/ks (predajná cena s DPH)
BValue = 20.00 EUR (tržba za 10 ks)
PrfPrc = 66.67% (marža)
```

## Použitie

- Kalkulácia nákladov a predajnej ceny výrobkov
- Stanovenie marže na základe nákladov a predajnej ceny
- Export kalkulovanej ceny do cenníka (PLS)
- Sledovanie štruktúry nákladov (materiál vs réžia)

## Business pravidlá

- SecMgc (gvSys.SecMgc) = hraničná tovarová skupina pre rozdelenie materiál/réžia
- CValue sa prepočítava automaticky pri zmene komponentov (CPI)
- PrfPrc = percentuálna marža vypočítaná z rozdielu AValue a CValue
- PdGsQnt umožňuje kalkulovať na dávku (napr. 100 ks)
- CPrice = nákladová cena na jednotku výrobku

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
