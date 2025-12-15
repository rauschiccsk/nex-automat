# Claude Tools - Inštalačný Návod (nex-automat)

## 🚀 Quick Start (5 minút)

### 1. Vytvor adresárovú štruktúru

```
C:\Development\nex-automat\
├── tools\
│   └── browser-extension\
│       └── claude-artifact-saver\
└── SESSION_NOTES\
```

### 2. Skopíruj súbory z artifacts

**Do `C:\Development\nex-automat\tools\`:**
- ✅ `installer.py`
- ✅ `claude-chat-loader.py`
- ✅ `claude-hotkeys.py`
- ✅ `artifact-server.py`
- ✅ `session-notes-manager.py`
- ✅ `context-compressor.py`
- ✅ `start-claude-tools.ps1`
- ✅ `stop-claude-tools.ps1`

**Do `C:\Development\nex-automat\tools\browser-extension\claude-artifact-saver\`:**
- ✅ `manifest.json`
- ✅ `content.js`
- ✅ `styles.css`
- ✅ `background.js`
- ✅ `popup.html`

**Do `C:\Development\nex-automat\` (root):**
- ✅ `README.md`

**Do `C:\Development\nex-automat\tools\` (tento súbor):**
- ✅ `INSTALLATION_GUIDE.md`

### 3. Spusti installer

```powershell
cd C:\Development\nex-automat\tools
python installer.py
```

**Čo installer spraví:**
- ✅ Skontroluje Python 3.8+
- ✅ Vytvorí potrebné adresáre
- ✅ Nainštaluje dependencies (pyperclip, keyboard, anthropic, fastapi, uvicorn)
- ✅ Vytvorí `config.py`
- ✅ Vytvorí session notes template

### 4. Spusti nástroje

```powershell
.\start-claude-tools.ps1
```

**Spustí:**
- 🌐 Artifact Server na `:8765`
- ⌨️ Hotkeys (na pozadí)

### 5. Nainštaluj Browser Extension (voliteľné)

1. Chrome: `chrome://extensions/`
2. Zapni "Developer mode"
3. "Load unpacked"
4. Vyber: `C:\Development\nex-automat\tools\browser-extension\claude-artifact-saver`

---

## 📋 Zoznam súborov s popisom

### Python Scripts

| Súbor | Veľkosť | Popis |
|-------|---------|-------|
| `installer.py` | ~5 KB | Automatická inštalácia všetkých komponentov |
| `claude-chat-loader.py` | ~3 KB | Load init prompt do nového chatu (Ctrl+Alt+L) |
| `claude-hotkeys.py` | ~5 KB | Klávesové skratky (Ctrl+Alt+S/G/D/N/I) |
| `artifact-server.py` | ~4 KB | FastAPI server pre ukladanie artifacts |
| `session-notes-manager.py` | ~6 KB | Správa a analýza session notes |
| `context-compressor.py` | ~5 KB | Kompresia histórie cez Claude API (voliteľné) |
| `config.py` | ~1 KB | Konfiguračný súbor (generovaný) |

### PowerShell Scripts

| Súbor | Veľkosť | Popis |
|-------|---------|-------|
| `start-claude-tools.ps1` | ~4 KB | Startup script - spustí všetky nástroje |
| `stop-claude-tools.ps1` | ~2 KB | Zastaví všetky bežiace procesy |

### Browser Extension

| Súbor | Veľkosť | Popis |
|-------|---------|-------|
| `manifest.json` | ~1 KB | Extension manifest (Chrome/Edge) |
| `content.js` | ~6 KB | Detekcia artifacts a pridanie save tlačítok |
| `styles.css` | ~2 KB | Styling pre tlačítka a notifikácie |
| `background.js` | ~1 KB | Background service worker |
| `popup.html` | ~2 KB | Extension popup UI |

### Dokumentácia

| Súbor | Veľkosť | Popis |
|-------|---------|-------|
| `README.md` | ~15 KB | Kompletná dokumentácia |
| `INSTALLATION_GUIDE.md` | ~3 KB | Tento súbor - quick start |

---

## ✅ Kontrolný zoznam

Po inštalácii skontroluj:

