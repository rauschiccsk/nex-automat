# INIT PROMPT - Nový chat (nex-automat)

## KONTEXT Z PREDCHÁDZAJÚCEHO CHATU

Úspešne sme implementovali Claude Tools pre nex-automat projekt - automatizáciu workflow pre prácu s claude.ai.

---

## AKTUÁLNY STAV PROJEKTU

**Projekt:** NEX Automat v2.0  
**Development:** `C:\Development\nex-automat\`  
**Deployment:** `C:\Development\nex-automat-deployment\`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop

---

## CLAUDE TOOLS - IMPLEMENTOVANÝ SYSTÉM

### Komponenty (všetky funkčné ✅)

**1. Artifact Server** (FastAPI)
- Beží na `http://localhost:8765`
- Ukladá artifacts z claude.ai do projektu
- Endpoints: `/`, `/save-artifact`, `/list-recent`, `/ping`

**2. Hotkeys System** (keyboard + pyperclip)
- Globálne klávesové skratky (fungujú všade)
- Všetky hotkeys testované a funkčné

**3. Chat Loader**
- Automatické načítanie init promptu do nového chatu
- Hotkey: `Ctrl+Alt+L`

**4. Session Notes Manager**
- Správa a analýza session notes
- Príkazy: `enhance`, `validate`, `template`

**5. Context Compressor** (voliteľné)
- Kompresia histórie pomocou Claude API
- Vyžaduje: ANTHROPIC_API_KEY v config.py

**6. Browser Extension** (voliteľné, nie testované)
- Automatické ukladanie artifacts
- Chrome extension pre claude.ai

### Adresárová štruktúra
```
C:\Development\nex-automat\
├── tools\                      ← Claude Tools
│   ├── installer.py
│   ├── claude-chat-loader.py
│   ├── claude-hotkeys.py
│   ├── artifact-server.py
│   ├── session-notes-manager.py
│   ├── context-compressor.py
│   ├── config.py               ← Autogenerovaný
│   ├── start-claude-tools.ps1
│   ├── stop-claude-tools.ps1
│   └── browser-extension\
├── docs\                       ← Dokumentácia
│   ├── SESSION_NOTES.md        ← Tu je session notes
│   └── INIT_PROMPT_NEW_CHAT.md ← Tu je init prompt
├── scripts\                    ← Setup scripty
│   ├── 01-create-directories.py
│   ├── 02-create-claude-tools-files.py
│   ├── 05-fix-config.py
│   └── 05b-fix-powershell-files.py
└── README.md
```

### Konfigurácia
```python
# tools/config.py
PROJECT_ROOT = r"C:\Development\nex-automat"
TOOLS_DIR = r"C:\Development\nex-automat\tools"
SESSION_NOTES_DIR = r"C:\Development\nex-automat\SESSION_NOTES"

ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"
ANTHROPIC_API_KEY = ""  # Voliteľné
```

---

## DOSTUPNÉ HOTKEYS (Ctrl+Alt+...)

| Hotkey | Funkcia | Status |
|--------|---------|--------|
| **L** | Load init prompt | ⏳ Nie testované |
| **S** | Copy session notes | ⏳ Nie testované |
| **G** | Git status | ⏳ Nie testované |
| **D** | Deployment info | ⏳ Nie testované |
| **N** | New chat template | ⏳ Nie testované |
| **I** | Show project info | ✅ Funguje |

---

## SPUSTENIE / ZASTAVENIE

### Spustenie nástrojov
```powershell
cd C:\Development\nex-automat\tools
.\start-claude-tools.ps1
```
**Výsledok:**
- Artifact Server: PID zobrazený, beží na :8765
- Hotkeys: PID zobrazený, bežia na pozadí

### Zastavenie nástrojov
```powershell
cd C:\Development\nex-automat\tools
.\stop-claude-tools.ps1
```
**Alebo s force:**
```powershell
.\stop-claude-tools.ps1 -Force
```

### Test hotkeys (interaktívne okno)
```powershell
python tools\claude-hotkeys.py
# Stlač Ctrl+Alt+I → zobrazí Project Info
# Ctrl+C → ukončenie
```

---

## ČO OSTÁVA UROBIŤ

### Priorita 1 (ihneď)
- [ ] **Otestovať všetky hotkeys** - zatiaľ len Ctrl+Alt+I
  - Ctrl+Alt+S → Copy session notes
  - Ctrl+Alt+G → Git status
  - Ctrl+Alt+D → Deployment info
  - Ctrl+Alt+L → Load init prompt
  - Ctrl+Alt+N → New chat template

- [ ] **Git commit** - commitnúť všetky tools súbory
  - Použiť commit message z artifacts
  - Vymazať dočasné scripty (01, 02, 05, 05b)

### Priorita 2 (tento týždeň)
- [ ] **Browser Extension** - nainštalovať a otestovať
  - Chrome → Extensions → Load unpacked
  - Test: vytvor artifact → klik "💾 Uložiť"

