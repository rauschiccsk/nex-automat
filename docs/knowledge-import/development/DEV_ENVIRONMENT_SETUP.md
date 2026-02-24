# NEX Automat - Development Environment Setup

## Prehľad

Konfigurácia vývojového prostredia pre NEX Automat na Dev PC (ZelenePC). PowerShell profil poskytuje automatizované spúšťanie všetkých potrebných služieb v Windows Terminal s tabmi.

## Umiestnenie profilu

```
C:\Users\ZelenePC\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

## Dostupné príkazy

| Príkaz | Alias | Popis |
|--------|-------|-------|
| `Start-NexServices` | `nex-start` | Spustí Windows Terminal so 6 tabmi |
| `Stop-NexServices` | `nex-stop` | Zastaví všetky NEX procesy |
| `Test-NexServices` | `nex-status` | Overí health endpointy služieb |

## Konfigurácia tabov

### Tab 1: RAG API Server
- **Port:** 8765
- **URL:** http://127.0.0.1:8765
- **Health:** http://127.0.0.1:8765/health
- **Príkaz:** `python -m uvicorn tools.rag.server_app:app --host 127.0.0.1 --port 8765 --log-level info`
- **Venv:** `C:\Development\nex-automat\venv`
- **Databáza:** PostgreSQL `localhost:5432/nex_automat_rag`

### Tab 2: NEX Brain API
- **Port:** 8003
- **URL:** http://127.0.0.1:8003
- **Health:** http://127.0.0.1:8003/health
- **Príkaz:** `python -m uvicorn api.main:app --reload --port 8003`
- **Venv:** `C:\Development\nex-automat\venv`
- **Účel:** AI Chat API s RAG integráciou

### Tab 3: Development CC
- **Účel:** Claude Code pre lokálny vývoj
- **Pracovný adresár:** `C:\Development\nex-automat`
- **Venv:** Aktivovaný automaticky

### Tab 4: ANDROS Ubuntu CC
- **Účel:** Claude Code pre ANDROS Ubuntu server
- **SSH:** `ssh andros@46.224.229.55 -p 22023`
- **Prostredie:** Ubuntu Linux, Docker, PostgreSQL

### Tab 5: ANDROS Windows CC
- **Účel:** Claude Code pre ANDROS Windows server
- **SSH:** `ssh andros` (cez Tailscale)
- **Tailscale IP:** 100.107.134.104
- **Prostredie:** Windows Server, NEX Automat production

### Tab 6: MAGER Windows CC
- **Účel:** Claude Code pre MAGER Windows server
- **SSH:** `ssh mager`
- **Tailscale IP:** 100.67.77.58
- **Prostredie:** Windows Server, NEX Automat production

## Služby a porty

| Služba | Port | Protokol | Popis |
|--------|------|----------|-------|
| RAG API | 8765 | HTTP | Vyhľadávanie v dokumentácii |
| NEX Brain | 8003 | HTTP | AI Chat API |
| PostgreSQL | 5432 | TCP | Databáza (nex_automat_rag) |

## Verejné endpointy (cez Cloudflare)

| Služba | URL |
|--------|-----|
| RAG API | https://rag-api.icc.sk |

## Použitie

### Štart služieb
```powershell
# V ľubovoľnom PowerShell
nex-start
```
Otvorí sa Windows Terminal s 6 tabmi. RAG API a NEX Brain sa spustia automaticky.

### Overenie stavu
```powershell
nex-status
```
Vypíše stav všetkých služieb (OK/FAIL).

### Zastavenie služieb
```powershell
nex-stop
```
Zastaví všetky Python procesy patriace NEX Automat.

### Manuálne načítanie profilu
```powershell
. $PROFILE
```

## Požiadavky

- Windows Terminal (`wt` príkaz)
- Python 3.12+ (64-bit) v `C:\Development\nex-automat\venv`
- Python 3.13 (32-bit) v `C:\Development\nex-automat\venv32` (pre Btrieve)
- PostgreSQL 15+ na localhost:5432
- Tailscale pre SSH na ANDROS/MAGER servery

## Súvisiace dokumenty

- [DEPLOYMENT_GUIDE_V3.md](../deployment/DEPLOYMENT_GUIDE_V3.md) - Nasadenie na produkciu
- [TODO_MASTER.md](../../TODO_MASTER.md) - Centrálny task tracking

## História zmien

| Dátum | Zmena |
|-------|-------|
| 2026-02-02 | Vytvorenie dokumentu, konfigurácia 6 tabov |
| 2026-02-02 | Odstránenie Cloudflared a Telegram Bot tabov |