# Šablóna analýzy NEX Genesis modulu

## Účel

Tento dokument slúži ako šablóna pre systematickú analýzu modulov NEX Genesis za účelom migrácie do NEX Automat.

---

## 1. Identifikácia modulu

### Základné údaje

| Položka | Hodnota |
|---------|---------|
| **Názov modulu** | [Napr. GSC - Katalóg produktov] |
| **Prefix** | [Napr. Gsc_] |
| **Hlavný súbor** | [Napr. NexModules/Gsc_F.pas] |
| **Hlavná trieda** | [Napr. TF_Gsc] |

### Popis funkcionality

[Stručný popis, čo modul robí - 2-3 vety]

---

## 2. Analýza zdrojového kódu

### Krok 1: Nájdenie hlavného súboru

```bash
# Hľadanie modulov podľa prefixu
find /mnt/c/Development/nex-genesis -name "{PREFIX}*.pas" | head -20
```

### Krok 2: Analýza uses section

Prečítať hlavný .pas súbor a identifikovať:

**Interface uses** (externé závislosti):
```pascal
uses
  // Core utilities
  Fnc, IcTypes, ...
  // Table handlers
  hTABLE1, hTABLE2, ...
  // UI components
  TableView, ...
```

**Implementation uses** (interné závislosti):
```pascal
uses
  DM_DATAMODULE, // Data moduly
  SubModule_F,   // Sub-formuláre
  ...
```

### Krok 3: Identifikácia tabuliek

Hľadať v kóde:
- `dm*.bt*.Open` - otvorenie tabuliek
- `h*` unity - table handlery
- BDF súbory podľa názvov tabuliek

---

## 3. Zoznam tabuliek

| Tabuľka | BDF súbor | Handler | Data modul | Popis |
|---------|-----------|---------|------------|-------|
| TABLE1 | table1.bdf | hTABLE1 | dmXXX.btTABLE1 | Popis |

### Pre každú tabuľku extrahovať:

```bash
cat /mnt/c/Development/nex-genesis/DefFiles/{table}.bdf
```

Dokumentovať:
- Polia (názov, typ, popis)
- Indexy (polia, vlastnosti)
- Relácie (FK → iné tabuľky)

---

## 4. Sub-moduly

### Kategorizácia podľa funkcie

| Kategória | Súbory | Popis |
|-----------|--------|-------|
| Úpravy | *_Edi_F.pas | CRUD operácie |
| Zobrazenie | *_Lst_V.pas | Zoznamy, výbery |
| Nástroje | *_Srch_F.pas | Vyhľadávanie, filtre |
| Údržba | *_Gen_F.pas | Generovanie, import |
| Servis | *_Chg_F.pas | Hromadné zmeny |

---

## 5. Prístupové práva

Hľadať v kóde:
- `gAfc.{Modul}.*` - prístupové funkcie
- `BookModify`, `BookRight` - oprávnenia na úpravu

| Právo | Popis |
|-------|-------|
| gAfc.Xxx.ItmAdd | Pridať položku |
| gAfc.Xxx.ItmDel | Zmazať položku |
| gAfc.Xxx.ItmMod | Upraviť položku |

---

## 6. Business logika

### Invarianty a pravidlá

Dokumentovať:
- Validačné pravidlá
- Automatické výpočty
- Závislosti medzi poľami
- Triggery a eventy

### Workflow

```
[Stav 1] → [Akcia] → [Stav 2]
```

---

## 7. Migračný plán

### Priorita

| Úroveň | Popis |
|--------|-------|
| P1 - Critical | Základná funkcionalita |
| P2 - High | Hlavné funkcie |
| P3 - Medium | Rozšírené funkcie |
| P4 - Low | Nice-to-have |

### Checklist migrácie

- [ ] Btrieve modely (packages/nexdata/)
- [ ] PostgreSQL modely (packages/nex-staging/)
- [ ] API endpoints (apps/xxx-api/)
- [ ] Desktop UI (PySide6)
- [ ] Web UI (React)
- [ ] Testy
- [ ] Dokumentácia

---

## 8. Prílohy

### Zoznam súborov modulu

```
NexModules/
├── {Prefix}_F.pas          # Hlavný formulár
├── {Prefix}_*_F.pas        # Sub-formuláre
├── {Prefix}_*_V.pas        # Views
└── {Prefix}_*.pas          # Unity

NexTables/
└── h{TABLE}.pas            # Table handlery

DefFiles/
└── {table}.bdf             # BDF definície
```

### Diagram závislostí

```
┌─────────────────┐
│   {Prefix}_F    │
├─────────────────┤
│ uses:           │
│ - hTABLE1       │
│ - hTABLE2       │
│ - DM_XXX        │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Btrieve │
    │ Tables  │
    └─────────┘
```

---

## Poznámky

[Špeciálne poznámky, problémy, TODO]
