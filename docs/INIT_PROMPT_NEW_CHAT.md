# Init Prompt - Post Documentation Cleanup

**Projekt:** NEX Automat  
**Last Session:** 2025-11-26 (Documentation Cleanup - Pravidlo 18)  
**This Session:** Implementation Phase  

---

## Quick Context

NEX Automat je projekt pre kompletnú automatizáciu podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- GO-LIVE: 2025-11-27 (Preview/Demo pre Mágerstav)
- Strategic Planning: ✅ COMPLETE
- Documentation: ✅ CLEAN (all docs comply with pravidlo 18)

---

## What Was Completed Last Session

### Documentation Cleanup ✅

Všetkých 6 strategických dokumentov upravených podľa pravidla 18:

**Modified (Fixed):**
- `docs/strategy/ARCHITECTURE.md` → v1.1
- `docs/strategy/REQUIREMENTS.md` → v1.1
- `docs/strategy/CURRENT_STATE.md` → v1.1

**Already compliant:**
- `docs/strategy/TERMINOLOGY.md` → v1.0
- `docs/strategy/VISION.md` → v1.0
- `docs/strategy/ROADMAP.md` → v1.0

**Zmeny:**
- Odstránené všetky box-drawing chars (┌─│└)
- Štandardné Markdown tabuľky
- Plain text formátovanie diagramov
- ASCII tree štruktúry zachované

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

## Project Structure

```
C:\Development\nex-automat\
├── docs\
│   ├── SESSION_NOTES.md
│   └── strategy\
│       ├── TERMINOLOGY.md
│       ├── CURRENT_STATE.md
│       ├── VISION.md
│       ├── ARCHITECTURE.md      ← v1.1 (fixed)
│       ├── REQUIREMENTS.md      ← v1.1 (fixed)
│       └── ROADMAP.md
├── apps\
│   ├── supplier-invoice-loader\   # FastAPI service
│   └── supplier-invoice-editor\   # PyQt5 GUI
└── packages\
    ├── invoice-shared\
    └── nex-shared\
```

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

## How to Start This Session

1. Commit dokumentáciu (3 upravené súbory)
2. Vyber ďalší krok:
   - **Opcia A:** Príprava na GO-LIVE (ak treba)
   - **Opcia B:** Fáza 3 - Btrieve Models (TSH, TSI, PLS, RPC)
   - **Opcia C:** Fáza 4 - GUI Editácia
   - **Opcia D:** Iné

---

## Important Notes

- **Strategic docs** sú v `docs/strategy/` - všetky vyhovujú pravidlu 18
- **CURRENT_STATE.md** obsahuje kompletný navrhnutý workflow
- **ROADMAP.md** obsahuje poradie implementácie
- Pri implementácii dodržiavať workflow z CURRENT_STATE.md

---

**Last Updated:** 2025-11-26  
**Version:** 1.0  
**Status:** 🟢 Ready for Implementation