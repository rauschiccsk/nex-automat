# Session Notes - Claude Tools Implementation & Testing

**Dátum:** 2025-12-06  
**Projekt:** NEX Automat v2.0 - Claude Tools  
**Téma:** Implementácia a testovanie automatizácie workflow pre prácu s claude.ai

---

## Dosiahnuté výsledky

### ✅ Kompletná inštalácia Claude Tools
**Cieľ:** Vytvoriť automatizovaný systém pre efektívnejšiu prácu s claude.ai bez potreby vlastného API chatu.

**Implementované komponenty:**
1. **Artifact Server** (FastAPI) - Lokálny server pre ukladanie artifacts z claude.ai
2. **Hotkeys System** (keyboard) - Klávesové skratky pre časté operácie
3. **Chat Loader** - Automatické načítanie init promptu do nového chatu
4. **Session Notes Manager** - Správa a analýza session notes
5. **Context Compressor** - Kompresia histórie pomocou Claude API (voliteľné)
6. **Browser Extension** - Automatické ukladanie artifacts (voliteľné)

### ✅ Úspešné testovanie hotkeys (Session 2)
**Otestované hotkeys:**
- `Ctrl+Win+I` - Project Info ✅ Funguje perfektne
- `Ctrl+Win+S` - Session Notes (538 riadkov) ✅ Funguje perfektne  
- `Ctrl+Win+G` - Git Status ✅ Funguje perfektne
- `Ctrl+Win+D` - Deployment Info ✅ Funguje perfektne
- `Ctrl+Win+N` - New Chat Template ("nový chat") ✅ Funguje perfektne
- `Ctrl+Win+P` - Load Init Prompt ❌ Koliduje s Windows Project mode

**Výsledok:** 5 z 6 hotkeys funkčných, čo je dostatočné pre praktické použitie.

### ✅ Adresárová štruktúra
**Vytvorené adresáre:**
```
C:\Development\nex-automat\
├── tools\
│   ├── installer.py
│   ├── claude-chat-loader.py
│   ├── claude-hotkeys.py
│   ├── artifact-server.py
│   ├── session-notes-manager.py
│   ├── context-compressor.py
│   ├── config.py (autogenerovaný)
│   ├── start-claude-tools.ps1
│   ├── stop-claude-tools.ps1
│   ├── INSTALLATION_GUIDE.md
│   ├── claude-tools.log (runtime)
│   └── browser-extension\
│       └── claude-artifact-saver\
│           ├── manifest.json
│           ├── content.js
│           ├── styles.css
│           ├── background.js
│           └── popup.html
├── SESSION_NOTES\
│   ├── SESSION_NOTES.md
│   └── INIT_PROMPT_NEW_CHAT.md
├── scripts\
│   ├── 01-create-directories.py
│   ├── 02-create-claude-tools-files.py
│   ├── 05-fix-config.py
│   ├── 05b-fix-powershell-files.py
│   ├── 06-fix-hotkey-L-to-P.py
│   ├── 07-fix-all-hotkeys-to-ctrl-shift.py
│   ├── 08-fix-hotkeys-to-ctrl-win.py
│   └── 09-fix-win-to-windows.py
└── README.md
```

### ✅ Python Dependencies
**Nainštalované packages:**
- `pyperclip` - Práca so schránkou
- `keyboard` - Globálne hotkeys
- `anthropic` - Claude API (pre context compressor)
- `fastapi` - Web framework pre artifact server
- `uvicorn` - ASGI server
- `pydantic` - Data validation

---

## Technické problémy a riešenia

### Session 1: Implementácia

#### Bug #1: Config.py Escape Sequences ✅
**Problém:** SyntaxError v config.py - neukončený string literal na riadku 4
```python
# CHYBNÉ:
config_content = f"""...
PROJECT_ROOT = r"C:\\\\Development\\\\nex-automat"  # príliš veľa backslashes
"""

# ERROR:
SyntaxError: unterminated string literal (detected at line 4)
```

**Príčina:** Zdvojené escape sequences v f-string → string sa nekončil správne

