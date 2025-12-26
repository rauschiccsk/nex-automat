# INIT PROMPT - ANDROS s.r.o. Deployment V2

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Typ:** Čistá inštalácia - Hybrid Linux + Windows  
**Architektúra:** Ubuntu Server 24.04 LTS + Windows Server 2022 VM  
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
| Storage | 8x 1.2TB SAS 10K RPM + 1x SSD (dokúpiť) |
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
│   LINUX NATÍVNE (192 GB)   │    WINDOWS VM - KVM (32-48 GB)    │
│   ┌──────────────────────┐ │ ┌────────────────────────────────┐ │
│   │ Docker Containers    │ │ │ Windows Server 2022            │ │
│   │ ├─ PostgreSQL (16GB) │ │ │ ├─ RDS (5-10 užívateľov)       │ │
│   │ ├─ Ollama (96GB)     │ │ │ ├─ NEX Genesis (Pascal ERP)    │ │
│   │ ├─ Temporal (4GB)    │ │ │ ├─ PyQt5 GUI Aplikácie         │ │
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
| **Windows VM (KVM)** | 32 GB | RDS + NEX Genesis + GUI |
| **Rezerva** | 43 GB | Cache, spike, rast |
| **Celkom** | **256 GB** | |

---

## 📋 Deployment Phases

### Phase 0: RAID + SSD Konfigurácia (PRED inštaláciou)

**RAID 10 pre HDD:**
| Parameter | Hodnota |
|-----------|---------|
| RAID Level | RAID 10 |
| Disky | 8x 1.2TB SAS 10K |
| Kapacita | ~4.8TB |
| Použitie | Dáta, zálohy, VM storage |

**SSD (dokúpiť):**
| Parameter | Hodnota |
|-----------|---------|
| Typ | SATA SSD alebo NVMe |
| Kapacita | 500GB - 1TB |
| Použitie | OS, Docker, PostgreSQL |

**Postup RAID:**
1. Boot → F2 (System Setup) alebo Ctrl+R
2. Device Settings → RAID Controller (H740p)
3. Create Virtual Disk → RAID 10
4. Vybrať všetkých 8 HDD diskov
5. Strip Size: 256KB
6. Read Policy: Adaptive Read Ahead
7. Write Policy: Write Back (s BBU)

---

### Phase 1: Ubuntu Server 24.04 LTS Inštalácia

```bash
# Inštalácia na SSD
# Partition layout:
# /boot/efi   512MB   EFI System
# /boot       1GB     ext4
# /           100GB   ext4 (root)
# /var        300GB   ext4 (Docker, logs)
# swap        32GB    swap

# Po inštalácii - základné balíky
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    vim htop tmux git curl wget \
    net-tools openssh-server \
    qemu-kvm libvirt-daemon-system \
    libvirt-clients bridge-utils virt-manager \
    docker.io docker-compose-v2 \
    nginx certbot python3-certbot-nginx

# Docker bez sudo
sudo usermod -aG docker $USER
sudo usermod -aG libvirt $USER

# Firewall
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3389/tcp   # RDP pre Windows VM
sudo ufw allow 5432/tcp   # PostgreSQL (len interné)
sudo ufw allow 7233/tcp   # Temporal
sudo ufw allow 8000/tcp   # NEX Automat API
sudo ufw allow 8233/tcp   # Temporal UI
sudo ufw enable
```

---

### Phase 2: Storage Mount (RAID array)

```bash
# Identifikácia RAID virtual disk
lsblk
# Typicky /dev/sdb pre RAID array

# Partition a format
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary ext4 0% 100%
sudo mkfs.ext4 /dev/sdb1

# Mount
sudo mkdir -p /data
sudo mount /dev/sdb1 /data

# Permanent mount
echo '/dev/sdb1 /data ext4 defaults 0 2' | sudo tee -a /etc/fstab

# Adresárová štruktúra
sudo mkdir -p /data/{vms,backups,nex-files,docker-volumes}
sudo chown -R $USER:$USER /data
```

---

### Phase 3: Docker Compose Stack

