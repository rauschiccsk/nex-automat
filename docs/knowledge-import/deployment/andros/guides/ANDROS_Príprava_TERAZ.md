# ANDROS Server - Príprava TERAZ

**Pre:** Zoltán Rausch  
**Dátum:** 2026-01-28  
**Účel:** Prípravné kroky BEZ dopadu na aktuálnu funkčnosť servera

---

## 1. INFORMÁCIE O AKTUÁLNOM STAVE

| Parameter | Hodnota |
|-----------|---------|
| Rozhranie | eno4 (altname: enp1s0f1) |
| MAC adresa | 84:16:0c:2a:16:b9 |
| Aktuálna konfigurácia | `/etc/netplan/50-cloud-init.yaml` (DHCP) |
| Windows VM autostart | ✅ Enabled |
| iptables-persistent | ✅ Nainštalovaný |

### Nové IP adresy (produkcia u zákazníka)

| Zariadenie | Nová IP |
|------------|---------|
| Ubuntu Server | 192.168.55.250 |
| iDRAC | 192.168.55.251 |
| Gateway | 192.168.55.1 |
| Windows VM | 192.168.122.75 (bez zmeny) |

---

## 2. VYTVORIŤ NETPLAN KONFIGURÁCIU

Vytvoriť súbor `/etc/netplan/99-static.yaml` (zatiaľ **NEAPLIKOVAŤ**):

```bash
sudo nano /etc/netplan/99-static.yaml
```

Obsah:
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eno4:
      addresses:
        - 192.168.55.250/24
      routes:
        - to: default
          via: 192.168.55.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
      dhcp4: false
```

```bash
sudo chmod 600 /etc/netplan/99-static.yaml
```

**⚠️ NEPOUŽÍVAŤ `netplan apply`!** Súbor sa aktivuje až po presune.

---

## 3. VYTVORIŤ SKRIPT NA PREPNUTIE SIETE

Vytvoriť `/root/switch-network.sh`:

```bash
sudo nano /root/switch-network.sh
```

Obsah:
```bash
#!/bin/bash
# Skript na prepnutie siete na produkčné prostredie

echo "=== Prepínanie na produkčnú sieť ==="

# Kontrola či existuje netplan konfigurácia
if [ ! -f /etc/netplan/99-static.yaml ]; then
    echo "CHYBA: /etc/netplan/99-static.yaml neexistuje!"
    exit 1
fi

# Aplikovanie netplan
echo "Aplikujem netplan konfiguráciu..."
netplan apply

# Čakanie na sieť
sleep 5

# Zobrazenie novej IP
echo ""
echo "=== Nová konfigurácia ==="
ip addr show eno4 | grep "inet "

echo ""
echo "Sieť prepnutá na produkčné prostredie"
echo "Nová IP: 192.168.55.250"
```

```bash
sudo chmod +x /root/switch-network.sh
```

---

## 4. VYTVORIŤ SKRIPT NA IPTABLES

Vytvoriť `/root/iptables-production.sh`:

```bash
sudo nano /root/iptables-production.sh
```

Obsah:
```bash
#!/bin/bash
# IPtables pravidlá pre produkčné prostredie

# Flush existujúcich NAT pravidiel
iptables -t nat -F PREROUTING

# NAT pre RDP na neštandardnom porte 33389
iptables -t nat -A PREROUTING -p tcp -d 192.168.55.250 --dport 33389 -j DNAT --to-destination 192.168.122.75:3389

# Uloženie
iptables-save > /etc/iptables/rules.v4

echo "IPtables pravidlá aktualizované"
echo "RDP dostupné na porte 33389 (nie štandardný 3389)"
```

```bash
sudo chmod +x /root/iptables-production.sh
```

---

## 5. PRIPRAVIŤ RUSTDESK SERVER

### 5.1 Vytvoriť adresár a docker-compose

```bash
sudo mkdir -p /opt/rustdesk/data
sudo nano /opt/rustdesk/docker-compose.yml
```

Obsah:
```yaml
version: '3'

services:
  hbbs:
    container_name: hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs -r 87.244.203.135:21117
    volumes:
      - ./data:/root
    network_mode: host
    restart: unless-stopped
    depends_on:
      - hbbr

  hbbr:
    container_name: hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./data:/root
    network_mode: host
    restart: unless-stopped
