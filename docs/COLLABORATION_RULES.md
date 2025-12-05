# Collaboration Rules / Pravidlá Spolupráce

**Project:** NEX Automat & Related Projects  
**Owner:** Zoltán  
**Assistant:** Claude (Anthropic)  
**Last Updated:** 2025-12-05  
**Version:** 1.0

---

## Structured Rules / Štruktúrované Pravidlá

### 🎯 Working Process / Pracovný Proces

**1. Single Solution Approach**
- Provide single recommended solution only, no alternatives unless requested
- Poskytni jediné odporúčané riešenie, žiadne alternatívy pokiaľ nie sú výslovne požadované

**2. Step-by-Step Execution**
- Present one step at a time, wait for confirmation before next step
- Prezentuj jeden krok, čakaj na potvrdenie pred pokračovaním

**3. Token Usage Statistics**
- End each response with token usage stats: Used/Total, Remaining, %, Status indicator
- Každá odpoveď končí: Used/Total, Remaining, %, Status indikátor

**8. No Multi-Step Generation**
- Claude works step-by-step, waits for confirmation before proceeding to next step, never generates multiple steps at once
- Nikdy negeneruj viacero krokov naraz

**9. One Best Solution Only**
- Claude provides only ONE best solution, never multiple alternatives unless explicitly requested
- Len JEDNO najlepšie riešenie (pokiaľ nie je výslovne inak)

**10. Systematic Error Resolution**
- When error occurs, Claude finds and fixes root cause systematically, never jumps to alternative solutions
- Pri chybe nájdi root cause, neskáč na alternatívy

**11. Quality Over Speed**
- Claude prioritizes quality and professional solutions over speed, takes time to analyze properly
- Priorita na profesionálne riešenia, nie rýchlosť

---

### 🌍 Communication / Komunikácia

**5. Language & Terminology**
- Communicate in Slovak language. For project names use exact terminology: uae-legal-agent, claude-dev-automation, NEX Genesis Server
- Jazyk: Slovenčina. Presná terminológia pre projekty

**18. Documentation Format**
- In docs use standard Markdown tables only, never ASCII box-drawing chars (┌─│└). Keep ASCII tree structures for file/folder listings.
- Štandardné Markdown tabuľky, NIE ASCII box-drawing. ASCII tree OK pre súbory/adresáre

---

### 📂 Project Workflow / Projekt Workflow

**4. GitHub Validation**
- NEVER start work if GitHub files fail to load - inform user and stop immediately
- NIKDY nezačni ak GitHub files zlyhajú - informuj a zastav

**6. Session Notes Priority**
- When loading session notes, immediately identify Current Status and Next Steps sections - start work based on these priorities
- Identifikuj Current Status a Next Steps, začni z nich

**12. Script-Based Changes**
- All project changes done via scripts for both new files and fixes of existing files
- Všetky zmeny projektu via scripty (nové súbory + opravy)

**17. Development Workflow**
- All fixes via Development → Git → Deployment workflow. Never fix directly in Deployment to avoid inconsistency
- Nikdy neopravuj priamo v Deployment

**19. Package Structure (CRITICAL)**
- CRITICAL: nex-shared package uses FLAT structure - "nex-shared" appears ONLY ONCE in path: packages/nex-shared/models/ NOT packages/nex-shared/nex_shared/models/
- KRITICKÉ: nex-shared flat štruktúra

---

### 🛠️ Scripts & Code / Scripty & Kód

**7. Artifacts Usage**
- Generate all code, configs, documents and outputs into artifacts
- Všetok kód, configs, dokumenty generuj do artifacts

**15. Python Scripts Only**
- All fixes done via .py scripts only - never generate alternative .ps1 scripts
- Všetky opravy len .py, nikdy .ps1 alternatívy

**20. Script Numbering (NEW)**
- Session scripts numbered from 01 sequentially. Only temporary scripts numbered, permanent scripts not.
- Session scripty od 01 plynule. Len dočasné číslované, trvalé nie.

---

### 📝 Documentation / Dokumentácia

**13. Git Operations**
- No need to write commit and push descriptions, user does Git operations himself
- Nepíš commit/push popisy, používateľ si to robí sám

**14. Manifest Generation**
- No need to write manifest generation instructions, user generates manifests himself
- Nepíš manifest inštrukcie, používateľ generuje sám

**16. Session Closure**
- When user says "novy chat" generate SESSION_NOTES.md, INIT_PROMPT_NEW_CHAT.md and commit message as plain text without commands
- Vygeneruj SESSION_NOTES.md, INIT_PROMPT_NEW_CHAT.md, commit message (plain text, bez príkazov)

---

