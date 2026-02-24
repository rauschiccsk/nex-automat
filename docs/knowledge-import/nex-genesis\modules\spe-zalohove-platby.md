# SPE - Evidencia zálohových platieb (Advance Payments)

## Prehľad modulu

- **Súbor**: `NexModules\Spe_F.pas`
- **Účel**: Správa zálohových platieb od odberateľov, vystavovanie daňových dokladov a čerpanie záloh
- **Kategória**: Financie / Zálohy
- **Mark modulu**: SPE (používa knihy SVB)

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| SPBLST | SPBLST.BTR | Zálohové účty odberateľov | 38 | 2 |
| SPD | SPDnnnnn.BTR | Zálohové platby odberateľa | 36 | 10 |
| SPV | SPVyynnn.BTR | Daňové doklady zálohových platieb | 35 | 7 |
| SPECONTO | SPECONTO.BTR | Zjednodušené zálohové účty | 13 | 2 |

**Celkom: 4 tabuľky, 122 polí, 21 indexov**

## Sub-moduly (17)

### Hlavné zobrazenie
| Súbor | Popis |
|-------|-------|
| Spe_F.pas | Hlavný formulár modulu |
| Spe_Conto_F.pas | Správa zálohového účtu partnera |
| Spe_Conto_V.pas | Výber zálohového účtu |
| Spe_DocLst_V.pas | Zoznam dokladov zálohového účtu |

### Príjem zálohy
| Súbor | Popis |
|-------|-------|
| Spe_IncDoc_F.pas | Príjem zálohovej platby + daňový doklad |

### Čerpanie zálohy
| Súbor | Popis |
|-------|-------|
| Spe_ExpDoc_F.pas | Čerpanie zálohy proti faktúre |
| Spe_ExpSpc_F.pas | Špecifikácia čerpania zálohy |

### Daňové doklady
| Súbor | Popis |
|-------|-------|
| Spe_SpvLst_F.pas | Zoznam daňových dokladov k zálohovým platbám |
| Spe_SpvProp_F.pas | Vlastnosti daňového dokladu |

### Výkazy
| Súbor | Popis |
|-------|-------|
| Spe_IncSpd_F.pas | Výkaz zálohových príjmov |
| Spe_ExpSpd_F.pas | Výkaz čerpania záloh |
| Spe_SpdSum_F.pas | Stav účtu k zadanému dátumu |

### Filter
| Súbor | Popis |
|-------|-------|
| Spe_SvdFilt_F.pas | Filter daňových dokladov |
| Spe_SvdFilt_V.pas | View filtrovaných dokladov |

### Údržba
| Súbor | Popis |
|-------|-------|
| Spe_ReCalc_F.pas | Prepočet zálohových účtov |

### Export/Import
| Súbor | Popis |
|-------|-------|
| Spe_TxtExp_F.pas | Export údajov do textového súboru |
| Spe_TxtImp_F.pas | Import údajov z textového súboru |

## Kľúčové vlastnosti

### Typy dokladov

| Prefix | Typ | Popis |
|--------|-----|-------|
| DZ* | Daňový zálohový | Daňový doklad k prijatej zálohe |
| OF* | Odberateľská faktúra | Doklad na ktorý sa čerpá záloha |
| ER* | ECR doklad | Doklad z elektronickej pokladne |
| ECR* | ECR pokladňa | Zálohová platba cez pokladňu |

### Formy platby (PayMode)

| Hodnota | Popis |
|---------|-------|
| H | Hotovosť |
| K | Kreditná karta |
| B | Bankový prevod |

### Štruktúra účtu

- **SPBLST** - Zálohový účet pre každého partnera (odberateľa)
- **SPD** - Jednotlivé pohyby na účte (príjmy/výdaje)
- **SPV** - Daňové doklady k zálohovým platbám

## DPH zo zálohy

Systém podporuje až 6 skupín DPH sadzieb:
- **VatPrc1-6** - Percentuálne sadzby DPH
- **IncVal1-6** - Celkové príjmy podľa skupín
- **ExpVal1-6** - Celkové výdaje podľa skupín
- **PrfVal1-6** - Vyúčtované hodnoty podľa skupín

### Výpočet DPH zo zálohy

