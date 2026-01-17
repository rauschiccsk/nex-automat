# INIT PROMPT - ANDROS s.r.o. Deployment v2

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2025-01-13  
**Session:** Ubuntu Reinstall - EFI Boot Fix

---

## ✅ DOKONČENÉ

### Hardware
- Dell R740XD server operational
- RAID 10 array: 8×1.2TB SAS → 4.364TB (funguje)
- NVMe SSD: WD_BLACK_SN7100 1TB (931.5GB) - rozpoznaný ako /dev/nvme0n1
- Sieť: eno4 - 192.168.100.23/24 (DHCP)

### Prvá Ubuntu inštalácia (NEÚSPEŠNÁ)
- Ubuntu 24.04.3 LTS nainštalovaný s custom partíciami
- Partície vytvorené správne:
  - nvme0n1p1: 1G EFI (fat32, /boot/efi)
  - nvme0n1p2: 1G ext4 (/boot)
  - nvme0n1p3: 100G ext4 (/)
  - nvme0n1p4: 350G ext4 (/var)
  - nvme0n1p5: 32G swap
- EFI súbory existujú: /EFI/ubuntu/shimx64.efi, grubx64.efi, grub.cfg

---

## ❌ PROBLÉM

**BIOS nevidí EFI partíciu na NVMe SSD:**
- Boot Manager → "Unavailable: Ubuntu"
- Boot From File → "There are no filesystems available"
- Add Boot Option → "There are no filesystems available"

**Diagnóza:**
- EFI partícia pravdepodobne nemá správny ESP flag
- Custom partitioning v Ubuntu installer nevytvoril EFI partition správne
- NVMe disk funguje (Linux ho vidí), ale UEFI BIOS ho nevidí ako bootovateľný

---

## 🎯 AKTUÁLNA ÚLOHA

**Preinštalovať Ubuntu s Guided storage** (nie Custom):

1. Boot z USB (F11 → UEFI: USB)
2. Spustiť Ubuntu Server installer
3. Pri "Guided storage configuration":
   - Vybrať **(X) Use an entire disk**
   - Vybrať **WD_BLACK_SN7100** (nie RAID!)
   - Zaškrtnúť **[X] Set up this disk as an LVM group**
   - **NEZAŠKRTÁVAŤ** Encrypt
4. Nechať installer automaticky vytvoriť partície
5. Profile setup:
   - Server name: `andros-nex-server`
   - Username: `andros`
   - Password: `MagNet-lin-1968`
6. SSH: Enable OpenSSH server
7. Snaps: Skip all
8. Reboot a overiť boot

---

## 📋 PO ÚSPEŠNOM BOOTE

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

## ⚠️ POZNÁMKY

- RAID array (4.364TB) zostáva nedotknutý
- Guided storage použije celý SSD, ale to je OK
- LVM umožní neskoršie resize partícií
- Po úspešnom boote pokračujeme s Docker stack deployment

---

## 📞 SERVER INFO

- **Model:** Dell PowerEdge R740XD 24 bay 2U
- **CPU:** 2x Intel Xeon Gold 6138 (40c/80t)
- **RAM:** 256GB DDR4
- **Service Tag:** GZ5L3N2
- **Network:** 192.168.100.23 (eno4)