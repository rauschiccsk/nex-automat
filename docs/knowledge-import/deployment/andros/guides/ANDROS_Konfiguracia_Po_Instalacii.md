# ANDROS Server - Konfigurácia po inštalácii u zákazníka

**Pre:** Zoltán Rausch  
**Dátum:** 2026-01-31  
**Účel:** Kroky po fyzickom pripojení servera na novom mieste

---

## 1. PRVOTNÝ PRÍSTUP

### 1.1 Prístup cez iDRAC (ak Ubuntu ešte nemá správnu IP)

1. Požiadať technika o pripojenie monitora/klávesnice
2. Alebo použiť iDRAC konzolu:
   - URL: https://192.168.55.251 (ak iDRAC už má novú IP)
   - Ak nie, technik musí zmeniť IP iDRAC lokálne

### 1.2 Zmena iDRAC IP (ak treba)

Ak iDRAC má stále starú IP (192.168.100.50):

1. Na serveri stlačiť F2 počas POST pre System Setup
2. iDRAC Settings → Network → IPv4 Settings
3. Nastaviť:
   - Static IP: 192.168.55.251
   - Gateway: 192.168.55.1
   - Subnet: 255.255.255.0
4. Apply a Exit

---

## 2. ZMENA SIEŤOVEJ KONFIGURÁCIE UBUNTU

### 2.1 Prístup na server

**Možnosť A - cez iDRAC Virtual Console:**
- https://192.168.55.251 → Virtual Console

**Možnosť B - fyzická konzola:**
- Požiadať technika o pripojenie monitora/klávesnice

### 2.2 Spustiť pripravený skript

```bash
# Prihlásiť sa ako andros
# Heslo: Andros-2026

sudo /root/switch-network.sh
```

### 2.3 Manuálne (ak skript neexistuje)

Vytvoriť `/etc/netplan/99-static.yaml`:

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
sudo netplan apply
```

### 2.4 Overenie

```bash
ip addr show eno4
ping 192.168.55.1
ping 8.8.8.8
```

Očakávaná IP: **192.168.55.250**

---

## 3. AKTUALIZÁCIA IPTABLES

### 3.1 Spustiť pripravený skript

```bash
sudo /root/iptables-production.sh
```

### 3.2 Manuálne (ak skript neexistuje)

```bash
# Vyčistiť staré NAT pravidlá
sudo iptables -t nat -F PREROUTING

# Pridať nové pravidlo pre RDP na neštandardnom porte
sudo iptables -t nat -A PREROUTING -p tcp -d 192.168.55.250 --dport 33389 -j DNAT --to-destination 192.168.122.75:3389

# Uložiť
sudo sh -c 'iptables-save > /etc/iptables/rules.v4'
```

### 3.3 Overenie

```bash
sudo iptables -t nat -L PREROUTING -n -v
```

---

## 4. OVERENIE SLUŽIEB

### 4.1 Docker kontajnery

```bash
docker ps
```

Očakávané kontajnery:
- nex-postgres, nex-postgres-icc
- nex-temporal, nex-temporal-icc
- nex-temporal-ui, nex-temporal-ui-icc
- nex-brain
- nex-ollama
- nex-qdrant
- nex-prometheus, nex-grafana, nex-alertmanager
- nex-cadvisor, nex-node-exporter, nex-postgres-exporter
- nex-telegram
- hbbs, hbbr (RustDesk)
- jitsi-meet-web-1, jitsi-meet-prosody-1, jitsi-meet-jicofo-1, jitsi-meet-jvb-1

### 4.2 Windows VM

```bash
sudo virsh list --all
```

Ak VM nebeží:
```bash
sudo virsh start win2025
```

### 4.3 Test RDP na VM

```bash
nc -zv 192.168.122.75 3389
```

---

## 5. OVERENIE JITSI MEET

### 5.1 Skontrolovať kontajnery

```bash
docker ps | grep jitsi
```

Očakávané (4 kontajnery):
- jitsi-meet-web-1
- jitsi-meet-prosody-1
- jitsi-meet-jicofo-1
- jitsi-meet-jvb-1

### 5.2 Ak kontajnery nebežia

```bash
cd /opt/jitsi-meet
sudo docker compose up -d
```

### 5.3 Test lokálne

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8880/
```