**Súbor:** `/opt/nex-automat/docker-compose.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: nex-postgres
    restart: always
    environment:
      POSTGRES_USER: nex
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: supplier_invoice_staging
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          memory: 16G
    command: >
      postgres
      -c shared_buffers=4GB
      -c effective_cache_size=12GB
      -c maintenance_work_mem=1GB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=64MB
      -c default_statistics_target=100
      -c random_page_cost=1.1
      -c effective_io_concurrency=200

  # Temporal Server
  temporal:
    image: temporalio/auto-setup:latest
    container_name: nex-temporal
    restart: always
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=nex
      - POSTGRES_PWD=${POSTGRES_PASSWORD}
      - POSTGRES_SEEDS=postgres
    depends_on:
      - postgres
    ports:
      - "7233:7233"
    deploy:
      resources:
        limits:
          memory: 4G

  # Temporal UI
  temporal-ui:
    image: temporalio/ui:latest
    container_name: nex-temporal-ui
    restart: always
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    depends_on:
      - temporal
    ports:
      - "8233:8080"

  # Ollama (LLM)
  ollama:
    image: ollama/ollama:latest
    container_name: nex-ollama
    restart: always
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        limits:
          memory: 96G

  # Qdrant (Vector DB)
  qdrant:
    image: qdrant/qdrant:latest
    container_name: nex-qdrant
    restart: always
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
      - "6334:6334"
    deploy:
      resources:
        limits:
          memory: 48G

  # NEX Automat API
  nex-automat-api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: nex-automat-api
    restart: always
    environment:
      - DATABASE_URL=postgresql://nex:${POSTGRES_PASSWORD}@postgres:5432/supplier_invoice_staging
      - TEMPORAL_HOST=temporal
      - TEMPORAL_PORT=7233
      - OLLAMA_HOST=ollama
      - QDRANT_HOST=qdrant
    depends_on:
      - postgres
      - temporal
      - ollama
      - qdrant
    ports:
      - "8000:8000"
    deploy:
      resources:
        limits:
          memory: 8G

  # NEX Temporal Worker
  nex-worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
    container_name: nex-worker
    restart: always
    environment:
      - DATABASE_URL=postgresql://nex:${POSTGRES_PASSWORD}@postgres:5432/supplier_invoice_staging
      - TEMPORAL_HOST=temporal
      - TEMPORAL_PORT=7233
      - OLLAMA_HOST=ollama
    depends_on:
      - postgres
      - temporal
      - ollama
    deploy:
      resources:
        limits:
          memory: 4G

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nex-nginx
    restart: always
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - nex-automat-api
      - temporal-ui

volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/docker-volumes/postgres
  ollama_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/docker-volumes/ollama
  qdrant_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/docker-volumes/qdrant
```

**Environment súbor:** `/opt/nex-automat/.env`
```env
POSTGRES_PASSWORD=SecurePassword2025!
LS_API_KEY=andros-api-key-2025
```

---

### Phase 4: Windows Server 2022 VM (KVM)

```bash
# Vytvorenie VM storage
mkdir -p /data/vms/windows-server

# Stiahnutie Windows Server 2022 ISO
# (manuálne z Microsoft Evaluation Center)

# Vytvorenie VM
sudo virt-install \
  --name windows-server-2022 \
  --ram 32768 \
  --vcpus 8 \
  --cpu host \
  --os-variant win2k22 \
  --disk path=/data/vms/windows-server/disk.qcow2,size=200,format=qcow2,bus=virtio \
  --network bridge=virbr0,model=virtio \
  --graphics vnc,listen=0.0.0.0,port=5900 \
  --cdrom /data/iso/windows-server-2022.iso \
  --boot cdrom,hd

# Po inštalácii Windows - VirtIO drivers
# Stiahnuť: https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/

# Nastavenie autostart
sudo virsh autostart windows-server-2022
```

**Windows VM Konfigurácia:**
| Parameter | Hodnota |
|-----------|---------|
| RAM | 32 GB (dynamicky do 48 GB) |
| vCPU | 8 jadier |
| Disk | 200 GB (qcow2 na RAID) |
| Sieť | Bridge (získa IP z DHCP/static) |
| RDP Port | 3389 |

---

### Phase 5: Windows VM - Interná konfigurácia

**Inštalovať na Windows VM:**
| Software | Verzia | Účel |
|----------|--------|------|
| Python 32-bit | 3.12.x | Btrieve/Pervasive |
| Python 64-bit | 3.12.x | GUI aplikácie |
| Pervasive PSQL | 11+ | Btrieve driver |
| Git | 2.40+ | Deployment |
| NSSM | 2.24 | Windows Services |

**RDS Konfigurácia:**
```powershell
# Inštalácia RDS role
Install-WindowsFeature -Name RDS-RD-Server -IncludeManagementTools

# Povoliť Remote Desktop
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"

# Vytvoriť užívateľov
$users = @("user1", "user2", "user3")
foreach ($user in $users) {
    New-LocalUser -Name $user -Password (ConvertTo-SecureString "Password123!" -AsPlainText -Force)
    Add-LocalGroupMember -Group "Remote Desktop Users" -Member $user
}
```

**Adresárová štruktúra (Windows VM):**
```
C:\NEX\                             # NEX súbory
    ├── IMPORT\SUPPLIER-INVOICES\   # Prijaté PDF
    ├── IMPORT\SUPPLIER-STAGING\    # Staging
    ├── IMPORT\SUPPLIER-ARCHIVE\    # Archív
    └── YEARACT\STORES\             # Btrieve súbory

C:\Apps\                            # Aplikácie
    ├── nex-genesis\                # Pascal ERP
    └── gui-apps\                   # PyQt5 aplikácie
```

---

### Phase 6: Sieťová Komunikácia Linux ↔ Windows

