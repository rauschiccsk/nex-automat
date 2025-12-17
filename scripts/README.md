# Scripts Directory

Utility scripts pre NEX Automat projekt.

## Utility Scripts

| Script | Účel |
|--------|------|
| `check_git_status.py` | Kontrola Git stavu - uncommitted changes, branch info |
| `check_nex_genesis_connection.py` | Test pripojenia k NEX Genesis serveru |
| `validate_config.py` | Validácia konfiguračných súborov |
| `preflight_check.py` | Pre-deployment kontrola - všetky závislosti a konfigurácie |

## Cleanup Scripts

| Script | Účel |
|--------|------|
| `cleanup_backup_files.py` | Vymazanie backup súborov (*.bak, *.old) |
| `cleanup_project.py` | Kompletný cleanup projektu - cache, __pycache__, temp |
| `clean_invalid_window_positions.py` | Reset neplatných pozícií okien v settings DB |

## Deployment Scripts

| Script | Účel |
|--------|------|
| `deploy_fresh.py` | Fresh deployment na produkciu |
| `init_database.py` | Inicializácia PostgreSQL databázy |
| `manage_service.py` | Správa Windows služieb (start/stop/restart) |

## Infrastructure

| Script | Účel |
|--------|------|
| `infrastructure/start-rag-services.bat` | Spustenie RAG služieb (PostgreSQL, API) |

---

**Poznámka:** Session-specific scripty (01_*.py, 02_*.py, ...) sa vytvárajú počas vývoja a po dokončení sa mažú.