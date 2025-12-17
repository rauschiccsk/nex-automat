# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** .md-old Cleanup IN PROGRESS
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** .md-old Cleanup & RAG Optimization (2025-12-17)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 23 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #23:** RAG Access - priamo požiadaj o Permission URL

---

## 🔄 DOKONČENÉ TÚTO SESSION

### RAG Workflow
- ✅ `tools/rag/rag_update.py` - unified command
- ✅ `--new` = files modified today, `--all` = full reindex

### Scripts Cleanup
- ✅ ~40 obsolete scripts removed
- ✅ scripts/README.md created

### Index Files
- ✅ 15x `00_*_INDEX.md` removed (RAG replaces)

### .md-old Analysis (PARTIAL)
- ✅ Deployment docs analyzed and cleaned
- ⏳ ~25 README.md-old files remaining

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Complete .md-old Cleanup
- Analyze remaining README.md-old files
- Bulk delete empty placeholders

### Priority #2: supplier-invoice-staging Application  
- New PySide6 app using shared-pyside6 package
- Basic staging invoice UI

---

## 📂 KEY PATHS

```
tools/rag/rag_update.py          # RAG workflow
scripts/README.md                 # Scripts docs
docs/operations/TROUBLESHOOTING.md  # NEW
docs/archive/releases/            # NEW folder
packages/shared-pyside6/          # Ready ✅
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

## Remaining .md-old Files (~25)

```
README.md-old (root + apps folders)
apps/supplier-invoice-editor/*.md-old
apps/supplier-invoice-loader/*.md-old  
docs/giudes/CONTRIBUTING.md-old
packages/nexdata/README.md-old
tools/INSTALLATION_GUIDE.md-old
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat  
**Memory Rules:** 23 active

---

**KONIEC INIT PROMPTU**
