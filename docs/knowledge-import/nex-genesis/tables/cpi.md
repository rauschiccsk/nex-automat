# CPI - Položky kalkulácie (Komponenty)

## Kľúčové slová / Aliases

CPI, CPI.BTR, položky, kalkulácie, komponenty

## Popis

Tabuľka položiek kalkulácie výrobkov. Obsahuje jednotlivé komponenty (materiál) a služby (réžia) vstupujúce do kalkulácie. Definuje množstvo, straty a ceny pre každý komponent. Každá kniha má vlastný súbor.

## Btrieve súbor

`CPInnnnn.BTR` (nnnnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DATA\CPInnnnn.BTR`

## Štruktúra polí (32 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdCode | longint | 4 | Tovarové číslo výrobku - **FK CPH** |
| CpCode | longint | 4 | Tovarové číslo komponentu - **FK GSCAT** |
| MgCode | longint | 4 | Tovarová skupina - **FK MGLST** |
| CpName | Str30 | 31 | Názov komponentu |
| BarCode | Str15 | 16 | Identifikačný kód komponentu |
| VatPrc | byte | 1 | Sadzba DPH v % |
| ItmType | Str1 | 2 | Typ položky (C=komponent, W=práca, S=služba) |
| Notice | Str80 | 81 | Poznámka k položke |

### Množstvo (v používanej MJ)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdGsQnt | double | 8 | Množstvo výrobku (dávka) |
| RcGsQnt | double | 8 | Čisté množstvo komponentu (receptúra) |
| LosPrc | double | 8 | Strata v % (odpad, zmetky) |
| CpGsQnt | double | 8 | Odpočítané množstvo = RcGsQnt × (1 + LosPrc/100) |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvo (v základnej MJ)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdGsQntu | double | 8 | Množstvo výrobku v základnej MJ |
| RcGsQntu | double | 8 | Čisté množstvo v základnej MJ |
| CpGsQntu | double | 8 | Odpočítané množstvo v základnej MJ |
| MsuName | Str10 | 11 | Základná merná jednotka |

### Nákladové ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CPrice | double | 8 | Nákupná cena/MJ bez DPH |
| CValue | double | 8 | Hodnota = CPrice × CpGsQnt |

### Predajné ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DPrice | double | 8 | Cenníková cena/MJ bez DPH |
| HPrice | double | 8 | Cenníková cena/MJ s DPH |
| APrice | double | 8 | Predajná cena/MJ bez DPH (po zľave) |
| BPrice | double | 8 | Predajná cena/MJ s DPH (po zľave) |

### Zľavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscPrc | double | 8 | Percentuálna zľava |
| DscType | Str1 | 2 | Typové označenie zľavy |

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

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PdCode, CpCode | PdCp | Unikátny |
| 1 | PdCode | PdCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PdCode | CPH.PdCode | Hlavička kalkulácie (výrobok) |
| CpCode | GSCAT.GsCode | Katalógová karta komponentu |
| MgCode | MGLST.MgCode | Tovarová skupina |

## Typy položiek

### Rozdelenie podľa MgCode

| Typ | MgCode | Popis | Sumár do |
|-----|--------|-------|----------|
| Materiál | < SecMgc | Suroviny, komponenty | CPH.CpiVal |
| Réžia | >= SecMgc | Práca, služby, náklady | CPH.CpsVal |

### ItmType pole

| Hodnota | Popis | Použitie |
|---------|-------|----------|
| C | Component | Materiálový komponent |
| W | Work | Práca (manuálna) |
| S | Service | Služba (externá) |

## Výpočet

```
┌─────────────────────────────────────────────────────────────────┐
│ ODPOČÍTANÉ MNOŽSTVO                                             │
│ CpGsQnt = RcGsQnt × (1 + LosPrc/100)                            │
│                                                                 │
│ Príklad: RcGsQnt=100g, LosPrc=5%                                │
│          CpGsQnt = 100 × 1.05 = 105g                            │
├─────────────────────────────────────────────────────────────────┤
│ HODNOTA KOMPONENTU                                              │
│ CValue = CPrice × CpGsQnt                                       │
│                                                                 │
│ Príklad: CPrice=0.008 EUR/g, CpGsQnt=105g                       │
│          CValue = 0.008 × 105 = 0.84 EUR                        │
└─────────────────────────────────────────────────────────────────┘
```

## Príklad

```
Výrobok: Sendvič (PdGsQnt=10 ks)
─────────────────────────────────────────────────────────────────
MATERIÁL (MgCode < 9000):
  Chlieb    RcGsQnt=20ks  LosPrc=0%   CpGsQnt=20ks  CValue=2.00€
  Šunka     RcGsQnt=500g  LosPrc=5%   CpGsQnt=525g  CValue=4.20€
  Syr       RcGsQnt=300g  LosPrc=2%   CpGsQnt=306g  CValue=1.60€
                                               Σ CpiVal=7.80€
─────────────────────────────────────────────────────────────────
RÉŽIA (MgCode >= 9000):
  Práca     RcGsQnt=0.5h  LosPrc=0%   CpGsQnt=0.5h  CValue=4.00€
  Energia   RcGsQnt=10ks  LosPrc=0%   CpGsQnt=10ks  CValue=0.20€
                                               Σ CpsVal=4.20€
─────────────────────────────────────────────────────────────────
```

## Použitie

- Definícia receptúry/BOM výrobku
- Kalkulácia nákladov s rezervou na straty (LosPrc)
- Rozdelenie nákladov na materiál a réžiu
- Cenotvorba komponentov

## Business pravidlá

- PdCode + CpCode = unikátny kľúč (jeden komponent raz vo výrobku)
- LosPrc zohľadňuje odpad, zmetky, technologické straty
- MgCode < SecMgc = materiál (CpiVal), MgCode >= SecMgc = réžia (CpsVal)
- CPrice sa načítava zo STK (LastPrice alebo AvgPrice podľa CPBLST.AvgClc)
- Pri zmene CPI sa automaticky prepočíta CPH (CpiVal, CpsVal, CValue, PrfPrc)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
