# INIT PROMPT - ANDROS WireGuard VPN Dokončenie v1

**Projekt:** nex-automat v3.0 + NEX Brain  
**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD (256GB RAM, 40c/80t)  
**Developer:** Zoltán Rausch  
**Dátum:** 2025-01-15  
**Session:** WireGuard VPN - dokončenie pre kolegu

---

## ✅ DOKONČENÉ

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
- 50 Device CAL licencie nainštalované
- RDP port forwarding funguje (192.168.100.23:3389 → 192.168.122.75:3389)

### WireGuard Server (čiastočne)
- WireGuard nainštalovaný a beží na Ubuntu
- Server kľúče vygenerované
- Konfigurácia vytvorená
- IP forwarding povolený
- Kľúče pre kolegu vygenerované

---

## 🔄 AKTUÁLNY STAV

**WireGuard server beží, ale potrebuje DDNS**

### Server konfigurácia (/etc/wireguard/wg0.conf):
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

### Server kľúče:
- **Public Key:** y8iHIP1j4khFohKEa5hWTniQuhIaKDXzp2TqhlMfHCA=
- **Private Key:** MI4e3e8dwnrjPXUSgNc+EgCBO0HKIxnsWwmSLQl/A00=

### Kolega kľúče:
- **Private Key:** iELeqbkSDITAqAWID98zOuayVwVSFhjG/gjR+K70gl4=
- **Public Key:** Uzc0p1/sh/k/ofzF7I4n2enZZX13UmqA0SiPS3qdvnw=

### Problém:
- ANDROS server nemá statickú verejnú IP
- Aktuálna IPv6: 2a01:c846:cc3:7200:8616:cff:fe2a:16b9 (dynamická)
- Potrebujeme DDNS riešenie

---

## 🎯 ĎALŠIE KROKY

### 1. Nastaviť DDNS
Možnosti:
- **Cloudflare DDNS** (ak má ANDROS doménu)
- **No-IP** (bezplatné, typ andros-server.ddns.net)
- **DuckDNS** (bezplatné, jednoduché)

### 2. Konfigurácia routera
- Port forward UDP 51820 na 192.168.100.23

### 3. Vytvoriť konfiguráciu pre kolegu
```ini
[Interface]
PrivateKey = iELeqbkSDITAqAWID98zOuayVwVSFhjG/gjR+K70gl4=
Address = 10.10.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = y8iHIP1j4khFohKEa5hWTniQuhIaKDXzp2TqhlMfHCA=
Endpoint = <DDNS_HOSTNAME>:51820
AllowedIPs = 10.10.0.0/24, 192.168.100.0/24, 192.168.122.0/24
PersistentKeepalive = 25
```

### 4. Otestovať VPN pripojenie

---

## 📞 SERVER INFO

### Ubuntu Host
- **IP:** 192.168.100.23
- **User:** andros
- **Password:** MagNet-lin-1968
- **SSH:** ssh andros@192.168.100.23

### Windows VM
- **Internal IP:** 192.168.122.75
- **RDP:** 192.168.100.23:3389 (port forwarded)
- **User:** Administrator

### WireGuard
- **Port:** UDP 51820
- **VPN Subnet:** 10.10.0.0/24
- **Server VPN IP:** 10.10.0.1
- **Kolega VPN IP:** 10.10.0.2

### iDRAC
- **URL:** https://192.168.100.50
- **User:** root