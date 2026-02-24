# ANDROS Tailscale VPN - Administrátorská dokumentácia

## Prehľad

Tailscale VPN pre vzdialený prístup k ANDROS serveru (Dell PowerEdge R740XD). Umožňuje pripojenie na Ubuntu host aj Windows Server 2025 VM cez Remote Desktop. Tailscale bol zvolený namiesto WireGuard kvôli ISP obmedzeniam port forwardingu.

## Sieťová topológia

```
Kolega (desktop-tibi)          ANDROS Server
100.67.176.24                  100.107.134.104
      │                              │
      └──────── Tailscale ───────────┘
                  │
                  ▼
         iptables NAT (DNAT)
                  │
                  ▼
         Windows Server 2025 VM
         192.168.122.75:3389
```

## Tailscale zariadenia

| Zariadenie | Tailscale IP | OS | Stav |
|------------|--------------|-----|------|
| nex-andros-server | 100.107.134.104 | Ubuntu 24.04 LTS | Connected |
| desktop-tibi | 100.67.176.24 | Windows 10 22H2 | Connected |

## Lokálne IP adresy

| Zariadenie | LAN IP | Poznámka |
|------------|--------|----------|
| Ubuntu host | 192.168.100.23 | Tailscale server |
| Windows VM | 192.168.122.75 | RDP cez DNAT |
| Router | 192.168.100.1 | Huawei HG8245W5 |
| iDRAC | 192.168.100.50 | Server management |

## Tailscale účet

| Parameter | Hodnota |
|-----------|---------|
| Účet | iccforai@gmail.com |
| Plán | Free |
| Admin konzola | https://login.tailscale.com/admin/machines |

## Pripojenie na Windows VM (RDP)

Kolega zadá v Remote Desktop Connection:

```
100.107.134.104
```

Port 3389 sa automaticky presmeruje na Windows VM (192.168.122.75).

## IPtables pravidlá pre RDP

### Aktuálne pravidlá (PREROUTING)

```bash
# Pre LAN prístup
iptables -t nat -A PREROUTING -p tcp -d 192.168.100.23 --dport 3389 -j DNAT --to-destination 192.168.122.75:3389

# Pre Tailscale prístup
iptables -t nat -A PREROUTING -p tcp -d 100.107.134.104 --dport 3389 -j DNAT --to-destination 192.168.122.75:3389
```

### Uloženie pravidiel

```bash
sudo sh -c 'iptables-save > /etc/iptables/rules.v4'
```

## Administrátorské príkazy

### Tailscale správa

```bash
# Status Tailscale
tailscale status

# Tailscale IP adresa
tailscale ip

# Reštart Tailscale
sudo systemctl restart tailscaled

# Logy
sudo journalctl -u tailscaled -f

# Odpojenie
sudo tailscale down

# Pripojenie
sudo tailscale up
```

### VM Management

```bash
# Zoznam všetkých VM
virsh list --all

# Spustiť VM
sudo virsh start win2025

# Vypnúť VM
sudo virsh shutdown win2025

# Force stop VM
sudo virsh destroy win2025
```

### Sieťová diagnostika

```bash
# Kontrola iptables pravidiel
sudo iptables -t nat -L PREROUTING -n -v | grep 3389

# Ping na Windows VM
ping 192.168.122.75

# Kontrola RDP portu na VM
nc -zv 192.168.122.75 3389
```

## Pridanie nového používateľa

1. Nový používateľ nainštaluje Tailscale: https://tailscale.com/download
2. Prihlási sa účtom **iccforai@gmail.com** (zdieľaný účet)
3. Zariadenie sa automaticky objaví v admin konzole
4. Môže sa pripojiť na 100.107.134.104 cez RDP

### Alternatíva - pozvánka

1. V admin konzole: Users → Invite users
2. Zadaj email nového používateľa
3. Používateľ si vytvorí vlastný účet a pripojí sa do tailnet

## DuckDNS (stále aktívne)

DuckDNS zostáva nakonfigurované pre prípad budúceho použitia:

| Parameter | Hodnota |
|-----------|---------|
| Doména | andros-vpn.duckdns.org |
| Token | 729c8ff5-6402-4fcf-9da5-8b430305e0e7 |
| Aktualizácia | ~/duckdns/duck.sh (cron každých 5 min) |

## WireGuard (nepoužíva sa)

WireGuard konfigurácia zostáva na serveri, ale nie je aktívne používaná kvôli ISP obmedzeniam port forwardingu na Huawei HG8245W5 routeri.

## Prihlasovacie údaje

### Ubuntu Host

| Parameter | Hodnota                   |
|-----------|---------------------------|
| IP | 192.168.100.23            |
| Tailscale IP | 100.107.134.104           |
| User | andros                    |
| Password | Andros-2026               |
| SSH | ssh andros@192.168.100.23 |

### Huawei Router

| Parameter | Hodnota |
|-----------|---------|
| IP | 192.168.100.1 |
| User | root |
| Password | vtw7dD |

### iDRAC

| Parameter | Hodnota |
|-----------|---------|
| URL | https://192.168.100.50 |
| User | root |

## Riešenie problémov

### Kolega sa nemôže pripojiť

1. Over, že Tailscale je aktívny na serveri: `tailscale status`
2. Over, že Windows VM beží: `sudo virsh list --all`
3. Over iptables pravidlá: `sudo iptables -t nat -L PREROUTING -n -v | grep 3389`
4. Reštartuj Tailscale: `sudo systemctl restart tailscaled`

### RDP timeout

1. Ping na Tailscale IP: `ping 100.107.134.104`
2. Ping na Windows VM: `ping 192.168.122.75`
3. Over, či VM má sieť: `sudo virsh domiflist win2025`

## História zmien

| Dátum | Zmena |
|-------|-------|
| 2026-01-15 | Vytvorená WireGuard konfigurácia |
| 2026-01-15 | Migrácia na Tailscale (ISP port forward obmedzenie) |
| 2026-01-15 | Pridané iptables DNAT pre Tailscale IP |