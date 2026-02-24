# ANDROS Docker Stack Deployment

**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**OS:** Ubuntu 24.04 LTS  
**Dátum nasadenia:** 2026-01-16  
**Verzia:** 1.0

---

## Prehľad služieb

| Služba | Port | Container | Image | Stav |
|--------|------|-----------|-------|------|
| PostgreSQL | 5432 | nex-postgres | postgres:16-alpine | ✅ |
| Temporal | 7233 | nex-temporal | temporalio/auto-setup:1.24.2 | ✅ |
| Temporal UI | 8080 | nex-temporal-ui | temporalio/ui:latest | ✅ |
| Ollama | 11434 | nex-ollama | ollama/ollama:latest | ✅ |
| Qdrant | 6333, 6334 | nex-qdrant | qdrant/qdrant:latest | ✅ |
| NEX Brain API | 8000 | nex-brain | nex-brain:latest | ✅ |

---

## Sieťová konfigurácia

### Ubuntu Host
- **LAN IP:** 192.168.100.23
- **Tailscale IP:** 100.107.134.104
- **User:** andros

### Windows VM (KVM)
- **Internal IP:** 192.168.122.75
- **RDP:** 100.107.134.104 (cez Tailscale)
- **User:** Administrator

### Prístupové URL
- NEX Brain API: http://192.168.100.23:8000
- Temporal UI: http://192.168.100.23:8080
- Qdrant Dashboard: http://192.168.100.23:6333/dashboard
- Ollama API: http://192.168.100.23:11434

---

## Adresárová štruktúra

```
/opt/nex-automat/           # Docker compose konfigurácia
├── docker-compose.yml
├── .env
├── nginx/
└── scripts/

/opt/nex-automat-src/       # Zdrojový kód (git repo)
├── apps/
│   ├── nex-brain/
│   ├── supplier-invoice-worker/
│   └── ...
├── packages/
└── Dockerfile.nex-brain

/data/docker-volumes/       # Perzistentné dáta (RAID 10)
├── postgres/
├── ollama/
├── qdrant/
└── temporal/
```

---

## Ollama modely

| Model | Veľkosť | Účel |
|-------|---------|------|
| llama3.1:8b | 4.9 GB | LLM pre chat/generovanie |
| nomic-embed-text | 274 MB | Embedding pre RAG (768 dim) |

---

## Windows VM Software

| Software | Verzia | Cesta |
|----------|--------|-------|
| Python 32-bit | 3.11.9 | C:\Python311-32 |
| Python 64-bit | 3.11.9 | C:\Python311-64 |
| Git | 2.52.0 | PATH |
| NSSM | 2.24 | C:\Windows\System32 |
| PowerShell | 7.5.4 | pwsh |

---

## Údržbové príkazy

### Štart/Stop/Reštart
```bash
cd /opt/nex-automat
docker compose up -d          # Štart všetkých služieb
docker compose down           # Stop všetkých služieb
docker compose restart        # Reštart všetkých služieb
docker compose restart nex-brain  # Reštart konkrétnej služby
```

### Logy
```bash
docker logs nex-brain -f --tail 100
docker logs nex-postgres -f --tail 100
docker logs nex-temporal -f --tail 100
```

### Stav
```bash
docker compose ps
docker stats --no-stream
```

### Aktualizácia NEX Brain
```bash
cd /opt/nex-automat-src
git pull origin develop
docker build -f Dockerfile.nex-brain -t nex-brain:latest .
cd /opt/nex-automat
docker compose up -d nex-brain
```

### Ollama - správa modelov
```bash
docker exec nex-ollama ollama list          # Zoznam modelov
docker exec nex-ollama ollama pull MODEL    # Stiahnutie modelu
docker exec nex-ollama ollama rm MODEL      # Odstránenie modelu
```

### Zálohovanie PostgreSQL
```bash
docker exec nex-postgres pg_dump -U nex_admin nex_automat > backup_$(date +%Y%m%d).sql
```

---

## Systemd service

Auto-start pri reštarte servera:
```bash
sudo systemctl status nex-automat
sudo systemctl start nex-automat
sudo systemctl stop nex-automat
```

---

## Testovanie pripojení

### NEX Brain API
```bash
curl http://localhost:8000/health
```

### PostgreSQL
```bash
docker exec nex-postgres psql -U nex_admin -d nex_automat -c "SELECT version();"
```

### Ollama
```bash
curl http://localhost:11434/api/tags
```

### Qdrant
```bash
curl http://localhost:6333/collections
```

### Windows → PostgreSQL
```powershell
Test-NetConnection -ComputerName 192.168.122.1 -Port 5432
```

---

## Dôležité poznámky

1. **Temporal databázy** - vytvorené manuálne: `temporal`, `temporal_visibility`
2. **SKIP_DB_CREATE=true** - Temporal nevytvára databázy automaticky
3. **PostgreSQL heslo** - pri zmene hesla treba vymazať `/data/docker-volumes/postgres/`
4. **Ollama modely** - uložené v `/data/docker-volumes/ollama/`, prežijú reštart