**Riešenie:**
```python
# SPRÁVNE:
config_content = '''...
PROJECT_ROOT = r"C:\\Development\\nex-automat"  # raw string, len jeden backslash
'''
```

**Oprava:** Script `05-fix-config.py` prepíše config.py správnym obsahom

#### Bug #2: PowerShell Encoding Issues ✅
**Problém:** Parse errors v stop-claude-tools.ps1
```
At C:\Development\nex-automat\tools\stop-claude-tools.ps1:116 char:60
The string is missing the terminator: ".
```

**Príčina:** UTF-8 encoding s BOM + špeciálne znaky (slovenčina) → PowerShell parser error

**Riešenie:**
```powershell
# Odstránené špeciálne znaky:
# PRED: "✅ Všetky Claude Tools procesy zastavené"
# PO:   "Vsetky Claude Tools procesy zastavene"
```

**Oprava:** Script `05b-fix-powershell-files.py` prepíše oba .ps1 súbory

#### Bug #3: uvicorn[standard] Dependency ✅
**Problém:** Installer zlyhával pri inštalácii `uvicorn[standard]`
```
Inštalujem uvicorn[standard]...
❌ uvicorn[standard] - chyba inštalácie
```

**Príčina:** PowerShell interpretuje `[` `]` ako špeciálne znaky

**Riešenie:**
```python
# PRED:
packages = ["uvicorn[standard]"]

# PO:
packages = ["uvicorn"]  # standard extras nie sú kritické
```

---

### Session 2: Testovanie a opravy hotkey kolízií

#### Bug #4: Kolízia so slovenskou klávesnicou ✅
**Problém:** `Ctrl+Alt+L` generoval špeciálny znak `Ł` namiesto triggerovania hotkey
```
Pôvodný hotkey: Ctrl+Alt+L (Load Init Prompt)
Výsledok: Vložil sa znak "Ł" do chatu
```

**Príčina:** Na SK/CZ klávesnici `Ctrl+Alt` = `AltGr` (generuje diakritiku a špeciálne znaky)

**Riešenie #1:** Zmena z `Ctrl+Alt+L` na `Ctrl+Alt+P`
- Script: `06-fix-hotkey-L-to-P.py`
- Výsledok: Stále nefunguje - `Ctrl+Alt+P` generuje znak `'`

**Riešenie #2:** Zmena z `Ctrl+Alt+...` na `Ctrl+Shift+...`
- Script: `07-fix-all-hotkeys-to-ctrl-shift.py`
- Výsledok: Stále nefunguje - koliduje s browser shortcuts

#### Bug #5: Kolízia s browser shortcuts ✅
**Problém:** `Ctrl+Shift+I` otvoril DevTools namiesto triggerovania hotkey
```
Ctrl+Shift+I → Browser DevTools (F12)
Ctrl+Shift+N → Incognito window
```

**Príčina:** Browser má prioritu nad globálnymi hotkeys pre `Ctrl+Shift+...` kombinácie

**Riešenie:** Zmena z `Ctrl+Shift+...` na `Ctrl+Win+...`
- Script: `08-fix-hotkeys-to-ctrl-win.py`
- Výsledok: Stále nefunguje - nesprávna syntax

#### Bug #6: Nesprávna syntax Windows key ✅
**Problém:** Hotkeys nereagovali po zmene na `Ctrl+Win+...`
```python
# CHYBNÉ - keyboard modul nepozná 'win'
keyboard.add_hotkey('ctrl+win+i', func)
```

**Príčina:** keyboard modul požaduje `'windows'` nie `'win'`

**Riešenie:**
```python
# SPRÁVNE - keyboard modul syntax
keyboard.add_hotkey('ctrl+windows+i', func)
```

**Oprava:** Script `09-fix-win-to-windows.py`
- Zmení `'ctrl+win+'` na `'ctrl+windows+'` v claude-hotkeys.py
- Výsledok: ✅ Všetky hotkeys fungujú!

#### Bug #7: Windows Project mode kolízia ⚠️
**Problém:** `Ctrl+Win+P` otvoril Windows Project mode namiesto načítania init promptu
```
Ctrl+Win+P → Windows "Premietať" menu (pripojenie projektora/displeja)
```