Očakávané: **200**

### 5.4 Test cez Nginx

```bash
curl -s -o /dev/null -w "%{http_code}" -k https://localhost -H "Host: meet.icc.sk"
```

Očakávané: **200**

### 5.5 SSL certifikát

```bash
echo | openssl s_client -connect localhost:443 -servername meet.icc.sk 2>/dev/null | openssl x509 -noout -issuer -dates
```

Očakávané: Let's Encrypt, platný do 1. mája 2026

---

## 6. SPUSTENIE RUSTDESK SERVERA

### 6.1 Spustiť kontajnery

```bash
cd /opt/rustdesk
sudo docker compose up -d
```

### 6.2 Získať verejný kľúč

```bash
cat /opt/rustdesk/data/id_ed25519.pub
```

**Zapísať kľúč** - bude potrebný pre konfiguráciu klientov.

### 6.3 Overenie

```bash
docker ps | grep rust
```

---

## 7. AKTUALIZÁCIA STALWART MAIL SERVER

### 7.1 Zmena allowed-ip

```bash
sudo nano /opt/stalwart/etc/config.toml
```

Zmeniť:
```toml
allowed-ip = { "127.0.0.1", "::1" }
```

### 7.2 Reštart služby

```bash
sudo systemctl restart stalwart-mail
sudo systemctl status stalwart-mail
```

---

## 8. AKTUALIZÁCIA FTP SERVERA

### 8.1 Zmena MasqueradeAddress

```bash
sudo nano /etc/proftpd/conf.d/custom.conf
```

Zmeniť:
```
MasqueradeAddress 87.244.203.135
```

### 8.2 Reštart služby

```bash
sudo systemctl restart proftpd
sudo systemctl status proftpd
```

---

## 9. AKTUALIZÁCIA DNS (CLOUDFLARE)

### 9.1 Prihlásiť sa na Cloudflare

URL: https://dash.cloudflare.com

### 9.2 Zmeniť A záznamy pre isnex.eu

| Typ | Name | Stará hodnota | Nová hodnota | Proxy |
|-----|------|---------------|--------------|-------|
| A | @ | 46.224.229.55 | 87.244.203.135 | Proxied |
| A | www | 46.224.229.55 | 87.244.203.135 | Proxied |
| A | mail | 46.224.229.55 | 87.244.203.135 | DNS only |
| A | ftp | 46.224.229.55 | 87.244.203.135 | DNS only |

**Dôležité:** mail a ftp musia byť "DNS only" (sivý oblak)!

### 9.3 DNS pre icc.sk (už nastavené)

| Typ | Name | Hodnota | Proxy |
|-----|------|---------|-------|
| A | meet | 87.244.203.135 | DNS only |

### 9.4 Overenie propagácie DNS

```bash
dig @8.8.8.8 isnex.eu A
dig @8.8.8.8 mail.isnex.eu A
dig @8.8.8.8 meet.icc.sk A
```

---

## 10. TEST EXTERNÉHO PRÍSTUPU

### 10.1 Z externej siete (mobil, iný PC)

```bash
# SSH
ssh andros@87.244.203.135

# alebo z Windows
telnet 87.244.203.135 22
telnet 87.244.203.135 33389   # RDP na neštandardnom porte
telnet 87.244.203.135 443
```

### 10.2 Test Jitsi Meet

Otvoriť v prehliadači:
- https://meet.icc.sk
- Vytvoriť testovaciu miestnosť
- Otestovať video/audio z mobilného zariadenia

### 10.3 Test emailu

Odoslať testovací email na rausch@isnex.eu z externej adresy (Gmail).

### 10.4 Test FTP

```bash
ftp ftp.isnex.eu
# alebo
sftp -P 22023 andros@87.244.203.135
```

### 10.5 Test webu

Otvoriť v prehliadači:
- https://isnex.eu
- https://www.isnex.eu

---

