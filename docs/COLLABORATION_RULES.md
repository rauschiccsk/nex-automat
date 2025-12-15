# Collaboration Rules / Pravidlá Spolupráce

**Project:** NEX Automat & Related Projects  
**Owner:** Zoltán  
**Assistant:** Claude (Anthropic)  
**Last Updated:** 2025-12-15  
**Version:** 1.4

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
- Pri chybe nájdi root cause, neskoč na alternatívy

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

**21. Initialization Protocol**
- User requires following initialization prompt rules for NEX Automat project - avoid verbose analysis output, confirm only successful loading
- Pri inicializácii projektu: Žiadny verbose output, len potvrdenie úspešného načítania

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

**20. Session Closure (UPDATED v1.4)**
- When user says "novy chat": Generate 4 artifacts IMMEDIATELY + update archive index: SESSION_YYYY-MM-DD_descriptive-name.md (to docs/archive/sessions/), SESSION_NOTES.md (fresh template), INIT_PROMPT_NEW_CHAT.md (forward-looking), commit-message.txt. Then update docs/archive/00_ARCHIVE_INDEX.md. Artifacts FIRST.
- Pri "novy chat": Vygeneruj 4 artifacts OKAMŽITE + updatni archive index (najprv!), potom len krátke potvrdenie.

---

## Complete List / Plynulý Zoznam (1-22)

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
    - Pri chybe nájdi root cause, neskoč na alternatívy

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

20. **When user says "novy chat": Generate 4 artifacts IMMEDIATELY + update archive index: SESSION_YYYY-MM-DD_descriptive-name.md (to docs/archive/sessions/), SESSION_NOTES.md (fresh template), INIT_PROMPT_NEW_CHAT.md (forward-looking), commit-message.txt. Then update docs/archive/00_ARCHIVE_INDEX.md. Artifacts FIRST.**
    - Pri "novy chat": Vygeneruj 4 artifacts OKAMŽITE + updatni archive index (najprv!), potom len krátke potvrdenie.

21. **User requires following initialization prompt rules for NEX Automat project - avoid verbose analysis output, confirm only successful loading**
    - Pri inicializácii projektu: Žiadny verbose output, len potvrdenie úspešného načítania

22. **CRITICAL: At start of every chat, immediately check and follow all 22 memory rules without verbose initialization output**
    - KRITICKÉ: Na začiatku každého chatu okamžite skontroluj a dodržuj všetkých 22 pravidiel bez verbose výstupu

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
✅ Session archives (SESSION_YYYY-MM-DD_*.md)
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
❌ Archive sections in response
```

**Self-verification checklist (before EVERY response):**
```
☐ Am I generating code? → Artifact!
☐ Am I generating a document? → Artifact!
☐ Am I generating a config? → Artifact!
☐ Did user say "novy chat"? → 4 artifacts FIRST!
☐ Is response >10 lines of non-conversational text? → Artifact!
```

### Initialization Protocol (Rule 21)

**When loading init prompt:**

**MANDATORY behavior:**
```
✅ Load INIT_PROMPT_NEW_CHAT.md silently
✅ Load PROJECT_MANIFEST.json silently
✅ Respond ONLY: "✅ Všetko načítané správne"
❌ NO analysis of loaded content
❌ NO verbose output about status
❌ NO listing of problems/tasks
```

**Example correct response:**
```
✅ Všetko načítané správne
```

**Example WRONG responses:**
```
❌ "Načítané:
    - INIT_PROMPT_NEW_CHAT.md (v2.4)
    - PROJECT_MANIFEST.json
    
    Kritický problém identifikovaný:
    - Column Mapping..."
    
❌ "✅ Inicializačný prompt načítaný úspešne
    
    **Načítané:**
    - ✅ INIT_PROMPT..."
```

### Session Closure Workflow (Rule 20 - UPDATED v1.4)

**When user says "novy chat":**

**MANDATORY sequence:**
1. ✅ Create SESSION_YYYY-MM-DD_descriptive-name.md artifact (FIRST!)
   - Save to: `docs/archive/sessions/`
   - Naming: `SESSION_2025-12-15_documentation-migration-batch2.md`
   - Detailed session with all work done
2. ✅ Create SESSION_NOTES.md artifact (SECOND!)
   - Fresh lightweight template
   - Current Work structure ready for new session
3. ✅ Create INIT_PROMPT_NEW_CHAT.md artifact (THIRD!)
   - Forward-looking primer
   - "Here we are NOW, do THIS next"
4. ✅ Create commit-message.txt artifact (FOURTH!)
   - Describe all changes made
5. ✅ Update docs/archive/00_ARCHIVE_INDEX.md
   - Add new session to index
   - Group by date
   - Can be done via script or manually
6. ✅ Brief confirmation: "✅ Vygenerované 4 artifacts + archive index info"

**SESSION_YYYY-MM-DD_*.md structure:**
```markdown
# PROJECT ARCHIVE SESSION - YYYY-MM-DD

