# Claude Tools - nex-automat projekt

Automatizácia workflow pre prácu s claude.ai.

## 📋 Rýchly štart

### Inštalácia

1. **Vytvor adresáre**:
   ```
   C:\Development\nex-automat\tools\
   C:\Development\nex-automat\SESSION_NOTES\
   ```

2. **Skopíruj všetky súbory** z artifacts do príslušných adresárov

3. **Spusti installer**:
   ```powershell
   cd C:\Development\nex-automat\tools
   python installer.py
   ```

4. **Spusti nástroje**:
   ```powershell
   .\start-claude-tools.ps1
   ```

---

## 🔧 Komponenty

### 1. Claude Hotkeys
**Klávesové skratky pre časté operácie**

| Hotkey | Funkcia |
|--------|---------|
| `Ctrl+Alt+L` | Load init prompt do nového chatu |
| `Ctrl+Alt+S` | Copy session notes |
| `Ctrl+Alt+G` | Git status |
| `Ctrl+Alt+D` | Deployment info |
| `Ctrl+Alt+N` | New chat template |
| `Ctrl+Alt+I` | Show project info |

### 2. Artifact Server
**Lokálny FastAPI server na :8765**
- Ukladá artifacts z claude.ai do projektu
- Používa ho browser extension

### 3. Session Notes Manager
**Správa session notes**
```bash
python session-notes-manager.py enhance   # Enhanced verzia
python session-notes-manager.py validate  # Validácia štruktúry
python session-notes-manager.py template  # Nový template
```

### 4. Context Compressor (voliteľné)
**Kompresia histórie cez Claude API**
```bash
python context-compressor.py notes  # Komprimuj session notes
python context-compressor.py init   # Komprimuj init prompt
```

*Vyžaduje `ANTHROPIC_API_KEY` v config.py*

### 5. Browser Extension (voliteľné)
**Pridáva "💾 Uložiť" tlačítka k artifacts**
- Chrome: `chrome://extensions/`
- Load unpacked: `C:\Development\nex-automat\tools\browser-extension\claude-artifact-saver`

---

## 🎯 Denný workflow

### Ráno (raz)
```powershell
cd C:\Development\nex-automat\tools
.\start-claude-tools.ps1
```

### Nový chat
1. claude.ai → New chat
2. `Ctrl+Alt+L` (auto-paste init prompt)
3. Enter

### Počas práce
- `Ctrl+Alt+S` → session notes do schránky
- `Ctrl+Alt+G` → git status
- Artifact → klik "💾 Uložiť" → automaticky do projektu

### Koniec chatu
1. Napíš: `novy chat`
2. Claude vygeneruje SESSION_NOTES.md + INIT_PROMPT_NEW_CHAT.md
3. Commit do Git

### Večer
```powershell
.\stop-claude-tools.ps1
```

---

## 📂 Štruktúra projektu

```
C:\Development\nex-automat\
├── tools\
│   ├── installer.py
│   ├── claude-chat-loader.py
│   ├── claude-hotkeys.py
│   ├── artifact-server.py
│   ├── session-notes-manager.py
│   ├── context-compressor.py
│   ├── start-claude-tools.ps1
│   ├── stop-claude-tools.ps1
│   ├── config.py (generované)
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
├── packages\
├── apps\
└── ...
```

---

## ⚙️ Konfigurácia

### config.py (generované pri inštalácii)

```python
PROJECT_ROOT = r"C:\Development\nex-automat"
TOOLS_DIR = r"C:\Development\nex-automat\tools"
SESSION_NOTES_DIR = r"C:\Development\nex-automat\SESSION_NOTES"

ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"

# Voliteľné - pre context compressor
ANTHROPIC_API_KEY = ""  # sk-ant-...
```

---

## ❓ Riešenie problémov

### Hotkeys nefungujú

**Problém:** `Ctrl+Alt+L` nič nerobí

**Riešenie:**
```powershell
# Skontroluj proces
Get-Process python | Where-Object { $_.CommandLine -like "*hotkeys*" }

# Reštartuj
.\stop-claude-tools.ps1 -Force
.\start-claude-tools.ps1
```

