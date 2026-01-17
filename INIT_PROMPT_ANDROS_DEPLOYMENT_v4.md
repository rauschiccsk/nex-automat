# INIT PROMPT - ANDROS s.r.o. Deployment v4

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2025-01-14  
**Session:** Ubuntu inštalácia - dokončenie

---

## ✅ DOKONČENÉ

### Hardware
- Dell R740XD server operational
- RAID 10 array: 8×1.2TB SAS → 4.364TB (funguje)
- NVMe SSD: WD_BLACK_SN7100 1TB (Sandisk Corp) v PCIe Slot 1
- Sieť: eno4 - 192.168.100.23/24 (DHCP)

### Firmware Updates (všetky dokončené)
- **BIOS:** 2.5.4 → 2.25.0 ✅
- **iDRAC:** 4.10.10.10 → 7.00.00.183 ✅

### iDRAC Setup
- iDRAC 9 Enterprise: https://192.168.100.50
- Username: root
- Firmware: 7.00.00.183

### NVMe Boot Problém - VYRIEŠENÉ WORKAROUNDOM
- BIOS nevidí NVMe SSD ako boot device (PCIe adaptér nie je bootovateľný)
- iDRAC vidí NVMe ako "PCIe Device - PCIe SSD in Slot 1 Disk 1"
- Ubuntu inštalátor vidí NVMe disk
- **Riešenie:** Boot partície na NVMe (ESP existovala), root na NVMe, /data na RAID

---

## 🔄 AKTUÁLNY STAV

**Ubuntu 24.04 inštalácia prebieha**

### Storage konfigurácia (nastavená v inštalátore):

| Mount Point | Disk | Veľkosť | Filesystem |
|-------------|------|---------|------------|
| /boot/efi | NVMe (WD_BLACK) partition 1 | 1.049G | vfat (ESP) |
| / | NVMe (WD_BLACK) partition 2 | 930.460G | ext4 (NOVÝ FORMÁT) |
| /data | RAID array | 4.364T | ext4 |

### Predchádzajúca chyba - OPRAVENÁ:
- `dpkg-divert: error: rename involves overwriting` - spôsobené použitím existujúcej partície bez preformátovania
- **Fix:** Zmenené Format z "Leave formatted as ext4" na "ext4" (nový formát)

---

## 🎯 ĎALŠIE KROKY

### 1. Dokončiť Ubuntu inštaláciu
- Počkať na dokončenie inštalácie
- Reštartovať server
- Overiť či server nabootuje z NVMe

### 2. Ak boot funguje - Post-install konfigurácia:
```bash
# Update systému
sudo apt update && sudo apt upgrade -y

# Základné balíky
sudo apt install -y vim htop tmux git curl wget \
    net-tools qemu-kvm libvirt-daemon-system \
    libvirt-clients bridge-utils \
    docker.io docker-compose-v2 nginx

# User permissions
sudo usermod -aG docker $USER
sudo usermod -aG libvirt $USER

# Overiť /data mount
df -h /data

# Reboot pre group permissions
sudo reboot
```

### 3. Ak boot NEFUNGUJE - Záložný plán:
- Presunúť /boot/efi a /boot na RAID array
- Reinštalovať Ubuntu s boot partíciami na RAID

---

## 🗂️ CIEĽOVÁ ARCHITEKTÚRA

### Storage:
- **NVMe SSD** (WD_BLACK 1TB): Ubuntu OS + Docker (/, /boot/efi)
- **RAID 10** (4.364TB): /data - VMs, backups, persistent volumes

### Docker Stack (plánovaný):

| Service | RAM | Purpose |
|---------|-----|---------|
| postgres | 16 GB | Hlavná databáza |
| temporal | 4 GB | Workflow orchestration |
| ollama | 96 GB | Llama 3 70B |
| qdrant | 48 GB | Vector DB |
| nex-automat-api | 8 GB | FastAPI |

### Windows VM (KVM):
- RAM: 32-48 GB
- vCPU: 8
- Disk: 200 GB na /data/vms/
- Purpose: RDS + NEX Genesis (Pascal ERP)

---

## 📞 SERVER INFO

- **Model:** Dell PowerEdge R740XD 24 bay 2U
- **CPU:** 2x Intel Xeon Gold 6138 (40c/80t)
- **RAM:** 256GB DDR4
- **Service Tag:** GZ5L3N2
- **BIOS:** 2.25.0
- **iDRAC:** 7.00.00.183 @ https://192.168.100.50

### Credentials:
- **Ubuntu:** andros / MagNet-lin-1968
- **iDRAC:** root / (default password)