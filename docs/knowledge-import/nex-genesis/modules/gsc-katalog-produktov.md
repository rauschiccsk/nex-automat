# GSC - Katalóg produktov (Evidencia tovaru)

## Popis modulu

Modul **GSC** (Goods Catalog) je jadrom skladového hospodárstva NEX Genesis. Spravuje kompletný katalóg produktov vrátane:
- Základné údaje o tovare (názov, cena, DPH)
- Tovarové a finančné skupiny
- Čiarové kódy (prvotné aj druhotné)
- Obrázky produktov
- Jazykové mutácie názvov
- Prepojenia na cenníky

## Hlavný súbor

**`NexModules/Gsc_F.pas`** - Hlavný formulár katalógu produktov

### Trieda
```pascal
TF_Gsc = class(TLangForm)
```

### Hlavné komponenty
- `TV_GsCat: TTableView` - Grid zobrazenie produktov
- `AL_Gsc: TActionList` - 50+ akcií pre menu operácie
- `M_Gsc: TMainMenu` - Menu (Program, Úpravy, Zobraziť, Tlač, Nástroje, Údržba, Servis)

## Používané tabuľky

| Tabuľka | Data modul | Dokumentácia |
|---------|------------|--------------|
| GSCAT | dmSTK.btGSCAT | [gscat.md](../tables/gscat.md) |
| BARCODE | dmSTK.btBARCODE | [barcode.md](../tables/barcode.md) |
| MGLST | dmSTK.btMGLST | [mglst.md](../tables/mglst.md) |
| FGLST | dmSTK.btFGLST | [fglst.md](../tables/fglst.md) |
| SGLST | dmSTK.btSGLST | [sglst.md](../tables/sglst.md) |
| GSNOTI | dmSTK.btGSNOTI | [gsnoti.md](../tables/gsnoti.md) |
| GSLANG | dmSTK.btGSLANG | [gslang.md](../tables/gslang.md) |
| GSCIMG | dmSTK.btGSCIMG | [gscimg.md](../tables/gscimg.md) |
| GSCLNK | dmSTK.btGSCLNK | [gsclnk.md](../tables/gsclnk.md) |
| GSCANA | - | [gscana.md](../tables/gscana.md) |
| GSCKEY | - | [gsckey.md](../tables/gsckey.md) |
| SRCAT | dmLDG.btSRCAT | Kategórie služieb |
| PLSLST | dmSTK.btPLSLST | Cenníky |
| SPCINF | dmSTK.btSPCINF | Špecifikačné info |

## Sub-moduly

### Úpravy (Edit)
| Súbor | Popis |
|-------|-------|
| `Gsc_ItmEdi_F.pas` | Evidenčná karta tovaru (CRUD) |
| `Gsc_ImgEdi_F.pas` | Obrázky k tovarovej položke |
| `Gsc_GscDel_F.pas` | Zrušenie vybraného tovaru |
| `Gsc_AddImg_F.pas` | Pripojenie obrázku |
| `Gsc_GsLang_F.pas` | Preklad do iných jazykov |

### Zobrazenie (View)
| Súbor | Popis |
|-------|-------|
| `Gsc_MgLst_V.pas` | Zoznam tovarových skupín |
| `Gsc_FgLst_V.pas` | Zoznam finančných skupín |
| `Gsc_SgLst_V.pas` | Zoznam špecifikačných skupín |
| `Gsc_GscAna_V.pas` | Zoznam doplnkových názvov |
| `Gsc_GscMod_V.pas` | Modifikácie tovaru |
| `Gsc_GslDel_V.pas` | Vyradené položky |
| `Gsc_GslDis_V.pas` | Disabled položky |
| `Gsc_PckLst_V.pas` | Zoznam balení |
| `Gsc_GpcLst_V.pas` | Cenové skupiny |
| `Gsc_WgsLst_V.pas` | Váhové položky |
| `Gsc_MgTree_V.pas` | Stromová štruktúra skupín |
| `Gsc_CraLst_V.pas` | Prepravkový tovar |
| `Gsc_GscLnk_V.pas` | Príslušenstvo k položke |
| `Gsc_CctLst.pas` | Jednotný colný sadzobník |

### Nástroje (Tools)
| Súbor | Popis |
|-------|-------|
| `Gsc_GscFilt_F.pas` | Filtrovanie tovarových kariet |
| `Gsc_BcSrch_F.pas` | Hľadať podľa čiarového kódu |
| `Gsc_NaSrch_F.pas` | Hľadať podľa názvu |
| `Gsc_NusGsc_F.pas` | Nepoužité tovarové položky |
| `Gsc_IbcGen_F.pas` | Generovať interný čiarový kód |
| `Gsc_DivSet_F.pas` | Hromadné nastavenie deliteľnosti |
| `Gsc_MinMax_F.pas` | Nastavenie skladových normatívov |
| `Sys_ImpGsc_F.pas` | Import evidencie tovaru |
| `Sys_ImpBac_F.pas` | Import druhotných kódov |
| `Imp_GscNot_F.pas` | Import poznámok k tovarom |
| `Gsc_SndShp_F.pas` | Odoslať kartu na Web/e-shop |

