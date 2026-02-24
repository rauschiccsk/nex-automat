# CPB - Kalkulácia výrobkov (Product Costing)

## Popis modulu

Modul pre kalkuláciu nákladov a predajnej ceny výrobkov. Umožňuje definovať zloženie výrobku z komponentov a služieb, vypočítať náklady a stanoviť predajnú cenu s požadovanou maržou. Integruje sa s cenníkom (PLS) a skladovými kartami (STK).

## Hlavný súbor

`NexModules\Cpb_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| CPBLST | CPBLST.BTR | Zoznam kníh kalkulácií | 19 | 1 |
| CPH | CPHnnnnn.BTR | Hlavičky kalkulácií (výrobky) | 26 | 3 |
| CPI | CPInnnnn.BTR | Položky kalkulácie (komponenty) | 31 | 2 |

**Celkom: 3 tabuľky, 76 polí, 6 indexov**

## Sub-moduly (14)

### Editácia
| Súbor | Popis |
|-------|-------|
| Cpb_CphEdi_F.pas | Editor hlavičky (výrobku) |
| Cpb_CpiLst_F.pas | Zoznam položiek (komponentov) |
| Cpb_CpiEdi_F.pas | Editor položky (komponentu) |
| Cpb_CpiEdt_F.pas | Alternatívny editor položky |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Cpb_CpiLst_V.pas | Pohľad na položky |
| Cpb_CphLst_V.pas | Pohľad na výrobky |
| Cpb_CphLst_F.pas | Výrobky s daným komponentom |

### Tlač
| Súbor | Popis |
|-------|-------|
| Cpb_DocPrn_F.pas | Tlač kalkulácie |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Cpb_CpiCmi_F.pas | Generovanie podľa kompletizácie (CMB) |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| Cpb_CpbEdit_F.pas | Vlastnosti knihy kalkulácií |

### Jadro
| Súbor | Popis |
|-------|-------|
| Cpd.pas | Trieda TCpd - výpočtové funkcie |

## Kalkulačný vzorec

```
┌─────────────────────────────────────────────────────────────────┐
│ MATERIÁL (komponenty)                                          │
│ Σ CPI.CValue kde MgCode < SecMgc                               │
│ = CpiVal (hodnota komponentov)                                 │
├─────────────────────────────────────────────────────────────────┤
│ RÉŽIA (služby)                                                 │
│ Σ CPI.CValue kde MgCode >= SecMgc                              │
│ = CpsVal (hodnota réžie)                                       │
├─────────────────────────────────────────────────────────────────┤
│ ÚPLNÉ NÁKLADY                                                  │
│ CValue = CpiVal + CpsVal                                       │
│ CPrice = CValue / PdGsQnt (NC/MJ)                              │
├─────────────────────────────────────────────────────────────────┤
│ PREDAJNÁ CENA                                                  │
│ BPrice = Σ(CPI.BPrice × CPI.CpGsQnt) (PC s DPH)                │
│ APrice = BPrice bez DPH                                        │
│ AValue = APrice × PdGsQnt                                      │
├─────────────────────────────────────────────────────────────────┤
│ MARŽA                                                          │
│ PrfPrc = (AValue - CValue) / CValue × 100 (%)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Typy položiek kalkulácie

### Rozdelenie podľa MgCode

| Typ | MgCode | Popis | Sumár do |
|-----|--------|-------|----------|
| Materiál | < SecMgc | Komponenty, suroviny | CpiVal |
| Réžia | >= SecMgc | Služby, práca, náklady | CpsVal |

### ItmType pole

| Hodnota | Farba | Popis |
|---------|-------|-------|
| C | Čierna | Komponent (materiál) |
| W | Čierna | Work (práca) |
| S | Zelená | Service (služba) |

## Štruktúra nákladov

### Položka kalkulácie (CPI)

| Pole | Popis |
|------|-------|
| RcGsQnt | Čisté množstvo komponentu (receptúra) |
| LosPrc | Strata v % (odpad, ztráž) |
| CpGsQnt | Odpočítané množstvo = RcGsQnt × (1 + LosPrc/100) |
| CPrice | Nákupná cena/MJ komponentu |
| CValue | Hodnota = CPrice × CpGsQnt |

### Príklad