Pri príjme zálohy sa DPH počíta metódou "zhora":
```
VatVal = BValue - BValue / (1 + VatPrc/100)
AValue = BValue - VatVal
```

## Workflow

```
1. Vytvorenie zálohového účtu pre odberateľa (SPBLST)
   ├→ Automatické pri prvej platbe
   └→ Alebo manuálne cez Spe_Conto_F
   ↓
2. Príjem zálohovej platby (Spe_IncDoc_F)
   ├→ Záznam v SPD (IncNum, DocVal > 0)
   ├→ Daňový doklad v SPV
   ├→ Aktualizácia SPBLST (IncVal, EndVal)
   └→ Automatické účtovanie (voliteľné)
   ↓
3. Čerpanie zálohy proti faktúre (Spe_ExpDoc_F)
   ├→ Volaný z ICB pri vystavení faktúry
   ├→ Záznam v SPD (ExpNum, DocVal < 0)
   ├→ Prepojenie ConDoc = číslo faktúry
   └→ Aktualizácia SPBLST (ExpVal, EndVal)
   ↓
4. Finálna faktúra (ICB)
   ├→ Odpočet čerpanej zálohy
   └→ Len zostatok k úhrade
```

## Integrácie

### Väzby na moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| ICB | SPD.ConDoc → ICH.DocNum | Faktúra na ktorú sa čerpá |
| PAB | SPBLST.PaCode → PAB.PaCode | Partner (odberateľ) |
| VTR | SPV.VatCls | Uzávierka DPH |
| JRN | DocAccount | Účtovanie daňových dokladov |
| CSB | Príjem zálohy | Platba v hotovosti |
| BSM | Príjem zálohy | Platba prevodom |

### Dátové toky

```
Objednávka/Zákazka → Záloha (SPE) → Daňový doklad (SPV)
                          ↓
                     Čerpanie
                          ↓
Faktúra (ICB) ← Odpočet zálohy ← SPD.ConDoc
```

## Biznis logika

### Zálohový účet (SPBLST)

```
EndVal = IncVal - ExpVal
```

Kde:
- **IncVal** = Súčet všetkých prijatých záloh
- **ExpVal** = Súčet všetkých čerpaní (záporné hodnoty)
- **EndVal** = Aktuálny zostatok na účte

### Príjem zálohy

1. Vytvorí sa záznam v SPD s kladnou hodnotou
2. Vytvorí sa daňový doklad v SPV
3. Aktualizuje sa kumulatív v SPBLST
4. Voliteľne sa zaúčtuje do JOURNAL

### Čerpanie zálohy

1. Vytvorí sa záznam v SPD so zápornou hodnotou
2. ConDoc obsahuje číslo faktúry
3. Na faktúre ICH sa odpočíta čerpaná suma
4. Aktualizuje sa kumulatív v SPBLST

### Mazanie dokladu

- Možné len pre posledný doklad na účte (IsLastRec)
- Pri mazaní OF dokladu sa odstránia aj položky ICI
- Automatický prepočet hlavičky ICH

## Číslovanie dokladov

### SPD - Zálohové platby

- **SerNum** - Poradové číslo všetkých dokladov
- **IncNum** - Poradové číslo príjmových dokladov
- **ExpNum** - Poradové číslo výdajových dokladov
- **DocNum** - Interné číslo (generované GenSeDocNum)

### SPV - Daňové doklady

- Používa knihy SVB (analogicky ako ICB používa OFB)
- Formát: SPVyynnn.BTR (yy=rok, nnn=číslo knihy)
- DocNum generovaný GenSvDocNum

## Tlačové zostavy

| Report | Popis |
|--------|-------|
| SPD_I | Príjmový doklad (po 01.05.2004) |
| SPD_N | Výdajový doklad |
| SPD_C | Príjmový doklad ECR |
| SPD_DI | Daňový doklad príjmu (pred 01.05.2004) |
| SPD_DN | Daňový doklad výdaju (pred 01.05.2004) |

## Konfigurácia

### INI parametre

| Parameter | Popis |
|-----------|-------|
| GetDefSpvBook | Predvolená kniha SPV |
| SpvAutoAcc | Automatické účtovanie SPV dokladov |
| GetVatPrc(1-5) | Sadzby DPH pre skupiny |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