### Údržba (Maintenance)
| Súbor | Popis |
|-------|-------|
| `Gsc_BacDup_F.pas` | Hľadať duplicitné identifikačné kódy |
| `Gsc_BacLos_F.pas` | Hľadať stratené druhotné kódy |
| `Gsc_PlsCpr_F.pas` | Porovnávanie s predajným cenníkom |
| `Gsc_GsnSrc_F.pas` | Vytvoriť názvový vyhľadávač |
| `Key_GscEdi_F.pas` | Vlastnosti programového modulu |
| `Gsc_CrpCpy.pas` | Kopírovanie do inej firmy |
| `Gsc_FgcChg.pas` | Zmeniť finančnú skupinu |
| `Gsc_IntDel.pas` | Hromadné zrušenie položiek |

### Servis (Service)
| Súbor | Popis |
|-------|-------|
| `Gsc_BacGen_F.pas` | Generovať interný čiarový kód |
| `Gsc_KeyGen_F.pas` | Generovať vyhľadávacie kľúče |
| `Gsc_VatChg_F.pas` | Zmena sadzby DPH |
| `Gsc_ReNum_F.pas` | Prečíslovanie tovaru |
| `Gsc_RefGen_F.pas` | Poslať ID kódy do pokladne |
| `Gsc_LinRef_F.pas` | Obnova poslednej nákupnej ceny |

## Prístupové práva

Riadenie prístupu cez `gAfc.Gsc.*`:

```pascal
gAfc.Gsc.ItmAdd  // Pridať tovar
gAfc.Gsc.ItmDel  // Zmazať tovar
gAfc.Gsc.ItmDis  // Vyradiť tovar z evidencie
gAfc.Gsc.ItmEna  // Obnoviť vyradený tovar
gAfc.Gsc.AddImg  // Pripojiť obrázok
gAfc.Gsc.GsnLng  // Editácia jazykových mutácií
```

## Závislosti

### Uses (interface)
```pascal
// Core utilities
Fnc, IcTypes, IcConv, IcButtons, IcVariab, IcTools,
NexError, NexGlob, BookRight, TxtCut, NexLang, NexMsg,
NexPath, NexSys, NexText, NexIni, DefRgh, BarCode

// Table handlers
hGSCAT, hGSCANA, hMGLST, hBARCODE, hSTM, hSTK, hPLS,
tIDEVAL, eCCTDEF, Afc

// UI components
BookList, ApplicView, TableView, LangForm, CntWin, PQRep_,
AdvGrid, SrchGrid
```

### Uses (implementation)
```pascal
DM_SYSTEM   // Systémové nastavenia
DM_STKDAT   // Skladové dáta
DM_LDGDAT   // Účtovné dáta
```

## Business logika

### Inicializácia (FormCreate)
```pascal
dmSTK.btGSCAT.Open;      // Hlavná tabuľka
dmLDG.btSRCAT.Open;      // Kategórie služieb
dmSTK.btGSNOTI.Open;     // Poznámky
dmSTK.btGSLANG.Open;     // Jazyky
dmSTK.btBARCODE.Open;    // Čiarové kódy
dmSTK.btGSCIMG.Open;     // Obrázky
dmSTK.btMGLST.Open;      // Tovarové skupiny
dmSTK.btFGLST.Open;      // Finančné skupiny
dmSTK.btSGLST.Open;      // Špecifikačné skupiny
dmSTK.btSPCINF.Open;     // Špecifikačné info
dmSTK.btPLSLST.Open;     // Cenníky
```

### Farebné označenie riadkov
- **Sivá (clGray)**: Vyradený tovar (`DisFlag = 1`)
- **Zelená (clGreen)**: Odoslaný do e-shopu (`SndShp = 1`)
- **Čierna (clBlack)**: Aktívny tovar

### Zmena DPH (VAT Change Prepare)
Modul obsahuje funkcionalitu pre hromadnú prípravu zmeny DPH:
- Farebné označenie podľa novej sadzby (0%, 5%, 19%, 23%)
- Pole `NewVatPrc` pre novú pripravenú sadzbu

## Stav migrácie do NEX Automat

| Funkcionalita | Stav | Poznámka |
|---------------|------|----------|
| GSCAT čítanie | ✅ | `packages/nexdata/nexdata/models/gscat.py` |
| BARCODE čítanie | ✅ | `packages/nexdata/nexdata/models/barcode.py` |
| MGLST čítanie | ✅ | `packages/nexdata/nexdata/models/mglst.py` |
| API endpoint | ❌ | Potrebné vytvoriť |
| Desktop UI | ❌ | PySide6 formulár |
| Web UI | ❌ | React komponenty |
