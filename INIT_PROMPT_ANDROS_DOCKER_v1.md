# INIT PROMPT - ANDROS Docker Stack Deployment v1

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2026-01-16  
**Session:** Docker Stack + Windows VM Software

---

## ✅ DOKONČENÉ (predchádzajúce sessions)

### Hardware & OS
- Dell R740XD server operational
- Ubuntu 24.04 LTS nainštalovaný
- NVMe SSD (WD_BLACK 1TB) ako root (/)
- RAID 10 (4.4TB) ako /data
- Docker, KVM/libvirt nainštalované

### Windows Server 2025 VM
- VM beží na KVM (49GB RAM, 8 vCPU, 200GB disk)
- Windows Server 2025 Standard - aktivovaný
- RDS Session Host + Licensing nainštalované
- 50 Device CAL licencie

### Remote Access (Tailscale)
- Tailscale VPN funkčný
- Server: 100.107.134.104
- Kolega (desktop-tibi): 100.67.176.24
- RDP cez Tailscale funguje
- IPtables pravidlá uložené

---

## 🎯 CIELE TEJTO SESSION

### 1. Docker Compose Stack (HIGH priority)
- [ ] Vytvoriť /opt/nex-automat adresár
- [ ] Vytvoriť Docker volumes na /data
- [ ] Nasadiť docker-compose.yml
- [ ] Vytvoriť .env súbor s heslami
- [ ] Spustiť kontajnery: PostgreSQL, Temporal, Temporal UI
- [ ] Vytvoriť systemd service pre auto-start

### 2. Windows VM Software (HIGH priority)
- [ ] Python 32-bit (pre Btrieve)
- [ ] Python 64-bit (pre GUI)
- [ ] Git
- [ ] NSSM (Windows Service Manager)
- [ ] Pervasive PSQL (Btrieve driver) - ak je dostupný

### 3. Sieťová integrácia (HIGH priority)
- [ ] PostgreSQL dostupný z Windows VM
- [ ] Test pripojenia Linux ↔ Windows

---

## 📋 SERVER INFO

### Ubuntu Host
- **LAN IP:** 192.168.100.23
- **Tailscale IP:** 100.107.134.104
- **User:** andros
- **Password:** MagNet-lin-1968
- **SSH:** ssh andros@192.168.100.23

### Windows VM
- **Internal IP:** 192.168.122.75
- **RDP:** 100.107.134.104 (cez Tailscale)
- **User:** Administrator

### Storage
- **Root (/):** NVMe SSD 1TB
- **Data (/data):** RAID 10 4.4TB
- **Docker volumes:** /data/docker-volumes/

### Tailscale
- **Účet:** iccforai@gmail.com
- **Admin:** https://login.tailscale.com/admin/machines

---

## 📊 RAM Rozdelenie (plánované)

| Komponent | RAM |
|-----------|-----|
| Ubuntu Host OS | 8 GB |
| Docker - PostgreSQL | 16 GB |
| Docker - Ollama | 96 GB |
| Docker - Temporal | 4 GB |
| Docker - NEX Automat API | 8 GB |
| Docker - Qdrant | 48 GB |
| Docker - Nginx | 1 GB |
| Windows VM (KVM) | 49 GB |
| Rezerva | ~26 GB |

---

## 🔧 DOCKER COMPOSE KONFIGURÁCIA

### Cieľová štruktúra
```
/opt/nex-automat/
├── docker-compose.yml
├── .env
├── nginx/
│   └── nginx.conf
└── Dockerfile.* (ak potrebné)

/data/docker-volumes/
├── postgres/
├── ollama/
├── qdrant/
└── temporal/
```

### Služby na nasadenie (Phase 1)
1. **PostgreSQL** - hlavná databáza
2. **Temporal Server** - workflow orchestration
3. **Temporal UI** - web rozhranie

### Služby na neskôr (Phase 2)
4. Ollama - LLM
5. Qdrant - Vector DB
6. NEX Automat API
7. NEX Worker
8. Nginx

---

## 📚 RAG QUERIES

```
https://rag-api.icc.sk/search?query=Docker+compose+PostgreSQL+Temporal&limit=5
https://rag-api.icc.sk/search?query=ANDROS+deployment+docker+volumes&limit=5
https://rag-api.icc.sk/search?query=Windows+Python+Pervasive+Btrieve&limit=5
```

---

## ⚠️ DÔLEŽITÉ POZNÁMKY

1. **Docker volumes na RAID** - /data/docker-volumes/ pre perzistenciu
2. **PostgreSQL heslo** - použiť silné heslo, uložiť do .env
3. **Temporal** - použiť auto-setup image pre jednoduchosť
4. **Windows VM** - potrebuje prístup k PostgreSQL na porte 5432
5. **Sieť** - VM je na 192.168.122.0/24 (virbr0 bridge)

---

## 🚀 ZAČAŤ S

```bash
ssh andros@192.168.100.23
```

Prvý krok: Vytvoriť adresárovú štruktúru pre Docker.