**Príčina:** Windows používa `Win+P` pre Project mode, kombinácia `Ctrl+Win+P` tiež koliduje

**Riešenie:** Zatiaľ nevyriešené
- Možnosti: Zmeniť na iné písmeno (L, O), alebo použiť manuálne kopírovanie
- Rozhodnutie: Ponechať ako je, 5/6 hotkeys stačí

---

## Workflow implementácie

### Session 1: Inštalácia

#### Krok 1: Vytvorenie adresárovej štruktúry
**Script:** `01-create-directories.py`
```python
# Vytvorené adresáre:
- C:\Development\nex-automat\tools\
- C:\Development\nex-automat\tools\browser-extension\claude-artifact-saver\
- C:\Development\nex-automat\SESSION_NOTES\
```
**Výsledok:** 3 nové adresáre, 2 už existovali

#### Krok 2: Vytvorenie placeholder súborov
**Script:** `02-create-claude-tools-files.py`
```python
# Vytvorených 15 súborov s placeholder obsahom:
- 6x Python (installer, chat-loader, hotkeys, server, manager, compressor)
- 2x PowerShell (start, stop)
- 5x Browser Extension (manifest, content, styles, background, popup)
- 2x Dokumentácia (README, INSTALLATION_GUIDE)
```
**Výsledok:** Všetky súbory vytvorené s "TODO: Skopíruj obsah z artifact"

#### Krok 3: Manuálne naplnenie obsahom
**Metóda:** Krok za krokom s potvrdením
```
Pre každý súbor:
1. Nájdi príslušný artifact v chate
2. Skopíruj celý obsah
3. Vlož do súboru
4. Ulož
5. Potvrdenie "hotovo" → ďalší súbor
```
**Výsledok:** 15 súborov naplnených, žiadne chýbajúce

#### Krok 4: Spustenie installera
**Príkaz:** `python tools/installer.py`
**Výsledok:**
- ✅ Python 3.13.7 detekované
- ✅ Dependencies nainštalované (okrem uvicorn[standard])
- ✅ config.py vytvorený
- ✅ SESSION_NOTES template vytvorený

#### Krok 5: Oprava config.py
**Script:** `05-fix-config.py`
**Výsledok:** Escape sequences opravené, raw strings správne naformátované

#### Krok 5b: Oprava PowerShell súborov
**Script:** `05b-fix-powershell-files.py`
**Výsledok:** Encoding opravený (UTF-8 bez BOM), diakritika odstránená

#### Krok 6: Úspešný štart systému
**Príkaz:** `.\start-claude-tools.ps1`
**Výsledok:**
```
Artifact Server spusteny (PID: 17396)
URL: http://localhost:8765
Server je dostupny ✓

Hotkeys spustene (PID: 4272)
Ctrl+Win+S/G/D/N/I - Ready ✓
```

---

### Session 2: Testovanie a opravy

#### Test 1: Ctrl+Win+I (úspešný hneď)
**Výsledok:** ✅ Funguje perfektne, zobrazí Project Info a skopíruje do schránky

#### Test 2-6: Postupné riešenie kolízií
**Kroky:**
1. `Ctrl+Alt+L` → kolízia so SK klávesnicou (AltGr)
2. Fix: zmena na `Ctrl+Alt+P` → stále kolízia
3. Fix: zmena na `Ctrl+Shift+...` → kolízia s browser
4. Fix: zmena na `Ctrl+Win+...` → nesprávna syntax ('win')
5. Fix: zmena na `'windows'` → ✅ funguje!
6. Zistenie: `Ctrl+Win+P` koliduje s Windows Project mode

#### Finálne testovanie (všetky hotkeys)
**Výsledok:**
```
Ctrl+Win+I ✅ Project Info zobrazené
Ctrl+Win+S ✅ Session Notes (538 riadkov) skopírované
Ctrl+Win+G ✅ Git Status zobrazený
Ctrl+Win+D ✅ Deployment Info zobrazené
Ctrl+Win+N ✅ "nový chat" skopírované
Ctrl+Win+P ❌ Windows Project mode menu
```

