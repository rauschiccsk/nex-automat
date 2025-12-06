# Collaboration Rules / Pravidlá Spolupráce

**Project:** NEX Automat & Related Projects  
**Owner:** Zoltán  
**Assistant:** Claude (Anthropic)  
**Last Updated:** 2025-12-06  
**Version:** 1.1

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

### 🌐 Communication / Komunikácia

**5. Language & Terminology**
- Communicate in Slovak language. For project names use exact terminology: uae-legal-agent, claude-dev-automation, NEX Genesis Server
- Jazyk: Slovenčina. Presná terminológia pre projekty

**17. Documentation Format**
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

**16. Development Workflow**
- All fixes via Development → Git → Deployment workflow. Never fix directly in Deployment to avoid inconsistency
- Nikdy neopravuj priamo v Deployment

**18. Package Structure (CRITICAL)**
- CRITICAL: nex-shared package uses FLAT structure - "nex-shared" appears ONLY ONCE in path: packages/nex-shared/models/ NOT packages/nex-shared/nex_shared/models/
- KRITICKÉ: nex-shared flat štruktúra

---

### 🛠️ Scripts & Code / Scripty & Kód

**7. Artifacts Usage (CRITICAL - UPDATED)**
- CRITICAL: ALL code/configs/documents/scripts MUST be artifacts. Triggers: Python files, any config, doc >10 lines, code >5 lines. ALWAYS artifacts FIRST, never plain text.
- KRITICKÉ: VŠETOK kód/configs/dokumenty/scripty MUSIA byť artifacts. VŽDY artifacts NAJPRV, nikdy plain text.

**15. Python Scripts Only**
- All fixes done via .py scripts only - never generate alternative .ps1 scripts
- Všetky opravy len .py, nikdy .ps1 alternatívy

**19. Script Numbering**
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

**20. Session Closure (NEW)**
- When user says "novy chat": Generate 3 artifacts IMMEDIATELY: SESSION_NOTES.md, INIT_PROMPT_NEW_CHAT.md, commit-message.txt. Artifacts FIRST, then brief confirmation only.
- Pri "novy chat": Vygeneruj 3 artifacts OKAMŽITE (najprv!), potom len krátke potvrdenie.

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

7. **CRITICAL: ALL code/configs/documents/scripts MUST be artifacts. Triggers: Python files, any config, doc >10 lines, code >5 lines. ALWAYS artifacts FIRST, never plain text.**
   - KRITICKÉ: VŠETOK kód/configs/dokumenty/scripty MUSIA byť artifacts. VŽDY artifacts NAJPRV, nikdy plain text.

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

16. **All fixes via Development → Git → Deployment workflow. Never fix directly in Deployment to avoid inconsistency**
    - Nikdy neopravuj priamo v Deployment

17. **In docs use standard Markdown tables only, never ASCII box-drawing chars (┌─│└). Keep ASCII tree structures for file/folder listings.**
    - Štandardné Markdown tabuľky, NIE ASCII box-drawing. ASCII tree OK pre súbory/adresáre

18. **CRITICAL: nex-shared package uses FLAT structure - "nex-shared" appears ONLY ONCE in path: packages/nex-shared/models/ NOT packages/nex-shared/nex_shared/models/**
    - KRITICKÉ: nex-shared flat štruktúra

19. **Session scripts numbered from 01 sequentially. Only temporary scripts numbered, permanent scripts not.**
    - Session scripty od 01 plynule. Len dočasné číslované, trvalé nie.

20. **When user says "novy chat": Generate 3 artifacts IMMEDIATELY: SESSION_NOTES.md, INIT_PROMPT_NEW_CHAT.md, commit-message.txt. Artifacts FIRST, then brief confirmation only.**
    - Pri "novy chat": Vygeneruj 3 artifacts OKAMŽITE (najprv!), potom len krátke potvrdenie.

---

## Usage Notes / Poznámky k Použitiu

### Artifacts Enforcement (Rule 7 - CRITICAL)

**ALWAYS create artifacts for:**
```
✅ Python files (.py)
✅ Config files (.json, .yaml, .py, .txt, .ini, .toml)
✅ Session notes (SESSION_NOTES.md)
✅ Init prompts (INIT_PROMPT_NEW_CHAT.md)
✅ Commit messages (commit-message.txt)
✅ Documents longer than 10 lines
✅ Code examples longer than 5 lines
✅ Any script or configuration
```

**NEVER generate in plain text:**
```
❌ Python code in response
❌ Config content in response
❌ Long documents in response
❌ Session notes in response
❌ Init prompts in response
```

**Self-verification checklist (before EVERY response):**
```
□ Am I generating code? → Artifact!
□ Am I generating a document? → Artifact!
□ Am I generating a config? → Artifact!
□ Did user say "novy chat"? → 3 artifacts FIRST!
□ Is response >10 lines of non-conversational text? → Artifact!
```

### Session Closure Workflow (Rule 20 - NEW)

**When user says "novy chat":**

**MANDATORY sequence:**
1. ✅ Create SESSION_NOTES.md artifact (FIRST!)
2. ✅ Create INIT_PROMPT_NEW_CHAT.md artifact
3. ✅ Create commit-message.txt artifact
4. ✅ Brief confirmation: "✅ Vygenerované 3 artifacts"

**FORBIDDEN:**
```
❌ Writing session notes in plain text
❌ Explaining before creating artifacts
❌ Creating only 1 or 2 artifacts
❌ Long response before artifacts
```

### Script Numbering Example (Rule 19)
```
Session 1:
✅ 01-create-component.py      (temporary)
✅ 02-fix-bug.py                (temporary)
✅ 03-update-config.py          (temporary)
❌ create-database-schema.py   (permanent - not numbered)

Session 2: (starts from 01 again)
✅ 01-add-feature.py            (temporary)
✅ 02-test-integration.py       (temporary)
```

### Token Usage Format (Rule 3)
```
Tokeny: 12345/190000, Zostáva: 177655, 6.5%, ✅ OK
```

### Git Workflow (Rule 16)
```
Development → git commit/push → Deployment
Never: Deployment → direct fix (creates inconsistency)
```

---

## Systematic Problem Prevention

### Issue: Artifacts not being used
**Root Cause:** Conflicting rules in memory_user_edits  
**Solution Applied (2025-12-06):**
- ❌ Removed Rule #16 (old): "...as plain text without commands"
- ❌ Removed Rule #21 (old): "...as plain text without commands"
- ✅ Updated Rule #7: Added CRITICAL enforcement and explicit triggers
- ✅ Added Rule #20: Mandatory artifacts-first workflow for "novy chat"

### Enforcement Mechanism
1. **Memory rules** - Explicit CRITICAL markers
2. **Self-verification** - Checklist before every response
3. **Fixed workflow** - "novy chat" always produces 3 artifacts first

---

## Version History / História Verzií

- **v1.1** (2025-12-06): Enhanced artifacts enforcement
  - **UPDATED Rule #7**: Added CRITICAL marker and explicit triggers
  - **NEW Rule #20**: Mandatory artifacts-first workflow for "novy chat"
  - Removed conflicting old rules #16 and #21
  - Added "Systematic Problem Prevention" section
  - Added detailed "Artifacts Enforcement" usage notes

- **v1.0** (2025-12-05): Initial version with 20 rules
  - Added Rule #19: Script numbering convention
  - Structured by categories: Process, Communication, Workflow, Scripts, Documentation

---

**Total Rules:** 20  
**Status:** Active & Enforced  
**Maintained By:** Zoltán & Claude  
**Critical Focus:** Artifacts enforcement (Rules #7 and #20)