```
[ ] Python 3.8+ nainštalovaný
[ ] Všetky Python dependencies nainštalované
[ ] config.py existuje v tools/
[ ] start-claude-tools.ps1 spustený
[ ] Artifact server beží na :8765
[ ] Hotkeys proces beží na pozadí
[ ] Browser extension loaded (voliteľné)
[ ] SESSION_NOTES.md existuje
[ ] INIT_PROMPT_NEW_CHAT.md existuje
```

---

## 🧪 Test funkčnosti

### Test 1: Hotkeys
```
1. Stlač Ctrl+Alt+I
2. Malo by sa zobraziť Project Info
3. Obsah je v schránke
```

### Test 2: Artifact Server
```powershell
Invoke-WebRequest http://localhost:8765/ping
# Output: {"status":"ok","timestamp":"..."}
```

### Test 3: Chat Loader
```
1. Otvor nový chat na claude.ai
2. Stlač Ctrl+Alt+L
3. Init prompt by sa mal automaticky vložiť
```

### Test 4: Browser Extension
```
1. Otvor claude.ai
2. Otvor DevTools (F12) → Console
3. Hľadaj: "🚀 Claude Artifact Saver - Loaded"
4. Vytvor artifact v Claude
5. Malo by sa objaviť tlačítko "💾 Uložiť"
```

---

## 🔧 Konfigurácia

### Základná konfigurácia (`config.py`)

```python
# Cesty k projektu nex-automat
PROJECT_ROOT = r"C:\Development\nex-automat"
TOOLS_DIR = r"C:\Development\nex-automat\tools"
SESSION_NOTES_DIR = r"C:\Development\nex-automat\SESSION_NOTES"

# Artifact Server
ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"

# Claude API (voliteľné - pre context compressor)
ANTHROPIC_API_KEY = ""
```

---

## 🎯 Denné použitie

### Ranný štart (raz denne)

```powershell
cd C:\Development\nex-automat\tools
.\start-claude-tools.ps1
```

### Otvorenie nového chatu

1. claude.ai → New chat
2. `Ctrl+Alt+L` → init prompt
3. Enter → pokračuj

### Počas práce

- `Ctrl+Alt+S` → session notes
- `Ctrl+Alt+G` → git status
- Artifact → klik "💾 Uložiť"

### Koniec dňa

```powershell
.\stop-claude-tools.ps1
```

---

## ❓ Časté problémy

### "Python nie je rozpoznaný"
```powershell
# Nainštaluj Python 3.8+
# Pridaj do PATH: C:\Python3X\
```

### "Hotkeys nefungujú"
```powershell
# Skontroluj či proces beží
Get-Process python | Where-Object { $_.CommandLine -like "*hotkeys*" }

# Reštartuj
.\stop-claude-tools.ps1 -Force
.\start-claude-tools.ps1
```

### "Server nedostupný"
```powershell
# Skontroluj port
netstat -an | findstr 8765

# Reštartuj server
python artifact-server.py
```

### "Extension nefunguje"
```
1. chrome://extensions/
2. Remove extension
3. Reload extension
4. Refresh claude.ai
5. Check DevTools console pre chyby
```

---

## 📚 Ďalšie kroky

Po úspešnej inštalácii:

1. **Prečítaj README.md** - kompletná dokumentácia
2. **Nastav ANTHROPIC_API_KEY** - ak chceš použiť context compressor
3. **Vytvor SESSION_NOTES.md** - začni pracovať s Claude
4. **Commit do Git** - zabezpeč konfiguráciu

---

## 💡 Tips

### Automatický startup s Windows

Vytvor skratku v:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

Target:
```
powershell.exe -ExecutionPolicy Bypass -File "C:\Development\nex-automat\tools\start-claude-tools.ps1"
```

### Vlastné hotkeys

Uprav `claude-hotkeys.py`, pridaj do `setup_hotkeys()`:
```python
keyboard.add_hotkey('ctrl+alt+m', self.my_function)
```

### Debug mode

Spusti s verbose:
```powershell
.\start-claude-tools.ps1 -Verbose
```

---

## 🎉 Úspech!

Ak všetko funguje:
- ✅ Ušetríš ~7 minút denne
- ✅ ~35 hodín ročne
- ✅ Žiadny manual copy-paste
- ✅ Automatické workflow

**Enjoy!** 🚀

---

*Vytvorené pre NEX Automat v2.0*  
*Version 1.0 - December 2024*