**Čas strávený:** ~4 hodiny (implementácia + testovanie + opravy)

---

## Konfigurácia

### config.py
**Automaticky generovaný súbor:**

```python
PROJECT_ROOT = r"C:\Development\nex-automat"
TOOLS_DIR = r"/tools"
SESSION_NOTES_DIR = r"/SESSION_NOTES"

ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"

ANTHROPIC_API_KEY = ""  # Voliteľné - pre context compressor

HOTKEY_LOAD_INIT = "p"  # Ctrl+Win+P (koliduje s Windows)
HOTKEY_COPY_NOTES = "s"
HOTKEY_GIT_STATUS = "g"
HOTKEY_DEPLOYMENT_INFO = "d"
HOTKEY_NEW_CHAT = "n"
HOTKEY_SHOW_INFO = "i"
```

**Kľúčové body:**
- Raw strings (`r"..."`) pre Windows cesty
- Relatívne cesty odvodené od PROJECT_ROOT
- Port 8765 pre artifact server (štandardný)
- API key prázdny (compressor je voliteľný)

### Artifact Server endpoints
```python
GET  /              - Health check, project info
POST /save-artifact - Uložiť artifact do projektu
GET  /list-recent   - Posledných N upravených súborov
GET  /ping          - Jednoduchý ping test
```

**CORS nastavenie:**
```python
allow_origins=[
    "https://claude.ai",
    "https://*.claude.ai",
    "http://localhost:*"
]
```

---

## Kľúčové poznatky

### Hotkey kolízie - kompletné zhrnutie

| Kombinácia | Problém | Status | Riešenie |
|------------|---------|--------|----------|
| `Ctrl+Alt+...` | AltGr na SK klávesnici | ❌ Nefunguje | Zmena na Ctrl+Win |
| `Ctrl+Shift+...` | Browser DevTools/Incognito | ❌ Koliduje | Zmena na Ctrl+Win |
| `Ctrl+Win+...` | Väčšinou OK | ✅ Funguje | Použiť 'windows' nie 'win' |
| `Ctrl+Win+P` | Windows Project mode | ❌ Koliduje | Manuálne kopírovanie |

**Ponaučenie:** Pri výbere hotkeys na Windows s ne-anglickou klávesnicou:
1. Vyhýbať sa `Ctrl+Alt` (AltGr konflikty)
2. Vyhýbať sa `Ctrl+Shift` (browser/app konflikty)
3. Preferovať `Ctrl+Win` kombinácie
4. Testovať každý hotkey pred finalizáciou
5. Kontrolovať Windows system hotkeys

### Windows Path Handling
```python
# ❌ CHYBNÉ - zdvojené backslashes v f-string
config = f"""PROJECT_ROOT = r"C:\\\\Development\\\\nex-automat" """

# ✅ SPRÁVNE - raw string v obyčajnom triple-quoted string
config = '''PROJECT_ROOT = r"C:\\Development\\nex-automat" '''

# ✅ ALTERNATÍVA - forward slashes (fungujú v Pythone)
PROJECT_ROOT = Path("C:/Development/nex-automat")
```

### PowerShell Encoding Best Practices
```powershell
# ❌ Problematické znaky v PowerShell
Write-Host "✅ Všetky úlohy dokončené" -ForegroundColor Green

# ✅ Bezpečné pre PowerShell parser
Write-Host "Vsetky ulohy dokoncene" -ForegroundColor Green

# 💡 Alebo použiť [char] pre Unicode
Write-Host "$([char]0x2705) Dokoncene" -ForegroundColor Green
```

### Artifact Server Pattern
```python
# Minimálny FastAPI server pre ukladanie artifacts
@app.post("/save-artifact")
async def save_artifact(data: ArtifactSave):
    file_path = PROJECT_ROOT / data.filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(data.content, encoding='utf-8')
    return {"status": "saved", "path": str(file_path)}
```

