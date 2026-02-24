# INIT PROMPT - ANDROS s.r.o. Deployment V2

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Typ:** Čistá inštalácia - Hybrid Linux + Windows  
**Architektúra:** Ubuntu Server 24.04 LTS + Windows Server 2025 VM  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🖥️ Hardware Konfigurácia

| Komponent | Špecifikácia |
|-----------|--------------|
| Server | Dell PowerEdge R740XD 24 bay 2U RACK |
| CPU | 2x Intel Xeon Gold 6138 (40 jadier / 80 vlákien) |
| RAM | 256GB DDR4 2666 |
| RAID | H740p controller |
| Storage | 8x 1.2TB SAS 10K RPM + 1TB NVMe SSD |
| Sieť | 2x 1GbE + 2x 10GbE RJ45 |
| Management | iDRAC Enterprise |
| Napájanie | 2x 750W redundant |

---

## 🏗️ Architektúra - Variant 4 (Linux + Windows VM)

```
┌─────────────────────────────────────────────────────────────────┐
│              HARDVÉR (Dell R740XD - 256 GB RAM)                 │
├─────────────────────────────────────────────────────────────────┤
│                  Ubuntu Server 24.04 LTS                        │
│                      + KVM/Libvirt                              │
├────────────────────────────┬────────────────────────────────────┤
│   LINUX NATÍVNE (192 GB)   │    WINDOWS VM - KVM (48 GB)       │
│   ┌──────────────────────┐ │ ┌────────────────────────────────┐ │
│   │ Docker Containers    │ │ │ Windows Server 2025            │ │
│   │ ├─ PostgreSQL (16GB) │ │ │ ├─ RDS (50 Device CAL)         │ │
│   │ ├─ Ollama (96GB)     │ │ │ ├─ NEX Genesis (Pascal ERP)    │ │
│   │ ├─ Temporal (4GB)    │ │ │ ├─ PySide6 GUI Aplikácie       │ │
│   │ ├─ NEX Automat (8GB) │ │ │ └─ Pervasive PSQL (Btrieve)    │ │
│   │ ├─ Qdrant (48GB)     │ │ └────────────────────────────────┘ │
│   │ └─ Nginx Proxy       │ │                                    │
│   └──────────────────────┘ │                                    │
│   + Rezerva: 32 GB         │                                    │
└────────────────────────────┴────────────────────────────────────┘
```

---

## 📊 RAM Rozdelenie (256 GB)

| Komponent | RAM | Účel |
|-----------|-----|------|
| **Ubuntu Host OS** | 8 GB | Kernel, systémové procesy |
| **Docker - PostgreSQL** | 16 GB | Hlavná DB + shared_buffers |
| **Docker - Ollama** | 96 GB | Llama 3 70B model |
| **Docker - Temporal** | 4 GB | Workflow orchestration |
| **Docker - NEX Automat API** | 8 GB | FastAPI služby |
| **Docker - Qdrant** | 48 GB | Vector DB (~500K docs v RAM) |
| **Docker - Nginx** | 1 GB | Reverse proxy |
| **Windows VM (KVM)** | 48 GB | RDS + NEX Genesis + GUI |
| **Rezerva** | 27 GB | Cache, spike, rast |
| **Celkom** | **256 GB** | |

---

## 📋 Deployment Phases

### Phase 0: RAID + SSD Konfigurácia (PRED inštaláciou) ✅

**RAID 10 pre HDD:**
| Parameter | Hodnota |
|-----------|---------|
| RAID Level | RAID 10 |
| Disky | 8x 1.2TB SAS 10K |
| Kapacita | ~4.4TB |
| Mount | /data |
| Použitie | VMs, Docker volumes, zálohy |

**NVMe SSD:**
| Parameter | Hodnota |
|-----------|---------|
| Typ | WD_BLACK SN7100 NVMe |
| Kapacita | 1TB |
| Mount | / |
| Použitie | Ubuntu OS |

---

### Phase 1: Ubuntu Server 24.04 LTS Inštalácia ✅

```bash
# Partície (NVMe SSD)
# /boot/efi   1GB     vfat
# /boot       2GB     ext4 (na RAID)
# /           915GB   ext4 (NVMe)

# Nainštalované služby
- Docker + docker-compose-v2
- KVM/libvirt (qemu-kvm, libvirt-daemon-system)
- Tailscale VPN
- WireGuard VPN
- Nginx
- OpenSSH server
```