```

### 5.2 Stiahnuť Docker image vopred

```bash
cd /opt/rustdesk
sudo docker compose pull
```

**Poznámka:** Toto len stiahne image, nespustí službu.

---

## 6. ZÁLOHOVAŤ KONFIGURÁCIU

```bash
# Vytvoriť zálohu
sudo mkdir -p /root/config-backup-$(date +%Y%m%d)
cd /root/config-backup-$(date +%Y%m%d)

# Sieťová konfigurácia
sudo cp -r /etc/netplan .

# IPtables
sudo iptables-save > iptables-backup.rules

# ProFTPD
sudo cp -r /etc/proftpd .

# Nginx
sudo cp -r /etc/nginx .

# Stalwart
sudo cp -r /opt/stalwart/etc stalwart-etc

# WireGuard
sudo cp -r /etc/wireguard . 2>/dev/null

# Docker compose súbory
sudo cp /opt/nex-automat/docker-compose*.yml .

echo "Záloha dokončená v $(pwd)"
ls -la
```

---

## 7. POZNAČIŤ DÔLEŽITÉ ÚDAJE

### 7.1 iDRAC heslo

Heslo je na štítku na prednej strane servera alebo na výsuvnom štítku.

| Parameter | Hodnota |
|-----------|---------|
| iDRAC User | root |
| iDRAC Password | _________________ |

### 7.2 Overiť aktuálnu iDRAC IP

```bash
# Z Ubuntu (ak je iDRAC v rovnakej sieti)
sudo apt install ipmitool -y
sudo ipmitool lan print 1
```

Alebo pozrieť počas POST obrazovky pri štarte servera.

| Parameter | Aktuálna hodnota | Nová hodnota (produkcia) |
|-----------|------------------|--------------------------|
| iDRAC IP | _________________ | 192.168.55.251 |

---

## 8. PRIPRAVIŤ POZNÁMKY PRE DNS A KONFIGURÁCIE

### 8.1 DNS zmeny (Cloudflare) - LEN POZNÁMKA

Po presune zmeniť v Cloudflare:

| Typ | Name | Stará hodnota | Nová hodnota |
|-----|------|---------------|--------------|
| A | @ | 46.224.229.55 | 87.244.203.135 |
| A | www | 46.224.229.55 | 87.244.203.135 |
| A | mail | 46.224.229.55 | 87.244.203.135 |
| A | ftp | 46.224.229.55 | 87.244.203.135 |

### 8.2 Stalwart Mail - LEN POZNÁMKA

Po presune zmeniť v `/opt/stalwart/etc/config.toml`:

```toml
# Zmeniť z:
allowed-ip = { "127.0.0.1", "::1", "10.10.0.1" }

# Na:
allowed-ip = { "127.0.0.1", "::1" }
```

### 8.3 ProFTPD - LEN POZNÁMKA

Po presune zmeniť v `/etc/proftpd/conf.d/custom.conf`:

```
# Zmeniť z:
MasqueradeAddress 46.224.229.55

# Na:
MasqueradeAddress 87.244.203.135
```

---

## 9. KONTROLNÝ ZOZNAM

### Spraviť TERAZ

- [ ] Vytvoriť `/etc/netplan/99-static.yaml`
- [ ] Vytvoriť `/root/switch-network.sh`
- [ ] Vytvoriť `/root/iptables-production.sh`
- [ ] Vytvoriť `/opt/rustdesk/docker-compose.yml`
- [ ] Stiahnuť RustDesk Docker image (`docker compose pull`)
- [ ] Vytvoriť zálohu konfigurácie
- [ ] Poznačiť iDRAC heslo
- [ ] Overiť aktuálnu iDRAC IP adresu

### Časový odhad: ~30 minút

---

## 10. OVERENIE

Po dokončení overiť, že súbory existujú:

```bash
ls -la /etc/netplan/99-static.yaml
ls -la /root/switch-network.sh
ls -la /root/iptables-production.sh
ls -la /opt/rustdesk/docker-compose.yml
ls -la /root/config-backup-*/
```

**⚠️ Server stále funguje normálne** - žiadna z týchto zmien neovplyvní aktuálnu prevádzku.