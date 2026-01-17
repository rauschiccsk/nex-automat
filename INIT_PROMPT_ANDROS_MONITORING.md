# INIT PROMPT - ANDROS Monitoring

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2026-01-16  
**Session:** Monitoring (Prometheus/Grafana)

---

## ✅ DOKONČENÉ (predchádzajúce sessions)

### Docker Stack (Linux - Ubuntu 24.04)

| Služba | Port | Container | Status |
|--------|------|-----------|--------|
| PostgreSQL | 5432 | nex-postgres | ✅ healthy |
| Temporal | 7233 | nex-temporal | ✅ running |
| Temporal UI | 8080 | nex-temporal-ui | ✅ running |
| Ollama | 11434 | nex-ollama | ✅ running |
| Qdrant | 6333/6334 | nex-qdrant | ✅ running |
| NEX Brain API | 8000 | nex-brain | ✅ healthy |
| Telegram Bots | - | nex-telegram | ✅ running |
| Nginx | 80/443 | systemd | ✅ running |

### Nginx Reverse Proxy

| URL | Služba |
|-----|--------|
| https://100.107.134.104/ | Hlavná stránka |
| https://100.107.134.104/api/docs | NEX Brain API |
| https://100.107.134.104/temporal/ | Temporal UI |
| https://100.107.134.104/qdrant/ | Qdrant Dashboard |

### Telegram Bots

| Bot | Username | Status |
|-----|----------|--------|
| Admin | @ai_dev_automatin_bot | ✅ |
| ICC | @NexBrainIcc_bot | ✅ |
| ANDROS | @NexBrainAndros_bot | ✅ |

---

## 📋 SERVER INFO

### Ubuntu Host
- **LAN IP:** 192.168.100.23
- **Tailscale IP:** 100.107.134.104
- **User:** andros
- **SSH:** ssh andros@192.168.100.23

### Adresáre
- Docker config: /opt/nex-automat/
- Zdrojový kód: /opt/nex-automat-src/
- Docker volumes: /data/docker-volumes/

---

## 🎯 AKTUÁLNA ÚLOHA: Monitoring

### Cieľ
Nasadiť Prometheus + Grafana pre monitoring všetkých Docker služieb.

### Komponenty na pridanie

| Služba | Port | Účel |
|--------|------|------|
| Prometheus | 9090 | Zber metrík |
| Grafana | 3000 | Vizualizácia |
| node-exporter | 9100 | Systémové metriky |
| cadvisor | 8081 | Docker metriky |

### Metriky na sledovanie
- CPU/RAM využitie (systém + kontajnery)
- PostgreSQL (spojenia, query časy)
- Temporal (workflows, tasks)
- Qdrant (vektory, latencia)
- Nginx (requesty, errors)

### Voliteľne
- Alertmanager + Telegram notifikácie

---

## 📚 RAG QUERIES

```
https://rag-api.icc.sk/search?query=prometheus+grafana+docker+monitoring&limit=5
https://rag-api.icc.sk/search?query=ANDROS+docker+deployment&limit=5
```

---

## 🔧 UŽITOČNÉ PRÍKAZY

```bash
# SSH pripojenie
ssh andros@192.168.100.23

# Docker stav
cd /opt/nex-automat && docker compose ps

# Logy
docker logs <container> -f --tail 50
```

---

## 🚀 ZAČAŤ S

```bash
ssh andros@192.168.100.23
cd /opt/nex-automat && docker compose ps
```

Pokračujeme s inštaláciou Prometheus + Grafana.