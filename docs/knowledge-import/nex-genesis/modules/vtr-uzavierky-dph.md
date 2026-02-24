# VTR - Evidencia uzávierok DPH (VAT Returns)

## Prehľad modulu

- **Súbor**: `NexModules\Vtr_F.pas`
- **Účel**: Správa uzávierok DPH, generovanie daňových priznaní a kontrolných výkazov
- **Kategória**: Financie / DPH
- **Mark modulu**: VTR

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| VTR | VTR.BTR | Zoznam daňových dokladov | 19 | 7 |
| VTRLST | VTRLST.BTR | Zoznam uzávierok DPH | 42 | 3 |
| VTRAWR | VTRAWR.BTR | Hodnoty daňového priznania | 41 | 1 |
| VATDOC | VATDOC.BTR | Súhrnné daňové doklady | 32 | 6 |
| VATCLS | VATCLS.BTR | Súhrn uzávierok DPH | 57 | 1 |
| VTDSPC | VTDSPC.BTR | Špecifikácie dokladov | 12 | 1 |
| VTI | VTI.BTR | Položky kontrolného výkazu | 26 | 5 |
| VTCLST | VTCLST.BTR | Kalkulačné obdobia | 12 | 1 |

**Celkom: 8 tabuliek, 241 polí, 25 indexov**

## Sub-moduly

### Hlavné zobrazenie
| Súbor | Popis |
|-------|-------|
| Vtr_F.pas | Hlavný formulár modulu |
| Vtr_VtrLst_F.pas | Zoznam daňových dokladov |

### XML Export
| Súbor | Popis |
|-------|-------|
| VtrXmr_F.pas | Export XML daňového priznania |
| VtrXmi_F.pas | Export XML kontrolného výkazu |
| VtrXms_F.pas | Export XML súhrnného výkazu |

### Tlač
| Súbor | Popis |
|-------|-------|
| Vtr_VtrPrn_F.pas | Tlač daňového priznania |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| Vtr_VtcLst_F.pas | Zoznam kalkulačných období |
| Vtr_VtdLst_F.pas | Zoznam špecifikácií dokladov |

## Kľúčové vlastnosti

### Typy výkazov (SttTyp)

| Hodnota | Popis |
|---------|-------|
| R | Riadny výkaz |
| O | Opravný výkaz |
| D | Dodatočný výkaz |

### Strany DPH (VatPart)

| Hodnota | Popis |
|---------|-------|
| I | Vstup (Input) - dodávateľské faktúry |
| O | Výstup (Output) - odberateľské faktúry |

### Typy riadkov kontrolného výkazu (RowTyp)

| Hodnota | Popis |
|---------|-------|
| A1 | Dodanie tovaru/služby - základ dane |
| A2 | Dodanie tovaru/služby - oprava |
| B1 | Nadobudnutie tovaru z EÚ |
| B2 | Nadobudnutie služby z EÚ |
| B3 | Tuzemské samozdanenie |
| C1 | Dovoz tovaru - colný dlh |
| C2 | Dovoz tovaru - odložená platba |
| D1 | Súhrnný riadok - základ dane |
| D2 | Súhrnný riadok - oprava |

### Osoby platiteľa dane (VatPrs)

| Hodnota | Popis |
|---------|-------|
| P | Právnická osoba |
| I | Individuálny podnikateľ |
| O | Ostatné osoby |
| Z | Zahraničná osoba |
| D | Dedič |

## Workflow

```
1. Definícia kalkulačného obdobia (VTCLST)
   ↓
2. Vytvorenie uzávierky DPH (VTRLST)
   ├→ Výber obdobia (BegDate - EndDate)
   └→ Typ výkazu (R/O/D)
   ↓
3. Zber daňových dokladov (VTR, VATDOC)
   ├→ Vstupné doklady (VatPart='I') z ISB
   └→ Výstupné doklady (VatPart='O') z ICB
   ↓
4. Výpočet hodnôt daňového priznania (VTRAWR)
   ├→ Value01-Value40 = riadky formulára
   └→ Zaokrúhlenie podľa predpisov
   ↓
5. Generovanie kontrolného výkazu (VTI)
   ├→ Položky podľa typu riadku
   └→ Súhrnné riadky (Sumarize=1)
   ↓
6. Export XML
   ├→ Daňové priznanie (VtrXmr_F)
   ├→ Kontrolný výkaz (VtrXmi_F)
   └→ Súhrnný výkaz (VtrXms_F)
```

## Integrácie

### Zdrojové moduly

| Modul | Typ dokladov | VatPart |
|-------|--------------|---------|
| ISB | Dodávateľské faktúry | I (vstup) |
| ICB | Odberateľské faktúry | O (výstup) |
| CSB | Pokladničné doklady | I/O |

### Väzby na tabuľky

| Tabuľka | Väzba | Popis |
|---------|-------|-------|
| ISH | VTR.DocNum | Dodávateľská faktúra |
| ICH | VTR.DocNum | Odberateľská faktúra |
| PAB | VTR.PaCode | Partner |

## Business pravidlá

### Výpočet DPH

- `InVatVal` = súčet DPH vstupných dokladov
- `OuVatVal` = súčet DPH výstupných dokladov
- `DfVatVal` = OuVatVal - InVatVal (daňová povinnosť)
- `VatVal` = DfVatVal + RndVal (suma k úhrade)
- `EndVal` = VatVal - PayVal (zostatok k úhrade)

### Uzatvorenie dokladov

- `DocCls=1` zapína uzatvorenie započítaných dokladov
- Po uzavretí sa doklady prepoja s uzávierkou cez ClsNum

### XML Export

- Formát podľa špecifikácie Finančnej správy SR
- Obsahuje registračné údaje z VTRLST
- Digitálny podpis pre elektronické podanie

## Daňové sadzby (6 skupín)

Systém podporuje až 6 rôznych sadzieb DPH:
- **VatPrc1-6** - percentuálne sadzby
- **VatVal1-6** - hodnoty DPH podľa skupín
- **BValue1-6** - hodnoty s DPH podľa skupín

### Štandardné sadzby SR

| Skupina | Sadzba | Použitie |
|---------|--------|----------|
| 1 | 20% | Základná sadzba |
| 2 | 10% | Znížená sadzba |
| 3 | 0% | Oslobodené plnenia |

## Registračné údaje (VTRLST)

| Pole | Popis |
|------|-------|
| VIN | IČ DPH |
| TIN | DIČ |
| RegName | Názov platiteľa |
| PaAddr1, PaAddr2 | Adresa |
| RegCtn, RegZip | Mesto, PSČ |
| RegStn | Štát |
| AutNam | Oprávnená osoba |
| AutTel | Telefón na oprávnenú osobu |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
