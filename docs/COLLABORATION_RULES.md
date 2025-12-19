# Collaboration Rules / Pravidlá Spolupráce

**Project:** NEX Automat & Related Projects  
**Owner:** Zoltán  
**Assistant:** Claude (Anthropic)  
**Last Updated:** 2025-12-19  
**Version:** 1.8

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

**7. Artifacts Usage (CRITICAL)**
- CRITICAL: ALL code/configs/documents/scripts MUST be artifacts. Triggers: Python files, any config, doc >10 lines, code >5 lines. ALWAYS artifacts FIRST, never plain text.
- KRITICKÉ: VŠETOK kód/configs/dokumenty/scripty MUSIA byť artifacts. VŽDY artifacts NAJPRV, nikdy plain text.

**15. Python Scripts Only**
- All fixes done via .py scripts only - never generate alternative .ps1 scripts
- Všetky opravy len .py, nikdy .ps1 alternatívy

**19. Script Numbering**
- Session scripts numbered from 01 sequentially. Only temporary scripts numbered, permanent scripts not.
- Session scripty od 01 plynule. Len dočasné číslované, trvalé nie.

**26. Subprocess in Scripts (CRITICAL - NEW v1.8)**
- In new_chat.py scripts, ALWAYS use sys.executable instead of "python" for subprocess calls to ensure correct venv is used
- V new_chat.py VŽDY použiť sys.executable namiesto "python" pre subprocess volania
- Toto zaručuje že subprocess používa rovnaký Python/venv ako hlavný script

---

### 📝 Documentation / Dokumentácia

**13. Git Operations**
- No need to write commit and push descriptions, user does Git operations himself
- Nepíš commit/push popisy, používateľ si to robí sám

**14. Manifest Generation**
- No need to write manifest generation instructions, user generates manifests himself
- Nepíš manifest inštrukcie, používateľ generuje sám

**20. Session Closure (UPDATED v1.8)**
- When user says "novy chat": new_chat.py creates SESSION_*.md (archive), KNOWLEDGE_*.md (docs/knowledge/ for RAG indexing), INIT_PROMPT_NEW_CHAT.md (root), then runs rag_update.py --new using sys.executable
- Pri "novy chat": new_chat.py vytvára SESSION (archív), KNOWLEDGE (docs/knowledge/ pre RAG), INIT_PROMPT (root), potom spúšťa rag_update cez sys.executable

---

### 🔍 RAG System / RAG Systém

**23. RAG Maintenance**
- RAG maintenance: "python tools/rag/rag_update.py --new" (daily, files modified today), --all (weekly full reindex), --stats (check stats)
- Po pridaní nových docs spusti --new. Týždenne full reindex s --all.

**24. RAG Access Protocol**
- RAG Workflow: Claude vypíše RAG URL, user vloží URL do chatu, Claude automaticky fetchne výsledky. NIKDY neskúšať fetch pred vložením URL userom.
- Claude poskytne URL, user vloží, Claude fetchne. Toto funguje - nemeňme to.

**25. PostgreSQL Password**
- PostgreSQL password via POSTGRES_PASSWORD env variable, no config.yaml needed for DB password
- Heslo pre PostgreSQL cez environment variable, nie v config súboroch

---

### ✅ Memory Check / Kontrola Memory

**22. Memory Rules Check**
- CRITICAL: At start of every chat, check and follow all memory rules without verbose output
- KRITICKÉ: Na začiatku každého chatu skontroluj a dodržuj všetky pravidlá bez verbose výstupu

---

## Complete List / Plynulý Zoznam (1-26)

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
20. **"novy chat": new_chat.py creates SESSION, KNOWLEDGE (for RAG), INIT_PROMPT, uses sys.executable**
21. **Initialization protocol - avoid verbose output, confirm only**
22. **CRITICAL: At start of every chat, check all memory rules**
23. **RAG maintenance: rag_update.py --new (daily), --all (weekly)**
24. **RAG Workflow: Claude provides URL, user pastes, Claude fetches**
25. **PostgreSQL password via POSTGRES_PASSWORD env variable**
26. **CRITICAL: In new_chat.py ALWAYS use sys.executable for subprocess calls**

