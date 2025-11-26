# Init Prompt - Post Strategic Planning

**Project:** NEX Automat  
**Last Session:** 2025-11-26 (Strategic Planning Complete)  
**This Session:** Implementation Phase  

---

## Quick Context

NEX Automat je projekt pre kompletnú automatizáciu podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- GO-LIVE: 2025-11-27 (Preview/Demo pre Mágerstav)
- Strategic Planning: ✅ COMPLETE

---

## What Was Completed Last Session

### Strategic Planning - ALL COMPLETE ✅

| Bod | Názov | Status |
|-----|-------|--------|
| 1 | Definícia cieľov | ✅ |
| - | Terminológia | ✅ |
| 2 | Aktuálny stav (inventory) | ✅ |
| 3 | Požiadavky & Priority | ✅ |
| 4 | Architektúra & Design | ✅ |
| 5 | Roadmap & Fázy | ✅ |
| 6 | Dokumentácia | ✅ |

### Strategická dokumentácia vytvorená

```
docs/strategy/
├── TERMINOLOGY.md      # Slovník pojmov NEX Genesis
├── CURRENT_STATE.md    # Inventory + navrhnutý workflow
├── VISION.md           # Vízia, stratégia, hodnota
├── ARCHITECTURE.md     # Komponenty, dátový tok
├── REQUIREMENTS.md     # Funkcionálne požiadavky
└── ROADMAP.md          # 9 fáz implementácie
```

---

## Implementation Roadmap

```
FÁZA 1: Email → Staging → GUI Zobrazenie     ✅ COMPLETE
FÁZA 2: GO-LIVE Preview/Demo                 🟡 IN PROGRESS (zajtra)
FÁZA 3: Btrieve Models (TSH, TSI, PLS, RPC)  ⚪ TODO ← NEXT
FÁZA 4: GUI Editácia + Farebné rozlíšenie    ⚪ TODO
FÁZA 5: Vytvorenie produktových kariet       ⚪ TODO
FÁZA 6: Zaevidovanie dodávateľského DL       ⚪ TODO
FÁZA 7: Požiadavky na zmenu cien             ⚪ TODO
FÁZA 8: Testovanie + Production Hardening    ⚪ TODO
FÁZA 9: Ďalší zákazníci + Rozšírenia         ⚪ FUTURE
```

---

## Navrhnutý Workflow v2.0

### Fáza A: Email → Staging ✅ HOTOVÉ
1. Email s PDF → n8n IMAP trigger
2. PDF extrakcia (regex)
3. ISDOC XML generovanie
4. FastAPI → PostgreSQL staging
5. NEX Lookup (EAN → PLU)

### Fáza B: GUI Kontrola ⚪ TODO
1. GUI zobrazí položky faktúry
2. Farebné rozlíšenie:
   - BIELA: PLU > 0 (existuje)
   - ČERVENÁ: PLU = 0, bez skupiny
   - ORANŽOVÁ: PLU = 0, so skupinou
   - ŽLTÁ: cena zmenená
3. Operátor priradí skupiny novým položkám
4. Operátor skontroluje/upraví marže

### Fáza C: Produktové karty ⚪ TODO
1. "Vytvoriť nové položky"
2. GSCAT.BTR zápis (nové PLU)
3. BARCODE.BTR zápis (EAN väzba)
4. Refresh PLU

### Fáza D: Dodací list ⚪ TODO
1. "Zaevidovať DL"
2. TSH zápis (hlavička)
3. TSI zápis (položky)
4. RPC zápis (zmenené ceny)
5. Spätná kontrola súm
6. Staging: status = completed

---

## Btrieve Tabuľky

| Tabuľka | Súbor | Model | READ | WRITE |
|---------|-------|-------|------|-------|
| GSCAT | GSCAT.BTR | ✅ | ✅ | ⚪ TODO |
| BARCODE | BARCODE.BTR | ✅ | ✅ | ⚪ TODO |
| PAB | PAB.BTR | ✅ | ✅ | — |
| MGLST | MGLST.BTR | ✅ | ✅ | — |
| TSH | TSHA-001.BTR | ⚪ TODO | ⚪ TODO | ⚪ TODO |
| TSI | TSIA-001.BTR | ⚪ TODO | ⚪ TODO | ⚪ TODO |
| PLS | PLSnnnnn.BTR | ⚪ TODO | ⚪ TODO | — |
| RPC | RPCnnnnn.BTR | ⚪ TODO | ⚪ TODO | ⚪ TODO |

---

## Project Structure

```
C:\Development\nex-automat\
├── docs\
│   ├── SESSION_NOTES.md
│   └── strategy\
│       ├── TERMINOLOGY.md
│       ├── CURRENT_STATE.md
│       ├── VISION.md
│       ├── ARCHITECTURE.md
│       ├── REQUIREMENTS.md
│       └── ROADMAP.md
├── apps\
│   ├── supplier-invoice-loader\   # FastAPI service
│   └── supplier-invoice-editor\   # PyQt5 GUI
└── packages\
    ├── invoice-shared\
    └── nex-shared\
```

---

## Key Files for Implementation

**Btrieve modely (existujúce):**
- `apps/supplier-invoice-editor/src/models/gscat.py`
- `apps/supplier-invoice-editor/src/models/barcode.py`
- `apps/supplier-invoice-editor/src/models/pab.py`
- `apps/supplier-invoice-editor/src/models/mglst.py`

**Btrieve modely (TODO):**
- `apps/supplier-invoice-editor/src/models/tsh.py` ← vytvoriť
- `apps/supplier-invoice-editor/src/models/tsi.py` ← vytvoriť
- `apps/supplier-invoice-editor/src/models/pls.py` ← vytvoriť
- `apps/supplier-invoice-editor/src/models/rpc.py` ← vytvoriť

---

## How to Start This Session

1. Potvrď GO-LIVE status (2025-11-27)
2. Vyber ďalší krok:
   - **Opcia A:** Príprava na GO-LIVE (ak treba)
   - **Opcia B:** Fáza 3 - Btrieve Models (TSH, TSI, PLS, RPC)
   - **Opcia C:** Fáza 4 - GUI Editácia
   - **Opcia D:** Iné

---

## Important Notes

- **Strategic docs** sú v `docs/strategy/` - vždy aktuálne
- **CURRENT_STATE.md** obsahuje kompletný navrhnutý workflow
- **ROADMAP.md** obsahuje poradie implementácie
- Pri implementácii dodržiavať workflow z CURRENT_STATE.md

---

**Last Updated:** 2025-11-26  
**Version:** 1.0  
**Status:** 🟢 Ready for Implementation