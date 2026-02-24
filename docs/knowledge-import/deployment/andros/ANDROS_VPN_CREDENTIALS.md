# ANDROS VPN Gateway - Credentials & Konfigurácia

**Vytvorené:** 2026-01-22  
**Účel:** Dočasný vzdialený prístup na ANDROS server (Komárno) cez Hetzner VPS

---

## 🌐 VPS Gateway (Hetzner)

| Parameter | Hodnota |
|-----------|---------|
| Názov | andros-gateway |
| Verejná IP | 46.224.229.55 |
| IPv6 | 2a01:4f8:1c1a:105b::1 |
| Lokalita | Nuremberg, Nemecko |
| OS | Ubuntu 24.04 |
| Cena | 3,49€/mesiac |

### SSH prístup na VPS
```
ssh root@46.224.229.55
Password: [zmenené pri prvom prihlásení]
```

### WireGuard konfigurácia (VPS)
```
/etc/wireguard/wg0.conf

[Interface]
Address = 10.10.0.1/24
ListenPort = 51820
PrivateKey = YCUC4l+dC/g1ItRqcD9UPD5jZmrzajRfZbI2oamDPk4=

[Peer]
PublicKey = Yk8Jsens05/BYRVbgSbwSWzNUlRCSbbug5p6V7R4qzM=
AllowedIPs = 10.10.0.2/32
```

### WireGuard kľúče (VPS)
- Private Key: `YCUC4l+dC/g1ItRqcD9UPD5jZmrzajRfZbI2oamDPk4=`
- Public Key: `q1ZnQhW0BCAYuep+OZuueMpvgzqDf9rR0IeW5C1KIiU=`

---

## 🖥️ ANDROS Server (Komárno)

| Parameter | Hodnota |
|-----------|---------|
| LAN IP | 192.168.100.23 |
| WireGuard IP | 10.10.0.2 |
| OS | Ubuntu 24.04 |
| Windows VM IP | 192.168.122.75 |

### WireGuard konfigurácia (ANDROS)
```
/etc/wireguard/wg0.conf

[Interface]
PrivateKey = yEHKMSfeWxKlVX4yc0MSi88AgREkE3ARMSCk4avXb0o=
Address = 10.10.0.2/24

[Peer]
PublicKey = q1ZnQhW0BCAYuep+OZuueMpvgzqDf9rR0IeW5C1KIiU=
Endpoint = 46.224.229.55:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

### WireGuard kľúče (ANDROS)
- Private Key: `yEHKMSfeWxKlVX4yc0MSi88AgREkE3ARMSCk4avXb0o=`
- Public Key: `Yk8Jsens05/BYRVbgSbwSWzNUlRCSbbug5p6V7R4qzM=`

---

## 🔌 Port Forwarding

### Prístup z internetu

| Služba | Externá adresa | Interná destinácia |
|--------|----------------|-------------------|
| SSH (ANDROS) | 46.224.229.55:22023 | 10.10.0.2:22 |
| RDP (Windows) | 46.224.229.55:3389 | 192.168.122.75:3389 |
| NEX API | 46.224.229.55:8000 | 10.10.0.2:8000 |
| SMTP | 46.224.229.55:25 | 10.10.0.2:25 |
| SMTPS | 46.224.229.55:465 | 10.10.0.2:465 |
| Submission | 46.224.229.55:587 | 10.10.0.2:587 |
| IMAPS | 46.224.229.55:993 | 10.10.0.2:993 |

### Príkazy na pripojenie

**SSH na ANDROS:**
```bash
ssh andros@46.224.229.55 -p 22023
```

**RDP na Windows VM:**
```
Adresa: 46.224.229.55:3389
User: Administrator
```

---

## 🔧 Správa služieb

### VPS (andros-gateway)
```bash
# WireGuard status
wg show

# Reštart WireGuard
systemctl restart wg-quick@wg0

# Iptables pravidlá
iptables -t nat -L -n -v
```

### ANDROS
```bash
# WireGuard status
sudo wg show

# Reštart WireGuard
sudo systemctl restart wg-quick@wg0

# Test konektivity na VPS
ping 10.10.0.1
```

---

## 📋 DNS záznamy pre isnex.eu

Nastaviť tieto záznamy:

| Typ | Názov | Hodnota | TTL |
|-----|-------|---------|-----|
| A | @ | 46.224.229.55 | 300 |
| A | mail | 46.224.229.55 | 300 |
| MX | @ | mail.isnex.eu (priority 10) | 300 |

---

## ⚠️ Dôležité poznámky

1. **Dočasné riešenie** - VPS je len na dobu kým ANDROS presunieme k zákazníkovi
2. **Po presune** - zrušiť VPS na Hetzner, vypnúť WireGuard na ANDROS
3. **Hetzner účet** - prihlasovacie údaje na https://console.hetzner.cloud
4. **Mesačné náklady** - 3,49€ (VPS) + 0,50€ (IPv4) = ~4€/mesiac

---

## 🔄 Architektúra

```
Internet
    │
    ▼
┌─────────────────────────┐
│  VPS (46.224.229.55)    │
│  WireGuard: 10.10.0.1   │
│  Port forwarding        │
└───────────┬─────────────┘
            │ WireGuard tunel
            │ (šifrovaný)
            ▼
┌─────────────────────────┐
│  ANDROS Ubuntu          │
│  LAN: 192.168.100.23    │
│  WireGuard: 10.10.0.2   │
└───────────┬─────────────┘
            │ KVM/libvirt
            ▼
┌─────────────────────────┐
│  Windows VM             │
│  192.168.122.75         │
│  RDP, NEX Genesis       │
└─────────────────────────┘
```