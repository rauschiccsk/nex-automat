
INIT PROMPT - UAE Legal Research - Testing Phase

Projekt: nex-automat
Session: UAE Anti-Money Laundering Legal Research - TESTING
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Dátum: 2026-01-09

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: RAG Testing & TIER 1 Completion

---

## Čo je hotové ✅

| Komponenta | Status | Poznámka |
|------------|--------|----------|
| Federal Decree-Law 10/2025 (AML) | ✅ DONE | Analysis complete |
| Federal Decree-Law 38/2022 (Criminal) | ✅ DONE | Full 83-page analysis |
| RAG Indexing | ✅ DONE | 82 docs, 265 chunks, 212K tokens |
| Test Script | ✅ CREATED | test_rag_uae.py ready |

**Progress:** TIER 1: [2/3] ████████░░ 67%

---

## Aktuálna úloha ⏳

### 1. RAG TESTING (IMMEDIATE)

**Run test script:**
```bash
cd C:\Development\nex-automat\scripts
python test_rag_uae.py
```

**Expected output:**
- 6 test queries executed
- Results from indexed legal documents
- Verify relevance scores and content accuracy

**If tests fail:**
- Check ChromaDB connection
- Verify tenant='uae' documents exist
- Review rag_manager.py configuration

### 2. TIER 1 COMPLETION

**Search for:** Cabinet Decision No. 10/2019

**Query:**
```
"UAE Cabinet Decision 10 2019 AML executive regulation PDF"
```

**Expected:** Detailed implementation procedures for AML Law

---

## Kritické zistenia pre prípad

### 🚨 DETENTION EXCESSIVE
- Klient: **1.5 roka zadržaný** (540+ dní)
- Zákonný max: 7+14 dní → 30-day extensions (Article 107)
- **Action:** Verify all extensions were legal

### 🚨 NEW LAW CHANGES (effective 14 Oct 2025)
- **Old:** "actual knowledge" required
- **New:** "sufficient evidence or circumstantial evidence"
- **Question:** Kedy bol klient odsúdený?

### 🚨 BAIL SHOULD HAVE BEEN POSSIBLE
- Money laundering ≠ death/life sentence
- Article 108: Public Prosecution can release
- **Question:** Prečo nebol bail granted?

---

## RAG Query Examples

```bash
# Test query via RAG API
https://rag-api.icc.sk/search?tenant=uae&query=money+laundering+definition&limit=5

# Via Telegram Bot
/ask money laundering burden of proof UAE
```

---

## Next Steps

1. **Execute RAG tests** → Verify indexing works
2. **Search Cabinet Decision 10/2019** → Complete TIER 1
3. **Analyze test results** → Prepare legal queries
4. **Document findings** → Build appeal arguments

---

## File Locations

**Knowledge Base:**
```
C:\Development\nex-automat\docs\knowledge\tenants\uae\
├── federal_laws/AML/Federal_Decree_Law_10_2025_AML_Analysis.md
└── federal_laws/Criminal/Federal_Decree_Law_38_2022_Criminal_Procedure_Analysis.md
```

**Scripts:**
```
C:\Development\nex-automat\scripts\
├── test_rag_uae.py (NEW - ready to run)
└── 02_test_uae_money_laundering.py (template for future queries)
```

---

## Critical Reminders

- Token budget monitor: Always show remaining tokens
- Step-by-step approach: One task at a time
- Test before proceeding: Verify each component works
- Document everything: Save artifacts to knowledge/

---

**Ready to start TESTING phase!**
