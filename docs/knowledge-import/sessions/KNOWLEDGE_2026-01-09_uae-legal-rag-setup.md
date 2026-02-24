
# UAE Legal Research & RAG Setup

**Dátum:** 2026-01-09
**Status:** ✅ TIER 1 PARTIALLY COMPLETE - RAG Indexed

---

## Dokončené úlohy

### ✅ TIER 1 - Critical Laws

1. **Federal Decree-Law No. 10/2025 (AML)** ✅
   - Status: ANALYSIS COMPLETE
   - Súbor: `Federal_Decree_Law_10_2025_AML_Analysis.md`
   - Kľúčové zistenia:
     - Lowered evidentiary threshold: "sufficient evidence or circumstantial evidence"
     - Knowledge can be "inferred from objective circumstances"
     - Predicate offences expanded (tax evasion, TF, PF)
     - Penalties increased: AED 5-100M for legal entities

2. **Federal Decree-Law No. 38/2022 (Criminal Procedure)** ✅
   - Status: FULL TEXT ANALYZED (83 pages)
   - Súbor: `Federal_Decree_Law_38_2022_Criminal_Procedure_Analysis.md`
   - Kľúčové články:
     - Article 2: Preservation of Personal Freedom
     - Article 48: Rights of the Accused (right to silence)
     - Article 107: Detention periods (7+14 days, then 30-day extensions)
     - Article 108-109: Bail procedures
     - Article 115-116: Asset freeze & grievance procedures
     - Article 230: Appeal rights (15 days)

3. **Cabinet Decision No. 10/2019 (Executive Regulations)** ⏳
   - Status: NOT YET SEARCHED
   - Priority: HIGH

### ✅ RAG System

- **Indexed:** 82 documents
- **Chunks:** 265
- **Tokens:** 212,980
- **Tenant:** `uae`
- **Time:** 40.0s

**Štruktúra knowledge:**
```
docs/knowledge/tenants/uae/
├── federal_laws/
│   ├── AML/
│   │   └── Federal_Decree_Law_10_2025_AML_Analysis.md ✅
│   └── Criminal/
│       └── Federal_Decree_Law_38_2022_Criminal_Procedure_Analysis.md ✅
```

---

## Aktuálny stav

### 🎯 Právny prípad

**Situácia:**
- Slovenský občan obvinený z money laundering v UAE
- Predaj nehnuteľností na Slovensku → prevod na firmu v UAE
- **Zadržaný:** 1.5 roka (18 mesiacov = 540+ dní)
- **Prvostupňový rozsudok:** 1 rok väzenia
- **Odvolanie:** Prebieha
- **Problém:** Dôkazy označené ako "nepresvedčivé"

### 🔥 KRITICKÉ ZISTENIA

**1. DETENTION PERIOD EXCESSIVE**
- Zákonný max (Article 107): 7+14 dní → 30 dní renewable
- Klient: **1.5 roka** = EXTRÉMNE nad limit
- **Otázka:** Boli všetky extensions správne schválené?

**2. EVIDENTIARY BURDEN LOWERED** 
- **Starý zákon (20/2018):** "actual knowledge" required
- **Nový zákon (10/2025):** "sufficient evidence or circumstantial evidence"
- **Platný od:** 14. október 2025
- **OTÁZKA:** Kedy bol klient odsúdený? (pred/po 14.10.2025)

**3. BAIL WAS POSSIBLE**
- Article 108: Death penalty/life sentence → Attorney General approval
- Money laundering ≠ death/life → **Public Prosecution could release**
- **Otázka:** Prečo nebol bail granted?

---

## Next Steps

### 📋 TIER 1 Completion

⏳ **Cabinet Decision No. 10/2019**
- Search: "UAE Cabinet Decision 10 2019 AML executive regulation"
- Expected: Detailed implementation procedures
- Priority: HIGH

### 🧪 RAG Testing

**Test Script Created:** `scripts/test_rag_uae.py`

**Status:** Ready to test (not yet executed)

**Test Queries:**
1. Money Laundering Definition
2. Detention Periods
3. Burden of Proof
4. Legal Representation Rights
5. Asset Freezing Procedures
6. Appeal Rights

**Run:**
```bash
cd C:\Development\nex-automat\scripts
python test_rag_uae.py
```

### 📊 Legal Analysis Needed

**For Appeal Preparation:**

1. **Timeline Analysis**
   - [ ] Get exact conviction date
   - [ ] Determine which law applies (20/2018 vs 10/2025)
   - [ ] Verify all detention extensions were legal

2. **Bail Analysis**
   - [ ] Why was bail denied?
   - [ ] Were bail requests made?
   - [ ] Document financial hardship

3. **Evidence Review**
   - [ ] What evidence was presented?
   - [ ] Was evidence properly disclosed? (Article 210)
   - [ ] Were all procedural rights respected?

4. **Grounds for Appeal**
   - [ ] Insufficient evidence
   - [ ] Procedural violations
   - [ ] Excessive detention
   - [ ] Misapplication of law

---

## Dôležité príkazy

### RAG Commands

```bash
# Update RAG with new documents
cd C:\\Development\\nex-automat\\tools\\rag
python rag_update.py --all

# Test RAG queries
cd C:\\Development\\nex-automat\\scripts
python test_rag_uae.py
```

### Search Next Law

```bash
# Continue with TIER 1 Item #3
Search: "UAE Cabinet Decision 10 2019 AML executive regulation PDF"
```

---

## Token Usage

**Current Session:**
- Used: 111,074 / 190,000 tokens
- Remaining: 78,926 tokens
- Status: ✅ SAFE (58% used)

**Recommendation:** Start new chat for testing phase