---

## Usage Notes / Poznámky k Použitiu

### Session Closure Workflow (Rule 20, 26 - UPDATED v1.8)

**When user says "novy chat":**

`new_chat.py` script automaticky vytvára:
1. `docs/archive/sessions/SESSION_YYYY-MM-DD_name.md` - archív session
2. `docs/knowledge/KNOWLEDGE_YYYY-MM-DD_topic.md` - knowledge pre RAG
3. `INIT_PROMPT_NEW_CHAT.md` - v ROOT projektu
4. Spúšťa `rag_update.py --new` cez **sys.executable** - indexuje nový knowledge dokument

**KRITICKÉ pre new_chat.py:**
```python
import subprocess
import sys  # POVINNÉ!

# SPRÁVNE - použiť sys.executable
subprocess.run([sys.executable, "tools/rag/rag_update.py", "--new"], ...)

# NESPRÁVNE - nikdy nepoužívať "python" string
subprocess.run(["python", "tools/rag/rag_update.py", "--new"], ...)  # ❌ ZAKÁZANÉ
```

**User workflow:**
```powershell
python new_chat.py
# Všetko sa vytvorí automaticky + RAG reindex
git add . && git commit -m "session: description"
```

**Výhody:**
- Knowledge dokument ide do RAG pre budúce vyhľadávanie
- SESSION zostáva v archíve (nie v RAG)
- INIT_PROMPT pripravený pre nový chat
- sys.executable zaručuje správny Python/venv

### RAG Access Protocol (Rule 24)

**Workflow:**
1. User asks question requiring RAG
2. Claude immediately provides URL for approval
3. User pastes URL into chat
4. Claude fetches and responds

**Example:**
```
Claude: Potrebujem RAG, vlož túto URL:
https://rag-api.icc.sk/search?query=NEX%20Brain&limit=5

User: [pastes URL]

Claude: [fetches and responds]
```

### Artifacts Enforcement (Rule 7 - CRITICAL)

**ALWAYS create artifacts for:**
- Python files (.py)
- Config files (.json, .yaml, .py, .txt, .ini, .toml)
- Init prompts (INIT_PROMPT_NEW_CHAT.md)
- Session archives (SESSION_YYYY-MM-DD_*.md)
- Knowledge documents (KNOWLEDGE_YYYY-MM-DD_*.md)
- Documents longer than 10 lines
- Code examples longer than 5 lines

---

## Version History / História Verzií

- **v1.8** (2025-12-19): sys.executable fix for subprocess
  - **NEW Rule #26**: In new_chat.py ALWAYS use sys.executable for subprocess calls
  - **UPDATED Rule #20**: Added sys.executable requirement
  - Fixes "ModuleNotFoundError: No module named 'yaml'" error in subprocess
  - Total rules: 26

- **v1.7** (2025-12-19): Knowledge document in session closure
  - **UPDATED Rule #20**: new_chat.py now creates KNOWLEDGE_*.md for RAG indexing
  - **NEW Rule #25**: PostgreSQL password via env variable
  - Session closure creates: SESSION (archive) + KNOWLEDGE (RAG) + INIT_PROMPT

- **v1.6** (2025-12-17): Added RAG system rules + automated session closure
  - **NEW Rule #23**: RAG maintenance protocol
  - **NEW Rule #24**: RAG Access - ask for Permission URL directly
  - **UPDATED Rule #20**: Changed to automated new_chat.py

- **v1.5** (2025-12-15): Removed SESSION_NOTES.md (redundant)

- **v1.4** (2025-12-15): Fixed session archive workflow

- **v1.3** (2025-12-13): Added initialization protocol

- **v1.2** (2025-12-08): Enhanced session closure workflow

- **v1.1** (2025-12-06): Enhanced artifacts enforcement

- **v1.0** (2025-12-05): Initial version with 20 rules

---

**Total Rules:** 26  
**Status:** Active & Enforced  
**Maintained By:** Zoltán & Claude  
**Critical Focus:** Artifacts (#7) + Session Closure (#20) + Memory (#22) + RAG (#23, #24) + sys.executable (#26)  
**Current Version:** 1.8 (2025-12-19)