## 11. AKTUALIZÁCIA LET'S ENCRYPT CERTIFIKÁTOV

### 11.1 Test auto-renewal

```bash
sudo certbot renew --dry-run
```

### 11.2 Certifikát pre meet.icc.sk (už nastavený)

Certifikát používa Cloudflare DNS plugin a obnovuje sa automaticky.

Konfigurácia: `/etc/letsencrypt/cloudflare.ini`

Manuálne obnovenie (ak treba):
```bash
sudo certbot certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini -d meet.icc.sk
```

### 11.3 Certifikáty pre isnex.eu (ak treba)

```bash
sudo certbot certonly --nginx -d isnex.eu -d www.isnex.eu
sudo certbot certonly --standalone -d mail.isnex.eu --preferred-challenges http
sudo certbot certonly --standalone -d ftp.isnex.eu --preferred-challenges http
```

---

## 12. ZRUŠENIE HETZNER VPS

### 12.1 Podmienky pre zrušenie

Zrušiť až keď:
- [ ] Všetky služby fungujú cez novú IP
- [ ] Email funguje (odosielanie aj prijímanie)
- [ ] FTP funguje
- [ ] Web funguje
- [ ] RDP funguje
- [ ] Jitsi Meet funguje
- [ ] Minimálne 1 týždeň bezproblémovej prevádzky

### 12.2 Kroky pre zrušenie

1. Prihlásiť sa na https://console.hetzner.cloud
2. Vybrať server "andros-gateway"
3. Delete server

### 12.3 Vypnutie WireGuard na ANDROS

```bash
sudo systemctl stop wg-quick@wg0
sudo systemctl disable wg-quick@wg0
```

---

## 13. FINÁLNY KONTROLNÝ ZOZNAM

### 13.1 Sieť

- [ ] Ubuntu má IP 192.168.55.250
- [ ] iDRAC má IP 192.168.55.251
- [ ] Ping na gateway funguje
- [ ] Ping na internet funguje

### 13.2 Služby

- [ ] Docker kontajnery bežia (23+)
- [ ] Windows VM beží
- [ ] RDP na VM funguje (lokálne)
- [ ] RDP na VM funguje (z internetu na porte 33389)
- [ ] RustDesk server beží
- [ ] Jitsi Meet beží

### 13.3 Externý prístup

- [ ] SSH z internetu
- [ ] RDP z internetu
- [ ] iDRAC z internetu (port 9443)
- [ ] HTTPS web (isnex.eu)
- [ ] Jitsi Meet (meet.icc.sk)
- [ ] Email odosielanie
- [ ] Email prijímanie
- [ ] FTP/FTPS
- [ ] SFTP

### 13.4 DNS

- [ ] isnex.eu → 87.244.203.135
- [ ] mail.isnex.eu → 87.244.203.135
- [ ] ftp.isnex.eu → 87.244.203.135
- [ ] meet.icc.sk → 87.244.203.135

### 13.5 Pracovné stanice

- [ ] Všetky pracovné stanice sa pripájajú cez RDP
- [ ] NEX Genesis funguje
- [ ] Tlač funguje

---

## 14. ČASOVÝ ODHAD

| Úloha | Čas |
|-------|-----|
| Zmena sieťovej konfigurácie | 10 min |
| Aktualizácia iptables | 5 min |
| Overenie služieb | 15 min |
| Overenie Jitsi Meet | 10 min |
| Spustenie RustDesk | 5 min |
| Aktualizácia DNS | 10 min |
| Čakanie na DNS propagáciu | 5-60 min |
| Testovanie | 30 min |
| **Celkom** | **~2 hodiny** |

---

## 15. ROLLBACK PLÁN

Ak niečo nefunguje a treba vrátiť server späť:

### 15.1 Obnovenie DHCP konfigurácie

```bash
sudo rm /etc/netplan/99-static.yaml
sudo netplan apply
```

### 15.2 Obnovenie iptables

```bash
sudo iptables-restore < /root/config-backup-*/iptables-backup.rules
```

### 15.3 DNS

Vrátiť záznamy v Cloudflare na 46.224.229.55 (Hetzner VPS).