# INIT PROMPT - ANDROS Docker Stack v2

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2026-01-16  
**Session:** Pokračovanie Docker Stack

---

## ✅ DOKONČENÉ (session 2026-01-16)

### Docker Stack (Linux - Ubuntu 24.04)
| Služba | Port | Image | Stav |
|--------|------|-------|------|
| PostgreSQL | 5432 | postgres:16-alpine | ✅ healthy |
| Temporal | 7233 | temporalio/auto-setup:1.24.2 | ✅ running |
| Temporal UI | 8080 | temporalio/ui:latest | ✅ running |
| Ollama | 11434 | ollama/ollama:latest | ✅ running |
| Qdrant | 6333/6334 | qdrant/qdrant:latest | ✅ running |
| NEX Brain API | 8000 | nex-brain:latest | ✅ healthy |

### Ollama modely
- llama3.1:8b (4.9 GB) - LLM
- nomic-embed-text (274 MB) - Embeddings

### Windows VM (KVM)
- Python 32-bit + 64-bit (3.11.9)
- Git 2.52.0
- NSSM 2.24
- PowerShell 7.5.4
- PostgreSQL pripojenie funguje

### Infraštruktúra
- Systemd autostart: nex-automat.service
- Tailscale VPN: 100.107.134.104
- Zdrojový kód: /opt/nex-automat-src (branch develop)

---

## 📋 SERVER INFO

### Ubuntu Host
- **LAN IP:** 192.168.100.23
- **Tailscale IP:** 100.107.134.104
- **User:** andros
- **SSH:** ssh andros@192.168.100.23

### Windows VM
- **Internal IP:** 192.168.122.75
- **RDP:** 100.107.134.104 (cez Tailscale)
- **User:** Administrator

### Adresáre
- Docker config: /opt/nex-automat/
- Zdrojový kód: /opt/nex-automat-src/
- Docker volumes: /data/docker-volumes/

---

## 🎯 MOŽNÉ ĎALŠIE ÚLOHY

### Priority HIGH
- [ ] Nginx reverse proxy + SSL
- [ ] Supplier Invoice Worker deployment
- [ ] NEX Brain Telegram bot konfigurácia

### Priority MEDIUM
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Backup stratégia
- [ ] CI/CD pipeline

### Priority LOW
- [ ] Load balancing
- [ ] Kubernetes migrácia

---

## 📚 RAG QUERIES

```
https://rag-api.icc.sk/search?query=ANDROS+docker+deployment&limit=5
https://rag-api.icc.sk/search?query=NEX+Brain+telegram+bot&limit=5
https://rag-api.icc.sk/search?query=supplier+invoice+worker&limit=5
```

---

## 🔧 UŽITOČNÉ PRÍKAZY

### Stav služieb
```bash
cd /opt/nex-automat && docker compose ps
```

### Logy
```bash
docker logs nex-brain -f --tail 100
docker logs nex-temporal -f --tail 50
```

### Reštart služby
```bash
docker compose restart nex-brain
```

### Aktualizácia NEX Brain
```bash
cd /opt/nex-automat-src && git pull origin develop
docker build -f Dockerfile.nex-brain -t nex-brain:latest .
cd /opt/nex-automat && docker compose up -d nex-brain
```

---

## 🚀 ZAČAŤ S

```bash
ssh andros@192.168.100.23
cd /opt/nex-automat && docker compose ps
```

Vyber úlohu z "MOŽNÉ ĎALŠIE ÚLOHY" alebo špecifikuj vlastnú.