## Complete List / Plynulý Zoznam (1-20)

1. **Provide single recommended solution only, no alternatives unless requested**
   - Poskytni jediné odporúčané riešenie, žiadne alternatívy pokiaľ nie sú výslovne požadované

2. **Present one step at a time, wait for confirmation before next step**
   - Prezentuj jeden krok, čakaj na potvrdenie pred pokračovaním

3. **End each response with token usage stats: Used/Total, Remaining, %, Status indicator**
   - Každá odpoveď končí: Used/Total, Remaining, %, Status indikátor

4. **NEVER start work if GitHub files fail to load - inform user and stop immediately**
   - NIKDY nezačni ak GitHub files zlyhajú - informuj a zastav

5. **Communicate in Slovak language. For project names use exact terminology: uae-legal-agent, claude-dev-automation, NEX Genesis Server**
   - Jazyk: Slovenčina. Presná terminológia pre projekty

6. **When loading session notes, immediately identify Current Status and Next Steps sections - start work based on these priorities**
   - Identifikuj Current Status a Next Steps, začni z nich

7. **Generate all code, configs, documents and outputs into artifacts**
   - Všetok kód, configs, dokumenty generuj do artifacts

8. **Claude works step-by-step, waits for confirmation before proceeding to next step, never generates multiple steps at once**
   - Nikdy negeneruj viacero krokov naraz

9. **Claude provides only ONE best solution, never multiple alternatives unless explicitly requested**
   - Len JEDNO najlepšie riešenie (pokiaľ nie je výslovne inak)

10. **When error occurs, Claude finds and fixes root cause systematically, never jumps to alternative solutions**
    - Pri chybe nájdi root cause, neskáč na alternatívy

11. **Claude prioritizes quality and professional solutions over speed, takes time to analyze properly**
    - Priorita na profesionálne riešenia, nie rýchlosť

12. **All project changes done via scripts for both new files and fixes of existing files**
    - Všetky zmeny projektu via scripty (nové súbory + opravy)

13. **No need to write commit and push descriptions, user does Git operations himself**
    - Nepíš commit/push popisy, používateľ si to robí sám

14. **No need to write manifest generation instructions, user generates manifests himself**
    - Nepíš manifest inštrukcie, používateľ generuje sám

15. **All fixes done via .py scripts only - never generate alternative .ps1 scripts**
    - Všetky opravy len .py, nikdy .ps1 alternatívy

16. **When user says "novy chat" generate SESSION_NOTES.md, INIT_PROMPT_NEW_CHAT.md and commit message as plain text without commands**
    - Vygeneruj SESSION_NOTES.md, INIT_PROMPT_NEW_CHAT.md, commit message (plain text, bez príkazov)

17. **All fixes via Development → Git → Deployment workflow. Never fix directly in Deployment to avoid inconsistency**
    - Nikdy neopravuj priamo v Deployment

18. **In docs use standard Markdown tables only, never ASCII box-drawing chars (┌─│└). Keep ASCII tree structures for file/folder listings.**
    - Štandardné Markdown tabuľky, NIE ASCII box-drawing. ASCII tree OK pre súbory/adresáre

19. **CRITICAL: nex-shared package uses FLAT structure - "nex-shared" appears ONLY ONCE in path: packages/nex-shared/models/ NOT packages/nex-shared/nex_shared/models/**
    - KRITICKÉ: nex-shared flat štruktúra

20. **Session scripts numbered from 01 sequentially. Only temporary scripts numbered, permanent scripts not.**
    - Session scripty od 01 plynule. Len dočasné číslované, trvalé nie.

---

## Usage Notes / Poznámky k Použitiu

### Script Numbering Example (Rule 20)
```
Session 1:
✅ 01_create_component.py      (temporary)
✅ 02_fix_bug.py                (temporary)
✅ 03_update_config.py          (temporary)
❌ create_database_schema.py   (permanent - not numbered)

Session 2: (starts from 01 again)
✅ 01_add_feature.py            (temporary)
✅ 02_test_integration.py       (temporary)
```

### Token Usage Format (Rule 3)
```
Token Usage: 12345/190000 | Remaining: 177655 | 6.5% | ✅ Dostatočná kapacita
```

### Git Workflow (Rule 17)
```
Development → git commit/push → Deployment
Never: Deployment → direct fix (creates inconsistency)
```

---

## Version History / História Verzií

- **v1.0** (2025-12-05): Initial version with 20 rules
  - Added Rule 20: Script numbering convention
  - Structured by categories: Process, Communication, Workflow, Scripts, Documentation

---

**Total Rules:** 20  
**Status:** Active  
**Maintained By:** Zoltán & Claude