```
┌─────────────────┐         ┌─────────────────┐
│  Ubuntu Host    │         │  Windows VM     │
│  192.168.122.1  │◄───────►│  192.168.122.10 │
├─────────────────┤  bridge ├─────────────────┤
│ PostgreSQL:5432 │         │ Btrieve Access  │
│ Temporal:7233   │         │ RDP:3389        │
│ API:8000        │         │ SMB shares      │
│ Ollama:11434    │         │                 │
└─────────────────┘         └─────────────────┘
```

**Windows prístup k Linux službám:**
```
PostgreSQL: 192.168.122.1:5432
Temporal:   192.168.122.1:7233
API:        192.168.122.1:8000
Ollama:     192.168.122.1:11434
```

**Linux prístup k Windows:**
```bash
# SMB share pre NEX súbory
sudo mount -t cifs //192.168.122.10/NEX /mnt/nex-files -o username=admin,password=xxx
```

---

### Phase 7: Ollama Model Setup

```bash
# Pripojiť sa do Ollama kontajnera
docker exec -it nex-ollama bash

# Stiahnuť modely
ollama pull llama3:70b          # Hlavný model (~40GB)
ollama pull nomic-embed-text    # Embedding model (~270MB)

# Test
ollama run llama3:70b "Ahoj, ako sa máš?"
```

---

### Phase 8: Nginx Reverse Proxy

**Súbor:** `/opt/nex-automat/nginx/nginx.conf`

```nginx
events {
    worker_connections 1024;
}

http {
    upstream nex_api {
        server nex-automat-api:8000;
    }

    upstream temporal_ui {
        server temporal-ui:8080;
    }

    server {
        listen 80;
        server_name andros.nex-automat.sk;

        location / {
            proxy_pass http://nex_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /temporal/ {
            proxy_pass http://temporal_ui/;
            proxy_set_header Host $host;
        }
    }
}
```

---

### Phase 9: Systemd Services (Linux)

```bash
# Docker Compose ako systemd service
sudo tee /etc/systemd/system/nex-automat.service << 'EOF'
[Unit]
Description=NEX Automat Docker Stack
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/nex-automat
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable nex-automat
sudo systemctl start nex-automat
```

---

### Phase 10: Verifikácia

```bash
# Docker kontajnery
docker ps

# Health checks
curl http://localhost:8000/health          # NEX API
curl http://localhost:7233                  # Temporal
curl http://localhost:11434/api/tags       # Ollama
curl http://localhost:6333/dashboard       # Qdrant

# Windows VM
sudo virsh list --all
# RDP test: xfreerdp /v:192.168.122.10 /u:admin

# Logy
docker logs nex-automat-api
docker logs nex-ollama
```

---

## 📊 Success Criteria

| Kritérium | Cieľ |
|-----------|------|
| Docker kontajnery running | ✅ |
| PostgreSQL pripojenie | ✅ |
| Temporal UI dostupné | ✅ |
| Ollama model loaded | ✅ |
| Qdrant zdravý | ✅ |
| Windows VM bootuje | ✅ |
| RDP funguje | ✅ |
| Sieťová komunikácia Linux↔Windows | ✅ |

---

## 🔗 RAG Queries

```
https://rag-api.icc.sk/search?query=Docker+compose+PostgreSQL+Temporal&limit=5
https://rag-api.icc.sk/search?query=KVM+Windows+Server+VM+setup&limit=5
https://rag-api.icc.sk/search?query=Ollama+Llama+70B+deployment&limit=5
https://rag-api.icc.sk/search?query=Qdrant+vector+database+setup&limit=5
```

---

## ⚠️ Dôležité Poznámky

1. **Hybrid architektúra** - Linux pre výkon, Windows pre legacy/GUI
2. **256GB RAM** - optimálne rozdelené medzi služby
3. **Docker na SSD** - kritické pre výkon
4. **Windows VM na RAID** - dostatočné pre RDS
5. **Zálohy** - VM snapshots + PostgreSQL pg_dump

---

## 🔄 Migrácia zo starého ANDROS servera

| Čo migrovať | Z (starý) | Do (nový) |
|-------------|-----------|-----------|
| NEX Genesis dáta | C:\NEX\ | Windows VM: C:\NEX\ |
| Btrieve súbory | C:\NEX\YEARACT\ | Windows VM: C:\NEX\YEARACT\ |
| PostgreSQL DB | localhost | Docker: postgres:5432 |
| PDF archív | D:\Data | /data/nex-files/ |

---

## 📅 Estimated Timeline

| Fáza | Čas |
|------|-----|
| Phase 0-1: RAID + Ubuntu | 2 hodiny |
| Phase 2-3: Storage + Docker | 2 hodiny |
| Phase 4-5: Windows VM | 3 hodiny |
| Phase 6-7: Networking + Ollama | 2 hodiny |
| Phase 8-10: Nginx + Verifikácia | 1 hodina |
| **Celkom** | **~10 hodín** |