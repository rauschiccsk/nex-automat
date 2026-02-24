# NEX Automat - Credentials & Sensitive Configuration

**Location:** docs/knowledge/credentials/
**Status:** NOT IN GIT - RAG indexed only
**Updated:** 2026-01-21

---

## Invoice Email Accounts (Webglobe)

**Mail Server:** mail.webglobe.sk
**IMAP Port:** 993 (SSL)
**SMTP Port:** 465 (SSL)

| Zákazník | Email | Heslo |
|----------|-------|-------|
| ANDROS | andros.invoices@icc.sk | Nex-Andros2026-Inv |
| MAGERSTAV | magerstav.invoices@icc.sk | Nex-Magerstav2026-Inv |
| ICC | icc.invoices@icc.sk | Nex-Icc2026-Inv |

**Vzorec hesiel:** `Nex-[Zákazník]2026-Inv`

---

## Gmail Account: magerstavinvoice@gmail.com (LEGACY)

**Purpose:** Invoice processing emails + SMTP notifications (MAGERSTAV - starý systém)
**Status:** Bude nahradený magerstav.invoices@icc.sk

### IMAP (receiving emails)
| Parameter | Value |
|-----------|-------|
| Host | imap.gmail.com |
| Port | 993 |
| User | magerstavinvoice@gmail.com |
| Password | M@gerstav772 |

### SMTP (sending emails)
| Parameter | Value |
|-----------|-------|
| Host | smtp.gmail.com |
| Port | 465 (SSL) |
| User | magerstavinvoice@gmail.com |
| App Password | ugrjqhqdvffrzgyr |

### OAuth2 (for n8n - LEGACY)
| Parameter | Value |
|-----------|-------|
| Client ID | 1078289465706-tpuet1lqt5ljqvtns0k9477tnj1pm7dh.apps.googleusercontent.com |
| Client Secret | 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 |

---

## Telegram Bots (NEX Brain)

✅ **Tokeny regenerované:** 2025-12-25

| Bot | Username | Token |
|-----|----------|-------|
| Admin | @ai_dev_automatin_bot | 8585064403:AAE-kFftrdpXwoLHVmrG0MvB5jfo1FmA1Y4 |
| ICC | @NexBrainIcc_bot | 8487965429:AAH2IUIFVEEtInFva8_GHAz84wCFdgGax9U |
| ANDROS | @NexBrainAndros_bot | 8178049225:AAEQ-vVQINeB2ASGClClK90HLBHhuBhyxBo |

**Admin User ID:** 7204918893 (Zoltán)

---

## Email Recipients

| Purpose | Email |
|---------|-------|
| Admin (dev) | rausch@icc.sk |
| Admin (backup) | rauscht@icc.sk |
| Customer (Mágerstav) | mate.bognar.22@gmail.com |

---

## ANDROS Server (Dell PowerEdge R740XD)

### Linux Host (Ubuntu 24.04)
| Parameter | Value |
|-----------|-------|
| LAN IP | 192.168.100.23 |
| Tailscale IP | 100.107.134.104 |
| SSH | ssh andros@192.168.100.23 |
| User | andros |
| Password | Andros-2026 |

### Windows VM (KVM)
| Parameter | Value |
|-----------|-------|
| Internal IP | 192.168.122.75 |
| RDP | 100.107.134.104 (cez Tailscale) |
| User | Administrator |

### Tailscale
| Parameter | Value |
|-----------|-------|
| Account | iccforai@gmail.com |
| Server IP | 100.107.134.104 |
| Admin | https://login.tailscale.com/admin/machines |

---

## Database

### PostgreSQL - Mágerstav (supplier_invoice_staging)
| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 5432 |
| Database | supplier_invoice_staging |
| User | postgres |
| Password | (from POSTGRES_PASSWORD env) |

### PostgreSQL - ANDROS (nex_automat)
| Parameter | Value |
|-----------|-------|
| Host (z Linuxu) | localhost:5432 |
| Host (z Windows VM) | 192.168.122.1:5432 |
| Host (z Docker) | postgres:5432 |
| Database | nex_automat |
| User | nex_admin |
| Password | Nex1968 |

**ANDROS Connection string:**
```
postgresql://nex_admin:Nex1968@192.168.122.1:5432/nex_automat
```

### PostgreSQL - ICC (nex_automat_icc) - PLÁNOVANÉ
| Parameter | Value |
|-----------|-------|
| Host (z Linuxu) | localhost:5433 |
| Host (z Windows VM) | 192.168.122.1:5433 |
| Database | nex_automat_icc |
| User | nex_admin |
| Password | Nex1968 |

**ICC Connection string:**
```
postgresql://nex_admin:Nex1968@192.168.122.1:5433/nex_automat_icc
```

---

## API Keys

| Service | Key |
|---------|-----|
| LS_API_KEY (dev) | ls-dev-key-change-in-production-2025 |
| LS_API_KEY (ANDROS) | andros-api-key-2026 |
| LS_API_KEY (ICC) | icc-api-key-2026 |

---

## Docker Ports (ANDROS Server)

| Stack | PostgreSQL | Temporal | Temporal UI |
|-------|------------|----------|-------------|
| ANDROS | 5432 | 7233 | 8080 |
| ICC | 5433 | 7234 | 8081 |

---

## Windows Services Ports (ANDROS VM)

| Zákazník | FastAPI Loader |
|----------|----------------|
| ANDROS | :8001 |
| ICC | :8002 |

---

## Stalwart Mail Server (ANDROS Server)

- **URL:** http://192.168.100.23:8088
- **Admin user:** admin
- **Password:** zMgmEFQx9L
- **Inštalácia:** /opt/stalwart/
- **Doména:** isnex.ai
- **Dátum:** 2026-01-21

---

## Security Notes

1. **Never commit** this file or docs/knowledge/credentials/ to Git
2. ✅ **Telegram tokens** regenerated 2025-12-25
3. **Gmail App Password** is separate from regular password
4. **POSTGRES_PASSWORD** is set as Windows environment variable on Mágerstav server
5. **ANDROS server** accessible via Tailscale VPN only (RDP)
6. **Webglobe emails** - štandardný IMAP/SMTP, bez OAuth2