# ANDROS s.r.o. - Server Deployment Knowledge Base

**Vytvorené:** 2025-01-15  
**Zákazník:** ANDROS s.r.o.  
**Projekt:** NEX Genesis Server + NEX Automat

---

## 1. HARDWARE

### Server
- **Model:** Dell PowerEdge R740XD 24 bay 2U
- **CPU:** 2x Intel Xeon Gold 6138 (40 cores / 80 threads)
- **RAM:** 256GB DDR4 (8x 32GB, 2400 MT/s)
- **Service Tag:** GZ5L3N2

### Storage
| Typ | Veľkosť | Mount | Účel |
|-----|---------|-------|------|
| NVMe SSD (WD_BLACK SN7100) | 1TB | / | Ubuntu OS |
| RAID 10 (8x 1.2TB SAS) | 4.4TB | /data | VMs, Docker volumes, backups |

### Sieť
- **eno4:** 192.168.100.23/24 (Gigabit, hlavná sieť)
- **iDRAC:** 192.168.100.50 (management)

---

## 2. UBUNTU 24.04 LTS

### Partície
| Mount | Filesystem | Veľkosť | Disk |
|-------|------------|---------|------|
| / | ext4 | 915GB | NVMe (nvme0n1p2) |
| /boot | ext4 | 2GB | RAID (sda2) |
| /boot/efi | vfat | 1GB | RAID (sda1) |
| /data | ext4 | 4.4TB | RAID (sda3) |

### Prihlasovacie údaje
- **User:** andros
- **Password:** Andros-2026

### Nainštalované služby
- Docker + docker-compose-v2
- KVM/libvirt (qemu-kvm, libvirt-daemon-system)
- WireGuard VPN
- Nginx
- OpenSSH server

---

## 3. WINDOWS SERVER 2025 VM

### VM konfigurácia
- **Meno:** win2025
- **RAM:** 48GB (49152 MB)
- **vCPU:** 8
- **Disk:** 200GB (qcow2, /data/vms/win2025.qcow2)
- **Sieť:** virtio, NAT (192.168.122.0/24)
- **VNC:** 192.168.100.23:5900

### Windows konfigurácia
- **Edícia:** Windows Server 2025 Standard
- **Licencia:** Aktivovaná
- **Internal IP:** 192.168.122.75
- **User:** Administrator

### RDS (Remote Desktop Services)
- RDS Session Host nainštalovaný
- RDS Licensing Server aktivovaný
- 50 Device CAL licencií nainštalovaných

### Port Forwarding
```
192.168.100.23:3389 → 192.168.122.75:3389 (RDP)
```

---

## 4. WIREGUARD VPN

### Server konfigurácia
- **Rozhranie:** wg0
- **Port:** UDP 51820
- **VPN Subnet:** 10.10.0.0/24
- **Server IP:** 10.10.0.1

### Kľúče
| Typ | Hodnota |
|-----|---------|
| Server Public | y8iHIP1j4khFohKEa5hWTniQuhIaKDXzp2TqhlMfHCA= |
| Server Private | MI4e3e8dwnrjPXUSgNc+EgCBO0HKIxnsWwmSLQl/A00= |
| Kolega Public | Uzc0p1/sh/k/ofzF7I4n2enZZX13UmqA0SiPS3qdvnw= |
| Kolega Private | iELeqbkSDITAqAWID98zOuayVwVSFhjG/gjR+K70gl4= |

### Konfiguračný súbor (/etc/wireguard/wg0.conf)
```ini
[Interface]
Address = 10.10.0.1/24
ListenPort = 51820
PrivateKey = MI4e3e8dwnrjPXUSgNc+EgCBO0HKIxnsWwmSLQl/A00=
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eno4 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eno4 -j MASQUERADE

[Peer]
# Kolega
PublicKey = Uzc0p1/sh/k/ofzF7I4n2enZZX13UmqA0SiPS3qdvnw=
AllowedIPs = 10.10.0.2/32
```

### Status
- Server beží a počúva na porte 51820
- Potrebuje DDNS (nemá statickú verejnú IP)
- Potrebuje port forward na routeri (UDP 51820)

---

## 5. IPTABLES PRAVIDLÁ

### NAT (PREROUTING)
```bash
iptables -t nat -A PREROUTING -p tcp -d 192.168.100.23 --dport 3389 -j DNAT --to-destination 192.168.122.75:3389
```

### FORWARD
```bash
iptables -I FORWARD 1 -i eno4 -o virbr0 -d 192.168.122.75 -p tcp --dport 3389 -j ACCEPT
iptables -I FORWARD 2 -i virbr0 -o eno4 -s 192.168.122.75 -p tcp --sport 3389 -j ACCEPT
```

### Persistencia
- Pravidlá uložené cez iptables-persistent
- Súbor: /etc/iptables/rules.v4

---

## 6. UŽITOČNÉ PRÍKAZY

### VM Management
```bash
virsh list --all          # Zoznam všetkých VM
virsh start win2025       # Spustiť VM
virsh shutdown win2025    # Vypnúť VM
virsh destroy win2025     # Force stop VM
```

### WireGuard
```bash
sudo wg show              # Status WireGuard
sudo systemctl restart wg-quick@wg0  # Reštart
```

### Docker
```bash
docker ps                 # Bežiace kontajnery
docker compose up -d      # Spustiť stack
```

### Sieť
```bash
ip addr                   # IP adresy
sudo iptables -L -n -v    # Firewall pravidlá
sudo tcpdump -i eno4 port 3389 -n  # Debug sieť
```

---

## 7. RIEŠENIE PROBLÉMOV

### NVMe Boot problém
- BIOS nevidí NVMe ako boot device
- Riešenie: /boot a /boot/efi na RAID, / na NVMe
- GRUB moduly (vrátane nvme.mod) musia byť na bootovateľnom disku

### DIMM chyba
- DIMM A12 hlásil uncorrectable memory error
- Riešenie: Výmena DIMM medzi slotmi (kontaktný problém)

### RDP nefunguje
- Príčina: LIBVIRT chains blokovali FORWARD pred custom pravidlami
- Riešenie: iptables -I FORWARD 1 (vložiť na začiatok)

### RDS Licensing sivé menu
- Príčina: License server nebol aktivovaný
- Riešenie: Advanced → Reactivate Server