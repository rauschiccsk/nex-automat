# SVB - Faktúry zálohových platieb (Advance Payment Invoices)

## Prehľad modulu

- **Súbor**: `NexModules\Svb_F.pas`
- **Účel**: Zobrazenie a správa daňových dokladov k zálohovým platbám s knižnou organizáciou
- **Kategória**: Predaj / Zálohy
- **Mark modulu**: SVB

## Vzťah SVB a SPE

| Modul | Účel | Tabuľka | Operácie |
|-------|------|---------|----------|
| **SPE** | Evidencia zálohových platieb | SPD, SPV | Vytvorenie záznamu |
| **SVB** | Správa daňových dokladov | SPV | Zobrazenie, účtovanie, tlač |

SVB modul je **prehliadač a správca** pre tabuľku SPV, ktorú vytvára modul SPE. Poskytuje knižnú organizáciu, prístupové práva a pokročilé funkcie správy.

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| SVBLST | SVBLST.BTR | Knihy faktúr zálohových platieb | 23 | 1 |
| SPV | SPVyynnn.BTR | Daňové doklady zálohových platieb | 35 | 7 |
| NXBDEF | NXBDEF.BTR | Centrálny register kníh | 13 | 2 |

**Celkom: 3 tabuľky, 71 polí, 10 indexov**

## Sub-moduly

### Hlavné zobrazenie
| Súbor | Popis |
|-------|-------|
| Svb_F.pas | Hlavný formulár modulu |

### Konfigurácia kníh
| Súbor | Popis |
|-------|-------|
| Key_SvbEdi_F.pas | Editor vlastností knihy SVB |
| Key_BokAdd_F.pas | Pridanie novej knihy |

### Účtovanie
| Súbor | Popis |
|-------|-------|
| Jrn_AccLst_V.pas | Zobrazenie účtovných zápisov dokladu |

### Prístupové práva
| Súbor | Popis |
|-------|-------|
| AfcSvb.pas | Definícia práv modulu SVB |

## Kľúčové funkcie

### Správa kníh
- **A_AddBook** - Pridanie novej knihy SVB
- **A_ModBook** - Úprava vlastností knihy
- **A_DelBook** - Zmazanie prázdnej knihy

### Účtovanie
- **A_Account** - Zaúčtovanie vybraného dokladu
- **A_AccBook** - Hromadné zaúčtovanie celej knihy
- **A_AccLst** - Zobrazenie účtovných zápisov

### Tlač a export
- **A_DocPrn** - Tlač zoznamu dokladov
- **A_Sending** - Hromadné odoslanie
- **A_SndSlct** - Označenie na odoslanie

## Konfigurácia knihy (Key_SvbEdi_F)

| Parameter | Typ | Popis |
|-----------|-----|-------|
| WriNum | word | Číslo prevádzkové jednotky |
| DocSnt | Str3 | Syntetický účet zálohy |
| DocAnl | Str6 | Analytický účet zálohy |
| VatSnt | Str3 | Syntetický účet DPH |
| VatAnl | Str6 | Analytický účet DPH |
| DvzName | Str3 | Mena knihy |
| ExnFrm | Str12 | Formát variabilného symbolu |
| AutAcc | byte | Automatické účtovanie (1=zapnuté) |
| WriSha | byte | Zdieľanie prevádzkových jednotiek |
| AccNeg | byte | Účtovanie záporných hodnôt |

## Prístupové práva (gAfc.Svb.*)

| Právo | Popis |
|-------|-------|
| AccLst | Zobrazenie účtovných zápisov |
| PrnDoc | Tlač dokladov |
| AccDoc | Účtovanie dokladu |
| SndDoc | Odoslanie dokladu |
| SndMas | Hromadné odoslanie |
| MntFnc | Údržbové funkcie (knihy) |
| SerFnc | Servisné funkcie |

## Workflow

```
SPE modul (vytvorenie)
    ↓
Príjem zálohy → SPD záznam + SPV daňový doklad
    ↓
SVB modul (správa)
    ↓
├→ Zobrazenie v knihe SVB
├→ Zaúčtovanie do JOURNAL
├→ Tlač daňového dokladu
└→ Odoslanie (FTP)
```

## Integrácie

### Väzby na moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| SPE | Vytvorenie SPV | Zdroj daňových dokladov |
| JRN | DocAccount | Účtovanie do denníka |
| WRI | WriNum | Prevádzkové jednotky |

### Dátové toky

```
SPE → SPV (vytvorenie) → SVB (správa) → JRN (účtovanie)
                                      → Tlač
                                      → FTP export
```

## Biznis logika

### Organizácia kníh

- Jedna kniha SVB = jeden rok + jedna prevádzková jednotka
- BookNum formát: X-NNN (napr. A-001)
- SPV súbor: SPVyyNNN.BTR (yy=rok, NNN=číslo knihy)

### Účtovanie

```
MD: DocSnt + DocAnl (účet zálohy)     = BValue
D:  VatSnt + VatAnl (účet DPH)        = VatVal
D:  Protiúčet (napr. pokladňa/banka)  = AValue
```

### Farebné rozlíšenie

- Štandardne čierna farba riadkov
- Možnosť rozšírenia podľa stavu dokladu

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| Nb_BokLst | Panel so zoznamom kníh |
| TV_Spv | TableView pre SPV záznamy |
| Splitter1 | Rozdeľovač panelu kníh |

### Menu štruktúra

- **Program** - Ukončenie, O programe
- **Zobrazit** - Účtovné zápisy
- **Tlač** - Zoznam dokladov
- **Nástroje** - Účtovanie
- **Servis** - Odosielanie

## Porovnanie s ICB

| Vlastnosť | SVB | ICB |
|-----------|-----|-----|
| Tabuľka | SPV | ICH, ICI |
| Typ dokladu | Daňový doklad zálohy | Odberateľská faktúra |
| Zdrojový modul | SPE | Priame vytváranie |
| Položky | Bez položiek | S položkami |

## Migračné poznámky

### Kľúčové body

1. SVB je len prehliadač - samotné záznamy vytvára SPE
2. SPV tabuľka je zdieľaná medzi SPE a SVB
3. Knižná organizácia cez SVBLST a NXBDEF
4. Účtovanie používa štandardnú funkciu DocAccount

### Pre PostgreSQL migráciu

- SVB bude view/API nad SPV tabuľkou
- Knihy ako filtračný parameter
- Prístupové práva cez role systém

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
