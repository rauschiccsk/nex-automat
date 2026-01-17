# INIT PROMPT - ANDROS s.r.o. Deployment v3

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2025-01-13  
**Session:** BIOS Update cez iDRAC

---

## ✅ DOKONČENÉ

### Hardware
- Dell R740XD server operational
- RAID 10 array: 8×1.2TB SAS → 4.364TB (funguje)
- NVMe SSD: WD_BLACK_SN7100 1TB v PCIe adaptéri
- Sieť: eno4 - 192.168.100.23/24 (DHCP)

### iDRAC Setup
- iDRAC 9 Enterprise prístupný na: https://192.168.100.50
- Username: root
- Password: (default password nastavené v BIOS)
- Firmware: 4.10.10.10

### Ubuntu inštalácia
- Ubuntu 24.04.3 LTS nainštalovaný na NVMe SSD
- Partície vytvorené správne (ESP, /boot, /, LVM)
- OpenSSH server enabled
- Profile: andros / MagNet-lin-1968

---

## ❌ PROBLÉM

**BIOS nevidí NVMe SSD ako boot device:**
- NVMe je v PCIe adaptéri (nie natívny M.2 slot)
- Starší BIOS 2.5.4 nepodporuje boot z PCIe NVMe
- Potrebujeme aktualizovať BIOS na najnovšiu verziu (2.21.2)

---

## 🎯 AKTUÁLNA ÚLOHA

**Aktualizovať BIOS cez iDRAC:**

1. Stiahnuť najnovší BIOS z Dell:
   - URL: https://www.dell.com/support/home/en-us/product-support/servicetag/GZ5L3N2/drivers
   - Hľadať: BIOS, najnovšia verzia (2.21.2 alebo vyššia)
   - Stiahnuť .exe súbor

2. V iDRAC (https://192.168.100.50):
   - Maintenance → System Update
   - Nahrať BIOS súbor
   - Spustiť aktualizáciu

3. Po aktualizácii BIOS:
   - Reštart servera
   - Overiť či BIOS vidí NVMe ako boot device
   - Ak áno, nastaviť boot poradie

---

## 📋 PO ÚSPEŠNOM BOOTE UBUNTU

### Post-install kroky:
```bash
# 1. Update systému
sudo apt update && sudo apt upgrade -y

# 2. Základné balíky
sudo apt install -y vim htop tmux git curl wget \
    net-tools qemu-kvm libvirt-daemon-system \
    libvirt-clients bridge-utils virt-manager \
    docker.io docker-compose-v2 nginx

# 3. User permissions
sudo usermod -aG docker $USER
sudo usermod -aG libvirt $USER

# 4. Mount RAID array
sudo parted /dev/sda mklabel gpt
sudo parted /dev/sda mkpart primary ext4 0% 100%
sudo mkfs.ext4 /dev/sda1
sudo mkdir -p /data
sudo mount /dev/sda1 /data
echo '/dev/sda1 /data ext4 defaults 0 2' | sudo tee -a /etc/fstab

# 5. Adresárová štruktúra
sudo mkdir -p /data/{vms,backups,nex-files,docker-volumes}
sudo mkdir -p /data/docker-volumes/{postgres,ollama,qdrant}
sudo chown -R $USER:$USER /data

# 6. Reboot pre group permissions
sudo reboot
```

---

## 🗂️ CIEĽOVÁ ARCHITEKTÚRA

### Storage:
- **NVMe SSD** (/dev/nvme0n1): Ubuntu OS + Docker
- **RAID 10** (/dev/sda → /data): VMs, backups, persistent volumes

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
- **BIOS:** 2.5.4 → potrebuje update
- **iDRAC:** https://192.168.100.50 (root / default password)