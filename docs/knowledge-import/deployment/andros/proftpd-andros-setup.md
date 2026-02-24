# ProFTPD Server - ANDROS

**Dátum:** 2026-01-23
**Server:** ANDROS (Dell PowerEdge R740XD, Ubuntu 24.04)
**Stav:** ✅ Plne funkčný

---

## Sieťová konfigurácia

| Parameter | Hodnota |
|-----------|---------|
| Server | nex-andros-server |
| LAN IP | 192.168.100.23 |
| WireGuard IP | 10.10.0.2 |
| Verejná IP | 46.224.229.55 (Hetzner VPS gateway) |
| FTP doména | ftp.isnex.eu |
| Web doména | www.isnex.eu |

## Porty a služby

| Služba | Port | Protokol |
|--------|------|----------|
| FTP control | 21 | FTP/FTPS |
| FTP passive | 30000-30100 | FTP |
| SFTP | 22023 | SSH |
| HTTPS | 443 | Web |
| HTTP | 80 | Redirect → HTTPS |

## Port forwarding (VPS iptables)

| Služba | Externá adresa | Interná destinácia |
|--------|----------------|-------------------|
| FTP control | 46.224.229.55:21 | 10.10.0.2:21 |
| FTP passive | 46.224.229.55:30000-30100 | 10.10.0.2:30000-30100 |
| HTTP | 46.224.229.55:80 | 10.10.0.2:80 |
| HTTPS | 46.224.229.55:443 | 10.10.0.2:443 |

---

## Adresárová štruktúra

```
/data/ftp/                  # HDD pole (4.1TB)
├── download/               # Verejný (www.isnex.eu/download/)
├── private/                # Súkromný (chmod 775)
├── shared/                 # Zdieľaný (chmod 775)
└── users/                  # Používateľské adresáre

/srv/ftp -> /data/ftp       # Symlink
```

---

## FTP Používatelia

| Používateľ | Home adresár | Prístup |
|------------|--------------|---------|
| admin | /data/ftp | Plný prístup |

**Súbor hesiel:** `/etc/proftpd/ftpd.passwd`

### Pridanie nového používateľa

```bash
# S plným prístupom
sudo ftpasswd --passwd --file=/etc/proftpd/ftpd.passwd --name=MENO --uid=113 --gid=65534 --home=/data/ftp --shell=/usr/sbin/nologin

# S obmedzeným prístupom (vlastný adresár)
sudo mkdir -p /data/ftp/users/MENO
sudo chown ftp:nogroup /data/ftp/users/MENO
sudo chmod 775 /data/ftp/users/MENO
sudo ftpasswd --passwd --file=/etc/proftpd/ftpd.passwd --name=MENO --uid=113 --gid=65534 --home=/data/ftp/users/MENO --shell=/usr/sbin/nologin
```

---

## Konfiguračné súbory

| Súbor | Účel |
|-------|------|
| /etc/proftpd/proftpd.conf | Hlavná konfigurácia |
| /etc/proftpd/conf.d/custom.conf | Vlastné nastavenia |
| /etc/proftpd/conf.d/tls.conf | TLS/SSL konfigurácia |
| /etc/proftpd/modules.conf | Moduly (mod_tls.c) |
| /etc/proftpd/ftpd.passwd | Virtuálni používatelia |

## Let's Encrypt certifikáty

| Doména | Certifikát | Expirácia |
|--------|------------|-----------|
| ftp.isnex.eu | /etc/letsencrypt/live/ftp.isnex.eu/ | 22.04.2026 |
| isnex.eu + www | /etc/letsencrypt/live/isnex.eu/ | 23.04.2026 |

---

## Pripojenie

### FTP/FTPS (Total Commander, FileZilla)

| Parameter | Hodnota |
|-----------|---------|
| Host | ftp.isnex.eu |
| Port | 21 |
| Šifrovanie | Explicit FTP over TLS |
| Používateľ | admin |

### SFTP

| Parameter | Hodnota |
|-----------|---------|
| Host | 46.224.229.55 |
| Port | 22023 |
| Používateľ | andros |

### Web download

- https://www.isnex.eu/download/
- https://isnex.eu/download/

---

## Užitočné príkazy

```bash
# Stav služby
sudo systemctl status proftpd

# Reštart
sudo systemctl restart proftpd

# Kontrola syntaxe
sudo proftpd -t

# Logy
sudo tail -f /var/log/proftpd/proftpd.log
sudo tail -f /var/log/proftpd/tls.log
sudo tail -f /var/log/proftpd/xferlog

# Zobrazenie používateľov
sudo cat /etc/proftpd/ftpd.passwd

# Test TLS certifikátu
openssl s_client -connect localhost:21 -starttls ftp
```

---

## Nginx konfigurácia

**Súbor:** `/etc/nginx/sites-available/isnex.eu.conf`

- HTTP redirect na HTTPS
- HTTPS s Let's Encrypt certifikátom
- /download → /data/ftp/download (autoindex)
- Security headers (HSTS, X-Content-Type-Options, X-Frame-Options)

---

## Cloudflare nastavenia

| Parameter | Hodnota |
|-----------|---------|
| DNS záznamy | ftp, mail, www, @ |
| SSL/TLS mode | Full (strict) |
| Proxy | ftp = DNS only, ostatné = Proxied |

---

## Dôležité poznámky

1. **FXP povolený** - kopírovanie medzi FTP servermi funguje
2. **EC certifikát** - Let's Encrypt používa ECDSA, nie RSA (TLSECCertificateFile)
3. **Auto-renewal** - certbot automaticky obnovuje certifikáty
4. **VPS gateway** - 46.224.229.55 je Hetzner VPS s WireGuard tunelom