```
Výrobok: Sendvič (1 ks)
─────────────────────────────────────────────────────────────────
Komponenty (MgCode < 9000):
  Chlieb        RcGsQnt=2ks × CPrice=0.10€ = 0.20€
  Šunka         RcGsQnt=50g × CPrice=0.008€ = 0.40€ (LosPrc=5%)
  Syr           RcGsQnt=30g × CPrice=0.006€ = 0.18€
                                    CpiVal = 0.78€
─────────────────────────────────────────────────────────────────
Réžia (MgCode >= 9000):
  Práca         RcGsQnt=0.05h × CPrice=8.00€ = 0.40€
  Energia       RcGsQnt=1ks × CPrice=0.02€ = 0.02€
                                    CpsVal = 0.42€
─────────────────────────────────────────────────────────────────
ÚPLNÉ NÁKLADY:              CValue = 1.20€
PREDAJNÁ CENA:              BPrice = 2.00€ (s DPH)
MARŽA:                      PrfPrc = 66.67%
```

## Workflow

```
1. Vytvorenie knihy kalkulácií (Cpb_CpbEdit_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ Nastavenie skladov (PdStkNum, CpStkNum)                    │
   │ Nastavenie cenníka (PdPlsNum)                              │
   │ Spôsob cenotvorby (AvgClc: 0=posledná NC, 1=priemerná NC)  │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
2. Pridanie výrobku (Cpb_CphEdi_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ Výber z katalógu (GSCAT) alebo zadanie BarCode             │
   │ Množstvo výrobku (PdGsQnt) - kalkulácia na dávku           │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
3. Pridanie komponentov (Cpb_CpiLst_F → Cpb_CpiEdi_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ Výber komponentu z katalógu/skladu                         │
   │ Zadanie množstva (RcGsQnt), straty (LosPrc)                │
   │ Automatický výpočet CpGsQnt, CValue                        │
   │ Nastavenie predajnej ceny komponentu (APrice, BPrice)      │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
4. Prepočet kalkulácie (TCpd.ClcDoc / hCPH.Clc)
   ┌─────────────────────────────────────────────────────────────┐
   │ CpiVal = Σ(CValue) kde MgCode < SecMgc                     │
   │ CpsVal = Σ(CValue) kde MgCode >= SecMgc                    │
   │ CValue = CpiVal + CpsVal                                   │
   │ CPrice = CValue / PdGsQnt                                  │
   │ BPrice = Σ(CPI.BPrice × CpGsQnt)                           │
   │ PrfPrc = (AValue - CValue) / CValue × 100                  │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
5. Export do cenníka (B_SavPlsClick)
   ┌─────────────────────────────────────────────────────────────┐
   │ PLS.BPrice := CPH.BPrice                                   │
   │ Automatický prenos zmien (PlsSave=1)                       │
   └─────────────────────────────────────────────────────────────┘
```

## Konfigurácia knihy (CPBLST)

| Parameter | Popis |
|-----------|-------|
| CpbNum | Číslo knihy kalkulácií |
| CpbName | Názov knihy |
| PdStkNum | Sklad hotových výrobkov |
| CpStkNum | Sklad komponentov |
| PdPlsNum | Predajný cenník výrobkov |
| RndType | Typ zaokrúhlenia ceny (0-6) |
| PlsSave | Automaticky prenášať do cenníka (1=áno) |
| AvgClc | Spôsob cenotvorby (0=posledná NC, 1=priemerná NC) |

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov (výrobky aj komponenty) |
| BARCODE | Čiarové kódy |
| STK | Skladové karty (LastPrice, AvgPrice) |
| PLS | Predajný cenník (export cien) |
| CMB/CMSPEC | Import receptúr z kompletizácie |
| MGLST | Tovarové skupiny (SecMgc = hranica réžie) |
| Plc | Cenové funkcie (gPlc.ClcPrfPrc, gPlc.ClcAPrice) |

## Business pravidlá

- SecMgc (gvSys.SecMgc) = hraničná tovarová skupina pre rozdelenie na materiál/réžiu
- Knihu možno zmazať len ak neobsahuje výrobky
- LosPrc umožňuje kalkulovať so stratou materiálu (odpad, zmetky)
- CpGsQnt = RcGsQnt × (1 + LosPrc/100)
- Pri zmene komponentov sa automaticky prepočíta hlavička
- Export do PLS aktualizuje predajnú cenu v cenníku

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| TV_Cph | TableView - zoznam výrobkov (kalkulácií) |
| TV_Cpi | TableView - zoznam komponentov |
| BL_CpbLst | BookList - výber knihy kalkulácií |
| L_CpiVal / L_CpsVal | Zobrazenie hodnoty materiálu/réžie |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
