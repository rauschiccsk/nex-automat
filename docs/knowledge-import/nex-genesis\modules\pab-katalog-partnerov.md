# PAB - Katalóg partnerov (Partners Catalog)

## Prehľad

Modul PAB (Partners Book) slúži na správu obchodných partnerov - dodávateľov a odberateľov. Je to jeden z hlavných modulov NEX Genesis pre evidenciu firiem a kontaktov.

## Základné údaje

| Položka | Hodnota |
|---------|---------|
| **Názov modulu** | Katalóg partnerov |
| **Prefix** | Pab_ |
| **Hlavný súbor** | NexModules/Pab_F.pas |
| **Hlavná trieda** | TF_Pab (extends TLangForm) |
| **Data modul** | DM_DLSDAT (dmDLS) |

## Funkcionalita

- Evidencia obchodných partnerov (dodávatelia/odberatelia)
- Správa kontaktných údajov a adries
- Evidencia bankových účtov
- Správa kontaktných osôb
- Evidencia prevádzok partnera
- Poznámky k partnerom
- Kategorizácia partnerov do skupín
- Číselníky (štáty, mestá, formy úhrady, doprava, banky)

## Hlavné tabuľky

| Tabuľka | BDF súbor | Popis |
|---------|-----------|-------|
| PAB | PABxxxxx.BTR | Hlavná tabuľka partnerov (x=číslo knihy) |
| PABLST | PABLST.BTR | Zoznam kníh partnerov |
| PABACC | PABACC.BTR | Bankové účty partnerov |
| PACNTC | PACNCT.BTR | Kontaktné osoby |
| PASUBC | PASUBC.BTR | Prevádzkové jednotky |
| PANOTI | PANOTI.BTR | Poznámky k partnerom |

## Číselníky

| Tabuľka | BDF súbor | Popis |
|---------|-----------|-------|
| PAGLST | PAGLST.BTR | Skupiny partnerov |
| STALST | STALST.BTR | Zoznam štátov |
| CTYLST | CTYLST.BTR | Zoznam miest a obcí |
| PAYLST | PAYLST.BTR | Formy úhrady |
| TRSLST | TRPLST.BTR | Spôsoby dopravy |
| BANKLST | BANKLST.BTR | Zoznam bánk |

## Sub-moduly (38)

### Editácia a správa
| Súbor | Popis |
|-------|-------|
| Pab_PacEdit_F.pas | Editor karty partnera |
| Pab_PaBacc_V.pas | Zobrazenie bankových účtov |
| Pab_PaCntc_V.pas | Zobrazenie kontaktov |
| Pab_PaSub_V.pas | Zobrazenie prevádzok |
| Pab_PaNoti_V.pas | Zobrazenie poznámok |

### Vyhľadávanie
| Súbor | Popis |
|-------|-------|
| Pab_NameSrch_F.pas | Vyhľadávanie podľa názvu |
| Pab_IcoSrch_F.pas | Vyhľadávanie podľa IČO |
| Pab_TelSrch_F.pas | Vyhľadávanie podľa telefónu |

### Číselníky
| Súbor | Popis |
|-------|-------|
| Pab_PagLst_V.pas | Skupiny partnerov |
| Pab_PayLst_V.pas | Formy úhrady |
| Pab_TrsLst_V.pas | Spôsoby dopravy |
| Pab_BankLst_V.pas | Bankové ústavy |
| Pab_CtyLst_F.pas, Pab_CtyLst_V.pas | Mestá a obce |
| Pab_StaLst_F.pas, Pab_StaLst_V.pas | Štáty |

### Import/Export
| Súbor | Popis |
|-------|-------|
| Pab_ImpPab_F.pas | Import partnerov |
| Pab_Clp_F.pas | Práca so schránkou |

### Servisné funkcie
| Súbor | Popis |
|-------|-------|
| Pab_Rpt_F.pas | Zostavy/Reporty |
| Pab_PacChg_F.pas | Hromadné zmeny |

## Prístupové práva

| Právo | Popis |
|-------|-------|
| gAfc.Pac.ItmAdd | Pridanie nového partnera |
| gAfc.Pac.ItmDel | Zmazanie partnera |
| gAfc.Pac.ItmMod | Úprava partnera |
| gAfc.Pac.CmpEdi | Úprava firemných údajov |

## UI komponenty

- **TV_Pab**: TTableView - hlavná tabuľka zobrazenia
- **BL_Pab**: TBookList - výber knihy partnerov
- **AL_Pab**: TIcActionList - akcie (pridať, upraviť, zmazať)

## Multi-book architektúra

Systém podporuje viacero "kníh" partnerov:
- Každá kniha má vlastný súbor PABxxxxx.BTR (x = číslo knihy)
- Zoznam kníh je v PABLST.BTR
- Umožňuje oddelenie dodávateľov od odberateľov alebo segmentáciu

## Business pravidlá

### Typy partnerov
- **SapType = 1**: Partner je dodávateľ
- **CusType = 1**: Partner je odberateľ
- Partner môže byť oboje súčasne

### Blokovanie
- **BuDisStat = 1**: Blokovaný nákup od dodávateľa
- **SaDisStat = 1**: Blokovaný predaj odberateľovi

### DPH
- **VatPay = 1**: Platiteľ DPH
- Evidencia IČO, DIČ, IČ DPH

### Adresy
Partner má 3 typy adries:
1. **Reg*** - Registrovaná (sídlo)
2. **Crp*** - Korešpondenčná
3. **Ivc*** - Fakturačná

## Závislosti modulu

### Uses (interface)
```pascal
Fnc, IcTypes, IcAction, LangForm, TableView, BookList,
hPAGLST, hSTALST, hCTYLST, hPAYLST, hTRSLST, hBANKLST,
hPABLST, hPABCAT, hPABACC, hPACNTC, hPASUBC, hPANOTI
```

### Uses (implementation)
```pascal
DM_DLSDAT,           // Hlavný data modul
Pab_PacEdit_F,       // Editor partnera
Pab_NameSrch_F,      // Vyhľadávanie
// ... ďalšie sub-moduly
```

## Diagram závislostí

```
┌─────────────────────┐
│       Pab_F         │
│   (Main Form)       │
├─────────────────────┤
│ uses:               │
│ - hPABCAT           │──────► PABxxxxx.BTR
│ - hPABLST           │──────► PABLST.BTR
│ - hPABACC           │──────► PABACC.BTR
│ - hPACNTC           │──────► PACNCT.BTR
│ - hPASUBC           │──────► PASUBC.BTR
│ - hPANOTI           │──────► PANOTI.BTR
│ - hPAGLST           │──────► PAGLST.BTR
│ - hSTALST           │──────► STALST.BTR
│ - hCTYLST           │──────► CTYLST.BTR
│ - hPAYLST           │──────► PAYLST.BTR
│ - hTRSLST           │──────► TRPLST.BTR
│ - hBANKLST          │──────► BANKLST.BTR
└─────────────────────┘
```

## Stav migrácie

- [ ] Btrieve modely (packages/nexdata/)
- [ ] PostgreSQL modely (packages/nex-staging/)
- [ ] API endpoints
- [ ] Desktop UI (PySide6)
- [ ] Web UI (React)
- [ ] Testy
- [ ] Dokumentácia

## Poznámky

- Modul je kritický pre všetky obchodné operácie (faktúry, objednávky)
- Prepojený s modulmi ICC (faktúry), ORC (objednávky), ISC (sklady)
- Kódovanie: KEYBCS2 (Kamenický) pre SK/CZ znaky