### Server nedostupný

**Problém:** Extension hlási "Server nie je dostupný"

**Riešenie:**
```powershell
# Skontroluj port
netstat -an | findstr 8765

# Test
Invoke-WebRequest http://localhost:8765/ping

# Reštartuj
python artifact-server.py
```

### Extension nedetekuje artifacts

**Problém:** Tlačítko "💾 Uložiť" sa neobjavuje

**Riešenie:**
1. F12 → Console → hľadaj chyby
2. `chrome://extensions/` → Reload
3. Refresh claude.ai

### Git status chyba

**Problém:** "nie si v Git repozitári"

**Riešenie:**
```bash
cd C:\Development\nex-automat
git init  # ak ešte nie je Git repo
```

---

## 💡 Tips & Tricks

### 1. Automatický štart s Windows

Vytvor skratku v Startup folder:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

Target:
```
powershell.exe -ExecutionPolicy Bypass -File "C:\Development\nex-automat\tools\start-claude-tools.ps1"
```

### 2. Vlastné hotkeys

Uprav `claude-hotkeys.py`:
```python
keyboard.add_hotkey('ctrl+alt+m', self.my_custom_function)
```

### 3. Rýchly prístup k notes

PowerShell alias:
```powershell
function notes { code C:\Development\nex-automat\SESSION_NOTES\SESSION_NOTES.md }
```

### 4. Sledovanie logu

```powershell
Get-Content C:\Development\nex-automat\tools\claude-tools.log -Wait -Tail 20
```

---

## 📊 Štatistiky

### Úspora času
- **7 minút/chat** (eliminovaný copy-paste)
- **35 hodín/rok** (pri 15 chatoch denne)

### Automatizované
- ✅ Init prompt loading
- ✅ Session notes access
- ✅ Git status check
- ✅ Artifact saving
- ✅ Deployment info

### Náklady
- **Claude MAX**: ~$20/mes
- **Žiadne API poplatky** (okrem voliteľného compressora)
- **Token limit**: 190k/chat (Claude MAX)

---

## 🔄 Údržba

### Denne
- Commit session notes do Git
- Backup dôležitých artifacts

### Týždenne
- Skontroluj `claude-tools.log`
- Update dependencies: `pip install --upgrade anthropic fastapi uvicorn`

### Mesačne
- Vyčisti staré compressed súbory
- Archivuj staré session notes

---

## 📚 Dokumentácia súborov

| Súbor | Popis |
|-------|-------|
| `README.md` | Tento súbor - prehľad |
| `INSTALLATION_GUIDE.md` | Detailný inštalačný návod |
| `installer.py` | Automatický inštalátor |
| `claude-chat-loader.py` | Auto-load init promptu |
| `claude-hotkeys.py` | Klávesové skratky |
| `artifact-server.py` | FastAPI server |
| `session-notes-manager.py` | Správa notes |
| `context-compressor.py` | Kompresia histórie |
| `start-claude-tools.ps1` | Startup script |
| `stop-claude-tools.ps1` | Shutdown script |

---

## 🎯 Používanie v praxi

### Typický deň:

**9:00** - Spusti tools (`start-claude-tools.ps1`)

**9:05** - Otvor nový chat, `Ctrl+Alt+L`, začni pracovať

**12:00** - Potrebuješ Git status? `Ctrl+Alt+G`

**14:00** - Claude vygeneroval skript? Klikni "💾 Uložiť"

**17:00** - Koniec práce? Napíš `novy chat`, commit SESSION_NOTES

**17:05** - Zastav tools (`stop-claude-tools.ps1`)

---

## 🚀 Budúce vylepšenia

Po nazbieraní skúseností na nex-automat projekte:

- [ ] Template pre ďalšie projekty
- [ ] Multi-project switching
- [ ] Automatické backup session notes
- [ ] Integration s n8n workflows
- [ ] Custom commands pre NEX-špecifické operácie

---

*Claude Tools pre NEX Automat v2.0*  
*Cesta k projektu: C:\Development\nex-automat*  
*Version 1.0 - December 2024*