**Prihlasovacie údaje:**
- **User:** andros
- **Password:** Andros-2026

---

### Phase 2: Storage Mount (RAID array) ✅

```bash
# RAID mount
/dev/sda3 /data ext4 defaults 0 2

# Adresárová štruktúra
/data/
├── vms/
│   └── win2025.qcow2      # Windows VM disk (200GB)
├── docker-volumes/
│   ├── postgres/
│   ├── ollama/
│   ├── qdrant/
│   ├── temporal/
│   ├── prometheus/
│   ├── grafana/
│   └── alertmanager/
└── backups/
```

---

### Phase 3: Docker Compose Stack ✅

**Umiestnenie:** `/opt/nex-automat/`

| Služba | Container | Port | Status |
|--------|-----------|------|--------|
| PostgreSQL | nex-postgres | 5432 | ✅ |
| Temporal | nex-temporal | 7233 | ✅ |
| Temporal UI | nex-temporal-ui | 8080 | ✅ |
| Ollama | nex-ollama | 11434 | ✅ |
| Qdrant | nex-qdrant | 6333/6334 | ✅ |
| NEX Brain API | nex-brain | 8000 | ✅ |
| Telegram Bots | nex-telegram | - | ✅ |
| Prometheus | nex-prometheus | 9090 | ✅ |
| Grafana | nex-grafana | 3000 | ✅ |
| Alertmanager | nex-alertmanager | 9093 | ✅ |
| Node Exporter | nex-node-exporter | 9100 | ✅ |
| cAdvisor | nex-cadvisor | 8081 | ✅ |
| Postgres Exporter | nex-postgres-exporter | 9187 | ✅ |

---

### Phase 4: Windows Server 2025 VM (KVM) ✅

```bash
# VM konfigurácia
VM Name:     win2025
RAM:         48GB (49152 MB)
vCPU:        8
Disk:        200GB (qcow2, /data/vms/win2025.qcow2)
Network:     virtio, NAT (192.168.122.0/24)
Internal IP: 192.168.122.75

# Autostart
sudo virsh autostart win2025

# Správa VM
virsh list --all
sudo virsh start win2025
sudo virsh shutdown win2025
```

**Windows konfigurácia:**
| Parameter | Hodnota |
|-----------|---------|
| Edícia | Windows Server 2025 Standard |
| Licencia | ✅ Aktivovaná |
| RDS Session Host | ✅ Nainštalovaný |
| RDS Licensing | ✅ 50 Device CAL |
| User | Administrator |

---

### Phase 5: Windows VM - Interná konfigurácia ✅

**Nainštalovaný software:**
| Software | Verzia | Cesta |
|----------|--------|-------|
| Python 32-bit | 3.11.9 | C:\Python311-32 |
| Python 64-bit | 3.11.9 | C:\Python311-64 |
| Git | 2.52.0 | PATH |
| NSSM | 2.24 | C:\Windows\System32 |
| PowerShell | 7.5.4 | pwsh |
| Pervasive PSQL | 11+ | - |

**Adresárová štruktúra (Windows VM):**
```
C:\NEX\                             # NEX súbory
    ├── IMPORT\SUPPLIER-INVOICES\   # Prijaté PDF
    ├── IMPORT\SUPPLIER-STAGING\    # Staging
    ├── IMPORT\SUPPLIER-ARCHIVE\    # Archív
    └── YEARACT\STORES\             # Btrieve súbory

C:\Apps\                            # Aplikácie
    ├── nex-genesis\                # Pascal ERP
    └── gui-apps\                   # PySide6 aplikácie
```

---

### Phase 6: Sieťová Komunikácia Linux ↔ Windows ✅

```
┌─────────────────────┐         ┌─────────────────────┐
│    Ubuntu Host      │         │    Windows VM       │
│   192.168.122.1     │◄───────►│   192.168.122.75    │
├─────────────────────┤  bridge ├─────────────────────┤
│ PostgreSQL:5432     │         │ Btrieve Access      │
│ Temporal:7233       │         │ RDP:3389            │
│ API:8000            │         │ SMB shares          │
│ Ollama:11434        │         │                     │
│ Grafana:3000        │         │                     │
│ Prometheus:9090     │         │                     │
└─────────────────────┘         └─────────────────────┘
```

**Tailscale VPN:**
| Zariadenie | Tailscale IP |
|------------|--------------|
| nex-andros-server | 100.107.134.104 |

