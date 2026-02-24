# Knowledge: ANDROS Nginx + Telegram Deployment

**Dátum:** 2026-01-16  
**Session:** andros-nginx-telegram  
**Server:** Dell PowerEdge R740XD (ANDROS)

---

## Nginx Reverse Proxy

### Konfigurácia
- **Súbor:** `/etc/nginx/sites-available/andros.conf`
- **SSL:** Self-signed certifikát (pre development cez Tailscale)
- **Certifikáty:** `/etc/nginx/ssl/andros.crt`, `/etc/nginx/ssl/andros.key`

### Endpointy

| URL | Služba | Backend |
|-----|--------|---------|
| https://100.107.134.104/ | Hlavná stránka | static HTML |
| https://100.107.134.104/api/ | NEX Brain API | localhost:8000 |
| https://100.107.134.104/temporal/ | Temporal UI | localhost:8080 |
| https://100.107.134.104/qdrant/ | Qdrant Dashboard | localhost:6333 |

### Príkazy

```bash
# Test konfigurácie
sudo nginx -t

# Reštart
sudo systemctl restart nginx

# Status
sudo systemctl status nginx
```

---

## Telegram Multi-Bot

### Docker kontajner
- **Image:** nex-telegram:latest
- **Container:** nex-telegram
- **Dockerfile:** `/opt/nex-automat-src/Dockerfile.telegram`

### Boty

| Bot | Username | Účel |
|-----|----------|------|
| Admin | @ai_dev_automatin_bot | Admin notifikácie, schvaľovanie |
| ICC | @NexBrainIcc_bot | ICC zákazníci |
| ANDROS | @NexBrainAndros_bot | ANDROS zákazníci |

### Environment variables (v .env)

```env
TELEGRAM_ADMIN_BOT_TOKEN=8585064403:AAE-kFftrdpXwoLHVmrG0MvB5jfo1FmA1Y4
TELEGRAM_ICC_BOT_TOKEN=8487965429:AAH2IUIFVEEtInFva8_GHAz84wCFdgGax9U
TELEGRAM_ANDROS_BOT_TOKEN=8178049225:AAEQ-vVQINeB2ASGClClK90HLBHhuBhyxBo
TELEGRAM_ADMIN_USER_ID=7204918893
```

### Príkazy

```bash
# Logy
docker logs nex-telegram -f --tail 50

# Reštart
docker restart nex-telegram

# Rebuild
cd /opt/nex-automat-src && docker build -f Dockerfile.telegram -t nex-telegram:latest .
cd /opt/nex-automat && docker compose up -d nex-telegram
```

---

## Docker Stack - Kompletný stav

| Služba | Container | Port | Status |
|--------|-----------|------|--------|
| PostgreSQL | nex-postgres | 5432 | ✅ |
| Temporal | nex-temporal | 7233 | ✅ |
| Temporal UI | nex-temporal-ui | 8080 | ✅ |
| Ollama | nex-ollama | 11434 | ✅ |
| Qdrant | nex-qdrant | 6333/6334 | ✅ |
| NEX Brain API | nex-brain | 8000 | ✅ |
| Telegram Bots | nex-telegram | - | ✅ |
| Nginx | systemd | 80/443 | ✅ |

---

## Súbory

| Súbor | Popis |
|-------|-------|
| /opt/nex-automat/docker-compose.yml | Docker stack definícia |
| /opt/nex-automat/.env | Environment variables |
| /opt/nex-automat-src/Dockerfile.telegram | Telegram bot image |
| /etc/nginx/sites-available/andros.conf | Nginx konfigurácia |
| /etc/nginx/ssl/andros.* | SSL certifikáty |

---

## Poznámky

1. **Tailscale HTTPS** - Free tier nepodporuje certifikáty, použitý self-signed
2. **Telegram konflikt** - Bot môže bežať len na jednom mieste (DEV alebo ANDROS)
3. **Produkcia** - Po presune do ANDROS s verejnou IP prejsť na Let's Encrypt

---

## RAG Queries

```
https://rag-api.icc.sk/search?query=ANDROS+nginx+reverse+proxy&limit=5
https://rag-api.icc.sk/search?query=nex-telegram+docker+deployment&limit=5
```

---

**Koniec knowledge dokumentu**