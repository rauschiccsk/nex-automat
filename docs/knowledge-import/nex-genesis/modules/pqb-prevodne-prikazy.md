# PQB - Prevodné príkazy (Payment Orders)

## Prehľad modulu

- **Súbor**: `NexModules\Pqb_F.pas`
- **Účel**: Vytváranie a správa prevodných príkazov pre úhradu dodávateľských faktúr
- **Kategória**: Financie / Bankové operácie
- **Mark modulu**: PQB (používa knihy SOB)

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| PQH | PQHyynnn.BTR | Hlavičky prevodných príkazov | 17 | 4 |
| PQI | PQIyynnn.BTR | Položky prevodných príkazov | 26 | 7 |
| PMQ | PMQyyyy.BTR | História prevodných príkazov | 10 | 4 |
| PQBLST | PQBLST.BTR | Zoznam kníh prevodných príkazov | 22 | 2 |

**Celkom: 4 tabuľky, 75 polí, 17 indexov**

## Sub-moduly (12)

### Editácia
| Súbor | Popis |
|-------|-------|
| Pqb_PqhEdit_F.pas | Editor hlavičky prevodného príkazu |
| Pqb_PqiLst_F.pas | Zoznam položiek prevodného príkazu |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Pqb_NpyIsd_F.pas | Neuhradené dodávateľské faktúry |

### Tlač
| Súbor | Popis |
|-------|-------|
| Pqb_DocPrn_F.pas | Tlač prevodného príkazu |

### Elektronické bankovníctvo
| Súbor | Popis |
|-------|-------|
| Pqb_AboSnd_F.pas | Export pre OTP banku |
| Pqb_AboSls_F.pas | Export pre Slovenskú sporiteľňu |
| Pqb_AboVub_F.pas | Export pre VÚB |
| Pqb_AboSbr_F.pas | Export pre Sberbank |
| Pqb_AboUni_F.pas | Export pre UniCredit |
| Pqb_EbaExp.pas | Export SEPA prevodného príkazu |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Sys_LdgFlt_F.pas | Filtrovanie dokladov |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| Key_SobEdi_F.pas | Nastavenie vlastností knihy |

## Kľúčové funkcie

### Správa dokladov
- **A_DocAdd** - Vytvorenie nového prevodného príkazu
- **A_DocMod** - Úprava existujúceho príkazu
- **A_SitLst** - Zobrazenie položiek príkazu
- **A_DocPrn** - Tlač prevodného príkazu
- **A_PqhCalc** - Prepočet hlavičky (súčet položiek)

### Elektronické bankovníctvo
- **A_AboSnd** - Odoslanie do elektronického bankovníctva
- **A_EbaExp** - Export SEPA platobného príkazu

### Faktúry
- **A_NpyIsd** - Výber z neuhradených dodávateľských faktúr
- **A_DocFlt** - Filtrovanie dokladov

## Typy elektronického bankovníctva (AboType)

| Hodnota | Banka |
|---------|-------|
| 0 | Žiadne (bez exportu) |
| 1 | OTP Banka |
| 2 | Slovenská sporiteľňa |
| 3 | VÚB |
| 4 | Sberbank |
| 5 | UniCredit |

## Stavy odoslania (AboStat)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Neodoslaný |
| O | Odoslaný do banky |

## Workflow

```
1. Vytvorenie prevodného príkazu (PQH)
   ↓
2. Výber faktúr na úhradu (A_NpyIsd)
   ├→ Automatické naplnenie položiek (PQI)
   └→ Údaje z ISH (číslo FA, VS, suma, účet)
   ↓
3. Kontrola a úprava položiek
   ↓
4. Export do elektronického bankovníctva (A_AboSnd)
   ├→ AboStat = 'O'
   ├→ AboDate = dátum odoslania
   └→ Vytvorenie záznamu v PMQ
   ↓
5. Tlač prevodného príkazu (A_DocPrn)
```

## Integrácie

### Väzby na moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| ISB | PQI.IsDocNum → ISH.DocNum | Uhrádzaná faktúra |
| PAB | Údaje dodávateľa | Bankové spojenie |
| BSM | Po úhrade | Párovanie vo výpise |

### Dátové toky

```
ISB (Faktúry) → PQB (Príkazy) → Banka (Export)
                      ↓
               PMQ (História)
                      ↓
               BSM (Výpisy) → Párovanie
```

## Biznis logika

### Vytvorenie položky
1. Výber neuhradených faktúr z ISB
2. Automatické doplnenie:
   - IsDocNum = číslo faktúry
   - IsExtNum = variabilný symbol
   - PayVal = suma na úhradu
   - ContoNum = bankový účet dodávateľa
   - BankCode = kód banky
   - Describe = názov dodávateľa

### Prepočet hlavičky
```
PQH.DocVal = SUM(PQI.PayVal)
PQH.ItmQnt = COUNT(PQI)
```

### Export do banky
- Generovanie súboru podľa formátu banky
- Uloženie do AboPath z PQBLST
- Zápis do histórie PMQ
- Nastavenie AboStat = 'O'

## SEPA podpora

Modul podporuje SEPA platby (Pqb_EbaExp):
- IBAN kódy (IbanCode)
- SWIFT/BIC kódy (SwftCode)
- Konštantný symbol (CsyCode)
- Špecifický symbol (SpcSymb)

## Konfigurácia knihy (PQBLST)

| Parameter | Popis |
|-----------|-------|
| ContoNum | Číslo bankového účtu platiteľa |
| BankCode | Kód banky platiteľa |
| IbanCode | IBAN účtu platiteľa |
| SwftCode | SWIFT/BIC kód |
| DvzName | Mena účtu |
| AboType | Typ elektronického bankovníctva |
| AboPath | Cesta pre export súborov |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