### Hotkeys Global Registration
```python
# Globálne hotkeys (fungujú aj keď okno nemá focus)
import keyboard

# SPRÁVNA SYNTAX - 'windows' nie 'win'
keyboard.add_hotkey('ctrl+windows+i', show_info_function)
keyboard.wait()  # Drží program bežať
```

---

## Testovanie

### Session 1 Tests

#### Test 1: Artifact Server dostupnosť
```powershell
Invoke-WebRequest http://localhost:8765/ping
# Expected: {"status":"ok","timestamp":"2025-12-06..."}
```
**Výsledok:** ✅ Server odpovedá správne

#### Test 2: Hotkeys funkčnosť (základný)
```bash
python tools/claude-hotkeys.py
# Stlač Ctrl+Win+I
# Expected: PROJECT INFO zobrazené + skopírované do schránky
```
**Výsledok:** ✅ Hotkey funguje, info zobrazené správne

#### Test 3: Config validácia
```python
from tools.config import PROJECT_ROOT, TOOLS_DIR
print(PROJECT_ROOT)  # Expected: C:\Development\nex-automat
```
**Výsledok:** ✅ Import funguje, cesty správne

---

### Session 2 Tests

#### Test 4: Všetky hotkeys (komplexný)
```bash
python tools/claude-hotkeys.py

# Test každého hotkey:
Ctrl+Win+I → ✅ Project Info
Ctrl+Win+S → ✅ Session Notes (538 riadkov)
Ctrl+Win+G → ✅ Git Status
Ctrl+Win+D → ✅ Deployment Info  
Ctrl+Win+N → ✅ "nový chat"
Ctrl+Win+P → ❌ Windows Project mode
```
**Výsledok:** 5/6 hotkeys funkčných (83% úspešnosť)

#### Test 5: Artifact Server ping
```powershell
curl http://localhost:8765/ping
# Expected: Status 200, JSON response
```
**Výsledok:** ✅ Server reaguje správne

#### Test 6: N8n workflow neovplyvnený
```powershell
Get-WmiObject Win32_Process | Where-Object {$_.Name -eq "python.exe"}
# Očakávané: Claude Tools + n8n procesy bežia súčasne
```
**Výsledok:** ✅ N8n workflow nebol ovplyvnený, oba systémy fungujú paralelne

---

## Štatistiky

### Session 1 (Implementácia)
- **Vytvorené súbory:** 15 (tools) + 4 (scripts) = 19
- **Opravené bugy:** 3 (config, powershell, uvicorn)
- **Nainštalované dependencies:** 6 Python packages
- **Spustené procesy:** 2 (Artifact Server, Hotkeys)
- **Čas implementácie:** ~3 hodiny
- **Použité tokeny:** ~100k / 190k (52.6%)

### Session 2 (Testovanie)
- **Otestované hotkeys:** 6/6
- **Funkčné hotkeys:** 5/6 (83%)
- **Vytvorené fix scripty:** 4 (06-09)
- **Opravené bugy:** 4 (SK klávesnica, browser, syntax, Windows)
- **Čas testovania:** ~4 hodiny
- **Použité tokeny:** ~58k / 190k (30.5%)

### Celkovo
- **Celkový čas:** ~7 hodín
- **Celkové tokeny:** ~158k / 190k (83%)
- **Úspešnosť:** 5/6 hotkeys (83%), Artifact Server 100%, systém použiteľný

---

## Ďalšie kroky

### Ihneď (najbližšia session)
1. **Git commit** - všetky zmeny
   - Použiť commit message z commit-message.txt artifact
   - Commitnúť: tools/, scripts/, SESSION_NOTES/
   - Zvážiť vymazanie dočasných scriptov (01, 02, 05, 05b)

2. **Voliteľné vylepšenia Ctrl+Win+P**
   - Zmeniť na iné písmeno (L, O, K)
   - Alebo ponechať ako manuálny workflow

### Krátkodobé (tento týždeň)
1. **Browser Extension inštalácia a test**
   - Load do Chrome
   - Test na claude.ai (vytvor artifact → klik "💾 Uložiť")

