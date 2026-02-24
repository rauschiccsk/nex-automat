# NEX Genesis - Štruktúra projektu

## Adresárová štruktúra

```
C:\Development\nex-genesis\
├── AppModules/      # Hlavné aplikačné moduly (EXE)
├── AppServices/     # Aplikačné služby
├── AppServers/      # Serverové komponenty
├── DefFiles/        # Btrieve tabuľkové definície (678 BDF súborov)
├── Libraries/       # Zdieľané knižnice
├── NexCommons/      # Spoločné komponenty a utility
├── NexDatamod/      # Data moduly (DataModule units)
├── NexDevices/      # Ovládače zariadení (váhy, čítačky, tlačiarne)
├── NexModules/      # Aplikačné moduly (formuláre a business logika)
├── NexTables/       # Tabuľkové handlery (wrappers nad Btrieve)
└── Packages/        # VCL komponenty a balíčky
```

## Konvencie pomenovania

### Súbory modulov (NexModules/)

Formát: `{Modul}_{Funkcia}_{Typ}.pas`

| Časť | Význam | Príklad |
|------|--------|---------|
| Modul | 3-písmenový prefix modulu | Gsc, Stk, Pab, Tsh |
| Funkcia | Skratka funkcie | ItmEdi, MgLst, BcSrch |
| Typ | F=Form, V=View, _=Unit | F, V, (prázdne) |

**Príklady:**
- `Gsc_F.pas` - Hlavný formulár Katalógu produktov
- `Gsc_ItmEdi_F.pas` - Formulár editácie tovaru
- `Gsc_MgLst_V.pas` - View zoznam tovarových skupín
- `Gsc_CrpCpy.pas` - Unit kopírovanie do inej firmy

### Tabuľkové handlery (NexTables/)

Formát: `h{TABULKA}.pas`

**Príklady:**
- `hGSCAT.pas` - Handler pre GSCAT.BTR
- `hBARCODE.pas` - Handler pre BARCODE.BTR
- `hMGLST.pas` - Handler pre MGLST.BTR

### Data moduly (NexDatamod/)

Formát: `DM_{OBLAST}.pas`

**Príklady:**
- `DM_SYSTEM.pas` - Systémové nastavenia
- `DM_STKDAT.pas` - Skladové dáta (btGSCAT, btBARCODE, btMGLST...)
- `DM_LDGDAT.pas` - Účtovné dáta
- `DM_TMPSTK.pas` - Dočasné skladové tabuľky

### BDF definície (DefFiles/)

Formát: `{tabulka}.bdf`

**Príklady:**
- `gscat.bdf` - Definícia GSCAT.BTR
- `barcode.bdf` - Definícia BARCODE.BTR
- `tsh.bdf` - Definícia TSH*.BTR

## Typy súborov

| Prípona | Typ | Popis |
|---------|-----|-------|
| `.pas` | Pascal unit | Zdrojový kód |
| `.dfm` | Delphi form | Definícia formulára (binárna/textová) |
| `.bdf` | Btrieve definition | Definícia štruktúry tabuľky |
| `.dpr` | Delphi project | Hlavný súbor projektu |
| `.dof` | Delphi options | Nastavenia projektu |
| `.res` | Resource | Zdroje (ikony, stringy) |

## BDF formát

BDF súbory definujú štruktúru Btrieve tabuliek:

```
GSCAT.BTR cPrealloc+cFree10   ;Evidencia tovaru

GsCode     longint      ;Tovarové číslo (PLU)
GsName     Str30        ;Názov tovaru
MgCode     longint      ;Číslo tovarovej skupiny
...

IND GsCode=GsCode
GLB cModif
SEG

IND MgCode,GsCode=MgGs
GLB cModif+cDuplic
SEG
```

### Dátové typy v BDF

| Typ | Veľkosť | Popis |
|-----|---------|-------|
| `byte` | 1 | Unsigned 8-bit |
| `word` | 2 | Unsigned 16-bit |
| `longint` | 4 | Signed 32-bit |
| `double` | 8 | 64-bit floating point |
| `Str{N}` | N+1 | Pascal ShortString (1 byte length + N data) |
| `DateType` | 4 | Delphi TDateTime (days since 1899-12-30) |
| `TimeType` | 4 | Milliseconds since midnight |

### Index flagy

| Flag | Význam |
|------|--------|
| `cModif` | Modifikovateľný index |
| `cDuplic` | Povoliť duplicity |
| `cInsensit` | Case-insensitive |

## Globálne premenné

| Premenná | Typ | Popis |
|----------|-----|-------|
| `gPath` | TNexPath | Cesty k súborom |
| `gIni` | TNexIni | INI nastavenia |
| `gRgh` | TBookRight | Prístupové práva |
| `gAfc` | TAfc | Access function control |
| `gNT` | TNexText | Lokalizované texty |
| `gvSys` | TSysVar | Systémové premenné |
| `dmSTK` | TDM_STKDAT | Data modul skladových dát |
| `dmLDG` | TDM_LDGDAT | Data modul účtovných dát |

## Vzťahy medzi vrstvami

```
┌─────────────────────────────────────────────┐
│           NexModules (Forms/Views)          │
│         Gsc_F.pas, Gsc_ItmEdi_F.pas         │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│            NexDatamod (Data Modules)        │
│    DM_STKDAT.pas (btGSCAT, btBARCODE...)    │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│           NexTables (Table Handlers)        │
│        hGSCAT.pas, hBARCODE.pas             │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│              Btrieve Engine                 │
│            GSCAT.BTR, BARCODE.BTR           │
└─────────────────────────────────────────────┘
```
