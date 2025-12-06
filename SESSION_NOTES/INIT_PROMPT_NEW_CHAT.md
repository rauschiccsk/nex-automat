# INIT PROMPT - Nový chat (nex-automat)

## KONTEXT Z PREDCHÁDZAJÚCEHO CHATU

Úspešne sme otestovali Claude Tools pre nex-automat projekt - 5 z 6 hotkeys funguje správne.

---

## AKTUÁLNY STAV PROJEKTU

**Projekt:** NEX Automat v2.0  
**Development:** `C:\Development\nex-automat\`  
**Deployment:** `C:\Development\nex-automat-deployment\`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop

---

## CLAUDE TOOLS - FUNKČNÝ SYSTÉM

### Komponenty (otestované)

**1. Artifact Server** (FastAPI)
- Beží na `http://localhost:8765`
- Ukladá artifacts z claude.ai do projektu
- Endpoints: `/`, `/save-artifact`, `/list-recent`, `/ping`
- Status: ✅ Funguje

**2. Hotkeys System** (keyboard + pyperclip)
- Globálne klávesové skratky
- **5 z 6 hotkeys funkčných**

**3. Chat Loader**
- Automatické načítanie init promptu do nového chatu
- Hotkey: `Ctrl+Win+P` ❌ (koliduje s Windows Project mode)
- Workaround: Manuálne skopírovať INIT_PROMPT_NEW_CHAT.md

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
├── SESSION_NOTES\              ← Dokumentácia
│   ├── SESSION_NOTES.md        ← Tu je session notes
│   └── INIT_PROMPT_NEW_CHAT.md ← Tu je init prompt
├── scripts\                    ← Fix scripty
│   ├── 06-fix-hotkey-L-to-P.py
│   ├── 07-fix-all-hotkeys-to-ctrl-shift.py
│   ├── 08-fix-hotkeys-to-ctrl-win.py
│   └── 09-fix-win-to-windows.py
└── README.md
```

### Konfigurácia

```python
# tools/config.py
PROJECT_ROOT = r"C:\Development\nex-automat"
TOOLS_DIR = r"/tools"
SESSION_NOTES_DIR = r"/SESSION_NOTES"

ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"
ANTHROPIC_API_KEY = ""  # Voliteľné
```

---

## DOSTUPNÉ HOTKEYS (Ctrl+Win+...)

| Hotkey | Funkcia | Status |
|--------|---------|--------|
| **I** | Show project info | ✅ Funguje |
| **S** | Copy session notes | ✅ Funguje |
| **G** | Git status | ✅ Funguje |
| **D** | Deployment info | ✅ Funguje |
| **N** | New chat template ("nový chat") | ✅ Funguje |
| **P** | Load init prompt | ❌ Koliduje s Windows |

**Poznámka:** `Ctrl+Win+P` koliduje s Windows Project mode (pripojenie projektora). Pre načítanie init promptu použiť manuálne kopírovanie.

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

**Známy problém:** Stop script niekedy nedetekuje procesy správne. Pre manuálne zastavenie:
```powershell
Get-WmiObject Win32_Process | Where-Object {$_.CommandLine -like "*artifact-server*" -or $_.CommandLine -like "*claude-hotkeys*"} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

### Test hotkeys (interaktívne okno)
```powershell
python tools\claude-hotkeys.py
# Stlač Ctrl+Win+I → zobrazí Project Info
# Ctrl+C → ukončenie
```

---

## ČO OSTÁVA UROBIŤ

### Priorita 1 (voliteľné)
- [ ] **Opraviť Ctrl+Win+P hotkey** - zmeniť na iné písmeno (L, O, alebo úplne iná kombinácia)
- [ ] **Git commit** - commitnúť všetky tools súbory a fix scripty
- [ ] **Vymazať dočasné scripty** - ponechať len potrebné

### Priorita 2 (tento týždeň/mesiac)
- [ ] **Browser Extension** - nainštalovať a otestovať
  - Chrome → Extensions → Load unpacked
  - Test: vytvor artifact → klik "💾 Uložiť"

- [ ] **Praktické používanie** v reálnej práci
  - Workflow: Nový chat → (manuálne načítaj prompt) → práca → "nový chat"
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

### Bug #4: Kolízia so slovenskou klávesnicou ✅
**Problém:** `Ctrl+Alt+...` = AltGr na SK klávesnici → generuje špeciálne znaky  
**Riešenie:** Zmena na `Ctrl+Win+...` cez fix scripty 06-09

### Bug #5: Kolízia s browser shortcuts ✅
**Problém:** `Ctrl+Shift+I` = DevTools, `Ctrl+Shift+N` = Incognito  
**Riešenie:** Zmena na `Ctrl+Win+...`

### Bug #6: Nesprávna syntax Windows key ✅
**Problém:** keyboard modul požaduje `'windows'` nie `'win'`  
**Riešenie:** Oprava cez `09-fix-win-to-windows.py`

### Bug #7: Windows Project mode ⚠️
**Problém:** `Ctrl+Win+P` koliduje s Windows (pripojenie projektora)  
**Riešenie:** Zatiaľ nevyriešené - použiť manuálne kopírovanie init promptu

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
2. Práca: Používaj hotkeys (Ctrl+Win+...)
3. Nový chat: Manuálne skopíruj init prompt (Ctrl+Win+P nefunguje)
4. Koniec práce: "nový chat" → vygeneruje SESSION_NOTES
5. Večer: .\stop-claude-tools.ps1
```

---

## TECHNICKÉ POZNÁMKY

### Hotkey kolízie - zhrnutie

| Kombinácia | Problém | Status |
|------------|---------|--------|
| `Ctrl+Alt+...` | AltGr na SK klávesnici | ❌ Nefunguje |
| `Ctrl+Shift+...` | Browser DevTools/Incognito | ❌ Koliduje |
| `Ctrl+Win+...` | Väčšinou OK | ✅ Funguje |
| `Ctrl+Win+P` | Windows Project mode | ❌ Koliduje |

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
- `SESSION_NOTES/README.md` - Kompletný prehľad
- `SESSION_NOTES/INSTALLATION_GUIDE.md` - Quick start
- `SESSION_NOTES/SESSION_NOTES.md` - Tento technický záznam

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

### ⚠️ N8n Workflow na pozadí
```powershell
# NIKDY nezabíjaj všetky Python procesy!
# Na serveri bežia n8n workflows (supplier-invoice-loader)

# ✅ Správne - kontroluj command line
Get-WmiObject Win32_Process | Where-Object {$_.CommandLine -like "*artifact-server*"}
```

---

**Init Prompt vytvorený:** 2025-12-06  
**Projekt:** nex-automat  
**Status:** Claude Tools funkčné (5/6 hotkeys OK)  

Pokračujem tam kde sme skončili v predchádzajúcom chate.