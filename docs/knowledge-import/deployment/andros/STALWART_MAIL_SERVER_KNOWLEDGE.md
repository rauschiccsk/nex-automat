# Stalwart Mail Server - Knowledge Document

**Projekt:** Email Server na ANDROS
**Dátum:** 2026-01-23
**Stav:** Konfigurácia Thunderbird klienta

---

## Infraštruktúra

| Komponent | Hodnota |
|-----------|---------|
| Server | ANDROS (Dell PowerEdge R740XD, Ubuntu 24.04) |
| Mail Software | Stalwart Mail Server v0.15.4 |
| Verejná IP | 46.224.229.55 (cez Hetzner VPS gateway) |
| LAN IP | 192.168.100.23 |
| Stalwart Admin | http://192.168.122.1:8088 (z Windows VM) |
| Admin credentials | admin / zMgmEFQx9L |

---

## Domény v Stalwart

| Doména | Stav |
|--------|------|
| isnex.eu | ✅ Aktívna, DNS na Cloudflare |
| isnex.ai | ✅ Pridaná (Gmail má automat@isnex.ai) |

---

## Emailové účty

### rausch@isnex.eu (hlavný)

| Parameter | Hodnota |
|-----------|---------|
| Email | rausch@isnex.eu |
| Meno | Zoltán Rausch |
| Heslo | PbtEem/QTSpe+4Jdq3ZtuAGda1k= |

### zoltan@isnex.eu

| Parameter | Hodnota |
|-----------|---------|
| Email | zoltan@isnex.eu |
| Heslo | (nenastavené) |

---

## DNS záznamy (Cloudflare - isnex.eu)

| Typ | Name | Content | Stav |
|-----|------|---------|------|
| A | mail | 46.224.229.55 | ✅ |
| MX | @ | mail.isnex.eu (priority 10) | ✅ |
| TXT | @ | v=spf1 mx a ip4:46.224.229.55 ~all | ✅ |
| TXT | _dmarc | v=DMARC1; p=quarantine; rua=mailto:zoltan@isnex.eu | ✅ |
| TXT | default._domainkey | v=DKIM1; k=rsa; p=MIIBIj... | ✅ |

---

## TLS Certifikát

| Parameter | Hodnota |
|-----------|---------|
| Typ | Let's Encrypt |
| Doména | mail.isnex.eu |
| Platnosť | do 23. apríla 2026 |
| Auto-renewal | ✅ certbot timer + restart hook |
| Cesta | /etc/letsencrypt/live/mail.isnex.eu/ |

---

## Port Forwarding (VPS Hetzner → ANDROS)

| Port | Služba | Stav |
|------|--------|------|
| 25 | SMTP | ✅ |
| 465 | SMTPS | ✅ |
| 587 | Submission | ✅ |
| 993 | IMAPS | ✅ |
| 143 | IMAP | ✅ |

---

## IMAP/SMTP Nastavenia pre klientov

### IMAP (prichádzajúca pošta)

| Parameter | Hodnota |
|-----------|---------|
| Server | mail.isnex.eu |
| Port | 993 |
| Security | SSL/TLS |
| Username | rausch@isnex.eu |

### SMTP (odchádzajúca pošta)

| Parameter | Hodnota |
|-----------|---------|
| Server | mail.isnex.eu |
| Port | 587 |
| Security | STARTTLS |
| Username | rausch@isnex.eu |

---

## Dokončené kroky

1. ✅ Stalwart Mail Server nainštalovaný a beží
2. ✅ Domény isnex.eu a isnex.ai pridané
3. ✅ Emailové účty vytvorené (rausch@isnex.eu, zoltan@isnex.eu)
4. ✅ DNS záznamy (MX, SPF, DKIM, DMARC) v Cloudflare
5. ✅ Nameservery prepnuté z Webglobe na Cloudflare
6. ✅ Port forwarding na VPS pre mailové porty
7. ✅ Let's Encrypt certifikát nakonfigurovaný
8. ✅ DKIM kľúče vygenerované
9. ✅ Thunderbird nainštalovaný na Development PC

---

## Aktuálny problém

Thunderbird sa nepripája na SMTP server. Test portu z PowerShell funguje:
```
Test-NetConnection -ComputerName mail.isnex.eu -Port 587 → TcpTestSucceeded: True
Test-NetConnection -ComputerName mail.isnex.eu -Port 465 → TcpTestSucceeded: True
```

Účet bol vymazaný a práve sa znova pridáva.

---

## Ďalšie kroky

1. Dokončiť konfiguráciu Thunderbird
2. Otestovať odosielanie/prijímanie emailov
3. (Voliteľné) Nainštalovať Roundcube webmail
4. (Voliteľné) Migrovať emaily z Mac Mail / Gmail