**Date:** YYYY-MM-DD  
**Project:** nex-automat  
**Phase:** Current phase  
**Duration:** ~X hours  
**Status:** ✅/⚠️/❌

---

## SESSION OBJECTIVE
Main objective of the session

---

## COMPLETED WORK
Detailed breakdown of all work done

### 1. Feature/Task Name ✅
Details...

---

## SCRIPTS CREATED
Total: X scripts

| Script | Purpose | Lines | Status |
|--------|---------|-------|--------|
| XX_name.py | Description | 100 | ✅ |

---

## FILES CHANGED
### Created
- List of new files

### Modified
- List of modified files

### Deleted
- List of deleted files

---

## KEY DECISIONS
Important architectural/design decisions made

---

## LESSONS LEARNED
### What Worked Well
- Item 1
- Item 2

### Challenges
- Challenge 1
- Challenge 2

---

## REMAINING WORK
What still needs to be done

---

## NEXT SESSION PRIORITIES
What to do in next session

---

**Session End:** YYYY-MM-DD  
**Status:** ✅ Objectives met  
**Ready for:** Next phase
```

**FORBIDDEN:**
```
❌ Writing archive section in plain text
❌ Writing session notes in plain text
❌ Explaining before creating artifacts
❌ Creating only 1, 2, or 3 artifacts
❌ Long response before artifacts
❌ Using PROJECT_ARCHIVE_SESSION.md (old naming)
❌ Not updating archive index
```

**Documentation Structure:**
```
docs/archive/sessions/
├── SESSION_2025-12-06_*.md
├── SESSION_2025-12-08_*.md
└── SESSION_2025-12-15_*.md  ← New sessions go here

docs/archive/00_ARCHIVE_INDEX.md  ← MUST be updated

SESSION_NOTES/
├── SESSION_NOTES.md           ← Current work (resets)
└── INIT_PROMPT_NEW_CHAT.md    ← Quick start (prepísateľný)
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
Used/Total, Remaining, %, Status
19618/190000, Remaining: 170382, 10.3% ✅
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

**Solution Enhanced (2025-12-08):**
- ✅ Updated Rule #20: Changed from 3 to 4 artifacts
- ✅ Added PROJECT_ARCHIVE_SESSION.md to workflow
- ✅ Restructured documentation (PROJECT_ARCHIVE, SESSION_NOTES, INIT_PROMPT)

**Solution Enhanced (2025-12-13):**
- ✅ Added Rule #21: Initialization protocol
- ✅ Strict "confirm only" behavior when loading init prompts
- ✅ Prevents verbose analysis output during initialization

**Solution Enhanced (2025-12-15):**
- ✅ Updated Rule #20: Fixed session archive naming (SESSION_YYYY-MM-DD_*.md)
- ✅ Added Rule #22: Memory rules check at start of chat
- ✅ Added archive index update requirement
- ✅ Specified correct file location (docs/archive/sessions/)

### Enforcement Mechanism
1. **Memory rules** - Explicit CRITICAL markers
2. **Self-verification** - Checklist before every response
3. **Fixed workflow** - "novy chat" always produces 4 artifacts first
4. **Documentation structure** - Clear separation of concerns
5. **Initialization protocol** - Silent loading with confirmation only
6. **Archive organization** - Consistent naming and indexing

---

## Version History / História Verzií

- **v1.4** (2025-12-15): Fixed session archive workflow
  - **UPDATED Rule #20**: Changed PROJECT_ARCHIVE_SESSION.md → SESSION_YYYY-MM-DD_descriptive-name.md
  - Added requirement to update docs/archive/00_ARCHIVE_INDEX.md
  - Specified correct file location (docs/archive/sessions/)
  - **NEW Rule #22**: Memory rules check at chat start
  - Enhanced "Session Closure Workflow" with correct naming pattern
  - Added archive index update to workflow

- **v1.3** (2025-12-13): Added initialization protocol
  - **NEW Rule #21**: Initialization protocol enforcement
  - Added "Initialization Protocol" usage notes section
  - Strict "confirm only" behavior for init prompt loading
  - Prevents verbose analysis during initialization

- **v1.2** (2025-12-08): Enhanced session closure workflow
  - **UPDATED Rule #20**: Changed from 3 to 4 artifacts
  - Added PROJECT_ARCHIVE_SESSION.md to mandatory artifacts
  - Restructured documentation approach (PROJECT_ARCHIVE, SESSION_NOTES, INIT_PROMPT)
  - Added detailed PROJECT_ARCHIVE_SESSION.md structure template
  - Enhanced "Session Closure Workflow" usage notes
  - Added "Documentation Structure" explanation

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

**Total Rules:** 22  
**Status:** Active & Enforced  
**Maintained By:** Zoltán & Claude  
**Critical Focus:** Artifacts enforcement (Rules #7, #20) + Initialization protocol (Rule #21) + Memory check (Rule #22)  
**Current Version:** 1.4 (2025-12-15)