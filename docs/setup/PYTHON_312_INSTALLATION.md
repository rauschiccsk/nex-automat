# Python 3.12 Installation Guide

**Projekt:** nex-automat RAG Implementation  
**Dátum:** 2025-12-16  
**Dôvod:** Python 3.13 nemá prebuilt wheels pre asyncpg, tiktoken

---

## 📋 Pred Inštaláciou

**Aktuálny stav:**
- ✓ Python 3.13.7 64-bit nainštalovaný
- ✗ Asyncpg, tiktoken vyžadujú kompiláciu
- ✗ Python 3.12 nie je nainštalovaný

**Cieľ:**
- ✓ Nainštalovať Python 3.12.8 64-bit (latest stable)
- ✓ Paralelne s Python 3.13 (nezmazávame 3.13)
- ✓ Vytvoriť nový venv s Python 3.12

---

## 🔗 Krok 1: Download Python 3.12

**Official Download Link:**
https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe

**Alternatívne (cez releases page):**
https://www.python.org/downloads/release/python-3128/

**Súbor:**
- Názov: `python-3.12.8-amd64.exe`
- Veľkosť: ~26 MB
- Verzia: 3.12.8 (December 2024 release)
- Architektúra: 64-bit

---

## 🛠️ Krok 2: Inštalácia

### Spustenie Installera

1. **Spusti:** `python-3.12.8-amd64.exe`

2. **DÔLEŽITÉ na prvom okne:**
   - ✅ **"Add python.exe to PATH"** - NEZAŠKRTÁVAJ!
   - (Kvôli konfliktom s Python 3.13)

3. **Vyber:** "Customize installation"

### Customize Installation - Optional Features

**Zaškrtni všetko:**
- ✅ Documentation
- ✅ pip
- ✅ tcl/tk and IDLE
- ✅ Python test suite
- ✅ py launcher
- ✅ for all users (requires admin privileges)

Klikni: **Next**

### Advanced Options

**Path:**
```
C:\Program Files\Python312\
```

**Zaškrtni:**
- ✅ Install Python for all users
- ✅ Associate files with Python (requires the py launcher)
- ✅ Create shortcuts for installed applications
- ✅ Add Python to environment variables - **NEZAŠKRTÁVAJ!**
- ✅ Precompile standard library
- ✅ Download debugging symbols
- ✅ Download debug binaries (requires VS 2015 or later)

**KRITICKÉ:** Customize install location na **C:\Program Files\Python312\**

Klikni: **Install**

### Dokončenie

- Počkaj na dokončenie inštalácie (~2-3 minúty)
- Klikni: **Close**

---

## ✅ Krok 3: Verifikácia

**Po inštalácii spusti verifikačný script:**

```powershell
python scripts/06_verify_python312.py
```

**Script skontroluje:**
- ✓ Python 3.12 existuje v C:\Program Files\Python312\
- ✓ Je 64-bit
- ✓ Verzia je 3.12.x
- ✓ pip funguje

---

## 🔄 Krok 4: Recreate venv

**Po úspešnej verifikácii:**

```powershell
python scripts/07_recreate_venv_python312.py
```

**Script:**
1. Vymaže starý venv (Python 3.13)
2. Vytvorí nový venv s Python 3.12
3. Overí 64-bit architektúru

---

## 📦 Krok 5: Install RAG Dependencies

**Po vytvorení nového venv:**

```powershell
.\venv\Scripts\activate.ps1
python scripts/02_install_rag_dependencies.py
```

**Tentokrát by mali všetky dependencies nainštalovať správne!**

---

## 🎯 Summary

**Po dokončení budeš mať:**
- ✓ Python 3.13.7 64-bit (C:\Program Files\Python313\)
- ✓ Python 3.13.7 32-bit (C:\Program Files (x86)\Python313-32\)
- ✓ **Python 3.12.8 64-bit (C:\Program Files\Python312\)** ← pre RAG
- ✓ venv vytvorený s Python 3.12
- ✓ Všetky RAG dependencies nainštalované

---

## ⚠️ Troubleshooting

### Python 3.12 sa nenainštaloval
- Skontroluj že máš admin práva
- Skúsi spustiť installer "ako správca"
- Skontroluj že cesta je presne: C:\Program Files\Python312\

### Verifikačný script hlási chybu
- Skontroluj cestu k Python 3.12
- Reštartuj PowerShell
- Spusti script znova

### venv sa nevytvorí
- Skontroluj že Python 3.12 je správne nainštalovaný
- Skúsi manuálne: `"C:\Program Files\Python312\python.exe" -m venv venv`

---

**Pripravené scripty:**
- ✓ scripts/06_verify_python312.py - Verifikácia
- ✓ scripts/07_recreate_venv_python312.py - Recreate venv
- ✓ scripts/02_install_rag_dependencies.py - Install deps

**Pokračuj s Krokom 1: Download Python 3.12**