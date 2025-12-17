# Collaboration Rules / Pravidlá Spolupráce

**Project:** NEX Automat & Related Projects  
**Owner:** Zoltán  
**Assistant:** Claude (Anthropic)  
**Last Updated:** 2025-12-17  
**Version:** 1.6

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

**20. Session Closure (UPDATED v1.6)**
- When user says "novy chat": Generate 2 artifacts - new_chat.py script (creates SESSION_*.md, updates 00_ARCHIVE_INDEX.md, creates INIT_PROMPT_NEW_CHAT.md, runs generate_projects_access.py + rag_reindex.py --new) + commit-message.txt
- Pri "novy chat": Vygeneruj 2 artifacts - new_chat.py script + commit-message.txt

---

### 🔍 RAG System / RAG Systém (NEW v1.6)

**23. RAG Maintenance**
- After adding new docs run "python tools/rag/rag_reindex.py --new". Full reindex weekly with --all. Check stats with --stats
- Po pridaní nových docs spusti reindex. Týždenne full reindex.

**24. RAG Access Protocol**
- RAG Access: When RAG is needed, directly ask for RAG Permission URL - don't try fetch first
- Keď potrebuješ RAG, priamo požiadaj o RAG Permission URL - neskúšaj fetch najprv

---

### ✅ Memory Check / Kontrola Memory

**22. Memory Rules Check**
- CRITICAL: At start of every chat, check and follow all memory rules without verbose output
- KRITICKÉ: Na začiatku každého chatu skontroluj a dodržuj všetky pravidlá bez verbose výstupu

---

## Complete List / Plynulý Zoznam (1-24)

1. **Provide single recommended solution only, no alternatives unless requested**
2. **Present one step at a time, wait for confirmation before next step**
3. **End each response with token usage stats: Used/Total, Remaining, %, Status indicator**
4. **NEVER start work if GitHub files fail to load - inform user and stop immediately**
5. **Communicate in Slovak language. For project names use exact terminology**
6. **When loading session notes, immediately identify Current Status and Next Steps sections**
7. **CRITICAL: ALL code/configs/documents/scripts MUST be artifacts**
8. **Claude works step-by-step, waits for confirmation before proceeding**
9. **Claude provides only ONE best solution**
10. **When error occurs, Claude finds and fixes root cause systematically**
11. **Claude prioritizes quality and professional solutions over speed**
12. **All project changes done via scripts**
13. **No need to write commit and push descriptions**
14. **No need to write manifest generation instructions**
15. **All fixes done via .py scripts only**
16. **All fixes via Development → Git → Deployment workflow**
17. **In docs use standard Markdown tables only**
18. **CRITICAL: nex-shared package uses FLAT structure**
19. **Session scripts numbered from 01 sequentially**
20. **"novy chat": 2 artifacts - new_chat.py + commit-message.txt**
21. **Initialization protocol - avoid verbose output, confirm only**
22. **CRITICAL: At start of every chat, check all memory rules**
23. **RAG maintenance: reindex after new docs, weekly full reindex**
24. **RAG Access: directly ask for Permission URL, don't try fetch first**

---

## Usage Notes / Poznámky k Použitiu

### RAG Access Protocol (Rule 24 - NEW)

**When Claude needs RAG information:**
```
✅ CORRECT: "Potrebujem RAG Permission URL: https://rag-api.icc.sk/search?query=..."
❌ WRONG: Try fetch first → FAIL → then ask for URL
```

**Workflow:**
1. User asks question requiring RAG
2. Claude immediately provides URL for approval
3. User pastes URL into chat
4. Claude fetches and responds

**Benefits:**
- Saves one round-trip
- No unnecessary error messages
- Cleaner conversation flow

### Artifacts Enforcement (Rule 7 - CRITICAL)

**ALWAYS create artifacts for:**
```
✅ Python files (.py)
✅ Config files (.json, .yaml, .py, .txt, .ini, .toml)
✅ Init prompts (INIT_PROMPT_NEW_CHAT.md)
✅ Commit messages (commit-message.txt)
✅ Session archives (SESSION_YYYY-MM-DD_*.md)
✅ Documents longer than 10 lines
✅ Code examples longer than 5 lines
✅ Any script or configuration
```

### Initialization Protocol (Rule 21)

**When loading init prompt:**
```
✅ Load INIT_PROMPT_NEW_CHAT.md silently
✅ Load PROJECT_MANIFEST.json silently
✅ Respond ONLY: "✅ Všetko načítané správne"
❌ NO analysis of loaded content
❌ NO verbose output about status
```

### Session Closure Workflow (Rule 20 - UPDATED v1.6)

**When user says "novy chat" - generate 2 artifacts:**

**Artifact 1: `new_chat.py`** - Script that does everything:
```python
# Script performs:
1. Creates docs/archive/sessions/SESSION_YYYY-MM-DD_name.md
2. Updates docs/archive/00_ARCHIVE_INDEX.md
3. Creates init_chat/INIT_PROMPT_NEW_CHAT.md
4. Runs: python tools/generate_projects_access.py
5. Runs: python tools/rag/rag_reindex.py --new
```

**Artifact 2: `commit-message.txt`** - As before

**User workflow:**
```powershell
python new_chat.py
# Review generated files
git add . && git commit -F commit-message.txt
```

**Benefits:**
- 2 artifacts instead of 3+
- Full automation with one command
- Consistent file generation

---

## Version History / História Verzií

- **v1.6** (2025-12-17): Added RAG system rules + automated session closure
  - **NEW Rule #23**: RAG maintenance protocol
  - **NEW Rule #24**: RAG Access - ask for Permission URL directly
  - **UPDATED Rule #20**: Changed to 2 artifacts (new_chat.py + commit-message.txt)
    - new_chat.py automates: SESSION_*.md, ARCHIVE_INDEX, INIT_PROMPT, scripts
  - Added "RAG System" section to structured rules
  - Added "RAG Access Protocol" usage notes
  - Total rules: 24

- **v1.5** (2025-12-15): Removed SESSION_NOTES.md (redundant)
  - **UPDATED Rule #20**: Changed from 4 to 3 artifacts
  - SESSION_NOTES.md is NO LONGER CREATED

- **v1.4** (2025-12-15): Fixed session archive workflow
  - **UPDATED Rule #20**: Changed PROJECT_ARCHIVE_SESSION.md → SESSION_YYYY-MM-DD_descriptive-name.md
  - **NEW Rule #22**: Memory rules check at chat start

- **v1.3** (2025-12-13): Added initialization protocol
  - **NEW Rule #21**: Initialization protocol enforcement

- **v1.2** (2025-12-08): Enhanced session closure workflow
  - **UPDATED Rule #20**: Changed from 3 to 4 artifacts

- **v1.1** (2025-12-06): Enhanced artifacts enforcement
  - **UPDATED Rule #7**: Added CRITICAL marker

- **v1.0** (2025-12-05): Initial version with 20 rules

---

**Total Rules:** 24  
**Status:** Active & Enforced  
**Maintained By:** Zoltán & Claude  
**Critical Focus:** Artifacts (#7, #20) + Initialization (#21) + Memory (#22) + RAG (#23, #24)  
**Current Version:** 1.6 (2025-12-17)