2. **Praktické používanie v reálnej práci**
   - Otestovať workflow: Nový chat → práca → "nový chat"
   - Zaznamenať problémy/vylepšenia

3. **Context Compressor setup** (voliteľné)
   - Získať Claude API key
   - Nastaviť v config.py
   - Test kompresie session notes

### Dlhodobé (budúce mesiace)
1. **Nazbierať skúsenosti na nex-automat**
   - Minimálne 2-3 týždne používania
   - Dokumentovať pain points
   - Optimalizovať workflow

2. **Template systém pre ďalšie projekty**
   - Vytvoriť `_claude-tools-template` master template
   - Script pre rýchle vytvorenie tools pre nový projekt
   - Multi-project management (prepínanie medzi projektmi)

3. **Advanced features**
   - Automatické Git commit session notes
   - Integration s n8n workflows
   - Custom commands pre NEX-špecifické operácie

---

## Poznámky pre Development → Deployment

### Súbory v Git
**Commitnuté:**
- `tools/*.py` - všetky Python nástroje
- `tools/*.ps1` - PowerShell skripty
- `tools/browser-extension/` - celý extension
- `SESSION_NOTES/README.md` - dokumentácia
- `SESSION_NOTES/INSTALLATION_GUIDE.md` - inštalačný návod

**Vylúčené (.gitignore):**
- `tools/config.py` - obsahuje lokálne cesty
- `tools/claude-tools.log` - runtime log
- `tools/__pycache__/` - Python cache
- `scripts/*.py` - dočasné setup scripty (môžu byť vymazané po commite)

### Deployment workflow
**Ak by sme chceli tools v Deployment:**
```bash
# Development
git add tools/ SESSION_NOTES/
git commit -m "feat: Claude Tools implementation"
git push

# Deployment
cd C:\Development\nex-automat-deployment
git pull
python tools/installer.py  # Vytvorí config.py s Deployment cestami
.\tools\start-claude-tools.ps1
```

**Poznámka:** Momentálne tools sú LEN pre Development. Deployment ich nepotrebuje.

---

## Kritické upozornenia

### ⚠️ API Key Security
```python
# ❌ NIKDY necommituj API key do Git
ANTHROPIC_API_KEY = "sk-ant-api03-..."

# ✅ Drž v config.py (ktorý je v .gitignore)
# ✅ Alebo použi environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
```

### ⚠️ Port Conflicts
```python
# Ak port 8765 je obsadený:
netstat -ano | findstr :8765
taskkill /F /PID <pid>

# Alebo zmeň port v config.py:
ARTIFACT_SERVER_PORT = 8766
```

### ⚠️ N8n Workflow na pozadí
```powershell
# NIKDY nezabíjaj všetky Python procesy!
# Na serveri bežia n8n workflows (supplier-invoice-loader)

# ✅ Správne - kontroluj command line
Get-WmiObject Win32_Process | Where-Object {
    $_.CommandLine -like "*artifact-server*" -or 
    $_.CommandLine -like "*claude-hotkeys*"
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

### ⚠️ Stop Script problém
```powershell
# Stop script niekedy nedetekuje procesy správne
# Pre istotu použiť manuálne zastavenie cez Get-WmiObject
```

---

## Resources

### Dokumentácia
- **README.md** - Kompletný prehľad projektu
- **INSTALLATION_GUIDE.md** - Rýchly setup návod
- **Tento SESSION_NOTES.md** - Detailný technický záznam

### External Links
- FastAPI docs: https://fastapi.tiangolo.com/
- keyboard package: https://github.com/boppreh/keyboard
- Anthropic API: https://docs.anthropic.com/
- Windows hotkeys: https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows

### Internal Links
- NEX Automat docs: `C:\Development\nex-automat\SESSION_NOTES\`
- Window persistence: `packages/nex-shared/ui/`
- Supplier Invoice Editor: `apps/supplier-invoice-editor/`

---

**Session ukončená:** 2025-12-06 17:10  
**Status:** ✅ Všetky primárne ciele dosiahnuté  
**Ďalšia session:** Git commit + praktické používanie