- [ ] **Praktické použitie** v reálnej práci
  - Workflow: Nový chat → Ctrl+Alt+L → práca → "novy chat"
  - Zaznamenať problémy/vylepšenia

### Priorita 3 (budúcnosť)
- [ ] **Context Compressor setup** - nastaviť API key
- [ ] **Nazbierať skúsenosti** - 2-3 týždne používania
- [ ] **Template systém** - až keď bude všetko vyladené
- [ ] **Rozšírenie na ďalšie projekty**

---

## VYRIEŠENÉ PROBLÉMY

### Bug #1: Config.py escape sequences ✅
**Problém:** SyntaxError - neukončený string  
**Riešenie:** Oprava cez `05-fix-config.py` - správne raw strings

### Bug #2: PowerShell encoding ✅
**Problém:** Parse errors kvôli špeciálnym znakom  
**Riešenie:** Oprava cez `05b-fix-powershell-files.py` - odstránená diakritika

### Bug #3: uvicorn[standard] dependency ✅
**Problém:** Inštalácia zlyhávala  
**Riešenie:** Zmenené na len `uvicorn` (bez extras)

### Warning: Pydantic validator deprecation ⚠️
**Status:** Len warning, neovplyvňuje funkcionalitu  
**Fix:** Možno opraviť neskôr na `@field_validator`

---

## WORKFLOW

### Development → Git → Deployment
```
Development (C:\Development\nex-automat\)
    ↓ zmeny v kóde
    ↓ test lokálne
Git commit & push
    ↓
Deployment (C:\Development\nex-automat-deployment\)
    ↓ git pull
    ↓ restart aplikácií
```

**NIKDY nerobiť zmeny priamo v Deployment!**

### Claude Tools workflow
```
1. Ráno: .\start-claude-tools.ps1
2. Práca: Používaj hotkeys (Ctrl+Alt+...)
3. Nový chat: Ctrl+Alt+L → vloží init prompt
4. Koniec práce: "novy chat" → vygeneruje SESSION_NOTES
5. Večer: .\stop-claude-tools.ps1
```

---

## TECHNICKÉ POZNÁMKY

### Windows Path Handling
```python
# ✅ SPRÁVNE - raw strings pre Windows cesty
PROJECT_ROOT = r"C:\Development\nex-automat"

# ✅ ALTERNATÍVA - forward slashes (fungujú v Pythone)
PROJECT_ROOT = Path("C:/Development/nex-automat")

# ❌ CHYBNÉ - zdvojené backslashes v f-string
f"""PROJECT_ROOT = r"C:\\\\Development" """  # SyntaxError!
```

### PowerShell Encoding
```powershell
# ❌ Problematické pre PowerShell parser
Write-Host "✅ Všetky úlohy dokončené"

# ✅ Bezpečné (bez diakritiky)
Write-Host "Vsetky ulohy dokoncene"
```

### Artifact Server Pattern
```python
# Minimálny server pre ukladanie artifacts
@app.post("/save-artifact")
async def save_artifact(data: ArtifactSave):
    file_path = PROJECT_ROOT / data.filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(data.content, encoding='utf-8')
    return {"path": str(file_path)}
```

---

## DEPENDENCIES

```
pyperclip     - Práca so schránkou
keyboard      - Globálne hotkeys  
anthropic     - Claude API (voliteľné)
fastapi       - Web framework
uvicorn       - ASGI server
pydantic      - Data validation
```

**Inštalácia:**
```bash
python tools/installer.py  # Nainštaluje všetko automaticky
```

---

## RESOURCES

### Dokumentácia
- `docs/README.md` - Kompletný prehľad
- `docs/INSTALLATION_GUIDE.md` - Quick start
- `docs/SESSION_NOTES.md` - Tento technický záznam

### Logs
- `tools/claude-tools.log` - Runtime log

### External
- FastAPI: https://fastapi.tiangolo.com/
- keyboard: https://github.com/boppreh/keyboard
- Anthropic: https://docs.anthropic.com/

---

## KRITICKÉ UPOZORNENIA

### ⚠️ API Key Security
```python
# ❌ NIKDY necommituj API key do Git
ANTHROPIC_API_KEY = "sk-ant-..."

# ✅ config.py je v .gitignore
# ✅ Alebo použi environment variable
```

### ⚠️ Port Conflicts
```bash
# Ak port 8765 je obsadený:
netstat -ano | findstr :8765
taskkill /F /PID <pid>

# Alebo zmeň v config.py:
ARTIFACT_SERVER_PORT = 8766
```

### ⚠️ Hotkeys Conflicts
```python
# Ak Ctrl+Alt+X koliduje s inou aplikáciou:
# Uprav hotkey v config.py
# Reštartuj claude-hotkeys.py
```

---

**Init Prompt vytvorený:** 2025-12-06  
**Projekt:** nex-automat  
**Status:** Claude Tools nainštalované a funkčné  

Pokračujem tam kde sme skončili v predchádzajúcom chate.