**RDP prístup cez Tailscale:**
```
100.107.134.104:3389 → 192.168.122.75:3389 (iptables DNAT)
```

---

### Phase 7: Ollama Model Setup ✅

```bash
# Nainštalované modely
ollama list

# Modely
| Model            | Veľkosť | Účel                    |
|------------------|---------|-------------------------|
| llama3.1:8b      | 4.9 GB  | LLM pre chat/generovanie|
| nomic-embed-text | 274 MB  | Embedding pre RAG       |
```

---

### Phase 8: Nginx Reverse Proxy ✅

**Konfigurácia:** `/etc/nginx/sites-available/andros.conf`

| URL | Služba |
|-----|--------|
| https://100.107.134.104/ | Hlavná stránka |
| https://100.107.134.104/api/ | NEX Brain API |
| https://100.107.134.104/temporal/ | Temporal UI |
| https://100.107.134.104/qdrant/ | Qdrant Dashboard |

**LAN prístup (bez HTTPS):**
| URL | Služba |
|-----|--------|
| http://192.168.100.23:3000 | Grafana |
| http://192.168.100.23:9090 | Prometheus |
| http://192.168.100.23:9093 | Alertmanager |

---

### Phase 9: Monitoring ✅

**Komponenty:**
- Prometheus (metriky)
- Grafana (vizualizácia)
- Alertmanager (notifikácie → Telegram)
- Node Exporter (systémové metriky)
- cAdvisor (Docker metriky)
- Postgres Exporter (PostgreSQL metriky)

**Grafana Dashboardy:**
| Dashboard | Grafana ID |
|-----------|------------|
| Node Exporter Full | 1860 |
| cAdvisor Exporter | 14282 |
| PostgreSQL Database | 9628 |

**Grafana prístup:**
- URL: http://192.168.100.23:3000
- User: admin
- Password: Andros-2026

**Telegram Alerty:**
- Bot: @ai_dev_automatin_bot
- Alerty: CPU, RAM, Disk, Container, PostgreSQL

---

### Phase 10: Telegram Bots ✅

| Bot | Username | Účel |
|-----|----------|------|
| Admin | @ai_dev_automatin_bot | Admin notifikácie, monitoring |
| ICC | @NexBrainIcc_bot | ICC zákazníci |
| ANDROS | @NexBrainAndros_bot | ANDROS zákazníci |

---

## 📊 Success Criteria

| Kritérium | Status |
|-----------|--------|
| Docker kontajnery running | ✅ |
| PostgreSQL pripojenie | ✅ |
| Temporal UI dostupné | ✅ |
| Ollama model loaded | ✅ |
| Qdrant zdravý | ✅ |
| Windows VM bootuje | ✅ |
| RDP funguje | ✅ |
| Sieťová komunikácia Linux↔Windows | ✅ |
| Monitoring (Prometheus/Grafana) | ✅ |
| Telegram notifikácie | ✅ |

---

## 🔗 RAG Queries

```
https://rag-api.icc.sk/search?query=ANDROS+Docker+deployment&limit=5
https://rag-api.icc.sk/search?query=ANDROS+Windows+Server+2025&limit=5
https://rag-api.icc.sk/search?query=ANDROS+monitoring+Prometheus+Grafana&limit=5
https://rag-api.icc.sk/search?query=ANDROS+Tailscale+VPN&limit=5
```

---

## ⚠️ Dôležité Poznámky

1. **Hybrid architektúra** - Linux pre výkon, Windows pre legacy/GUI
2. **256GB RAM** - optimálne rozdelené medzi služby
3. **Docker na NVMe SSD** - kritické pre výkon
4. **Windows VM na RAID** - dostatočné pre RDS
5. **Zálohy** - VM snapshots + PostgreSQL pg_dump
6. **Tailscale** - VPN prístup kvôli ISP obmedzeniam port forwardingu

---

## 📅 Deployment History

| Dátum | Fáza | Status |
|-------|------|--------|
| 2025-01-15 | Ubuntu + RAID + KVM | ✅ |
| 2025-01-15 | Windows Server 2025 VM | ✅ |
| 2025-01-15 | RDS + 50 CAL licencie | ✅ |
| 2026-01-16 | Docker Stack | ✅ |
| 2026-01-16 | Nginx + Telegram | ✅ |
| 2026-01-16 | Monitoring | ✅ |